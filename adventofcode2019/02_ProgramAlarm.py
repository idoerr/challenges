from typing import Dict, List

def process_alarm(data_tape: List[int]):

    for pcntr in range(0, len(data_tape), 4):
        instr = data_tape[pcntr]
        read_1 = data_tape[pcntr+1]
        read_2 = data_tape[pcntr+2]
        dest_ind = data_tape[pcntr+3]

        if instr == 1:
            data_tape[dest_ind] = data_tape[read_1] + data_tape[read_2]
        elif instr == 2:
            data_tape[dest_ind] = data_tape[read_1] * data_tape[read_2]
        elif instr == 99:
            break
        else:
            raise ValueError( "Invalid Instruction Passed!" )


input_file = 'adventofcode2019/02_ProgramAlarm.txt'

if __name__ == '__main__':

    file_obj = open(input_file, 'r')

    input_str = file_obj.readline()

    input_arr = list(map(int, input_str.split(',')))

    input_arr[1] = 82
    input_arr[2] = 50

    process_alarm(input_arr)

    print(input_arr[0])
    print(int(True))
    print(int(False))