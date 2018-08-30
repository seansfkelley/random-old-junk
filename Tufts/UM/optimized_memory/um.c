#include <stdio.h>
#include <stdlib.h>

#include "um_types.h"
#include "um_memory.h"
#include "seq.h"
#include "mem.h"

// Define macros for very fast access to the instruction's fields.
#define A(x) (x << 23) >> 29
#define B(x) (x << 26) >> 29
#define C(x) (x << 29) >> 29

#define OPCODE(x) x >> 28
#define LV_REG(x) (x << 4) >> 29
#define LV_VAL(x) (x << 7) >> 7

void UM_main(Seq_T instruction_seq){
  if (instruction_seq == NULL){
    exit(0);
  }

  // Initialize instruction array (0).
  UM_memory memory = UM_memory_new();
  UM_word inst_array = UM_memory_activate(memory, Seq_length(instruction_seq));
  for (int i = 0; i < Seq_length(instruction_seq); ++i){
    UM_memory_set(memory, inst_array, i, 
		  (unsigned long) Seq_get(instruction_seq, i));
  }
  UM_memory_load_program(memory, inst_array);
  UM_memory_inactivate(memory, inst_array);

  // Initialize state variables.
  UM_word program_counter = 0;
  UM_word regs[8];
  for (UM_word i = 0; i < 8; ++i){
    regs[i] = 0;
  }

  UM_word instruction;
  int input_char;

  while (1){
    instruction = UM_memory_get(memory, 0, program_counter);
    switch(OPCODE(instruction)){
    case COND_MOVE:
      if (regs[C(instruction)] != 0){
	regs[A(instruction)] = regs[B(instruction)];
      }      
      break;
    case INDEX:
      regs[A(instruction)] = UM_memory_get(memory, regs[B(instruction)], 
					   regs[C(instruction)]);      
      break;
    case UPDATE:
      UM_memory_set(memory, regs[A(instruction)], 
		    regs[B(instruction)], regs[C(instruction)]);      
      break;
    case ADD:
      regs[A(instruction)] = regs[B(instruction)] + regs[C(instruction)];
      break;
    case MULTIPLY:
      regs[A(instruction)] = regs[B(instruction)] * regs[C(instruction)];
      break;
    case DIVIDE:
      regs[A(instruction)] = regs[B(instruction)] / regs[C(instruction)];
      break;
    case NAND:
      regs[A(instruction)] = ~(regs[B(instruction)] & regs[C(instruction)]);
      break;
    case HALT:
      UM_memory_free(memory);
      return;
      break;
    case ACTIVATE:
      regs[B(instruction)] = UM_memory_activate(memory, regs[C(instruction)]);
      break;
    case INACTIVATE:
      UM_memory_inactivate(memory, regs[C(instruction)]);
      break;
    case OUTPUT:
      putchar(regs[C(instruction)]);
      break;
    case INPUT:
      input_char = getchar();
      if (input_char == EOF){
	regs[C(instruction)] = ~((UM_word) 0);
      }
      regs[C(instruction)] = input_char % 256;
      break;
    case LOAD_PROGRAM:
      UM_memory_load_program(memory, regs[B(instruction)]);
      program_counter = regs[C(instruction)] - 1;
      break;
    case LOAD_VALUE:
      // Program runs a bit faster when this is separated out into it's own if
      // statement at the beginning... mysterious.
      regs[LV_REG(instruction)] = LV_VAL(instruction);
      break;
    }
    ++program_counter;
  }

  // Not that this should be reached in any reasonable scenario.
  UM_memory_free(memory);
  return;
}
