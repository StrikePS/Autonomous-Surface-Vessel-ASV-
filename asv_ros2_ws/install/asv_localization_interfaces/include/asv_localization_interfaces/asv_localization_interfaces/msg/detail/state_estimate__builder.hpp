// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from asv_localization_interfaces:msg/StateEstimate.idl
// generated code does not contain a copyright notice

#ifndef ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__BUILDER_HPP_
#define ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "asv_localization_interfaces/msg/detail/state_estimate__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace asv_localization_interfaces
{

namespace msg
{

namespace builder
{

class Init_StateEstimate_sigma
{
public:
  explicit Init_StateEstimate_sigma(::asv_localization_interfaces::msg::StateEstimate & msg)
  : msg_(msg)
  {}
  ::asv_localization_interfaces::msg::StateEstimate sigma(::asv_localization_interfaces::msg::StateEstimate::_sigma_type arg)
  {
    msg_.sigma = std::move(arg);
    return std::move(msg_);
  }

private:
  ::asv_localization_interfaces::msg::StateEstimate msg_;
};

class Init_StateEstimate_mu
{
public:
  explicit Init_StateEstimate_mu(::asv_localization_interfaces::msg::StateEstimate & msg)
  : msg_(msg)
  {}
  Init_StateEstimate_sigma mu(::asv_localization_interfaces::msg::StateEstimate::_mu_type arg)
  {
    msg_.mu = std::move(arg);
    return Init_StateEstimate_sigma(msg_);
  }

private:
  ::asv_localization_interfaces::msg::StateEstimate msg_;
};

class Init_StateEstimate_header
{
public:
  Init_StateEstimate_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_StateEstimate_mu header(::asv_localization_interfaces::msg::StateEstimate::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_StateEstimate_mu(msg_);
  }

private:
  ::asv_localization_interfaces::msg::StateEstimate msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::asv_localization_interfaces::msg::StateEstimate>()
{
  return asv_localization_interfaces::msg::builder::Init_StateEstimate_header();
}

}  // namespace asv_localization_interfaces

#endif  // ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__BUILDER_HPP_
