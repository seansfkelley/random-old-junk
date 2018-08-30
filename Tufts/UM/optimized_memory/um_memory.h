#ifndef UM_MEMORY_H
#define UM_MEMORY_H

#include "um_types.h"

#define T UM_memory

typedef struct T* T;

T       UM_memory_new ();
void    UM_memory_free(T memory);

UM_word UM_memory_get(T memory, UM_word array_i, UM_word element_i);
void    UM_memory_set(T memory, UM_word array_i, 
		      UM_word element_i, UM_word value);

UM_word UM_memory_activate    (T memory, UM_word size);
void    UM_memory_inactivate  (T memory, UM_word array_i);
void    UM_memory_load_program(T memory, UM_word inst_array_i);

#undef T

#endif
