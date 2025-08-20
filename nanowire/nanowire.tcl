# -------------------------------------------------------------
# VMD/TopoTools script for converting XYZ → LAMMPS data file
#
# Input  : nano.xyz (generated from Python script)
# Output: data.nano (LAMMPS data file, atom_style = angle)
#
# Workflow is based on Axel Kohlmeyer’s TopoTools tutorial:
# https://sites.google.com/site/akohlmey/software/topotools/tutorial-part-1
# Steps:
#   1. Load the XYZ structure
#   2. Assign atom types and masses
#   3. Recalculate bonds and infer angles
#   4. Define a periodic simulation box
#   5. Export to LAMMPS data format
# -------------------------------------------------------------

# Load required plugins
package require topotools
package require pbctools

# ----------------------
# 1. Load XYZ file
# ----------------------
# "autobonds no" → do not guess bonds automatically
# "waitfor all"  → ensures full file is loaded before continuing
mol new nano.xyz autobonds no waitfor all

# ----------------------
# 2. Select all atoms and assign properties
# ----------------------
set sel [atomselect top all]
$sel set type A      ;# Atom type (can be changed if multiple types are needed)
$sel set mass 20.0   ;# Mass of each coarse-grained bead (in atomic mass units)

# ----------------------
# 3. Guess topology
# ----------------------
mol bondsrecalc top   ;# Recalculate bonds using distance criteria
topo retypebonds      ;# Assign bond types based on atom types
topo guessangles      ;# Infer angles automatically from bonded triples

# ----------------------------------
# 4. Define periodic simulation box
# ----------------------------------
# Syntax: pbc set {lx ly lz alpha beta gamma}
# Example: cubic box of 100 Å per side
pbc set {100.0 100.0 100.0 90.0 90.0 90.0}

# ------------------------------
# 5. Export to LAMMPS data file
# ------------------------------
# "angle" = output format for atom_style angle (atoms, bonds, angles included)
topo writelammpsdata data.nano angle

# End of script
puts "LAMMPS data file 'data.nano' written successfully."
