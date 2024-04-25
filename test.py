import math

def get_distance_from_center(arr):
    distances = []
    rows = len(arr)
    cols = len(arr[0])
    center_x = cols / 2
    center_y = rows / 2
    
    for i in range(rows):
        for j in range(cols):
            x = j - center_x
            y = center_y - i  # Reversed due to the orientation of arrays vs Cartesian coordinates
            distance = math.sqrt(x**2 + y**2) * 0.2  # Multiplying by 0.2 to convert grid units to cm
            distances.append(distance)
    
    return distances

# Example usage
array = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

distances = get_distance_from_center(array)
for i, row in enumerate(array):
    for j, value in enumerate(row):
        print(f"Distance from center to voxel at ({i}, {j}): {distances[i * len(row) + j]} cm")

