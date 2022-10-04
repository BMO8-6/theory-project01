#! /usr/bin/env python3

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
                

def main():
    path = "kSAT.cnf"
    wff_gen = ReadWff(path)
    for _ in range(10):
        wff = next(wff_gen)
        print(wff)

    return 0


if __name__ == '__main__':
    main()