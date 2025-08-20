#!/usr/bin/env python3
"""
Generate a simple nanostructure as an XYZ file.

- Creates a 3D grid of nanowires made of coarse-grained atoms.
- The system size is defined by the number of atoms along x, y, z.
- The lattice spacings along each direction are user-defined.
- Output is written in XYZ format for visualization in VMD, Ovito, etc.

Author: Souvick Chakraborty
"""

import numpy as np

# ----------------------
# Lattice parameters
# ----------------------
xs = 3.0   # spacing along x-axis (Å)
ys = 3.0   # spacing along y-axis (Å)
zs = 1.0   # spacing along z-axis (Å)

a = 100    # number of atoms along x-axis
b = 10     # number of atoms along y-axis
c = 10     # number of atoms along z-axis

# ----------------------
# Total atoms
# ----------------------
n_atoms = a * b * c

# ----------------------
# Write XYZ file
# ----------------------
with open("nano.xyz", "w") as f:
    # XYZ file header
    f.write(f"{n_atoms}\n")
    f.write("Carbon nanostructure\n")

    # Generate atomic coordinates
    for i in range(a):
        x = i * xs
        for j in range(b):
            y = j * ys
            for k in range(c):
                z = k * zs
                f.write(f"C\t{x:.3f}\t{y:.3f}\t{z:.3f}\n")

print(f"XYZ file 'nano.xyz' written with {n_atoms} atoms")
