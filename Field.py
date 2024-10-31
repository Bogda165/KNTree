import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.spatial import KDTree

# Define initial points for each class
points = {
    "R": [(-4500, -4400), (-4100, -3000), (-1800, -2400), (-2500, -3400), (-2000, -1400)],
    "G": [(4500, -4400), (4100, -3000), (1800, -2400), (2500, -3400), (2000, -1400)],
    "B": [(-4500, 4400), (-4100, 3000), (-1800, 2400), (-2500, 3400), (-2000, 1400)],
    "P": [(4500, 4400), (4100, 3000), (1800, 2400), (2500, 3400), (2000, 1400)]
}

# Initialize points and class labels for KDTree setup
all_points = []
all_labels = []

for label, coords in points.items():
    all_points.extend(coords)
    all_labels.extend([label] * len(coords))

# Build the initial KDTree
tree = KDTree(all_points)

# Define colors for visualization
colors = {'R': 'red', 'G': 'green', 'B': 'blue', 'P': 'purple'}


def classify(X, Y, k):
    # Find the k nearest neighbors
    distances, indices = tree.query((X, Y), k)

    # Ensure indices is a list (even if k=1 returns a single integer)
    if k == 1:
        indices = [indices]  # Wrap in a list if it's a single value

    # Retrieve their labels and find the most common label among them
    nearest_labels = [all_labels[i] for i in indices]
    most_common = Counter(nearest_labels).most_common(1)
    return most_common[0][0]

# Function to generate new points based on probabilities
def generate_point(label):
    if label == "R":
        x = random.randint(-5000, 500) if random.random() < 0.99 else random.randint(-5000, 5000)
        y = random.randint(-5000, 500) if random.random() < 0.99 else random.randint(-5000, 5000)
    elif label == "G":
        x = random.randint(-500, 5000) if random.random() < 0.99 else random.randint(-5000, 5000)
        y = random.randint(-5000, 500) if random.random() < 0.99 else random.randint(-5000, 5000)
    elif label == "B":
        x = random.randint(-5000, 500) if random.random() < 0.99 else random.randint(-5000, 5000)
        y = random.randint(-500, 5000) if random.random() < 0.99 else random.randint(-5000, 5000)
    elif label == "P":
        x = random.randint(-500, 5000) if random.random() < 0.99 else random.randint(-5000, 5000)
        y = random.randint(-500, 5000) if random.random() < 0.99 else random.randint(-5000, 5000)
    return (x, y)

# Experiment with different values of k
k_values = [1, 3, 7, 15]

for k in k_values:
    correct = 0
    new_points = []
    new_labels = []

    for _ in range(10000):
        for label in ["R", "G", "B", "P"]:
            x, y = generate_point(label)
            classified_label = classify(x, y, k)
            if classified_label == label:
                correct += 1
            new_points.append((x, y))
            new_labels.append(classified_label)

    # Update KDTree with new points and labels for next classifications
    all_points.extend(new_points)
    all_labels.extend(new_labels)
    tree = KDTree(all_points)  # Rebuild KDTree with updated points

    # Calculate and print accuracy
    accuracy = correct / 40000
    print(f'Accuracy for k={k}: {accuracy:.2%}')

    # Visualization for each k value
    x_coords = [p[0] for p in all_points]
    y_coords = [p[1] for p in all_points]
    label_colors = [colors[l] for l in all_labels]

    plt.figure(figsize=(10, 10))
    plt.scatter(x_coords, y_coords, c=label_colors, s=10, alpha=0.6)
    plt.title(f'2D Classification Result for k={k}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()