#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/imu.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <sensor_msgs/msg/nav_sat_fix.hpp>
#include <std_msgs/msg/float32.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

// Gazebo includes
#include <gz/transport/Node.hh>
#include <gz/msgs/imu.pb.h>
#include <gz/msgs/odometry.pb.h>
#include <gz/msgs/navsat.pb.h>
#include<gz/msgs/double.pb.h>
#include<gz/msgs/pose_v.pb.h>

class CustomBridge : public rclcpp::Node {
public:
    CustomBridge() : Node("custom_gazebo_bridge") {
        //Define QoS profile for sensors
        rclcpp::QoS sensor_qos = rclcpp::SensorDataQoS();
        // ROS Publishers
        imu_pub_ = this->create_publisher<sensor_msgs::msg::Imu>("/gz_trans/imu/data", sensor_qos);
        odom_pub_ = this->create_publisher<nav_msgs::msg::Odometry>("gz_trans/odometry", sensor_qos);
        pose_pub = this->create_publisher<geometry_msgs::msg::PoseStamped>("gz_trans/pose", sensor_qos);
        gps_pub_ = this->create_publisher<sensor_msgs::msg::NavSatFix>("gz_trans/gps/fix", sensor_qos);
        u1_pub = this->create_publisher<std_msgs::msg::Float32>("gz_trans/u1_thrust", 10);
        u2_pub = this->create_publisher<std_msgs::msg::Float32>("gz_trans/u2_thrust", 10);

        // Configure Gazebo Node with your specific partition
        gz::transport::NodeOptions options;
        options.SetPartition("ros_gz_example");
        gz_node_ = std::make_shared<gz::transport::Node>(options);

        // Gazebo Subscriptions
        gz_node_->Subscribe("/world/waves/model/blueboat/link/imu_link/sensor/imu_sensor/imu", &CustomBridge::OnImu, this);
        gz_node_->Subscribe("/model/blueboat/odometry", &CustomBridge::OnOdometry, this);
        gz_node_->Subscribe("/model/blueboat/pose", &CustomBridge::OnPose, this);
        gz_node_->Subscribe("/world/waves/model/blueboat/link/gps_link/sensor/navsat_sensor/navsat", &CustomBridge::OnGps, this);
        gz_node_->Subscribe("/model/blueboat/joint/motor_port_joint/cmd_thrust", &CustomBridge::Onu1, this);
        gz_node_->Subscribe("/model/blueboat/joint/motor_stbd_joint/cmd_thrust", &CustomBridge::Onu2, this);

        RCLCPP_INFO(this->get_logger(), "Custom C++ Bridge Initialized.");
    }

private:
    // IMU Callback
    void OnImu(const gz::msgs::IMU &_gz_msg) {
        sensor_msgs::msg::Imu ros_msg;
        ros_msg.header.stamp.sec = _gz_msg.header().stamp().sec();
        ros_msg.header.stamp.nanosec = _gz_msg.header().stamp().nsec();
        ros_msg.header.frame_id = "imu_link";

        ros_msg.orientation.x = _gz_msg.orientation().x();
        ros_msg.orientation.y = _gz_msg.orientation().y();
        ros_msg.orientation.z = _gz_msg.orientation().z();
        ros_msg.orientation.w = _gz_msg.orientation().w();

        ros_msg.angular_velocity.x = _gz_msg.angular_velocity().x();
        ros_msg.angular_velocity.y = _gz_msg.angular_velocity().y();
        ros_msg.angular_velocity.z = _gz_msg.angular_velocity().z();

        ros_msg.linear_acceleration.x = _gz_msg.linear_acceleration().x();
        ros_msg.linear_acceleration.y = _gz_msg.linear_acceleration().y();
        ros_msg.linear_acceleration.z = _gz_msg.linear_acceleration().z();
        
        // Map angular velocity and linear acceleration here...
        
        imu_pub_->publish(ros_msg);
    }

    // Odometry Callback
    void OnOdometry(const gz::msgs::Odometry &_gz_msg) {
        nav_msgs::msg::Odometry ros_msg;
        ros_msg.header.stamp.sec = _gz_msg.header().stamp().sec();
        ros_msg.header.stamp.nanosec = _gz_msg.header().stamp().nsec();
        ros_msg.header.frame_id = "odom";
        ros_msg.child_frame_id = "base_link";

        ros_msg.pose.pose.position.x = _gz_msg.pose().position().x();
        ros_msg.pose.pose.position.y = _gz_msg.pose().position().y();
        ros_msg.pose.pose.position.z = _gz_msg.pose().position().z();

        odom_pub_->publish(ros_msg);
    }

    // GPS Callback
    void OnGps(const gz::msgs::NavSat &_gz_msg) {
        sensor_msgs::msg::NavSatFix ros_msg;
        ros_msg.header.stamp.sec = _gz_msg.header().stamp().sec();
        ros_msg.header.stamp.nanosec = _gz_msg.header().stamp().nsec();
        ros_msg.header.frame_id = "gps";

        ros_msg.latitude = _gz_msg.latitude_deg();
        ros_msg.longitude = _gz_msg.longitude_deg();
        ros_msg.altitude = _gz_msg.altitude();

        gps_pub_->publish(ros_msg);
    }

    void Onu1(const gz::msgs::Double &_gz_msg) {
        std_msgs::msg::Float32 ros_msg;
        ros_msg.data = _gz_msg.data();
        u1_pub->publish(ros_msg);
    }

    void Onu2(const gz::msgs::Double &_gz_msg) {
        std_msgs::msg::Float32 ros_msg;
        ros_msg.data = _gz_msg.data();
        u2_pub->publish(ros_msg);
    }

    void OnPose(const gz::msgs::Pose_V &_gz_msg) {
        // Iterate through all poses in the vector
        for (int i = 0; i < _gz_msg.pose_size(); ++i) {
            const auto &gz_pose = _gz_msg.pose(i);

            // Optional: If the vector contains poses for all the boat's links, 
            // you might want to filter only for the main model pose:
            // if (gz_pose.name() != "blueboat") continue; 

            geometry_msgs::msg::PoseStamped ros_msg;
            ros_msg.header.stamp.sec = gz_pose.header().stamp().sec();
            ros_msg.header.stamp.nanosec = gz_pose.header().stamp().nsec();
            
            // Safely extract the frame_id from the header data if it exists
            if (gz_pose.header().data_size() > 0 && gz_pose.header().data(0).key() == "frame_id") {
                
                // Check if the value array actually has at least one string in it
                if (gz_pose.header().data(0).value_size() > 0) {
                    ros_msg.header.frame_id = gz_pose.header().data(0).value(0); // <-- Added (0) here
                } else {
                    ros_msg.header.frame_id = "pose";
                }
                
            } else {
                ros_msg.header.frame_id = "pose";
            }

            ros_msg.pose.position.x = gz_pose.position().x();
            ros_msg.pose.position.y = gz_pose.position().y();
            ros_msg.pose.position.z = gz_pose.position().z();

            ros_msg.pose.orientation.x = gz_pose.orientation().x();
            ros_msg.pose.orientation.y = gz_pose.orientation().y();
            ros_msg.pose.orientation.z = gz_pose.orientation().z();
            ros_msg.pose.orientation.w = gz_pose.orientation().w();

            pose_pub->publish(ros_msg);
        }
    }

    std::shared_ptr<gz::transport::Node> gz_node_;
    rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_pub_;
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_pub_;
    rclcpp::Publisher<sensor_msgs::msg::NavSatFix>::SharedPtr gps_pub_;
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr u1_pub;
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr u2_pub;
    rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr pose_pub;
};

// int main(int argc, char * argv[]) {
//     rclcpp::init(argc, argv);
//     rclcpp::spin(std::make_shared<CustomBridge>());
//     rclcpp::shutdown();
//     return 0;
// }

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    
    auto node = std::make_shared<CustomBridge>();
    rclcpp::executors::MultiThreadedExecutor executor;
    executor.add_node(node);
    
    // Spin with multiple threads
    executor.spin();
    
    rclcpp::shutdown();
    return 0;
}