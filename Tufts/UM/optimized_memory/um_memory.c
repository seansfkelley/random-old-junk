#include <string.h> // memset, memcpy

#include "um_memory.h"
#include "seq.h"
#include "mem.h"

#define T UM_memory

struct T{
  UM_word **arrays;  // An array where each element is an array created by 
                     // an activate-array instruction. The zeroth element in
                     // each array contains the length of that array, including
                     // the zeroth element itself. This index/length is not 
                     // accessible to the clients of this interface.
  UM_word allocated; // How many arrays are currently in use.
  UM_word true_size; // How many arrays there is space for in 'arrays'.
  Seq_T empty_slots; // A stack that tracks previously-inactivated arrays.
};

T UM_memory_new (){
  UM_memory mem;
  NEW(mem);

  // Reserve the first slot.
  mem->arrays = CALLOC(1, sizeof(UM_word *));
  mem->arrays[0] = CALLOC(1, sizeof(UM_word));
  mem->arrays[0][0] = 1;
  mem->true_size = mem->allocated = 1;

  mem->empty_slots = Seq_new(1);

  return mem;
}

void UM_memory_free(T memory){
  for (UM_word i = 0; i < memory->true_size; ++i){
    FREE(memory->arrays[i]);
  }
  FREE(memory->arrays);
  Seq_free(&(memory->empty_slots));
  FREE(memory);
}

// These two functions add one to element_i to account for the length metadata
// that lives in the zeroth spot of every array.
UM_word UM_memory_get(T memory, UM_word array_i, UM_word element_i){
  return memory->arrays[array_i][element_i + 1];
}

void UM_memory_set(T memory, UM_word array_i, 
		   UM_word element_i, UM_word value){
  memory->arrays[array_i][element_i + 1] = value;
}

UM_word UM_memory_activate(T memory, UM_word size){
  // Being a 32-bit machine, any given array cannot hold more than 2^32 bytes.
  // If more than 4GB (size >= 2^30) and possibly a little less is ever asked 
  // for, the behavior of this function is undefined and at the mercy of ALLOC.
  UM_word *array = CALLOC(size + 1,  sizeof(UM_word));
  memset(array, (UM_word) 0, (size + 1) * sizeof(UM_word));
  array[0] = size + 1;

  if (Seq_length(memory->empty_slots) == 0){
    if (memory->allocated == memory->true_size){
      RESIZE(memory->arrays, 2 * memory->true_size * sizeof(UM_word *));
      memset(&(memory->arrays[memory->true_size]), 
	     (UM_word) 0, memory->true_size * sizeof(UM_word *));
      memory->true_size *= 2;
    }
    memory->arrays[memory->allocated] = array;
    ++memory->allocated;
    return memory->allocated - 1;
  }
  else{
    UM_word index = (unsigned long) Seq_remhi(memory->empty_slots);
    memory->arrays[index] = array;
    ++memory->allocated;
    return index;
  }
}

void UM_memory_inactivate(T memory, UM_word array_i){
  FREE(memory->arrays[array_i]);
  --memory->allocated;
  Seq_addhi(memory->empty_slots, (void *)(unsigned long) array_i);
}

void UM_memory_load_program(T memory, UM_word inst_array_i){
  if (inst_array_i == 0){
    return;
  }
  // Avoid the UM_memory_[in]activate functions because we need to control the 
  // destination of this array.

  FREE(memory->arrays[0]);

  UM_word num_words = memory->arrays[inst_array_i][0];
  UM_word *array = CALLOC(num_words, sizeof(UM_word));
  memcpy(array, 
	 memory->arrays[inst_array_i],
	 num_words * sizeof(UM_word));

  memory->arrays[0] = array;
}

#undef T
