# -------------------------------------------------------------
# SASA Calculation Script (for VMD)
#
# This script computes the Solvent Accessible Surface Area (SASA)
# for all atoms in a trajectory loaded into VMD.
#
# Usage:
#   1. Load your trajectory (PDB, PSF + DCD, etc.) into VMD.
#   2. Run this script inside the VMD Tk Console:
#        source sasa.tcl
#   3. The script will prompt you for a "selection mode"
#      (e.g., "protein", "backbone", "resid 1", "all").
#   4. The SASA is computed for each frame of the trajectory.
#   5. Results are written to a file named:
#         SASA_<selection>.dat
#
# Note:
#   - Probe radius is set to 0.2 Å (fine-grained SASA surface).
#   - Atom radii are initialized to 1.0 Å (can be adjusted).
#   - Output is one SASA value per frame (in Å^2).
# -------------------------------------------------------------

# Prompt user for selection string
puts -nonewline "\n  Selection: "
gets stdin selmode

# Select all atoms as initial group
set atom [atomselect top all]

# Set atomic radius (required for SASA calculation)
$atom set radius 1.0

# Get number of frames in the trajectory
set n [molinfo top get numframes]

# Open output file (named according to selection mode)
set output [open "SASA_$selmode.dat" w]

# Loop over trajectory frames
for {set i 0} {$i < $n} {incr i} {
    # Set trajectory to frame i
    molinfo top set frame $i

    # Compute SASA for current frame
    # Arguments:
    #   0.2 = probe radius (Å)
    #   $atom = atom selection to measure
    set sasa [measure sasa 0.2 $atom]

    # Print progress to console
    puts "    progress: $i/$n"

    # Write SASA value to file
    puts $output "$sasa"
}

# Final message and cleanup
puts "    progress: $n/$n"
puts "Output file: SASA_$selmode.dat"
close $output
