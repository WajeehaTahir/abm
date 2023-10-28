# ABM Simulator

## Project Purpose

The ABM Simulator project aims to develop a stack-based microprocessor simulator for the ABM abstract machine. The objective is to create a robust simulator capable of executing any program written in the ABM machine language.

## Overview

The ABM Simulator implements the instructions provided in the ABM abstract machine, allowing users to execute ABM programs. It supports a range of operations, including stack manipulation, control flow, arithmetic and logical operators, relational operators, output functionalities, and subprogram control.

### Supported Operations

- **Stack Manipulation:** Includes operations such as push, rvalue, lvalue, pop, :=, and copy.
- **Control Flow:** Instructions for labels, jumps, conditional jumps, and halting execution.
- **Arithmetic & Logical Operators:** Arithmetic operations like addition, subtraction, multiplication, division, and logical AND, OR, and NOT operations.
- **Relational Operators:** Instructions for comparison operations like less than, greater than, equal to, not equal to, etc.
- **Output:** Functions to print stack contents and display literal strings.
- **Subprogram Control:** Marking subprogram beginnings and endings, returning from subroutines, and making subroutine calls.

### Implementation

The simulator is written in Python and provided as a class named `ABM`. It reads and compiles ABM code from a file, then runs the simulation for the compiled code.

## Getting Started

1. **Compile:** Use the `compile` method to load ABM code from a file and parse it into instructions and labels.
2. **Run:** Utilize the `run` method to execute the compiled code on the simulator.

Example:

```python
obj = ABM()
obj.compile("recursiveFactorial.abm")
obj.run()
```

This example compiles the `recursiveFactorial.abm` file and runs the simulation.

## Files Included

The project contains sample ABM program files such as `demo.abm`, `factProc.abm`, `foo.abm`, `operatorsTest.abm`, and `recursiveFactorial.abm`. These files can be used for reference to understand the syntax and semantics of the ABM machine language.

### Note

The project is designed for Linux operating systems and is intended to be a functional, comprehensive ABM simulator.

*Documented by ChatGPT*
