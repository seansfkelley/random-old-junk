#include <stdio.h>
#include <stdlib.h>

#include "um_memory.h"
#include "um_types.h"

#include "assert.h"
#include "mem.h"

// Test simple (i.e. only one) array activation and inactivation, as well as
// getting and setting values with a variety of array sizes.
void single_array(){
  UM_memory mem = UM_memory_new(2);
  UM_word size, index;
  for (int exponent = 0; exponent < 17; ++exponent){
    size = 1 << exponent;
    index = UM_memory_activate(mem, size); 
    for (UM_word i = 0; i < size; ++i){
      UM_memory_set(mem, index, i, i);
    }
    for (UM_word j = 0; j < size; ++j){
      assert(UM_memory_get(mem, index, j) == j);
    }
    UM_memory_inactivate(mem, index);
  }

  UM_memory_free(mem);
}

// Test memory reuse by activating a block of arrays and then randomly
// inactivating and re-activating, making sure that the re-activated arrays
// occupy the same space as their just-inactivated counterparts.
void random_reuse(){
  UM_memory mem = UM_memory_new(257);
  UM_word *indices = ALLOC(256*sizeof(UM_word));
  for (UM_word i = 0; i < 256; ++i){
    indices[i] = UM_memory_activate(mem, 1);
  }
  
  UM_word to_free, old_index;
  for (int trial = 0; trial < 65536; ++trial){
    to_free = rand() % 256;
    old_index = indices[to_free];
    UM_memory_inactivate(mem, old_index);
    indices[to_free] = UM_memory_activate(mem, 1);
    assert(indices[to_free] == old_index);
  }

  FREE(indices);
  UM_memory_free(mem);
}

// Test two cases: a copy from one array to the zeroth, and then a 'jump'
// inside the zeroth array.
void load_program(){
  UM_memory mem = UM_memory_new(2);
  UM_word source = UM_memory_activate(mem, 256);
  for (UM_word i = 0; i < 256; ++i){
    UM_memory_set(mem, source, i, i);
  }

  UM_memory_load_program(mem, source);
  UM_memory_inactivate(mem, source);
  for (UM_word j = 0; j < 256; ++j){
    assert(UM_memory_get(mem, 0, j) == j);
  }

  UM_memory_load_program(mem, 0);
  for (UM_word k = 0; k < 256; ++k){
    assert(UM_memory_get(mem, 0, k) == k);
  }

  UM_memory_free(mem);
}

int main(){
  single_array();
  printf("single_array test passed!\n");
  random_reuse();
  printf("random_reuse test passed!\n");
  load_program(); 
  printf("load_program passed!\n");
}
