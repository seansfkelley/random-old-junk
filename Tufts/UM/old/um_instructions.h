#ifndef UM_INSTRUCTIONS_H
#define UM_INSTRUCTIONS_H

#include "um_types.h"
#include "um_memory.h"

// One Signature to rule them all.
// One Signature to find them.
// One Signature to bring them all, and in the darkness bind them.
void UM_cond_move   (UM_memory memory, UM_state state);
void UM_index       (UM_memory memory, UM_state state);
void UM_update      (UM_memory memory, UM_state state);
void UM_add         (UM_memory memory, UM_state state);
void UM_multiply    (UM_memory memory, UM_state state);
void UM_divide      (UM_memory memory, UM_state state);
void UM_nand        (UM_memory memory, UM_state state);
void UM_halt        (UM_memory memory, UM_state state);
void UM_activate    (UM_memory memory, UM_state state);
void UM_inactivate  (UM_memory memory, UM_state state);
void UM_output      (UM_memory memory, UM_state state);
void UM_input       (UM_memory memory, UM_state state);
void UM_load_program(UM_memory memory, UM_state state);
// void UM_load_value  (UM_memory memory, UM_state state);

typedef void (*inst_func_pointer)(UM_memory, UM_state);

inst_func_pointer instruction_functions[13] = 
{UM_cond_move, UM_index, UM_update, UM_add, UM_multiply, UM_divide, UM_nand, 
 UM_halt, UM_activate, UM_inactivate, UM_output, UM_input, UM_load_program};


#endif
