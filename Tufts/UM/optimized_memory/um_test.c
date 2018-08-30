#include <stdio.h>
#include <string.h>

#include "um.h"
#include "seq.h"
#include "um_unit_test.h"

int main(){
  Seq_T inst = Seq_new(10);
  
  // ------------------------------------------------------------ Test 1 - Halt
  emit_halt(inst);
  
  UM_main(inst);
  printf("Test 1 - Halt passed!\n");
  
  Seq_free(&inst);
  inst = Seq_new(10);

  // ------------------------------------------ Test 2 - Load Value, and Output
  char *str = "Test 2 - Load and Output passed!\n";
  for (unsigned i = 0; i < strlen(str); ++i){
    emit_load_value(inst, r0, str[i]);
    emit_output(inst, r0);
  }
  emit_halt(inst);

  UM_main(inst);

  Seq_free(&inst);
  inst = Seq_new(10);

  // ----------------------------------------------------------- Test 3 - Input
  emit_input(inst, r0);
  str = "Test 3 - Input passed if your letter follows: ";
  for (unsigned i = 0; i < strlen(str); ++i){
    emit_load_value(inst, r1, str[i]);
    emit_output(inst, r1);
  }
  emit_output(inst, r0);
  emit_halt(inst);
  
  printf("Type a letter and press enter: ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // ------------------------------------------------ Test 4 - Conditional Move
  emit_load_value(inst, r0, 'A');
  emit_load_value(inst, r1, 'B');
  emit_load_value(inst, r2, 0); // C
  emit_cond_move(inst, r0, r1, r2);
  emit_output(inst, r0);
  emit_load_value(inst, r2, 1);
  emit_cond_move(inst, r0, r1, r2);
  emit_output(inst, r0);
  emit_halt(inst);

  printf("Test 4 - Conditional Move passed if this line ends with \"AB\": ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // ------------------------------------------------------------- Test 5 - Add
  emit_load_value(inst, r0, '5' - 1);
  emit_load_value(inst, r1, 1);
  emit_add(inst, r2, r0, r1);
  emit_output(inst, r2);
  emit_halt(inst);

  printf("Test 5 - Add passed if this line ends with \"5\": ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // -------------------------------------------------------- Test 6 - Multiply
  emit_load_value(inst, r0, 2);
  emit_load_value(inst, r1, 27);
  emit_multiply(inst, r2, r0, r1);
  emit_output(inst, r2);
  emit_halt(inst);

  printf("Test 6 - Multiply passed if this line ends with \"6\": ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // ---------------------------------------------------------- Test 7 - Divide
  emit_load_value(inst, r0, 110);
  emit_load_value(inst, r1, 2);
  emit_divide(inst, r2, r0, r1);
  emit_output(inst, r2);
  emit_load_value(inst, r0, 223);
  emit_load_value(inst, r1, 4);
  emit_divide(inst, r2, r0, r1);
  emit_output(inst, r2);
  emit_halt(inst);

  printf("Test 7 - Divide passed if this line ends with \"77\": ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // ------------------------------------------------------------ Test 8 - NAND
  UM_word all_ones = 4294967295; // 2^32 - 1

  emit_load_value_32_bits(inst, r0, r3, all_ones - 1);
  emit_load_value_32_bits(inst, r1, r3, all_ones - 1);
  emit_nand(inst, r2, r0, r1);
  emit_load_value(inst, r3, '8' - 1);
  emit_add(inst, r2, r2, r3);
  emit_output(inst, r2);
  
  emit_load_value_32_bits(inst, r0, r3, all_ones - 1); 
  emit_load_value_32_bits(inst, r1, r3, all_ones);
  emit_nand(inst, r2, r0, r1);
  emit_load_value(inst, r3, '8' - 1);
  emit_add(inst, r2, r2, r3);
  emit_output(inst, r2);

  emit_load_value_32_bits(inst, r0, r3, all_ones); 
  emit_load_value_32_bits(inst, r1, r3, all_ones);
  emit_nand(inst, r2, r0, r1);
  emit_load_value(inst, r3, '8');
  emit_add(inst, r2, r2, r3);
  emit_output(inst, r2);
  emit_halt(inst);
  
  printf("Test 8 - NAND passed if this line ends with \"888\": ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // -------------------------------------------------------- Test 9 - Activate
  emit_activate(inst, r0, r1);
  emit_load_value(inst, r1, 'P');
  emit_load_value(inst, r2, 'F');
  emit_cond_move(inst, r2, r1, r0);
  emit_output(inst, r2);
  emit_halt(inst);
  
  printf("Test 9 - Activate passed if this line ends with \"P\": ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);
  
  // ----------------------------------------------------- Test 10 - Inactivate
  emit_activate(inst, r7, r0);
  emit_inactivate(inst, r7);
  emit_activate(inst, r6, r0);
  emit_subtract(inst, r6, r7, r0, r1);
  emit_load_value(inst, r1, 'P');
  emit_load_value(inst, r2, 'F');
  emit_cond_move(inst, r1, r2, r0);
  emit_output(inst, r1);
  emit_halt(inst);
  
  printf("Test 10 - Inactivate passed if this line ends with \"P\": ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // ---------------------------------------------------------- Test 11 - Index
  emit_load_value(inst, r1, 1);
  emit_activate(inst, r0, r1);
  emit_load_value(inst, r1, 0);
  emit_index(inst, r2, r0, r1);
  emit_load_value(inst, r3, '0');
  emit_add(inst, r2, r2, r3);
  emit_output(inst, r2);
  emit_halt(inst);
  
  printf("Test 11 - Index passed if this line ends with \"0\": ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // --------------------------------------------------------- Test 12 - Update
  emit_load_value(inst, r1, 1);
  emit_activate(inst, r0, r1);
  emit_load_value(inst, r1, 0);
  emit_load_value(inst, r3, '1');
  emit_update(inst, r0, r1, r3);
  emit_index(inst, r2, r0, r1);
  emit_output(inst, r2);
  emit_halt(inst);
  
  printf("Test 12 - Update passed if this line ends with \"1\": ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // ---------------------------------------------------------- Test 13A - Goto
  emit_load_value(inst, r0, 'F');
  emit_load_value(inst, r1, 0);
  emit_load_value(inst, r2, 5);
  emit_load_program(inst, r1, r2);
  emit_output(inst, r0);
  emit_halt(inst);
  
  printf("Test 13A - Goto passed if no output follows: ");
  UM_main(inst);
  printf("\n");

  Seq_free(&inst);
  inst = Seq_new(10);

  // -------------------------------------------------- Test 13B - Load Program
  emit_load_value(inst, r0, 'P');
  emit_output(inst, r0);
  emit_load_value(inst, r6, 2);
  emit_activate(inst, r7, r6);
  emit_load_value_32_bits(inst, r1, r2, (unsigned long) Seq_get(inst, 1));
  emit_load_value(inst, r3, 0);
  emit_update(inst, r7, r3, r1);

  // Due to our lack of labels and design of the emit* functions, the best way
  // to get a single HALT instruction is to create this temporary sequence.
  Seq_T temp = Seq_new(1);
  emit_halt(temp);

  emit_load_value_32_bits(inst, r1, r2, (unsigned long) Seq_get(temp, 0));
  emit_load_value(inst, r4, 1);
  emit_update(inst, r7, r4, r1);
  emit_load_program(inst, r7, r3);
  emit_halt(inst);
  
  printf("Test 13B - Load Program passed if this line ends with \"PP\": ");
  UM_main(inst);
  printf("\n");
}
