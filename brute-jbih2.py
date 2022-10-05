#!/usr/binenv python3

# Libraries

# Class to hold all the metadata from the file input
class CNF:
    def __init__(self, max_n_literals, n_vars, n_clauses, std_answer, wff):
        self.max_n_literals = max_n_literals
        self.n_vars = n_vars
        self.n_clauses = n_clauses
        self.std_answer = std_answer
        self.wff = wff


# function that reads file input to the CNF class
def ReadCNFObject(path):
    with open(path) as fp:
        wff = []
        for line in fp:
            if line.startswith(('c')):
                _, _, max_n_literals, std_answer = line.split(" ")
            elif line.startswith(('p')):
                _, _, n_vars, n_clauses = line.split(" ")
            else:
                items = [int(x) for x in line.split(',')]
                wff.append(items[:-1])

                if len(wff) == int(n_clauses):
                    yield CNF(int(max_n_literals), int(n_vars), int(n_clauses), std_answer.strip(), wff)
                    wff = []

# creates the input for each CNF problem
def GenerateInput(cnf):
    for i in range(2 ** cnf.n_vars):
        bin_str = bin(i)[2:].zfill(cnf.n_vars)
        comb = []
        for n in bin_str:
            comb.append(1) if int(n)==1 else comb.append(-1)
        yield comb

# checks whether the generated input from the function actually works
def verify_input(cnf, input):
    for clause in cnf.wff:
        for literal in clause:
            if input[abs(literal) - 1] * literal > 0:
                break
            elif literal == clause[-1]:
                return False
    
    return True

def main():
    filename = "test"
    cnf_gen = ReadCNFObject(filename + ".cnf")

    # iter handles which problem number is being calculated
    for iter, cnf in enumerate(cnf_gen):
        sat_flag = False
        print(f"{iter + 1}. Generating input with {cnf.n_vars} vars with answer {cnf.std_answer}")
        input_gen = GenerateInput(cnf)

        for input in input_gen:
            if verify_input(cnf, input):
                sat_flag = True
                break
        

if __name__ == '__main__':
    main()