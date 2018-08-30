#ifndef UM_UNIT_TEST_H
#define UM_UNIT_TEST_H

#include "seq.h"
#include "bitpack.h"
#include "inttypes.h"
#include "um_types.h"

typedef uint8_t reg_index;

enum reg_index {r0 = 0, r1, r2, r3, r4, r5, r6, r7};

static void emit_codeword(Seq_T inst, UM_opcode opcode, reg_index A,
		   reg_index B, reg_index C, UM_word value){
  uint64_t codeword = Bitpack_newu(0, 4, 28, opcode);
  if (opcode != LOAD_VALUE){
    codeword = Bitpack_newu(codeword, 3, 0, C);
    codeword = Bitpack_newu(codeword, 3, 3, B);
    codeword = Bitpack_newu(codeword, 3, 6, A);
  }
  else{
    codeword = Bitpack_newu(codeword, 3, 25, A);
    codeword = Bitpack_newu(codeword, 25, 0, value);
  }

  Seq_addhi(inst, (void *)(unsigned long) codeword);
}

static inline void emit_cond_move(Seq_T inst, reg_index A,
				  reg_index B, reg_index C){
  emit_codeword(inst, COND_MOVE, A, B, C, 0);
}

static inline void emit_index(Seq_T inst, reg_index A,
			      reg_index B, reg_index C){
  emit_codeword(inst, INDEX, A, B, C, 0);
}

static inline void emit_update(Seq_T inst, reg_index A,
			       reg_index B, reg_index C){
  emit_codeword(inst, UPDATE, A, B, C, 0);
}

static inline void emit_add(Seq_T inst, reg_index A,
			    reg_index B, reg_index C){
  emit_codeword(inst, ADD, A, B, C, 0);
}

static inline void emit_multiply(Seq_T inst, reg_index A,
				 reg_index B, reg_index C){
  emit_codeword(inst, MULTIPLY, A, B, C, 0);
}

static inline void emit_divide(Seq_T inst, reg_index A,
			       reg_index B, reg_index C){
  emit_codeword(inst, DIVIDE, A, B, C, 0);
}

static inline void emit_nand(Seq_T inst, reg_index A,
			     reg_index B, reg_index C){
  emit_codeword(inst, NAND, A, B, C, 0);
}

static inline void emit_halt(Seq_T inst){
  emit_codeword(inst, HALT, 0, 0, 0, 0);
}

static inline void emit_activate(Seq_T inst, reg_index B, reg_index C){
  emit_codeword(inst, ACTIVATE, 0, B, C, 0);
}

static inline void emit_inactivate(Seq_T inst, reg_index C){
  emit_codeword(inst, INACTIVATE, 0, 0, C, 0);
}

static inline void emit_output(Seq_T inst, reg_index C){
  emit_codeword(inst, OUTPUT, 0, 0, C, 0);
}

static inline void emit_input(Seq_T inst, reg_index C){
  emit_codeword(inst, INPUT, 0, 0, C, 0);
}

static inline void emit_load_program(Seq_T inst, reg_index B, reg_index C){
  emit_codeword(inst, LOAD_PROGRAM, 0, B, C, 0);
}

static inline void emit_load_value(Seq_T inst, reg_index A, UM_word value){
  emit_codeword(inst, LOAD_VALUE, A, 0, 0, value);
}


// Composite instructions.
static inline void emit_load_value_32_bits(Seq_T inst, reg_index A,
					   reg_index B, UM_word value){
  emit_load_value(inst, A, value >> 7);
  emit_load_value(inst, B, 1 << 7);
  emit_multiply(inst, A, A, B);
  emit_load_value(inst, B, value % (1 << 7));
  emit_add(inst, A, A, B);  
}

static inline void emit_subtract(Seq_T inst, reg_index A, reg_index B,
				 reg_index C, reg_index D){
  emit_nand(inst, C, B, B);
  emit_load_value(inst, D, 1);
  emit_add(inst, C, C, D);
  emit_add(inst, C, C, A);
}

#endif
