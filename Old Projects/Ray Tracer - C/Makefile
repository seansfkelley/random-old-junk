OBJECTS=ray.o sphere.o tracer.o vec.o 
CC=g++
NAME=rt
OPTS=`freetype-config --cflags` -I/usr/local/include  -L/usr/local/lib -lpng -lpngwriter -lz -lfreetype
TESTPARAMS=

test: $(NAME) $(TESTPARAMS)
	./$(NAME) $(TESTPARAMS)

$(NAME): $(OBJECTS)
	rm -f $(NAME); $(CC) $(OBJECTS) $(OPTS) -o $(NAME)

all_objects.h:

defs.h: 

object.h: defs.h ray.h 

ray.h: defs.h vec.h 

sphere.h: object.h 

tracer.h: all_objects.h defs.h ray.h vec.h 

vec.h: defs.h 

ray.o: ray.cpp ray.h 
	$(CC) $(OPTS) -c ray.cpp

sphere.o: sphere.cpp sphere.h 
	$(CC) $(OPTS) -c sphere.cpp

tracer.o: tracer.cpp tracer.h 
	$(CC) $(OPTS) -c tracer.cpp

vec.o: vec.cpp vec.h 
	$(CC) $(OPTS) -c vec.cpp

clean:
	rm -f $(OBJECTS)
