#ifndef UM_TYPES_H
#define UM_TYPES_H

#include "inttypes.h"

typedef uint32_t UM_word;
typedef uint8_t  UM_opcode;

enum UM_opcode {COND_MOVE = 0, INDEX, UPDATE, ADD, MULTIPLY, DIVIDE, NAND,
     HALT, ACTIVATE, INACTIVATE, OUTPUT, INPUT, LOAD_PROGRAM, LOAD_VALUE};

#endif
