#ifndef BITSTREAM_T
#define BITSTREAM_T

#include <stdio.h>
#include <stdint.h>

#define T Bitstream_T
typedef struct T *T;

extern T Bitstream_new(FILE *fp, char mode); //creates a new bitstream outputting to fp
extern void Bitstream_free(T *bsptr);
/* Frees an instance of Bitstream. If the bistream has not been flushed since
 * the last call to Bitstream_put, it is not guaranteed that all bits have
 * been written. */

extern uint64_t Bitstream_get(T bs, unsigned numbits);
extern void Bitstream_put(T bs, uint64_t word, unsigned numbits);
/* Dumps the least significant numbits bits of word onto the bitstream. May
 * not output them to file immediately. */
extern void Bitstream_flush(T bs);
/* Flushes the stream, guaranteeing that all bits put on the stream have been
 * output to file. The output will be padded to the nearest 8 bits by 0's */

#undef T
#endif
