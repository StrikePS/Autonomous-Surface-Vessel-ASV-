// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from asv_localization_interfaces:msg/BiasStateEstimate.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "asv_localization_interfaces/msg/detail/bias_state_estimate__rosidl_typesupport_introspection_c.h"
#include "asv_localization_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "asv_localization_interfaces/msg/detail/bias_state_estimate__functions.h"
#include "asv_localization_interfaces/msg/detail/bias_state_estimate__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  asv_localization_interfaces__msg__BiasStateEstimate__init(message_memory);
}

void asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_fini_function(void * message_memory)
{
  asv_localization_interfaces__msg__BiasStateEstimate__fini(message_memory);
}

size_t asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__size_function__BiasStateEstimate__mu(
  const void * untyped_member)
{
  (void)untyped_member;
  return 9;
}

const void * asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_const_function__BiasStateEstimate__mu(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_function__BiasStateEstimate__mu(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__fetch_function__BiasStateEstimate__mu(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_const_function__BiasStateEstimate__mu(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__assign_function__BiasStateEstimate__mu(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_function__BiasStateEstimate__mu(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__size_function__BiasStateEstimate__sigma(
  const void * untyped_member)
{
  (void)untyped_member;
  return 81;
}

const void * asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_const_function__BiasStateEstimate__sigma(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_function__BiasStateEstimate__sigma(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__fetch_function__BiasStateEstimate__sigma(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_const_function__BiasStateEstimate__sigma(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__assign_function__BiasStateEstimate__sigma(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_function__BiasStateEstimate__sigma(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_message_member_array[3] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(asv_localization_interfaces__msg__BiasStateEstimate, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "mu",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    9,  // array size
    false,  // is upper bound
    offsetof(asv_localization_interfaces__msg__BiasStateEstimate, mu),  // bytes offset in struct
    NULL,  // default value
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__size_function__BiasStateEstimate__mu,  // size() function pointer
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_const_function__BiasStateEstimate__mu,  // get_const(index) function pointer
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_function__BiasStateEstimate__mu,  // get(index) function pointer
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__fetch_function__BiasStateEstimate__mu,  // fetch(index, &value) function pointer
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__assign_function__BiasStateEstimate__mu,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "sigma",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    81,  // array size
    false,  // is upper bound
    offsetof(asv_localization_interfaces__msg__BiasStateEstimate, sigma),  // bytes offset in struct
    NULL,  // default value
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__size_function__BiasStateEstimate__sigma,  // size() function pointer
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_const_function__BiasStateEstimate__sigma,  // get_const(index) function pointer
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__get_function__BiasStateEstimate__sigma,  // get(index) function pointer
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__fetch_function__BiasStateEstimate__sigma,  // fetch(index, &value) function pointer
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__assign_function__BiasStateEstimate__sigma,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_message_members = {
  "asv_localization_interfaces__msg",  // message namespace
  "BiasStateEstimate",  // message name
  3,  // number of fields
  sizeof(asv_localization_interfaces__msg__BiasStateEstimate),
  asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_message_member_array,  // message members
  asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_init_function,  // function to initialize message memory (memory has to be allocated)
  asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_message_type_support_handle = {
  0,
  &asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_asv_localization_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, asv_localization_interfaces, msg, BiasStateEstimate)() {
  asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_message_type_support_handle.typesupport_identifier) {
    asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &asv_localization_interfaces__msg__BiasStateEstimate__rosidl_typesupport_introspection_c__BiasStateEstimate_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
