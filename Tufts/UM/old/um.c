#include <stdio.h>
#include <stdlib.h>

#include "um_types.h"
#include "um_memory.h"
#include "um_instructions.h"
#include "seq.h"
#include "bitpack.h"
#include "mem.h"

#include "inttypes.h"

/*
static UM_state UM_state_new(){
  UM_state state;
  NEW(state);
  for (int i = 0; i < 8; ++i){
    state->registers[i] = 0;
  }
  state->program_counter = 0;
  
}
*/

enum UM_opcode {COND_MOVE = 0, INDEX, UPDATE, ADD, MULTIPLY, DIVIDE, NAND,
     HALT, ACTIVATE, INACTIVATE, OUTPUT, INPUT, LOAD_PROGRAM, LOAD_VALUE};

void UM_main(Seq_T instruction_seq){
  
  if (instruction_seq == NULL){
    exit(0);
  }

  UM_memory memory = UM_memory_new(256);
  UM_word inst_array = UM_memory_activate(memory, Seq_length(instruction_seq));
  for (int i = 0; i < Seq_length(instruction_seq); ++i){
    UM_memory_set(memory, inst_array, i, 
		  (unsigned long) Seq_get(instruction_seq, i));
  }
  UM_memory_load_program(memory, inst_array);
  UM_memory_inactivate(memory, inst_array);

  Seq_free(&instruction_seq);

  UM_state state;
  NEW0(state);

  UM_word instruction;
  UM_opcode opcode;

  while (1){
    // printf("%u\n", state->program_counter);
    instruction = UM_memory_get(memory, 0, state->program_counter);
    opcode = Bitpack_getu(instruction, 4, 28);
    // printf("%u\n", opcode);
    if (opcode == LOAD_VALUE){
      state->regs[Bitpack_getu(instruction, 3, 25)] = 
	Bitpack_getu(instruction, 25, 0);
    }
    else{
      state->A = Bitpack_getu(instruction, 3, 6);
      state->B = Bitpack_getu(instruction, 3, 3);
      state->C = Bitpack_getu(instruction, 3, 0);
      instruction_functions[opcode](memory, state);
    }
    if (opcode != LOAD_PROGRAM){
      ++state->program_counter;
    }
  }

  UM_memory_free(memory);
  FREE(state);
}
