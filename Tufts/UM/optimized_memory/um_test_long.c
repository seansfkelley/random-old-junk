#include <string.h>

#include "seq.h"
#include "um.h"
#include "um_unit_test.h"

int main(){
  Seq_T inst = Seq_new(10);

  char *str = "Beginning 50-million instruction unit test!\n";
  for (unsigned i = 0; i < strlen(str); ++i){
    emit_load_value(inst, r0, str[i]);
    emit_output(inst, r0);
  }

  // For loop, with an empty body. UM version.
  
  emit_load_value(inst, r1, 1);                    // increment amount
  emit_load_value_32_bits(inst, r5, r0, 10000000); // upper bound
  emit_load_value(inst, r6, 0);                    // instruction array

  emit_load_value(inst, r0, 0); // loop counter
  
  emit_add(inst, r0, r0, r1);                      // increment
  emit_subtract(inst, r0, r5, r3, r2);             // termination condition
  emit_load_value(inst, r4, Seq_length(inst) - 5); //  |
  emit_load_value(inst, r7, Seq_length(inst) + 3); //  |
  emit_cond_move(inst, r7, r4, r3);                //  |
  emit_load_program(inst, r6, r7);                 //  -

  // The -5 and +3 in the load values amount to simple labelling - they dictate
  // where to jump to (-5: the beginning of the loop; +3: break the loop).

  str = "50 million instructions finished!\n";
  for (unsigned i = 0; i < strlen(str); ++i){
    emit_load_value(inst, r0, str[i]);
    emit_output(inst, r0);
  }

  emit_halt(inst);

  UM_main(inst);
  Seq_free(&inst);
}
