// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from asv_localization_interfaces:msg/BiasStateEstimate.idl
// generated code does not contain a copyright notice
#include "asv_localization_interfaces/msg/detail/bias_state_estimate__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
asv_localization_interfaces__msg__BiasStateEstimate__init(asv_localization_interfaces__msg__BiasStateEstimate * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    asv_localization_interfaces__msg__BiasStateEstimate__fini(msg);
    return false;
  }
  // mu
  // sigma
  return true;
}

void
asv_localization_interfaces__msg__BiasStateEstimate__fini(asv_localization_interfaces__msg__BiasStateEstimate * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // mu
  // sigma
}

bool
asv_localization_interfaces__msg__BiasStateEstimate__are_equal(const asv_localization_interfaces__msg__BiasStateEstimate * lhs, const asv_localization_interfaces__msg__BiasStateEstimate * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // mu
  for (size_t i = 0; i < 9; ++i) {
    if (lhs->mu[i] != rhs->mu[i]) {
      return false;
    }
  }
  // sigma
  for (size_t i = 0; i < 81; ++i) {
    if (lhs->sigma[i] != rhs->sigma[i]) {
      return false;
    }
  }
  return true;
}

bool
asv_localization_interfaces__msg__BiasStateEstimate__copy(
  const asv_localization_interfaces__msg__BiasStateEstimate * input,
  asv_localization_interfaces__msg__BiasStateEstimate * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // mu
  for (size_t i = 0; i < 9; ++i) {
    output->mu[i] = input->mu[i];
  }
  // sigma
  for (size_t i = 0; i < 81; ++i) {
    output->sigma[i] = input->sigma[i];
  }
  return true;
}

asv_localization_interfaces__msg__BiasStateEstimate *
asv_localization_interfaces__msg__BiasStateEstimate__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  asv_localization_interfaces__msg__BiasStateEstimate * msg = (asv_localization_interfaces__msg__BiasStateEstimate *)allocator.allocate(sizeof(asv_localization_interfaces__msg__BiasStateEstimate), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(asv_localization_interfaces__msg__BiasStateEstimate));
  bool success = asv_localization_interfaces__msg__BiasStateEstimate__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
asv_localization_interfaces__msg__BiasStateEstimate__destroy(asv_localization_interfaces__msg__BiasStateEstimate * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    asv_localization_interfaces__msg__BiasStateEstimate__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__init(asv_localization_interfaces__msg__BiasStateEstimate__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  asv_localization_interfaces__msg__BiasStateEstimate * data = NULL;

  if (size) {
    data = (asv_localization_interfaces__msg__BiasStateEstimate *)allocator.zero_allocate(size, sizeof(asv_localization_interfaces__msg__BiasStateEstimate), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = asv_localization_interfaces__msg__BiasStateEstimate__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        asv_localization_interfaces__msg__BiasStateEstimate__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__fini(asv_localization_interfaces__msg__BiasStateEstimate__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      asv_localization_interfaces__msg__BiasStateEstimate__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

asv_localization_interfaces__msg__BiasStateEstimate__Sequence *
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  asv_localization_interfaces__msg__BiasStateEstimate__Sequence * array = (asv_localization_interfaces__msg__BiasStateEstimate__Sequence *)allocator.allocate(sizeof(asv_localization_interfaces__msg__BiasStateEstimate__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = asv_localization_interfaces__msg__BiasStateEstimate__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__destroy(asv_localization_interfaces__msg__BiasStateEstimate__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    asv_localization_interfaces__msg__BiasStateEstimate__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__are_equal(const asv_localization_interfaces__msg__BiasStateEstimate__Sequence * lhs, const asv_localization_interfaces__msg__BiasStateEstimate__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!asv_localization_interfaces__msg__BiasStateEstimate__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
asv_localization_interfaces__msg__BiasStateEstimate__Sequence__copy(
  const asv_localization_interfaces__msg__BiasStateEstimate__Sequence * input,
  asv_localization_interfaces__msg__BiasStateEstimate__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(asv_localization_interfaces__msg__BiasStateEstimate);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    asv_localization_interfaces__msg__BiasStateEstimate * data =
      (asv_localization_interfaces__msg__BiasStateEstimate *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!asv_localization_interfaces__msg__BiasStateEstimate__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          asv_localization_interfaces__msg__BiasStateEstimate__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!asv_localization_interfaces__msg__BiasStateEstimate__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
