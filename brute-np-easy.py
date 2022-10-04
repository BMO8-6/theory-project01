#! /usr/bin/env python3

# Libraries
import itertools

# reads in file and generates the next wff each time called on next()
def ReadWff(path):
    with open(path) as fp:
        wff = []
        for line in fp:
            if line.startswith(('c')) and wff:
                yield wff
                wff = []
            elif not line.startswith(('c', 'p')):
                items = [int(x) for x in line.split(',')]
                wff.append(items[:-1])

# TODO I don't know whether we'll need the meta data for the wffs (num of vars, answer of S/U, etc) so I created this
# pretty equivalent version of generator working with a class. Pick which one is needed.

class CNF:
    def __init__(self, problem_id, max_n_literals, n_vars, n_clauses, std_answer, wff):
        self.problem_id = problem_id
        self.max_n_literals = max_n_literals
        self.n_vars = n_vars
        self.n_clauses = n_clauses
        self.std_answer = std_answer
        self.wff = wff


def ReadCNFObject(path):
    with open(path) as fp:
        wff = []
        for line in fp:
            if line.startswith(('c')):
                if wff:
                    yield CNF(int(problem_id), int(max_n_literals), int(n_vars), int(n_clauses), std_answer, wff)
                    wff = []
                [_, problem_id, max_n_literals, std_answer] = line.split(" ")
            elif line.startswith(('p')):
                [_, _, n_vars, n_clauses] = line.split(" ")
            else:
                items = [int(x) for x in line.split(',')]
                wff.append(items[:-1])


def GenerateInput(wff):
    num_var = wff.n_vars
    start_set = set()

    for i in range(num_var + 1):
        temp_arr = [-1]*(num_var-i) + [1]*(i)
        for x in itertools.permutations(temp_arr):
            start_set.add(x)

    return start_set

def main():
    path = "kSAT.cnf"
    cnf_gen = ReadCNFObject(path)
    for _ in range(10):
        cnf = next(cnf_gen)
        input = GenerateInput(cnf)
        print(input)

    return 0


if __name__ == '__main__':
    main()