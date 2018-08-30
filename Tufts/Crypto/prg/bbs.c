#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "ap.h"
#include "ap-ext.h"
#include "assert.h"
#include "bitstream.h"

AP_T get_seed(int numbits, Bitstream_T bin);

int main(int argc, char *argv[]) {
  if (argc != 3) {
    fprintf(stderr, "Usage: %s seedsize numbits\n", argv[0]);
    exit(1);
  }
  
  int seedsize = atoi(argv[1]);
  if (seedsize <= 0) {
    fprintf(stderr, "%s: seedsize must be a positive integer\n", argv[0]);
    exit(1);
  }
  if (seedsize < 32) {
    fprintf(stderr, "%s: working with small seed sizes isn't interesting\n",
	    argv[0]);
    exit(1);
  }
  int numbits = atoi(argv[2]);
  if (numbits <= 0) {
    fprintf(stderr, "%s: numbits must be a positive integer\n", argv[0]);
    exit(1);
  }

  FILE *rand = fopen("/dev/random", "r");
  Bitstream_T bin = Bitstream_new(rand, 'r');

  AP_T pp = get_seed(seedsize/4, bin);
  AP_T pq = get_seed(seedsize/4, bin);
  AP_T x = get_seed(seedsize/2, bin);

  AP_T p = AP_next_3prime(pp, rand);
  AP_T q = AP_next_3prime(pq, rand);
  AP_free(&pp);
  AP_free(&pq);
  AP_T n = AP_mul(p, q);
  AP_free(&p);
  AP_free(&q);

  AP_T two = AP_new(2);

  Bitstream_free(&bin);
  fclose(rand);

  AP_T start = AP_pow(x, two, n);
  AP_free(&x);
  AP_T gcd = AP_gcd(start, n);
  if (AP_cmpi(gcd, 1) != 0) {
    fprintf(stderr, "How unlikely, we stumbled on a factor of n...aborting\n");
    AP_free(&gcd);
    AP_free(&start);
    AP_free(&n);
    AP_free(&two);
    exit(1);
  }
  AP_free(&gcd);
  AP_T current = AP_pow(start, two, n);

  AP_T pseudorandom = AP_new(0);
  for (int i=0; i<numbits && AP_cmp(start, current) != 0; i++){
    int b = AP_modi(current, 2);
    AP_T temp = AP_lshift(pseudorandom, 1);
    AP_free(&pseudorandom);
    pseudorandom = AP_addi(temp, b);
    AP_free(&temp);
    temp = AP_pow(current, two, n);
    AP_free(&current);
    current = temp;
  }

  if (AP_cmp(start, current) == 0) {
    fprintf(stderr, "%s: Generated more bits than the security parameter... "
	    "aborted early\n", argv[0]);
  }

  char *s = AP_tostr(NULL, 0, 10, pseudorandom);
  fprintf(stderr, "%s\n", s);
  
  free(s);
  AP_free(&pseudorandom);
  AP_free(&n);
  AP_free(&current);
  AP_free(&start);
  AP_free(&two);

  return 0;
}

AP_T get_seed(int numbits, Bitstream_T bin) {
  AP_T seed = AP_new(0);
  for (int i=0; i<numbits/64; i++) {
    uint64_t q = Bitstream_get(bin, 64);
    AP_T temp = AP_lshift(seed, 64);
    AP_free(&seed);
    seed = AP_addi(temp, q);
    AP_free(&temp);
  }
  if (numbits % 64 != 0) {
    uint64_t q = Bitstream_get(bin, numbits % 64);
    AP_T temp = AP_lshift(seed, numbits % 64);
    AP_free(&seed);
    seed = AP_addi(temp, q);
    AP_free(&temp);
  }
  return seed;
}
