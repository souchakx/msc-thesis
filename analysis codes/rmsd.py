#!/usr/bin/env python3
"""
RMSD (Root Mean Square Deviation) calculation for a LAMMPS trajectory (.lammpstrj or .dump).

- Uses the `rmsd` Python package for centroid alignment and quaternion-based RMSD.
- Reference = the first frame of the trajectory.
- Outputs a text file (RMSD_vs_time.dat) with frame vs RMSD,
  and a plot (rmsd_plot.png).

Author: [Your Name]
"""

import numpy as np
import matplotlib.pyplot as plt
import rmsd   # pip install rmsd

# ----------------------
# User parameters
# ----------------------
filename = "npt.lammpstrj"   # Input trajectory file
output_data = "RMSD_vs_time.dat"  # Output RMSD data file
output_plot = "rmsd_plot.png"     # Output RMSD plot

# ----------------------
# Detect number of atoms and frames
# ----------------------
with open(filename, "r") as f:
    lines = f.readlines()

# In LAMMPS trajectory:
# line 0   = "ITEM: TIMESTEP"
# line 1   = timestep value
# line 2   = "ITEM: NUMBER OF ATOMS"
# line 3   = number of atoms  <-- we need this
n_atoms = int(lines[3].strip())

# Each frame = 9 header lines + atom coordinate lines
frame_size = n_atoms + 9
total_lines = len(lines)
n_frames = total_lines // frame_size

print(f"Atoms per frame: {n_atoms}")
print(f"Frames detected: {n_frames}")

# ----------------------
# Read reference frame (first frame)
# ----------------------
ref = np.loadtxt(filename, skiprows=9, usecols=(1,2,3), max_rows=n_atoms)
ref -= rmsd.centroid(ref)   # Center coordinates

# ----------------------
# Compute RMSD for each frame
# ----------------------
rmsd_values = []
frames = []

skip = 0
for frame in range(n_frames):
    coords = np.loadtxt(filename, skiprows=9+skip, usecols=(1,2,3), max_rows=n_atoms)
    skip += frame_size

    coords -= rmsd.centroid(coords)  # Center

    rmsd_val = rmsd.quaternion_rmsd(ref, coords)
    rmsd_values.append(rmsd_val)
    frames.append(frame)  # Frame index (can replace with timestep if desired)

# ----------------------
# Save RMSD data
# ----------------------
np.savetxt(output_data,
           np.column_stack((frames, rmsd_values)),
           header="frame   RMSD(Å)", fmt="%f")

# ----------------------
# Plot RMSD vs Frame
# ----------------------
plt.plot(frames, rmsd_values, "-o", markersize=3)
plt.xlabel("Frame index")
plt.ylabel("RMSD (Å)")
plt.title("RMSD vs Simulation Time")
plt.grid(True)
plt.tight_layout()
plt.savefig(output_plot, dpi=150)
plt.show()

print(f"RMSD analysis complete.\nData saved to: {output_data}\nPlot saved to: {output_plot}")
