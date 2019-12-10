import itertools
from typing import Dict, List

class IntCodeProcessor:

    def __init__(self, data_tape, inputs=[]):
        self.data_tape = data_tape.copy()
        self.pcntr = 0
        self.finished = False
        self.inputs = inputs
        self.outputs = []

    def run_program(self):
        while not self.finished and self.pcntr < len(self.data_tape):
            continue_running = self.process_instruction()

            if continue_running is not None and not continue_running:
                return False
        
        return True
    
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
            if len(self.inputs) == 0:
                return False
            
            value = self.inputs.pop(0)
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



def create_amplifiers(instr_arr, amplifier_settings):

    amp_list = []

    is_first_iter = True
    for x in amplifier_settings:
        input_arr = [x]
        if is_first_iter:
            input_arr.append(0)
        
        amp_list.append(IntCodeProcessor(instr_arr, input_arr))

        is_first_iter = False
    
    for i in range(len(amp_list)):
        first_amp = amp_list[i]
        second_index = (i + 1) % len(amp_list)
        second_amp = amp_list[second_index]

        first_amp.outputs = second_amp.inputs
    
    return amp_list

    


input_file = 'adventofcode2019/07_Amplifier.txt'
# input_file = '02_ProgramAlarm.txt'

if __name__ == '__main__':

    file_obj = open(input_file, 'r')

    input_str = file_obj.readline()

    instr_arr = list(map(int, input_str.split(',')))

    print("Part 1 Result")

    def amplifier_run(amplifier_settings):

        amp_list = create_amplifiers(instr_arr, amplifier_settings)
        program_finished = False

        while not program_finished:
            for amp in amp_list:
                run_status = amp.run_program()
                program_finished |= run_status
        
        return amp_list[0].inputs[0]

    max_run = max(itertools.permutations(range(5)), key=amplifier_run)
    print(max_run, amplifier_run(max_run))
    
    print()
    print("Part 2 Result")

    max_run = max(itertools.permutations(range(5,10)), key=amplifier_run)
    print(max_run, amplifier_run(max_run))


