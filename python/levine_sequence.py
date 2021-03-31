import argparse


def next_levine(row):
    counter = 1
    new_row = list()

    for index in range(len(row) - 1, -1, -1):
        for _ in range(row[index]):
            new_row.append(counter)
        counter += 1
    return new_row

def levine_sequence(max_iter):

    row = [2]
    rows = [[2]]
    vals = [2]

    for iteration in range(max_iter-1):
        new_row = next_levine(row)
        vals.append(sum(new_row))
        rows.append(new_row)
        row = new_row
    return rows, vals

def main():
    parser = argparse.ArgumentParser(description="description of what program does")
    parser.add_argument("max_iters", help="maximum number of iterations wanted for the Levine Sequence", type=int)
    parser.add_argument("-i", "--ignore", help="ignore warning message", action="store_true")
    args = parser.parse_args()
    if args.max_iters <= 10 or args.ignore:
        max_iters = args.max_iters
    else:
        print("WARNING: The Levine Sequence past 10 is memory intensive. Use the --ignore flag to sotp viewing this message.")
        return


    ls_rows, ls_vals = levine_sequence(max_iters)
    for row, val in zip(ls_rows, ls_vals):
        print("{:4} : {}".format(val, row))

if __name__ == "__main__":
    main()
