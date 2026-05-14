// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from asv_localization_interfaces:msg/BiasStateEstimate.idl
// generated code does not contain a copyright notice

#ifndef ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__BIAS_STATE_ESTIMATE__FUNCTIONS_H_
#define ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__BIAS_STATE_ESTIMATE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "asv_localization_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "asv_localization_interfaces/msg/detail/bias_state_estimate__struct.h"

/// Initialize msg/BiasStateEstimate message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * asv_localization_interfaces__msg__BiasStateEstimate
 * )) before or use
 * asv_localization_interfaces__msg__BiasStateEstimate__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
bool
asv_localization_interfaces__msg__BiasStateEstimate__init(asv_localization_interfaces__msg__BiasStateEstimate * msg);

/// Finalize msg/BiasStateEstimate message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
void
asv_localization_interfaces__msg__BiasStateEstimate__fini(asv_localization_interfaces__msg__BiasStateEstimate * msg);

/// Create msg/BiasStateEstimate message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * asv_localization_interfaces__msg__BiasStateEstimate__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
asv_localization_interfaces__msg__BiasStateEstimate *
asv_localization_interfaces__msg__BiasStateEstimate__create();

/// Destroy msg/BiasStateEstimate message.
/**
 * It calls
 * asv_localization_interfaces__msg__BiasStateEstimate__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
void
asv_localization_interfaces__msg__BiasStateEstimate__destroy(asv_localization_interfaces__msg__BiasStateEstimate * msg);

/// Check for msg/BiasStateEstimate message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
bool
asv_localization_interfaces__msg__BiasStateEstimate__are_equal(const asv_localization_interfaces__msg__BiasStateEstimate * lhs, const asv_localization_interfaces__msg__BiasStateEstimate * rhs);

/// Copy a msg/BiasStateEstimate message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
bool
asv_localization_interfaces__msg__BiasStateEstimate__copy(
  const asv_localization_interfaces__msg__BiasStateEstimate * input,
  asv_localization_interfaces__msg__BiasStateEstimate * output);

/// Initialize array of msg/BiasStateEstimate messages.
/**
 * It allocates the memory for the number of elements and calls
 * asv_localization_interfaces__msg__BiasStateEstimate__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
bool
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__init(asv_localization_interfaces__msg__BiasStateEstimate__Sequence * array, size_t size);

/// Finalize array of msg/BiasStateEstimate messages.
/**
 * It calls
 * asv_localization_interfaces__msg__BiasStateEstimate__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
void
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__fini(asv_localization_interfaces__msg__BiasStateEstimate__Sequence * array);

/// Create array of msg/BiasStateEstimate messages.
/**
 * It allocates the memory for the array and calls
 * asv_localization_interfaces__msg__BiasStateEstimate__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
asv_localization_interfaces__msg__BiasStateEstimate__Sequence *
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__create(size_t size);

/// Destroy array of msg/BiasStateEstimate messages.
/**
 * It calls
 * asv_localization_interfaces__msg__BiasStateEstimate__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
void
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__destroy(asv_localization_interfaces__msg__BiasStateEstimate__Sequence * array);

/// Check for msg/BiasStateEstimate message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
bool
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__are_equal(const asv_localization_interfaces__msg__BiasStateEstimate__Sequence * lhs, const asv_localization_interfaces__msg__BiasStateEstimate__Sequence * rhs);

/// Copy an array of msg/BiasStateEstimate messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_asv_localization_interfaces
bool
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__copy(
  const asv_localization_interfaces__msg__BiasStateEstimate__Sequence * input,
  asv_localization_interfaces__msg__BiasStateEstimate__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ASV_LOCALIZATION_INTERFACES__MSG__DETAIL__BIAS_STATE_ESTIMATE__FUNCTIONS_H_
