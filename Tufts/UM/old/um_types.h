#ifndef UM_TYPES_H
#define UM_TYPES_H

#include "inttypes.h"

typedef uint32_t UM_word;
typedef uint8_t  UM_reg_index;
typedef uint8_t  UM_opcode;

#define T UM_state

// The 8 registers, which are currently selected for use, and the PC.
// Initialization is left up to the user of this struct.
typedef struct T{
  UM_word regs[8];
  UM_reg_index A, B, C; // Which registers are selected by the currently
                        // executing instruction.
  UM_word program_counter;
}* T;

#undef T

#endif
