# Calculates the van eck sequence, and plots it
import matplotlib.pyplot as plt

# Get the index of an item starting from the back
def indexReverse(aList, item):
    aList.reverse()
    result = aList.index(item)
    aList.reverse()
    return result

# Append the next item to our list
def next(seq):
    # Pop the element
    x = seq.pop()
    # Check if previously seen
    if x in seq:
        ind = indexReverse(seq, x) + 1
    else:
        ind = 0
    seq.append(x)
    seq.append(ind)

# Run the calculation several iterations and plot
def main():
    seq = [0, 0]
    iters = 10000
    for _ in range(iters):
        next(seq)
    print(seq)
    print("Iterations:", iters)
    print("Max:", max(seq))

    plt.plot(range(len(seq)), seq)
    plt.show()

main()
