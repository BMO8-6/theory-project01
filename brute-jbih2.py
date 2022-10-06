#!/usr/binenv python3


# Libraries
import time
import xlwt


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
                _, _, max_literals, answer = line.strip().split(' ')

            # problem line
            elif line.startswith(('p')):
                _, _, num_vars, num_clauses = line.strip().split(' ')

            # the clauses
            else:
                items = [int(x) for x in line.strip().split(',')]
                wff.append(items[:-1])

                # if we've read all the clauses, yield and reset the wff array
                if len(wff) == int(num_clauses):
                    yield CNF(int(max_literals), int(num_vars), 0, int(num_clauses), answer, wff, 0)
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
        for iter, literal in enumerate(clause):
            # no reason to continue checking for loop if one input is postive since the literals are OR'd
            if input[abs(literal) - 1] * literal > 0:
                break

            # if at last literal and didn't pass the if statement above, then clearly the clause is False
            elif iter == len(clause) - 1:
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


# creates output str to print to csv file
def create_output_str(cnf, iter, sat_cond, corr_answer, corr_input):
    output_str = f"{iter + 1},{cnf.num_vars},{cnf.num_clauses},{cnf.max_literals},{cnf.num_literals},{sat_cond},{corr_answer},{cnf.runtime}"

    # if there's a solution arr, add it to the end of the str
    if corr_input:
        output_str = output_str + "," + ",".join(list(map(str, corr_input)))

    return output_str


# just creates output str for the last line in the csv
def create_last_str(filename, iter, num_sat, num_unsat, num_ans_provided, num_corr_ans):
    output_str = f"{filename},jbih2,{iter + 1},{num_sat},{num_unsat},{num_ans_provided},{num_corr_ans}"

    return output_str


def main():
    # intialization of variables 
    num_time_decimal_round, num_var_skip = 1, 18
    num_sat = num_unsat = num_ans_provided = num_corr_ans = csv_row = 0    

    # user input for filename and whether to skip certain wff's
    filename = input('Please enter the filename without the .cnf: ')   
    skip_flag = True if input(f"Would you like to skip any WFFs with over {num_var_skip} variables (Y/N): ").lower() == 'y' else False

    # initialize csv file
    output_wb = xlwt.Workbook()
    cnf_solutions_sheet = output_wb.add_sheet("Sheet 1")

    # generate the first cnf
    cnf_gen = read_input(filename + ".cnf")

    # iter handles which problem number is being calculated
    for iter, cnf in enumerate(cnf_gen):
        # initialize
        sat_cond = 'U'
        corr_answer = 0
        corr_input = []

        # if the option to skip variables was selected, then skip over wff's with over a certain number of variables
        if skip_flag and cnf.num_vars > num_var_skip:
            print(f"{iter + 1}) Skipped - over {num_var_skip} variables...")
            continue
        
        print(f"{iter + 1}) Generating solution...")

        # generate first input arr to not check any more inputs than necessary (just need 1 success for satisfiability)
        input_gen = create_input(cnf)
        
        # starts timer
        start_time = time.time()
        
        for arr in input_gen:
            # condition for if a solution input has been verified
            if verify_input(cnf, arr):
                corr_input = arr
                sat_cond = 'S'
                num_sat += 1
                print("   S - The WFF is satisfiable.")
                break
        
        # calculates the time taken for each operation
        done_time = time.time()
        cnf.runtime = round((done_time - start_time) * pow(10, 6), num_time_decimal_round)

        # finds the number of literals in each wff
        cnf.num_literals = cnf_literals_counter(cnf)

        # if the problem specified an answer, check whether it matches what we got (returns -1 if not, 0 if no specification, and 1 if match)
        if cnf.answer != '?':
            num_ans_provided += 1

            # checks if what we got matches the comment
            if cnf.answer == sat_cond:
                corr_answer = 1  
                num_corr_ans += 1

            # if we didn't match
            else:   
                corr_answer = -1
        
        # increment if unsatisfiable
        if sat_cond == 'U':
            print("   U - The WFF is unsatisfiable.")
            num_unsat += 1

        # write wff info to the csv file
        cnf_solutions_sheet.write(csv_row, 0, create_output_str(cnf, iter, sat_cond, corr_answer, input_conversion(corr_input)))
        csv_row += 1

    # write last line of csv file and save
    cnf_solutions_sheet.write(csv_row, 0, create_last_str(filename, iter, num_sat, num_unsat, num_ans_provided, num_corr_ans))
    output_wb.save(f"{filename}_cnf_solutions.xls")
    print("\n***CSV file generated***\n")


if __name__ == '__main__':
    main()