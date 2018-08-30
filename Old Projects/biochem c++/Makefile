OBJECTS=driver.o isomorphism.o molfile.o graph_mods.o rings.o mat_gen.o
NEWMAT=/usr/include/newmat10/
OPTS=-L$(NEWMAT) -lnewmat
NAME=free-energy
TESTPARAMS=tests/glutamate fgroups

test: $(NAME) $(TESTPARAMS)
	./$(NAME) $(TESTPARAMS)

$(NAME): $(OBJECTS)
	rm -f $(NAME); g++ $(OBJECTS) $(OPTS) -o $(NAME)

driver.o: driver.cpp driver.h definitions.h molfile.h isomorphism.h
	g++ -c driver.cpp

isomorphism.o: isomorphism.cpp isomorphism.h definitions.h molfile.h graph_mods.h
	g++ -c isomorphism.cpp

molfile.o: molfile.cpp molfile.h definitions.h
	g++ -c molfile.cpp

graph_mods.o: graph_mods.cpp graph_mods.h definitions.h
	g++ -c graph_mods.cpp

rings.o: rings.cpp rings.h definitions.h
	g++ -c rings.cpp

mat_gen.o: mat_gen.cpp mat_gen.h definitions.h
	g++ -c mat_gen.cpp

clean:
	rm -f $(OBJECTS)
