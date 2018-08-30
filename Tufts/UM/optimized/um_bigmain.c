#include <stdio.h>
#include <stdlib.h>

#include "um_types.h"
#include "um_memory.h"
#include "seq.h"
#include "bitpack.h"
#include "mem.h"

/*
#define A Bitpack_getu(instruction, 3, 6)
#define B Bitpack_getu(instruction, 3, 3)
#define C Bitpack_getu(instruction, 3, 0)
*/

// These macros yield a sizeable improvement over the previous ones. Is Bitpack
// really necessary, or, since the machine is allowed to be so unstable, can
// we just do this?
#define A(x) (x << 23) >> 29
#define B(x) (x << 26) >> 29
#define C(x) (x << 29) >> 29

// What about these?
#define OPCODE(x) x >> 28
#define LV_REG(x) (x << 4) >> 29
#define LV_VAL(x) (x << 7) >> 7

static UM_word program_counter = 0;
static UM_word regs[8];

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

  for (UM_reg_index i = 0; i < 8; ++i){
    regs[i] = 0;
  }

  UM_word instruction;
  int c;

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
      exit(0);
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
      c = getchar();
      if (c == EOF){
	regs[C(instruction)] = ~((UM_word) 0);
      }
      regs[C(instruction)] = c % 256;
      break;
    case LOAD_PROGRAM:
      UM_memory_load_program(memory, regs[B(instruction)]);
      program_counter = regs[C(instruction)] - 1;
      break;
    case LOAD_VALUE:
      // Program runs faster when this is separated out into it's own if
      // statement at the beginning... mysterious.
      regs[LV_REG(instruction)] = LV_VAL(instruction); // Savings: ~5.4 -> ~5.0
      break;
    }
    ++program_counter;
  }

  // Not that this should be reached in any reasonable scenario.
  UM_memory_free(memory);
}
