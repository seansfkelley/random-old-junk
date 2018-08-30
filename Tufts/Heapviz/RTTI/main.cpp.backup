#include <iostream>
#include <typeinfo>

#include "classes.h"

using namespace std;

void store_and_retrieve(int i, Base *b){
  typeid(*b).name();
}

int main(){
  Base *b;
  b = new PlusOne();
  store_and_retrieve(10, b);
  b = new MinusOne();
  store_and_retrieve(10, b);
  b = new PlusTwo();
  store_and_retrieve(10, b);
}
