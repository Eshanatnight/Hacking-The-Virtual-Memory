CC = gcc
CXX = g++

OUTPUT_DIR = ./build
OBJ_DIR =  $(OUTPUT_DIR)/intermediates
SRC_DIR =  ./src


# Compiler flags
CFLAGS = -Og -Wall -Wextra -Wpedantic -Werror

all: main
	$(CC) $(CFLAGS) $(OBJ_DIR)/loop.o -o $(OUTPUT_DIR)/loop

run: main
	$(CC) $(CFLAGS) $(OBJ_DIR)/loop.o -o $(OUTPUT_DIR)/loop
	$(OUTPUT_DIR)/loop

main:
	$(CC) $(CFLAGS) -c src/loop.c -o $(OBJ_DIR)/loop.o
