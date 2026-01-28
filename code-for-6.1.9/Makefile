
CXX = g++


CXXFLAGS = -std=c++17 -Wall -g


TARGET = exec

SRCS = driver.cc graph.cc


OBJS = $(SRCS:.cc=.o)



all: $(TARGET)


$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

%.o: %.cc graph.hpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(TARGET) $(OBJS)

.PHONY: all clean exec