import numpy as np
from PIL import Image
import argparse
import random

# Image dimensions
width, height = 2000, 1200

# Set up argument parser to take the filename as input
parser = argparse.ArgumentParser(description='Generate a random procedurally generated image.')
parser.add_argument('filename', type=str, help='The name of the output file (e.g., output.png)')
args = parser.parse_args()

# Create a new blank image
image = Image.new("RGB", (width, height))

# Define possible mathematical functions
def sin(x):
    return np.sin(x)

def cos(x):
    return np.cos(x)

def tan(x):
    return np.tan(x)

def exp(x):
    return np.exp(-abs(x))  # To avoid overflow issues

def log(x):
    return np.log(abs(x) + 1)  # To avoid log(0)

def sqrt(x):
    return np.sqrt(abs(x))  # Only works on positive values

def sinh(x):
    return np.sinh(x)

def cosh(x):
    return np.cosh(x)

def arcsin(x):
    return np.arcsin(np.clip(x, -1, 1))  # Clip values to the valid domain of arcsin

def arctan(x):
    return np.arctan(x)

# List of available mathematical functions
functions = [sin, cos, tan, exp, log, sqrt, sinh, cosh, arcsin, arctan]

# Random seed for reproducibility (optional)
seed = random.randint(0, 1000000)
np.random.seed(seed)
print(f"Random Seed: {seed}")

# Function to generate a random mathematical expression
def random_function():
    # Choose random functions from the list
    f1 = random.choice(functions)
    f2 = random.choice(functions)
    f3 = random.choice(functions)
    
    # Generate random constants for the function
    a = np.random.uniform(1, 10)
    b = np.random.uniform(1, 10)
    c = np.random.uniform(1, 10)
    d = np.random.uniform(1, 10)
    e = np.random.uniform(1, 10)
    
    # Create a nested mathematical expression
    def expression(x, y):
        nx = x / width - 0.5  # Normalize x to the range [-0.5, 0.5]
        ny = y / height - 0.5  # Normalize y to the range [-0.5, 0.5]
        
        # Apply polynomial terms and combine with trigonometric/hyperbolic functions
        result = (f1(a * nx + b * ny) + f2(c * nx * ny) + f3(d * nx + e * ny)) ** 2 + (a * nx ** 2 + b * ny ** 3)
        return result
    
    return expression

# Randomize color channels using different expressions
red_func = random_function()
green_func = random_function()
blue_func = random_function()

# Function to compute color for each pixel using randomized functions
def compute_color(x, y):
    # Scale the functions' output to be between 0 and 255
    r = int(255 * (red_func(x, y) % 1))
    g = int(255 * (green_func(x, y) % 1))
    b = int(255 * (blue_func(x, y) % 1))
    
    # Clamp values to [0, 255]
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    return r, g, b

# Generate pixel values
for x in range(width):
    for y in range(height):
        color = compute_color(x, y)
        image.putpixel((x, y), color)

# Save the generated image with the specified filename
image.save(args.filename)
print(f"Image generated and saved as '{args.filename}'.")
