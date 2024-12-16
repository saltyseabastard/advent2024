import numpy as np

def load_and_compute():
    # Load the file
    data = np.loadtxt('data/day1.txt')  # Replace 'your_file.txt' with your actual file name

    # Split into two arrays
    column1 = data[:, 0]
    column2 = data[:, 1]

    column1.sort()
    column2.sort()

    #print("Column 1:", column1)
    #print("Column 2:", column2)

    distances = []

    for a, b in zip(column1, column2):
        distances.append(abs(a-b))

    print("Total distance " + str(sum(distances)))

    similarities = []

    for a in column1:
        similarity = 0
        for b in column2:
            if a == b:
                similarity += 1
        similarities.append(similarity * a)

    print(f"Total similarities {sum(similarities)}")
