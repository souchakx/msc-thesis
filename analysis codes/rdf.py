#!/usr/bin/env python3
"""
Radial Distribution Function (RDF) calculator for a LAMMPS trajectory (.lammpstrj file).

Reads atomic coordinates from a LAMMPS dump, computes pairwise distances,
and accumulates histogram to produce g(r).
"""

import numpy as np
import math
import matplotlib.pyplot as plt

# -----------------------
# Parameters
# -----------------------
n_atoms   = 10000          # Number of atoms in system
box_volume = 70000.0       # Simulation box volume (Å^3) – adjust as per simulation
num_frames = 1             # Number of frames to process
dr         = 0.05          # Bin width (Å)
r_max      = 2.0           # Maximum distance to consider (Å)
dumpfile   = "npt.lammpstrj"    # Input LAMMPS dump file
outfile    = "rdf.dat"     # Output data file

# Derived values
rho = n_atoms / box_volume           # Number density
n_bins = int(r_max / dr)             # Number of histogram bins
r = np.linspace(0.0, r_max, n_bins)  # Bin centers

# Initialize accumulators
g = np.zeros(n_bins)
counts = np.zeros(n_bins)
shell_volumes = np.zeros(n_bins)

# Precompute spherical shell volumes for each bin
for l in range(n_bins):
    shell_volumes[l] = (4.0 / 3.0) * math.pi * (
        (r[l] + dr)**3 - r[l]**3
    )

# -----------------------
# Distance function
# -----------------------
def distance(coords, i, j):
    """Euclidean distance between atoms i and j (no PBC)."""
    dx = coords[i, 1] - coords[j, 1]
    dy = coords[i, 2] - coords[j, 2]
    dz = coords[i, 3] - coords[j, 3]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

# -----------------------
# Main RDF loop
# -----------------------
skip = 0
pair_count = 0

for frame in range(num_frames):
    # Read one frame (LAMMPS dump: skip 9 header lines + previous frames)
    coords = np.loadtxt(dumpfile, skiprows=9+skip, usecols=(0,1,2,3), max_rows=n_atoms)
    skip += n_atoms + 9

    # Loop over all unique atom pairs
    for i in range(n_atoms):
        for j in range(i+1, n_atoms):
            dist = distance(coords, i, j)
            if dist < r_max:
                index = int(dist / dr)
                counts[index] += 2   # each pair counts twice (i–j and j–i)
            pair_count += 1

# -----------------------
# Normalize g(r)
# -----------------------
g = counts / (rho * shell_volumes * n_atoms * num_frames)

# -----------------------
# Save and plot
# -----------------------
np.savetxt(outfile, np.column_stack((r, g)), header="r (Å)   g(r)")

plt.plot(r, g)
plt.xlabel("r (Å)")
plt.ylabel("g(r)")
plt.title("Radial Distribution Function")
plt.grid(True)
plt.savefig("rdf.png", dpi=150)
plt.show()

print(f"RDF computed for {num_frames} frames, written to {outfile}")
