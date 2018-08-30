#include <stdbool.h>
#include <stdio.h>

#include "ap.h"
#include "ap-ext.h"
#include "assert.h"

AP_T AP_gcd(AP_T a, AP_T b) {
  assert(AP_cmpi(a, 0) != 0);
  assert(AP_cmpi(b, 0) != 0);
  AP_T remainder, last_remainder, new_remainder;
  if (AP_cmp(a, b) < 0) {
    remainder = AP_addi(b, 0);
    last_remainder = AP_addi(a, 0);
  } else {
    remainder = AP_addi(b, 0);
    last_remainder = AP_addi(a, 0);
  }
  while (AP_cmpi(remainder, 0) != 0) {
    new_remainder = AP_mod(last_remainder, remainder);
    AP_free(&last_remainder);
    last_remainder = remainder;
    remainder = new_remainder;
  }
  AP_free(&remainder);
  return last_remainder;
}

bool AP_isKnownComposite(AP_T n, FILE *rand) {
  for (int i = 0; i<7; i++) {
    AP_T a = AP_new(0);
    while (AP_cmpi(a, 0) == 0 || AP_cmp(a, n) == 0) {
      while (AP_cmp(a, n) < 0) {
	AP_T new_a = AP_lshift(a, 8);
	AP_free(&a);
	int c = fgetc(rand);
	a = AP_addi(new_a, c);
	AP_free(&new_a);
      }
      AP_T temp = AP_mod(a, n);
      AP_free(&a);
      a = temp;
    }
    // now we have a random a less than n
    AP_T gcd = AP_gcd(a, n);
    if (AP_cmpi(gcd, 1) != 0) {
      AP_free(&gcd);
      AP_free(&a);
      return true;
    }
    AP_free(&gcd);
    AP_T nm1 = AP_subi(n, 1);
    AP_T exp = AP_pow(a, nm1, n);
    AP_free(&nm1);
    if (AP_cmpi(exp, 1) != 0) {
      AP_free(&a);
      AP_free(&exp);
      return true;
    }
    AP_free(&exp);
    AP_free(&a);
  }
  return false;
}

AP_T AP_next_3prime(AP_T n, FILE *rand) {
  assert(n);
  int r = AP_modi(n, 4);
  if (r == 3)
    r = 0;
  else
    r = 3 - r;
  AP_T candidate = AP_addi(n, r);

  while (AP_isKnownComposite(candidate, rand)) {
    AP_T temp = AP_addi(candidate, 4);
    AP_free(&candidate);
    candidate = temp;
  }
  return candidate;
}
