// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from asv_localization_interfaces:msg/StateEstimate.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "asv_localization_interfaces/msg/detail/state_estimate__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace asv_localization_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void StateEstimate_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) asv_localization_interfaces::msg::StateEstimate(_init);
}

void StateEstimate_fini_function(void * message_memory)
{
  auto typed_message = static_cast<asv_localization_interfaces::msg::StateEstimate *>(message_memory);
  typed_message->~StateEstimate();
}

size_t size_function__StateEstimate__mu(const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * get_const_function__StateEstimate__mu(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 6> *>(untyped_member);
  return &member[index];
}

void * get_function__StateEstimate__mu(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 6> *>(untyped_member);
  return &member[index];
}

void fetch_function__StateEstimate__mu(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__StateEstimate__mu(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__StateEstimate__mu(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__StateEstimate__mu(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__StateEstimate__sigma(const void * untyped_member)
{
  (void)untyped_member;
  return 36;
}

const void * get_const_function__StateEstimate__sigma(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 36> *>(untyped_member);
  return &member[index];
}

void * get_function__StateEstimate__sigma(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 36> *>(untyped_member);
  return &member[index];
}

void fetch_function__StateEstimate__sigma(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__StateEstimate__sigma(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__StateEstimate__sigma(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__StateEstimate__sigma(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember StateEstimate_message_member_array[3] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(asv_localization_interfaces::msg::StateEstimate, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "mu",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(asv_localization_interfaces::msg::StateEstimate, mu),  // bytes offset in struct
    nullptr,  // default value
    size_function__StateEstimate__mu,  // size() function pointer
    get_const_function__StateEstimate__mu,  // get_const(index) function pointer
    get_function__StateEstimate__mu,  // get(index) function pointer
    fetch_function__StateEstimate__mu,  // fetch(index, &value) function pointer
    assign_function__StateEstimate__mu,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "sigma",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    36,  // array size
    false,  // is upper bound
    offsetof(asv_localization_interfaces::msg::StateEstimate, sigma),  // bytes offset in struct
    nullptr,  // default value
    size_function__StateEstimate__sigma,  // size() function pointer
    get_const_function__StateEstimate__sigma,  // get_const(index) function pointer
    get_function__StateEstimate__sigma,  // get(index) function pointer
    fetch_function__StateEstimate__sigma,  // fetch(index, &value) function pointer
    assign_function__StateEstimate__sigma,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers StateEstimate_message_members = {
  "asv_localization_interfaces::msg",  // message namespace
  "StateEstimate",  // message name
  3,  // number of fields
  sizeof(asv_localization_interfaces::msg::StateEstimate),
  StateEstimate_message_member_array,  // message members
  StateEstimate_init_function,  // function to initialize message memory (memory has to be allocated)
  StateEstimate_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t StateEstimate_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &StateEstimate_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace asv_localization_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<asv_localization_interfaces::msg::StateEstimate>()
{
  return &::asv_localization_interfaces::msg::rosidl_typesupport_introspection_cpp::StateEstimate_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, asv_localization_interfaces, msg, StateEstimate)() {
  return &::asv_localization_interfaces::msg::rosidl_typesupport_introspection_cpp::StateEstimate_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
