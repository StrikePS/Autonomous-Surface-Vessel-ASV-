// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from asv_localization_interfaces:msg/StateEstimate.idl
// generated code does not contain a copyright notice

#ifndef ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__STRUCT_HPP_
#define ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__asv_localization_interfaces__msg__StateEstimate __attribute__((deprecated))
#else
# define DEPRECATED__asv_localization_interfaces__msg__StateEstimate __declspec(deprecated)
#endif

namespace asv_localization_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct StateEstimate_
{
  using Type = StateEstimate_<ContainerAllocator>;

  explicit StateEstimate_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 6>::iterator, double>(this->mu.begin(), this->mu.end(), 0.0);
      std::fill<typename std::array<double, 36>::iterator, double>(this->sigma.begin(), this->sigma.end(), 0.0);
    }
  }

  explicit StateEstimate_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    mu(_alloc),
    sigma(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 6>::iterator, double>(this->mu.begin(), this->mu.end(), 0.0);
      std::fill<typename std::array<double, 36>::iterator, double>(this->sigma.begin(), this->sigma.end(), 0.0);
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _mu_type =
    std::array<double, 6>;
  _mu_type mu;
  using _sigma_type =
    std::array<double, 36>;
  _sigma_type sigma;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__mu(
    const std::array<double, 6> & _arg)
  {
    this->mu = _arg;
    return *this;
  }
  Type & set__sigma(
    const std::array<double, 36> & _arg)
  {
    this->sigma = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator> *;
  using ConstRawPtr =
    const asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__asv_localization_interfaces__msg__StateEstimate
    std::shared_ptr<asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__asv_localization_interfaces__msg__StateEstimate
    std::shared_ptr<asv_localization_interfaces::msg::StateEstimate_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const StateEstimate_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->mu != other.mu) {
      return false;
    }
    if (this->sigma != other.sigma) {
      return false;
    }
    return true;
  }
  bool operator!=(const StateEstimate_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct StateEstimate_

// alias to use template instance with default allocator
using StateEstimate =
  asv_localization_interfaces::msg::StateEstimate_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace asv_localization_interfaces

#endif  // ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__STRUCT_HPP_
