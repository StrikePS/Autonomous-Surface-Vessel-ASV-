// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from asv_localization_interfaces:msg/StateEstimate.idl
// generated code does not contain a copyright notice

#ifndef ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__STRUCT_H_
#define ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/StateEstimate in the package asv_localization_interfaces.
typedef struct asv_localization_interfaces__msg__StateEstimate
{
  std_msgs__msg__Header header;
  /// Mean vector (6x1) - [x, y, z, x_dot, y_dot, theta_dot]
  double mu[6];
  /// Covariance matrix (6x6) - row-major flattened
  double sigma[36];
} asv_localization_interfaces__msg__StateEstimate;

// Struct for a sequence of asv_localization_interfaces__msg__StateEstimate.
typedef struct asv_localization_interfaces__msg__StateEstimate__Sequence
{
  asv_localization_interfaces__msg__StateEstimate * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} asv_localization_interfaces__msg__StateEstimate__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__STATE_ESTIMATE__STRUCT_H_
