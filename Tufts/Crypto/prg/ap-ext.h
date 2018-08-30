#include <stdbool.h>
#include "ap.h"

// returns the gcd of a and b
AP_T AP_gcd(AP_T a, AP_T b);

// returns the next prime congruent to 3 mod 4 after a
AP_T AP_next_3prime(AP_T a, FILE *rand);

// returns true if a is definitely a composite, false if it is probably a prime
bool AP_isKnownComposite(AP_T n, FILE *rand);
