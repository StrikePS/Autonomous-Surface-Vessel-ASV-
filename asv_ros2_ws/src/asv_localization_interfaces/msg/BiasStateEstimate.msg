std_msgs/Header header

# Mean vector (9x1) - [x, y, z, x_dot, y_dot, theta_dot, b_ax, b_ay, b_wz]
float64[9] mu

# Covariance matrix (9x9) - row-major flattened
float64[81] sigma