from typing import Dict, List

class IntCodeProcessor:

    def __init__(self, data_tape, inputs=[]):
        self.data_tape = data_tape.copy()
        self.pcntr = 0
        self.finished = False
        self.inputs = iter(inputs)
        self.outputs = []

    def run_program(self):
        while not self.finished and self.pcntr < len(self.data_tape):
            self.process_instruction()
    
    def process_instruction(self):
        
        instr_base = self.data_tape[self.pcntr]
        instr = instr_base % 100
        arg_refstr = str(instr_base // 100)[::-1]

        # Add Instruction
        if instr == 1:
            calc = self.fetch_arg(arg_refstr, 0) + self.fetch_arg(arg_refstr, 1)
            self.put_value(arg_refstr, 2, calc)
            self.pcntr += 4
        # Multiply Instruction
        elif instr == 2:
            calc = self.fetch_arg(arg_refstr, 0) * self.fetch_arg(arg_refstr, 1)
            self.put_value(arg_refstr, 2, calc)
            self.pcntr += 4
        # Get Input Instruction
        elif instr == 3:
            try:
                value = next(self.inputs)
            except StopIteration:
                raise ValueError("Ran out of input values while running!")
            self.put_value(arg_refstr, 0, value)
            self.pcntr += 2
        # Send Output Instruction
        elif instr == 4:
            value = self.fetch_arg(arg_refstr, 0)
            self.outputs.append(value)
            self.pcntr += 2
        # Jump-if-true Instruction
        elif instr == 5:
            value = self.fetch_arg(arg_refstr, 0)
            if value != 0:
                self.pcntr = self.fetch_arg(arg_refstr, 1)
            else:
                self.pcntr += 3
        # Jump-if-false Instruction
        elif instr == 6:
            value = self.fetch_arg(arg_refstr, 0)
            if value == 0:
                self.pcntr = self.fetch_arg(arg_refstr, 1)
            else:
                self.pcntr += 3
        # Less-than instruction
        elif instr == 7:
            compare = self.fetch_arg(arg_refstr, 0) < self.fetch_arg(arg_refstr, 1)
            self.put_value(arg_refstr, 2, int(compare))
            self.pcntr += 4
        # Equals instruction
        elif instr == 8:
            compare = self.fetch_arg(arg_refstr, 0) == self.fetch_arg(arg_refstr, 1)
            self.put_value(arg_refstr, 2, int(compare))
            self.pcntr += 4
        # Halt Instruction
        elif instr == 99:
            self.finished = True
            self.pcntr += 1
        else:
            raise ValueError( "Invalid Instruction Passed!" )
    
    def fetch_arg(self, arg_refstr, arg_index):
        if arg_index >= len(arg_refstr):
            arg_mode = 0
        else:
            arg_mode = int(arg_refstr[arg_index])
        
        # Position Mode
        if arg_mode == 0:
            address = self.data_tape[self.pcntr + 1 + arg_index]
            return self.data_tape[address]
        # Immediate Mode
        elif arg_mode == 1:
            return self.data_tape[self.pcntr + 1 + arg_index]
        else:
            raise ValueError("Invalid ArgMode Passed!")
    
    def put_value(self, arg_refstr, arg_index, value):
        if arg_index >= len(arg_refstr):
            arg_mode = 0
        else:
            arg_mode = int(arg_refstr[arg_index])
        
        # Position Mode
        if arg_mode == 0:
            address = self.data_tape[self.pcntr + 1 + arg_index]
            write_index = address
        # Immediate Mode
        elif arg_mode == 1:
            write_index = self.data_tape[self.pcntr + 1 + arg_index]
            raise ValueError("Uh... this isn't really defined!")
        else:
            raise ValueError("Invalid ArgMode Passed!")

        self.data_tape[write_index] = value


input_file = 'adventofcode2019/05_SunnyAsteroids.txt'
# input_file = '02_ProgramAlarm.txt'

if __name__ == '__main__':

    file_obj = open(input_file, 'r')

    input_str = file_obj.readline()

    input_arr = list(map(int, input_str.split(',')))

    print("Part 1 Result")
    processor = IntCodeProcessor(input_arr, [1])
    processor.run_program()

    for x in processor.outputs:
        print(x)
    
    print("Part 2 Result")
    processor = IntCodeProcessor(input_arr, [5])
    processor.run_program()

    for x in processor.outputs:
        print(x)
