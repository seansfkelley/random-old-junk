#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "bitstream.h"
#include "bitpack.h"

#define T Bitstream_T
struct T {
  FILE *fp;
  unsigned head; // which bit of the character 'stream' is next to be written
  char stream; // the bits that have yet to be written to file
  char mode;
};

static inline void Bitstream_pull(T bs) {
  if (bs->head != 8) {
    int t = fgetc(bs->fp);
    if (t == EOF) {
      fprintf(stderr, "Bitstream: Premature EOF\n");
      exit(1);
    }
    bs->stream = t;
    bs->head = 8;
  }
}

/* Bits are written as follows:
 * char stream: _ _ _ _ _ _ _ _
 *              8 7 6 5 4 3 2 1
 * if the head is currently on 8, and the bits '001' are written:
 *              0 0 1 _ _ _ _ _
 * the head will now be on 8-3=5. If the head is on zero, the character
 * is written to file and the head is reset to 8.
 */

T Bitstream_new(FILE *fp, char mode) {
  T bs = malloc(sizeof(struct T));
  bs->fp = fp;
  bs->head = 8;
  bs->mode = mode;
  if (mode == 'w')
    bs->stream = 0;
  else {
    int t = fgetc(bs->fp);
    bs->stream = t;
  }
  return bs;
}

void Bitstream_free(T *bsptr) {
  free(*bsptr);
  *bsptr = NULL;
}

uint64_t Bitstream_get(T bs, unsigned numbits) {
  if (bs->mode != 'r') {
    fprintf(stderr, "Bitstream: invalid read\n");
    exit(1);
  }
  uint64_t word = 0;
  if (bs->head >= numbits) {
    bs->head -= numbits;
    word = Bitpack_getu(bs->stream, numbits, bs->head);
    if(bs->head == 0)
      Bitstream_pull(bs);
  } else {
    // first, pull the current char
    word = Bitpack_newu(0, bs->head, numbits-bs->head,
				 Bitpack_getu(bs->stream, bs->head, 0));
    numbits -= bs->head;
    bs->head = 0;
    Bitstream_pull(bs);
    while (numbits > 0) {
      if (numbits >= 8) {
	word = Bitpack_newu(word, 8, numbits-8, 
			    Bitpack_getu(bs->stream, 8, 0));
	bs->head = 0;
	Bitstream_pull(bs);
	numbits -= 8;
      } else {
	bs->head = 8 - numbits;
	word = Bitpack_newu(word, numbits, 0,
			    Bitpack_getu(bs->stream, numbits, bs->head));
	numbits = 0;
      }
    }
  }
  return word;
}

void Bitstream_put(T bs, uint64_t word, unsigned numbits) {
  if (bs->mode != 'w') {
    fprintf(stderr, "Bitstream: invalid write\n");
    exit(1);
  }
  if (bs->head >= numbits) {
    bs->head -= numbits;
    bs->stream = Bitpack_newu(bs->stream, numbits, bs->head, word);
    if (bs->head == 0)
      Bitstream_flush(bs);
  } else {
    // first, fill the current char
    bs->stream = Bitpack_newu(bs->stream, bs->head, 0,
			      Bitpack_getu(word, bs->head,
					   numbits - bs->head));
    numbits -= bs->head;
    bs->head = 0;
    Bitstream_flush(bs);
    while (numbits > 0) {
      if (numbits >= 8) {
	bs->stream = Bitpack_getu(word, 8, numbits-8);
	bs->head = 0;
	Bitstream_flush(bs);
	numbits -= 8;
      } else {
	bs->head = 8 - numbits;
	bs->stream = Bitpack_newu(bs->stream, numbits, bs->head,
				  Bitpack_getu(word, numbits, 0));
	numbits = 0;
      }
    }
  }
 }

void Bitstream_flush(T bs) {
  if (bs->mode != 'w') {
    fprintf(stderr, "Bitstream: invalid flush\n");
    exit(1);
  }
  // it is guaranteed that the unused bits in stream are zero
  if (bs->head != 8) {
    fputc(bs->stream, bs->fp);
    bs->head = 8;
    bs->stream = 0;
  }
}

#undef T
