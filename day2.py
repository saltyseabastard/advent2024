import numpy as np

def load_and_compute():
    # Create a multidimensional array from the file
    reports = []

    with open('data/day2.txt', 'r') as file:  # Replace with your file name
        for line in file:
            # Split the line into integers and append to the outer list
            reports.append([int(num) for num in line.split()])

    safe = 0
    for report in reports:
        print(report)

        if get_is_sequential_with_gap(report, 3) == -1:
            safe += 1
            print("safe")
        else:
            print("unsafe")
            # try to remove one of the elements
            for i in range(len(report)):
                # Create a new copy of the list without the element at index i
                new_report = report[:i] + report[i + 1:]

                # Test if the modified list is sequential
                if get_is_sequential_with_gap(new_report, 3) == -1:
                    safe += 1
                    print("safe")
                    break

    print(f"Total safe: {safe}")



def get_is_sequential_with_gap(arr, max_gap=3):

    # Determine the difference between the first two elements, 2 - 1 = 1, 1 - 2 = -1
    diff = arr[1] - arr[0]

    ascending = diff > 0

    for i in range(1, len(arr)):
        diff = arr[i] - arr[i - 1]

        if diff == 0:
            return i

        if abs(diff) > max_gap:  # Check if the gap exceeds the max allowed
            #print("Gap too large")
            return i

        if ascending and diff < 0:
            return i
        elif not ascending and diff > 0:
            return i

    return -1