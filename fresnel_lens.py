import ezdxf as ez


# Given specifications
f = 40  # Focal Length in mm
D = 25.4  # Diameter in mm
n = 6  # Number of Rings
n_ref = 1.53  # Refractive Index

# Calculate the radius of curvature R
R = f * (n_ref - 1)

# Divide the lens diameter into n rings
radii = [D * (i / n) for i in range(1, n + 1)]

# Calculate the height y for each ring boundary using the lens profile equation
heights = [(r**2) / (2 * R) for r in radii]


