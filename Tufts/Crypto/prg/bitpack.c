#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "bitpack.h"

#define shift_left64(w, m)  ((w << (m % 63)) << (m - (m % 63)))
#define shift_right64(w, m)  ((w >> (m % 63)) >> (m - (m % 63)))

static const uint64_t one = 1;
static const uint64_t zero = 0;

bool Bitpack_fitsu(uint64_t n, unsigned width) {
  if (width >= 64) {
    return true;
  }
  
  uint64_t excess = shift_left64(one, width);
  return (n < excess);
}

bool Bitpack_fitss(int64_t n, unsigned width) {
  if (width >= 64) {
    return true;
  }

  int64_t negone = -1;

  int64_t excess = shift_left64(one, width-1);
  int64_t minimum = shift_left64(negone, width-1);

  return (n >= minimum && n < excess);
}

uint64_t Bitpack_getu(uint64_t word, unsigned width, unsigned lsb) {
  if (width + lsb > 64 || width == 0) {
    fprintf(stderr, "Bitpack: Value does not fit.\n");
    exit(1);
  }

  return (word << (64-(width+lsb))) >> (64-width);
}

int64_t Bitpack_gets(uint64_t word, unsigned width, unsigned lsb) {
  if (width + lsb > 64 || width == 0) {
    fprintf(stderr, "Bitpack: Value does not fit.\n");
    exit(1);
  }

  return ((int64_t)word << (64-(width+lsb))) >> (64-width);
}

uint64_t Bitpack_newu(uint64_t word, unsigned width, 
		      unsigned lsb, uint64_t value) {
  if (width + lsb > 64 || !Bitpack_fitsu(value, width)) {
    fprintf(stderr, "Bitpack: Value does not fit.\n");
    exit(1);
  }
  
  uint64_t filter = shift_left64(one, width) - 1;
  filter = shift_left64(filter, lsb);

  uint64_t result = word & (~filter);
  uint64_t insert = shift_left64(value, lsb);
  result = result | insert;

  return result;
}

uint64_t Bitpack_news(uint64_t word, unsigned width,
		      unsigned lsb,  int64_t value) {

  if (width + lsb > 64 || !Bitpack_fitss(value, width)) {
    fprintf(stderr, "Bitpack: Value does not fit.\n");
    exit(1);
  }

  uint64_t filter = shift_left64(one, width) - 1;
  filter = shift_left64(filter, lsb);
  
  uint64_t result = word & (~filter);
  int64_t insert = shift_left64(value, lsb);
  insert = insert & filter;
  result = result | insert;

  return result;
}
