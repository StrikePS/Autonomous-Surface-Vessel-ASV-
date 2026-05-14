"""
GNSS + IMU State Estimation using Error-State Kalman Filter (ESKF)
==================================================================
Inputs:
  - GNSS: [lat, lon, alt]  (degrees, degrees, meters)
  - IMU:  quaternion [qw, qx, qy, qz] + angular velocity + linear acceleration

State vector (15-DOF):
  x = [position (3), velocity (3), orientation quaternion (4),
       accel_bias (3), gyro_bias (3)]

Error state (15-DOF):
  dx = [dp (3), dv (3), dtheta (3), dba (3), dbg (3)]
"""

import numpy as np
from scipy.spatial.transform import Rotation as R


# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
EARTH_A  = 6378137.0          # WGS84 semi-major axis (m)
EARTH_E2 = 6.6943799901e-3    # WGS84 first eccentricity squared
G_VEC    = np.array([0, 0, -9.81])  # gravity in NED frame (m/s²)


# ─────────────────────────────────────────────
# Coordinate helpers
# ─────────────────────────────────────────────

def lla_to_ecef(lat_deg, lon_deg, alt_m):
    """Convert geodetic LLA to ECEF (m)."""
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)
    N = EARTH_A / np.sqrt(1 - EARTH_E2 * np.sin(lat)**2)
    x = (N + alt_m) * np.cos(lat) * np.cos(lon)
    y = (N + alt_m) * np.cos(lat) * np.sin(lon)
    z = (N * (1 - EARTH_E2) + alt_m) * np.sin(lat)
    return np.array([x, y, z])


def ecef_to_ned(ecef, ref_ecef, ref_lat_deg, ref_lon_deg):
    """Convert ECEF displacement to local NED frame."""
    lat = np.radians(ref_lat_deg)
    lon = np.radians(ref_lon_deg)
    R_en = np.array([
        [-np.sin(lat)*np.cos(lon), -np.sin(lat)*np.sin(lon),  np.cos(lat)],
        [-np.sin(lon),              np.cos(lon),               0          ],
        [-np.cos(lat)*np.cos(lon), -np.cos(lat)*np.sin(lon), -np.sin(lat)]
    ])
    return R_en @ (ecef - ref_ecef)


def quat_to_rot(q):
    """Quaternion [qw, qx, qy, qz] → 3×3 rotation matrix."""
    return R.from_quat([q[1], q[2], q[3], q[0]]).as_matrix()


def rot_to_quat(rot_mat):
    """3×3 rotation matrix → quaternion [qw, qx, qy, qz]."""
    r = R.from_matrix(rot_mat)
    q = r.as_quat()           # scipy: [qx, qy, qz, qw]
    return np.array([q[3], q[0], q[1], q[2]])


def skew(v):
    """Skew-symmetric matrix of a 3-vector."""
    return np.array([
        [ 0,    -v[2],  v[1]],
        [ v[2],  0,    -v[0]],
        [-v[1],  v[0],  0   ]
    ])


def quat_normalize(q):
    return q / np.linalg.norm(q)


def quat_multiply(p, q):
    """Hamilton product: p ⊗ q, both [qw, qx, qy, qz]."""
    pw, px, py, pz = p
    qw, qx, qy, qz = q
    return np.array([
        pw*qw - px*qx - py*qy - pz*qz,
        pw*qx + px*qw + py*qz - pz*qy,
        pw*qy - px*qz + py*qw + pz*qx,
        pw*qz + px*qy - py*qx + pz*qw
    ])


# ─────────────────────────────────────────────
# ESKF Class
# ─────────────────────────────────────────────

class GNSS_IMU_ESKF:
    """
    Error-State Kalman Filter for GNSS + IMU fusion.

    State (nominal):
        p  : position in local NED (m)         [3]
        v  : velocity in NED (m/s)             [3]
        q  : orientation quaternion [qw,qx,qy,qz]  [4]
        ba : accelerometer bias (m/s²)         [3]
        bg : gyroscope bias (rad/s)            [3]

    Error state dx ∈ R^15:
        [dp(3), dv(3), dθ(3), dba(3), dbg(3)]
    """

    def __init__(self,
                 init_lla,
                 init_quat=None,
                 sigma_acc=0.1,       # IMU accel noise (m/s²/√Hz)
                 sigma_gyro=0.01,     # IMU gyro noise (rad/s/√Hz)
                 sigma_ba=0.001,      # accel bias random walk
                 sigma_bg=0.0001,     # gyro bias random walk
                 sigma_gnss_pos=2.0): # GNSS position noise (m)

        # ── Reference origin ──────────────────
        self.ref_lat = init_lla[0]
        self.ref_lon = init_lla[1]
        self.ref_alt = init_lla[2]
        self.ref_ecef = lla_to_ecef(*init_lla)

        # ── Nominal state ─────────────────────
        self.p  = np.zeros(3)                          # NED position
        self.v  = np.zeros(3)                          # NED velocity
        self.q  = init_quat if init_quat is not None \
                  else np.array([1., 0., 0., 0.])      # [qw,qx,qy,qz]
        self.ba = np.zeros(3)                          # accel bias
        self.bg = np.zeros(3)                          # gyro bias

        # ── Error covariance (15×15) ──────────
        self.P = np.diag([
            1., 1., 1.,        # dp
            0.1, 0.1, 0.1,     # dv
            0.01, 0.01, 0.01,  # dθ
            0.01, 0.01, 0.01,  # dba
            0.001,0.001,0.001  # dbg
        ])

        # ── Noise parameters ──────────────────
        self.sigma_acc  = sigma_acc
        self.sigma_gyro = sigma_gyro
        self.sigma_ba   = sigma_ba
        self.sigma_bg   = sigma_bg
        self.sigma_gnss = sigma_gnss_pos

        self.initialized = False

    # ──────────────────────────────────────────
    # IMU Propagation  (call at ~100–1000 Hz)
    # ──────────────────────────────────────────

    def predict(self, acc_body, gyro_body, dt):
        """
        Propagate state using raw IMU measurements.

        Parameters
        ----------
        acc_body  : np.array(3)  linear acceleration in body frame (m/s²)
        gyro_body : np.array(3)  angular velocity in body frame (rad/s)
        dt        : float        time step (s)
        """
        # Remove biases
        acc_ub  = acc_body  - self.ba
        gyro_ub = gyro_body - self.bg

        # Current rotation matrix (body → NED)
        C = quat_to_rot(self.q)

        # ── Nominal state integration (midpoint / 1st-order) ──
        acc_ned = C @ acc_ub + G_VEC

        self.p += self.v * dt + 0.5 * acc_ned * dt**2
        self.v += acc_ned * dt

        # Orientation update via quaternion kinematics
        omega_norm = np.linalg.norm(gyro_ub)
        if omega_norm > 1e-10:
            axis  = gyro_ub / omega_norm
            angle = omega_norm * dt
            dq = np.concatenate([[np.cos(angle/2)],
                                  np.sin(angle/2) * axis])
        else:
            dq = np.array([1., 0., 0., 0.])

        self.q = quat_normalize(quat_multiply(self.q, dq))

        # ── Error-state covariance propagation ──
        # Linearised state transition F (15×15)
        F = np.eye(15)

        # dp/dv
        F[0:3, 3:6] = np.eye(3) * dt

        # dv/dθ  →  -C [acc_ub]× dt
        F[3:6, 6:9] = -C @ skew(acc_ub) * dt

        # dv/dba  →  -C dt
        F[3:6, 9:12] = -C * dt

        # dθ/dθ  →  exp(−[gyro_ub]× dt)  ≈ I − [gyro_ub]× dt
        F[6:9, 6:9] = np.eye(3) - skew(gyro_ub) * dt

        # dθ/dbg  →  -I dt
        F[6:9, 12:15] = -np.eye(3) * dt

        # Process noise Q (15×15)
        Q = np.zeros((15, 15))
        sa2 = (self.sigma_acc  * dt)**2
        sg2 = (self.sigma_gyro * dt)**2
        Q[3:6,  3:6]  = np.eye(3) * sa2
        Q[6:9,  6:9]  = np.eye(3) * sg2
        Q[9:12, 9:12] = np.eye(3) * (self.sigma_ba  * dt)**2
        Q[12:15,12:15]= np.eye(3) * (self.sigma_bg  * dt)**2

        self.P = F @ self.P @ F.T + Q

    # ──────────────────────────────────────────
    # GNSS Update  (call at ~1–10 Hz)
    # ──────────────────────────────────────────

    def update_gnss(self, lla):
        """
        Correct state with a new GNSS fix.

        Parameters
        ----------
        lla : np.array(3)  [latitude_deg, longitude_deg, altitude_m]
        """
        # Convert LLA → local NED
        ecef  = lla_to_ecef(lla[0], lla[1], lla[2])
        p_ned = ecef_to_ned(ecef, self.ref_ecef, self.ref_lat, self.ref_lon)

        # Innovation
        z = p_ned - self.p

        # Observation matrix H (3×15): only position block
        H = np.zeros((3, 15))
        H[0:3, 0:3] = np.eye(3)

        # Measurement noise
        R_meas = np.eye(3) * self.sigma_gnss**2

        # Kalman gain
        S = H @ self.P @ H.T + R_meas
        K = self.P @ H.T @ np.linalg.inv(S)

        # Error state correction
        dx = K @ z

        # ── Inject error state into nominal state ──
        self.p  += dx[0:3]
        self.v  += dx[3:6]

        # Orientation correction via small-angle quaternion
        dtheta = dx[6:9]
        dq = np.concatenate([[1.0], 0.5 * dtheta])
        dq /= np.linalg.norm(dq)
        self.q  = quat_normalize(quat_multiply(self.q, dq))

        self.ba += dx[9:12]
        self.bg += dx[12:15]

        # ── Covariance update (Joseph form for stability) ──
        I_KH    = np.eye(15) - K @ H
        self.P  = I_KH @ self.P @ I_KH.T + K @ R_meas @ K.T

    # ──────────────────────────────────────────
    # IMU quaternion update (optional)
    # If your IMU gives you orientation directly,
    # use this instead of / alongside predict().
    # ──────────────────────────────────────────

    def update_imu_quat(self, q_imu, sigma_q=0.01):
        """
        Fuse a quaternion measurement from IMU/AHRS.

        Parameters
        ----------
        q_imu   : np.array(4)  [qw, qx, qy, qz]
        sigma_q : float        orientation measurement noise (rad)
        """
        q_imu = quat_normalize(q_imu)

        # Quaternion error → rotation vector (small angle)
        q_err = quat_multiply(
            np.array([self.q[0], -self.q[1], -self.q[2], -self.q[3]]),
            q_imu
        )
        # Small angle: dθ ≈ 2 * [qx, qy, qz]
        dtheta_meas = 2.0 * q_err[1:4]

        # H: maps error state → orientation error (3×15)
        H = np.zeros((3, 15))
        H[0:3, 6:9] = np.eye(3)

        R_q = np.eye(3) * sigma_q**2
        S   = H @ self.P @ H.T + R_q
        K   = self.P @ H.T @ np.linalg.inv(S)

        dx = K @ dtheta_meas

        # Inject
        self.p  += dx[0:3]
        self.v  += dx[3:6]
        dq = np.concatenate([[1.0], 0.5 * dx[6:9]])
        dq /= np.linalg.norm(dq)
        self.q  = quat_normalize(quat_multiply(self.q, dq))
        self.ba += dx[9:12]
        self.bg += dx[12:15]

        I_KH   = np.eye(15) - K @ H
        self.P = I_KH @ self.P @ I_KH.T + K @ R_q @ K.T

    # ──────────────────────────────────────────
    # Accessors
    # ──────────────────────────────────────────

    @property
    def position_ned(self):
        """NED position (m) relative to origin."""
        return self.p.copy()

    @property
    def velocity_ned(self):
        """NED velocity (m/s)."""
        return self.v.copy()

    @property
    def orientation_quat(self):
        """Body orientation quaternion [qw, qx, qy, qz]."""
        return self.q.copy()

    @property
    def orientation_euler_deg(self):
        """Roll, Pitch, Yaw in degrees (ZYX convention)."""
        rpy = R.from_quat([self.q[1], self.q[2], self.q[3], self.q[0]]).as_euler('zyx', degrees=True)
        return np.array([rpy[2], rpy[1], rpy[0]])  # [roll, pitch, yaw]

    def get_state(self):
        return {
            "position_NED_m"     : self.position_ned,
            "velocity_NED_ms"    : self.velocity_ned,
            "quaternion_wxyz"    : self.orientation_quat,
            "euler_RPY_deg"      : self.orientation_euler_deg,
            "accel_bias_ms2"     : self.ba.copy(),
            "gyro_bias_rads"     : self.bg.copy(),
            "covariance_diagonal": np.diag(self.P)
        }


# ─────────────────────────────────────────────
# Demo / Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    np.random.seed(42)

    # ── Initialise filter ──
    init_lla = np.array([22.5726, 88.3639, 10.0])  # Kolkata, India
    init_q   = np.array([1., 0., 0., 0.])          # level, north-facing

    eskf = GNSS_IMU_ESKF(
        init_lla    = init_lla,
        init_quat   = init_q,
        sigma_acc   = 0.05,
        sigma_gyro  = 0.005,
        sigma_ba    = 0.001,
        sigma_bg    = 0.0001,
        sigma_gnss_pos = 2.0
    )

    dt_imu  = 0.01   # 100 Hz
    dt_gnss = 1.0    # 1 Hz
    N_steps = 500    # 5 seconds

    gnss_counter = 0

    print(f"{'Step':>5}  {'N (m)':>8}  {'E (m)':>8}  {'D (m)':>8}"
          f"  {'Roll°':>7}  {'Pitch°':>7}  {'Yaw°':>7}  {'Source'}")
    print("-" * 75)

    for i in range(N_steps):
        # ── Simulate IMU reading ──
        acc_body  = np.array([0.1, 0.0, 9.81]) + np.random.randn(3) * 0.05
        gyro_body = np.array([0.0, 0.0, 0.01]) + np.random.randn(3) * 0.005

        # IMU quaternion (simulating a slowly rotating platform)
        true_yaw  = 0.01 * i * dt_imu
        q_imu_sim = np.array([np.cos(true_yaw/2), 0., 0., np.sin(true_yaw/2)])

        # Predict step
        eskf.predict(acc_body, gyro_body, dt_imu)

        # Fuse IMU quaternion
        eskf.update_imu_quat(q_imu_sim, sigma_q=0.005)

        gnss_counter += dt_imu

        source = "IMU"

        # ── Simulate GNSS update every 1 second ──
        if gnss_counter >= dt_gnss:
            gnss_counter = 0.0
            gnss_noise = np.random.randn(3) * 2.0   # ±2 m noise

            # Simulated true position: moving north at 1 m/s
            true_north_m = 1.0 * i * dt_imu
            # Approximate back to LLA (simple flat-earth)
            dlat = true_north_m / 111320.0
            sim_lla = np.array([
                init_lla[0] + dlat + gnss_noise[0]/111320.0,
                init_lla[1] + gnss_noise[1]/(111320.0 * np.cos(np.radians(init_lla[0]))),
                init_lla[2] + gnss_noise[2]
            ])

            eskf.update_gnss(sim_lla)
            source = "GNSS+IMU"

        # ── Print every 50 steps ──
        if i % 50 == 0:
            s = eskf.get_state()
            p = s["position_NED_m"]
            e = s["euler_RPY_deg"]
            print(f"{i:>5}  {p[0]:>8.2f}  {p[1]:>8.2f}  {p[2]:>8.2f}"
                  f"  {e[0]:>7.2f}  {e[1]:>7.2f}  {e[2]:>7.2f}  {source}")

    print("\n── Final State ──")
    for k, v in eskf.get_state().items():
        print(f"  {k}: {np.round(v, 4)}")