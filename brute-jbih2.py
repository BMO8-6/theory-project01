#!/usr/binenv python3

# Libraries
import time


# class to hold all the necessary metadata from the file input
class CNF:
    def __init__(self, max_literals, num_vars, num_clauses, num_literals, answer, wff, runtime):
        self.max_literals = max_literals
        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.num_literals = num_literals
        self.answer = answer
        self.wff = wff
        self.runtime = runtime


# function that reads file input to the CNF class
def read_input(path):
    with open(path) as fp:
        wff = []

        for line in fp:
            # comment line
            if line.startswith(('c')):
                _, _, max_literals, answer = line.split(" ")

            # problem line
            elif line.startswith(('p')):
                _, _, num_vars, num_clauses = line.split(" ")

            # the clauses
            else:
                items = [int(x) for x in line.split(',')]
                wff.append(items[:-1])

                # if we've read all the clauses, yield
                if len(wff) == int(num_clauses):
                    yield CNF(int(max_literals), int(num_vars), 0, int(num_clauses), answer.strip(), wff, 0)
                    wff = []


# creates a complete set of inputs for each problem
def create_input(cnf):
    # there are 2^n possibilities of input variations
    for i in range(pow(2, cnf.num_vars)):
        bin_str = bin(i)[2:].zfill(cnf.num_vars)
        perm_arr = []

        # the -1 replaces 0 since 2 negatives multiplied by each other is positive (can multiply input and literal as a shortcut method)
        for bit in bin_str:
            if int(bit) == 1:
                perm_arr.append(1)
            else:
                perm_arr.append(-1)

        yield perm_arr


# checks whether the generated input from the function actually works
def verify_input(cnf, input):
    for clause in cnf.wff:
        for literal in clause:
            # no reason to continue checking for loop if one input is postive since the literals are OR'd
            if input[abs(literal) - 1] * literal > 0:
                break

            # if at last literal and didn't pass the if statement above, then clearly the clause is False
            elif literal == clause[-1]:
                return False
    
    # only happens if all the clauses have been checked and passed
    return True


# converts the successful input's -1's to 0's
def input_conversion(input):
    for iter, bit in enumerate(input):
        if bit == -1:
            input[iter] = 0

    return input


# goes through the wff to find how many literals there are
def cnf_literals_counter(cnf):
    count = 0

    for clause in cnf.wff:
        for _ in clause:
            count += 1
    
    return count


# creates output str to print to excel file
def create_output(cnf, iter, sat_cond, corr_answer, corr_input):
    output_str = f"{iter + 1},{cnf.num_vars},{cnf.num_clauses},{cnf.max_literals},{cnf.num_literals},{sat_cond},{corr_answer},{cnf.runtime}"

    # if there's a solution, add it to the end of the str
    if corr_input:
        output_str = output_str + "," + ",".join(list(map(str, corr_input)))

    return output_str


def main():
    filename = "test"
    cnf_gen = read_input(filename + ".cnf")
    num_decimals = 1

    # iter handles which problem number is being calculated
    for iter, cnf in enumerate(cnf_gen):
        sat_cond = 'U'
        corr_answer = 0
        corr_input = []
        input_gen = create_input(cnf)

        # doesn't check any more inputs than necessary (just need 1 success for sat)
        start_time = time.time()
        for input in input_gen:

            if verify_input(cnf, input):
                corr_input = input
                sat_cond = 'S'
                break
        
        # calculates the time taken for each operation
        done_time = time.time()
        cnf.runtime = round((done_time - start_time) * pow(10, 6), num_decimals)

        # finds the number of literals in each wff
        cnf.num_literals = cnf_literals_counter(cnf)

        # if the problem specified an answer, check whether it matches what we got (returns -1 if not, 0 if no specification, and 1 if match)
        if cnf.answer:
            corr_answer = 1 if cnf.answer == sat_cond else -1
        
        print(create_output(cnf, iter, sat_cond, corr_answer, input_conversion(corr_input)))


if __name__ == '__main__':
    main()