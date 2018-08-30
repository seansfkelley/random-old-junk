#ifndef CLASSES_H
#define CLASSES_H

class Base{
 public:
 Base() : datum(0), __classname_index(0) {}
  int get(){ return datum; }

  virtual void set(int i) = 0;

 protected:
  int datum;

 private:
  int __classname_index;
private: int __classid;private: int __classid;private: int __classid;private: int __classid;};

class SecondBase{
 public:
 SecondBase() : datum2(0), __classname_index(1) {}

  virtual void set2(int i) = 0;

 protected:
  int datum2;

 private:
  int __classname_index;
private: int __classid;private: int __classid;private: int __classid;private: int __classid;};

class PlusOne : public Base{
 public:
 PlusOne() : __classname_index(2) {}
  void set(int i){ datum = i + 1; }

 private:
  int __classname_index;
private: int __classid;private: int __classid;private: int __classid;private: int __classid;};

class MinusOne : public Base{
 public:
 MinusOne() : __classname_index(3) {}
  void set(int i){ datum = i - 1; }

 private:
  int __classname_index;
private: int __classid;private: int __classid;private: int __classid;private: int __classid;};

class PlusTwo : public PlusOne, public SecondBase{
 public:
 PlusTwo() : __classname_index(4) {}
  void set(int i){ datum = i + 2; }
  void set2(int i){ datum2 = i + 2; }

 private:
  int __classname_index;
private: int __classid;private: int __classid;private: int __classid;private: int __classid;};

#endif
