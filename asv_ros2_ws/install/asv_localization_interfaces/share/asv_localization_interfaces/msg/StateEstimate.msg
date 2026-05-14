std_msgs/Header header

# Mean vector (6x1) - [x, y, z, x_dot, y_dot, theta_dot]
float64[6] mu

# Covariance matrix (6x6) - row-major flattened
float64[36] sigma