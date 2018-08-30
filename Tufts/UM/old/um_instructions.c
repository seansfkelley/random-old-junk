#include <stdio.h>
#include <stdlib.h>
#include "um_types.h"
#include "um_memory.h"

void UM_cond_move(UM_memory memory, UM_state state){
  (void) memory;
  if (state->regs[state->C] != 0)
    state->regs[state->A] = state->regs[state->B];
}

void UM_index(UM_memory memory, UM_state state){
  state->regs[state->A] = UM_memory_get(memory, state->regs[state->B],
					state->regs[state->C]);
}

void UM_update(UM_memory memory, UM_state state){
  UM_memory_set(memory, state->regs[state->A], 
		state->regs[state->B], state->regs[state->C]);
}

void UM_add(UM_memory memory, UM_state state){
  (void) memory;
  state->regs[state->A] = state->regs[state->B] + state->regs[state->C];
}

void UM_multiply(UM_memory memory, UM_state state){
  (void) memory;
  state->regs[state->A] = state->regs[state->B] * state->regs[state->C];
}

void UM_divide(UM_memory memory, UM_state state){
  (void) memory;
  state->regs[state->A] = state->regs[state->B] / state->regs[state->C];
}

void UM_nand(UM_memory memory, UM_state state){
  (void) memory;
  state->regs[state->A] = ~(state->regs[state->B] & state->regs[state->C]);
}

void UM_halt(UM_memory memory, UM_state state){
  (void) memory;
  (void) state;
  exit(0);
}

void UM_activate(UM_memory memory, UM_state state){
  state->regs[state->B] = UM_memory_activate(memory, state->regs[state->C]);
}

void UM_inactivate(UM_memory memory, UM_state state){
  UM_memory_inactivate(memory, state->regs[state->C]);
}

void UM_output(UM_memory memory, UM_state state){
  (void) memory;
  putchar(state->regs[state->C]);
}

void UM_input(UM_memory memory, UM_state state){
  (void) memory;
  int c = getchar();
  if (c == EOF){
    state->regs[state->C] = ~((UM_word) 0);
  }
  state->regs[state->C] = c % 256;
}

void UM_load_program(UM_memory memory, UM_state state){
  UM_memory_load_program(memory, state->regs[state->B]);
  state->program_counter = state->regs[state->C];
}
