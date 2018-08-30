#include <string.h> // memcpy

#include "um_memory.h"
#include "seq.h"
#include "mem.h"

#define T UM_memory

struct T{
  Seq_T c_arrays;    // Each element is a C array created by an activate-
                     // array instruction.
  Seq_T empty_slots; // A queue that tracks previously-inactivated slots.
  Seq_T lengths;     // lengths[i] is the length of c_arrays[i].
};

T UM_memory_new (UM_word size_hint){
  UM_memory mem;
  NEW(mem);
  mem->c_arrays = Seq_new(size_hint);
  mem->empty_slots = Seq_new(size_hint);
  mem->lengths = Seq_new(size_hint);

  // Reserve the zeroth slot for the instructions.
  Seq_addhi(mem->c_arrays, NULL);
  Seq_addhi(mem->lengths, (void *) 0);
  return mem;
}

void UM_memory_free(T memory){
  UM_word *array;
  for (int i = 0; i < Seq_length(memory->c_arrays); ++i){
    // FREE attempts to set its parameter to null, which is not possible if
    // FREE's parameter is a function call. For this reason we have to assign
    // the contents to a local variable first.
    array = Seq_get(memory->c_arrays, i);
    FREE(array);
  }
  Seq_free(&(memory->c_arrays));
  Seq_free(&(memory->empty_slots));
  Seq_free(&(memory->lengths));
  FREE(memory);
}

UM_word UM_memory_get(T memory, UM_word array_i, UM_word element_i){
  UM_word *array = Seq_get(memory->c_arrays, array_i);
  return array[element_i];
}

void UM_memory_set(T memory, UM_word array_i, 
		   UM_word element_i, UM_word value){
  UM_word *array = Seq_get(memory->c_arrays, array_i);
  array[element_i] = value;
}

UM_word UM_memory_activate(T memory, UM_word size){
  // Being a 32-bit machine, any given array cannot hold more than 2^32 bytes.
  // If more than 4GB (size >= 2^30) and possibly a little less is ever asked 
  // for, the behavior of this function is undefined and at the mercy of ALLOC.
  UM_word *array = ALLOC(size * sizeof(UM_word));
  for (UM_word i = 0; i < size; ++i){
    array[i] = 0;
  }
  if (Seq_length(memory->empty_slots) == 0){
    Seq_addhi(memory->c_arrays, array);
    Seq_addhi(memory->lengths, (void *)(unsigned long) size);
    return Seq_length(memory->c_arrays) - 1;
  }
  else{
    UM_word index = (unsigned long) Seq_remhi(memory->empty_slots);
    Seq_put(memory->c_arrays, index, array);
    Seq_put(memory->lengths, index, (void *)(unsigned long) size);
    return index;
  }
}

void UM_memory_inactivate(T memory, UM_word array_i){
  // See comment in UM_memory_free regarding this two-line construct.
  UM_word *array = Seq_get(memory->c_arrays, array_i);
  FREE(array);
  Seq_put(memory->c_arrays, array_i, NULL);
  Seq_put(memory->lengths, array_i, (void *) 0);
  Seq_addhi(memory->empty_slots, (void *)(unsigned long) array_i);
}

void UM_memory_load_program(T memory, UM_word inst_array_i){
  if (inst_array_i == 0){
    return;
  }
  // Avoid the UM_memory_[in]activate functions because we need to control the 
  // destination of this array.
  // The comment in UM_memory_activate is relevant to this as well.

  UM_word *array = Seq_get(memory->c_arrays, 0);
  FREE(array);

  UM_word num_words = (unsigned long) Seq_get(memory->lengths, inst_array_i);
  array = ALLOC(num_words * sizeof(UM_word));
  
  memcpy(array, 
	 Seq_get(memory->c_arrays, inst_array_i),
	 num_words * sizeof(UM_word));


  Seq_put(memory->c_arrays, 0, array);
  Seq_put(memory->lengths, 0, (void *)(unsigned long) num_words);
}

#undef T
