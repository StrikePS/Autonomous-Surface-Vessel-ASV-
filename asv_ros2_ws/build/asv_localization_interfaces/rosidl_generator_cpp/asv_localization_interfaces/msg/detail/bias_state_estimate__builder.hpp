// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from asv_localization_interfaces:msg/BiasStateEstimate.idl
// generated code does not contain a copyright notice

#ifndef ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__BIAS_STATE_ESTIMATE__BUILDER_HPP_
#define ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__BIAS_STATE_ESTIMATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "asv_localization_interfaces/msg/detail/bias_state_estimate__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace asv_localization_interfaces
{

namespace msg
{

namespace builder
{

class Init_BiasStateEstimate_sigma
{
public:
  explicit Init_BiasStateEstimate_sigma(::asv_localization_interfaces::msg::BiasStateEstimate & msg)
  : msg_(msg)
  {}
  ::asv_localization_interfaces::msg::BiasStateEstimate sigma(::asv_localization_interfaces::msg::BiasStateEstimate::_sigma_type arg)
  {
    msg_.sigma = std::move(arg);
    return std::move(msg_);
  }

private:
  ::asv_localization_interfaces::msg::BiasStateEstimate msg_;
};

class Init_BiasStateEstimate_mu
{
public:
  explicit Init_BiasStateEstimate_mu(::asv_localization_interfaces::msg::BiasStateEstimate & msg)
  : msg_(msg)
  {}
  Init_BiasStateEstimate_sigma mu(::asv_localization_interfaces::msg::BiasStateEstimate::_mu_type arg)
  {
    msg_.mu = std::move(arg);
    return Init_BiasStateEstimate_sigma(msg_);
  }

private:
  ::asv_localization_interfaces::msg::BiasStateEstimate msg_;
};

class Init_BiasStateEstimate_header
{
public:
  Init_BiasStateEstimate_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_BiasStateEstimate_mu header(::asv_localization_interfaces::msg::BiasStateEstimate::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_BiasStateEstimate_mu(msg_);
  }

private:
  ::asv_localization_interfaces::msg::BiasStateEstimate msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::asv_localization_interfaces::msg::BiasStateEstimate>()
{
  return asv_localization_interfaces::msg::builder::Init_BiasStateEstimate_header();
}

}  // namespace asv_localization_interfaces

#endif  // ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__BIAS_STATE_ESTIMATE__BUILDER_HPP_
