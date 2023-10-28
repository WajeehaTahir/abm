class ABM:
    filename = ""
    instructions = {}
    labels = {}
    variable_stack = []
    integer_stack = []
    data_segment = [{}]
    frame_pointer = 0
    halt = False;
    current_instruction = 0
    argument_flag = 0   #0: write in own frame, 1: read from parent and write to child frame, 2: read from child and write to parent frame
    return_address = []

    def compile(self, filename):    #load code from file and parse into instructions and labels
        self.filename = filename
        with open(self.filename) as f:
            self.instructions = {number: (line.rstrip('\n')).strip() for number, line in enumerate(f)}  #taking line number as key and instruction string as value
        self.labels = {instruction.split(' ', 1)[1]: number for number, instruction in enumerate(list(self.instructions.values())) if instruction.split(' ', 1)[0] == "label"}  #if instruction string contains the word label, take label name as key and line number as value
        f.close()
        f = open(self.filename[:len(self.filename) - 4] + ".out", "w")  #creating output file
        f.close()

    def run(self):
        while (self.current_instruction < len(self.instructions) and not(self.halt)):   #if either the code ends or halt flag is on, end
            instruction = self.instructions[self.current_instruction]   #load instruction
            ins = instruction.split(' ', 1)[0]  #get instruction keyword

            if ins == "goto" or ins == "gofalse" or ins == "gotrue" or ins == "halt":
                self.control_flow(instruction)

            if ins == "print" or ins == "show":
                self.output(instruction)

            if ins == "push" or ins == "rvalue" or ins == "lvalue" or ins == "pop" or ins == ":=" or ins == "copy":
                self.stack_manipulation(instruction)
            
            if ins == "+" or ins == "-" or ins == "*" or ins == "/" or ins == "div":
                self.arithmetic(ins)

            if ins == "&" or ins == "!" or ins == "|":
                self.logical(ins)

            if ins == "<>" or ins == "<=" or ins == ">=" or ins == "<" or ins == ">" or ins == "=":
                self.relational(ins)

            if ins == "begin" or ins == "end" or ins == "return" or ins == "call":
                self.subprogram_control(instruction)

            self.current_instruction = self.current_instruction + 1 #move to next instruction

    def stack_manipulation(self, instruction):
        ins = instruction.split(' ', 1)[0]  #instruction keyword

        if ins == "push":
            self.integer_stack.append(int(instruction.split(' ', 1)[1]))

        if ins == "rvalue":
            temp = self.frame_pointer
            if self.argument_flag == 1: #if a new function is being called
                temp = temp - 1     #point to parent frame
            if instruction.split(' ', 1)[1] not in self.data_segment[temp]:
                self.data_segment[temp][instruction.split(' ', 1)[1]] = 0   #if variable doesn't exist, create and initialize to zero
            self.integer_stack.append(int(self.data_segment[temp][instruction.split(' ', 1)[1]]))   #copy variable value to integer stack

        if ins == "lvalue":
            self.variable_stack.append(instruction.split(' ', 1)[1])    #add variable name to variable stack

        if ins == "pop":
            del self.integer_stack[-1]

        if ins == ":=":
            temp = self.frame_pointer
            if self.argument_flag == 2: #if function is returning
                temp = temp - 1 #point to parent frame
            self.data_segment[temp][self.variable_stack[-1]] = self.integer_stack[-1]   #store value in variable
            del self.integer_stack[-1]
            del self.variable_stack[-1]

        if ins == "copy":
            self.integer_stack.append(self.integer_stack[-1])
    
    def control_flow(self, instruction):
        if instruction == "halt":
            self.halt = True

        ins = instruction.split(' ', 1)[0]  #instruction keyword

        if ins == "goto":
            self.current_instruction = self.labels[instruction.split(' ', 1)[1]]    #set current instruction to line number of label
        
        if ins == "gofalse":
            if not(self.integer_stack[-1]): #if top value is 0
                self.current_instruction = self.labels[instruction.split(' ', 1)[1]]

        if ins == "gotrue":
            if self.integer_stack[-1]:  #if top value is 1
                self.current_instruction = self.labels[instruction.split(' ', 1)[1]]

    def arithmetic(self, instruction):
        a = self.integer_stack[-1]  #first integer
        del self.integer_stack[-1]
        b = self.integer_stack[-1]  #second integer
        del self.integer_stack[-1]

        if instruction == "+":
            self.integer_stack.append(a+b)
            
        if instruction == "-":
            self.integer_stack.append(b-a)
            
        if instruction == "*":
            self.integer_stack.append(a*b)
            
        if instruction == "/":
            self.integer_stack.append(int(b/a))
            
        if instruction == "div":
            self.integer_stack.append(b%a)

    def logical(self, instruction):
        a = self.integer_stack[-1]
        del self.integer_stack[-1]

        if instruction == "!":
            self.integer_stack.append(int(not(a)))

        else:
            b = self.integer_stack[-1]
            del self.integer_stack[-1]

            if instruction == "&":
                self.integer_stack.append(a&b)
            
            if instruction == "|":
                self.integer_stack.append(a|b)

    def relational(self, instruction):
        a = self.integer_stack[-1]
        del self.integer_stack[-1]
        b = self.integer_stack[-1]
        del self.integer_stack[-1]

        if instruction == "<>":
            self.integer_stack.append(int(a!=b))
            
        if instruction == "<=":
            self.integer_stack.append(int(b<=a))
            
        if instruction == ">=":
            self.integer_stack.append(int(b>=a))
            
        if instruction == "<":
            self.integer_stack.append(int(b<a))
            
        if instruction == ">":
            self.integer_stack.append(int(b>a))

        if instruction == "=":
            self.integer_stack.append(int(a==b))

    def output(self, instruction):
        f = open(self.filename[:len(self.filename) - 4] + ".out", "a")  #open output file in append mode
        if instruction.split(' ', 1)[0] == "show":
            print((instruction.split(' ', 1)[1]).strip() if (len(instruction) > 4) else "\n")   #display the string contained in the instruction
            f.write(((instruction.split(' ', 1)[1]).strip() + "\n") if (len(instruction) > 4) else "\n")    #write the same string to file
    
        if instruction.split(' ', 1)[0] == "print":
            print(self.integer_stack[-1])   #display top value of integer stack
            f.write(str(self.integer_stack[-1]) + "\n") #write to file too
            
        f.close()

    def subprogram_control(self, instruction):
        ins = instruction.split(' ', 1)[0]  #instruction keyword
        if ins == "begin":
            self.data_segment.append({})    #create new frame
            self.frame_pointer = self.frame_pointer + 1;
            self.argument_flag = 1; #flag to transfer values from parent to child frame

        if ins == "end":
            self.frame_pointer = self.frame_pointer - 1
            self.argument_flag = 0
            del self.data_segment[-1]   #delete last added frame

        if ins == "return":
            self.argument_flag = 2  #flag to return values from child to parent
            self.current_instruction = self.return_address[-1]  #return to instruction that followed the function call
            del self.return_address[-1] #pop return address

        if ins == "call":
            self.argument_flag = 0
            self.return_address.append(self.current_instruction)    #save return address
            self.current_instruction = self.labels[instruction.split(' ', 1)[1]]    #set current instruction to label line number


obj = ABM()
obj.compile("recursiveFactorial.abm")
obj.run()