#!/usr/binenv python3

# Libraries

# class to hold all the necessary metadata from the file input
class CNF:
    def __init__(self, max_literals, num_vars, num_clauses, answer, wff):
        self.max_literals = max_literals
        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.answer = answer
        self.wff = wff


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
                    yield CNF(int(max_literals), int(num_vars), int(num_clauses), answer.strip(), wff)
                    wff = []


# creates a complete set of inputs for each problem
def create_input(cnf):
    for i in range(pow(2, cnf.num_vars)):
        bin_str = bin(i)[2:].zfill(cnf.num_vars)
        permutations = []

        # the -1 replaces 0 since 2 negatives multiplied by each other is positive (can multiply input and literal as a shortcut method)
        for bit in bin_str:
            permutations.append(1) if int(bit) == 1 else permutations.append(-1)

        yield permutations


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


def main():
    filename = "test"
    cnf_gen = read_input(filename + ".cnf")

    # iter handles which problem number is being calculated
    for iter, cnf in enumerate(cnf_gen):
        sat_flag = False
        print(f"{iter + 1}. Generating input with {cnf.num_vars} vars with answer {cnf.answer}")
        input_gen = create_input(cnf)

        # doesn't check any more inputs than necessary (just need 1 success for satisfiability)
        for input in input_gen:
            if verify_input(cnf, input):
                sat_flag = True
                break
        

if __name__ == '__main__':
    main()