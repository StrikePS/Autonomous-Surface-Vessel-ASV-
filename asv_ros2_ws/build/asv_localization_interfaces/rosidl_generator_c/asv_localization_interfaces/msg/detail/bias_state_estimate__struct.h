// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from asv_localization_interfaces:msg/BiasStateEstimate.idl
// generated code does not contain a copyright notice

#ifndef ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__BIAS_STATE_ESTIMATE__STRUCT_H_
#define ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__BIAS_STATE_ESTIMATE__STRUCT_H_

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

/// Struct defined in msg/BiasStateEstimate in the package asv_localization_interfaces.
typedef struct asv_localization_interfaces__msg__BiasStateEstimate
{
  std_msgs__msg__Header header;
  /// Mean vector (9x1) - [x, y, z, x_dot, y_dot, theta_dot, b_ax, b_ay, b_wz]
  double mu[9];
  /// Covariance matrix (9x9) - row-major flattened
  double sigma[81];
} asv_localization_interfaces__msg__BiasStateEstimate;

// Struct for a sequence of asv_localization_interfaces__msg__BiasStateEstimate.
typedef struct asv_localization_interfaces__msg__BiasStateEstimate__Sequence
{
  asv_localization_interfaces__msg__BiasStateEstimate * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} asv_localization_interfaces__msg__BiasStateEstimate__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__BIAS_STATE_ESTIMATE__STRUCT_H_
