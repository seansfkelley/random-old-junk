// To do:
// unit tests
// ask - should memory be able to handle allocations of size 0?
//     - should it skip allocation and instead use null/length 0?
// benchmarking - it's pretty slow :(

#include <stdio.h>
#include <stdlib.h>
#include "um_types.h"
#include "um.h"
#include "seq.h"
#include "bitpack.h"

#include "inttypes.h"

Seq_T file_to_seq(FILE *fp){
  Seq_T inst_seq = Seq_new(256);					
  UM_word instruction;
  unsigned char c;
  while (!feof(fp)){
    instruction = 0;
    for (int i = 24; i >= 0; i -= 8){
      c = fgetc(fp);
      // printf("%d: %u\n", i, c);
      instruction = Bitpack_newu(instruction, 8, i, c);
    }
    Seq_addhi(inst_seq, (void *)(unsigned long) instruction);
  }
  return inst_seq;
}

int main(int argc, char *argv[]){
  if (argc == 1){
    UM_main(file_to_seq(stdin));
  }
  else if(argc == 2){ 
    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL){
      fprintf(stderr, "%s: %s could not be opened for reading\n",
	      argv[0], argv[1]);
      exit(1);
    }
    UM_main(file_to_seq(fp));
    fclose(fp);
  }
  else{
    fprintf(stderr, "%s: too many files\n", argv[0]);
    exit(1);
  }
}
