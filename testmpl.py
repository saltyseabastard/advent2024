import matplotlib.pyplot as plt
import numpy as np
import time

# Convert grid to a numeric representation
def grid_to_numeric(grid):
    mapping = {'.': 0, '#': 1, '^': 2}
    try:
        numeric_grid = np.array([[mapping.get(c, -1) for c in row] for row in grid])
        return numeric_grid
    except Exception as e:
        print(f"Error in grid_to_numeric: {e}")
        return None

# Example grid initialization
data_by_line = [
    ['#', '.', '.', '.', '#', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '#', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '#', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '#', '.', '.', '^', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
    ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '#', '.', '.', '.']
]

# Initialize Matplotlib
fig, ax = plt.subplots()

# Update function
def update_grid(data_by_line, frame_idx):
    print(f"Frame {frame_idx}: Updating grid...")
    numeric_grid = grid_to_numeric(data_by_line)
    if numeric_grid is None:
        print("Failed to convert grid to numeric. Skipping this frame.")
        return
    print(f"Numeric grid for frame {frame_idx}:\n{numeric_grid}")
    ax.clear()  # Clear the axis
    ax.matshow(numeric_grid, cmap="coolwarm", vmin=0, vmax=2)
    ax.set_xticks([])  # Hide x-axis ticks
    ax.set_yticks([])  # Hide y-axis ticks
    plt.draw()
    plt.pause(0.5)

# Initial Display
update_grid(data_by_line, 0)

# Simulate Updates
for frame_idx in range(1, 6):
    try:
        # Debugging: Print the current state of the grid
        print(f"Before update for frame {frame_idx}:")
        for row in data_by_line:
            print("".join(row))

        # Move the guard for demonstration
        data_by_line[6][4] = '.'
        if frame_idx % 2 == 0:
            data_by_line[5][4] = '^'
        else:
            data_by_line[6][5] = '^'

        update_grid(data_by_line, frame_idx)

        print(f"After update for frame {frame_idx}:")
        for row in data_by_line:
            print("".join(row))

    except Exception as e:
        print(f"Error in frame {frame_idx}: {e}")
        break
