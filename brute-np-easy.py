#!/usr/bin/env python3

import pprint

# reads in file and returns a 2d list
def open_cnf_file(path):
    a = []

    with open(path) as fp:
        for line in fp:
            # doesn't account for comments or listing or problems
            if not line.startswith(('c', 'p')):
                items = [int(x) for x in line.split(',')]
                a.append(items[:-1])
            elif line.startswith(('p')):
                items = [x for x in line.split()]
                a.append(items[:-1])
    
    return a
                

def main():
    path = "kSAT.cnf"
    cnf_list = open_cnf_file(path)
    for line in cnf_list:
        print(line)
        
    return 0

if __name__ == '__main__':
    main()