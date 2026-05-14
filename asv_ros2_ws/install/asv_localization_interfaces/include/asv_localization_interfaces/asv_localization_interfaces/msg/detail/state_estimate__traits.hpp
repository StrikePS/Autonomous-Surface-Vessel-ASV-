// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from asv_localization_interfaces:msg/StateEstimate.idl
// generated code does not contain a copyright notice

#ifndef ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__TRAITS_HPP_
#define ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "asv_localization_interfaces/msg/detail/state_estimate__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace asv_localization_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const StateEstimate & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: mu
  {
    if (msg.mu.size() == 0) {
      out << "mu: []";
    } else {
      out << "mu: [";
      size_t pending_items = msg.mu.size();
      for (auto item : msg.mu) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: sigma
  {
    if (msg.sigma.size() == 0) {
      out << "sigma: []";
    } else {
      out << "sigma: [";
      size_t pending_items = msg.sigma.size();
      for (auto item : msg.sigma) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const StateEstimate & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: mu
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.mu.size() == 0) {
      out << "mu: []\n";
    } else {
      out << "mu:\n";
      for (auto item : msg.mu) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: sigma
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.sigma.size() == 0) {
      out << "sigma: []\n";
    } else {
      out << "sigma:\n";
      for (auto item : msg.sigma) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const StateEstimate & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace asv_localization_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use asv_localization_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const asv_localization_interfaces::msg::StateEstimate & msg,
  std::ostream & out, size_t indentation = 0)
{
  asv_localization_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use asv_localization_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const asv_localization_interfaces::msg::StateEstimate & msg)
{
  return asv_localization_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<asv_localization_interfaces::msg::StateEstimate>()
{
  return "asv_localization_interfaces::msg::StateEstimate";
}

template<>
inline const char * name<asv_localization_interfaces::msg::StateEstimate>()
{
  return "asv_localization_interfaces/msg/StateEstimate";
}

template<>
struct has_fixed_size<asv_localization_interfaces::msg::StateEstimate>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<asv_localization_interfaces::msg::StateEstimate>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<asv_localization_interfaces::msg::StateEstimate>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__TRAITS_HPP_
