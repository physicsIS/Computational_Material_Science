from ase.build import fcc111, add_adsorbate
from ase.visualize import view

# Create an Al(111) surface with a 2x2x2 supercell
slab = fcc111('Al', size=(2, 2, 2), vacuum=10.0)

# Add an oxygen atom on top of an aluminum atom
add_adsorbate(slab, 'O', height=1.5, position='ontop')

# Add another oxygen atom in an fcc hollow site
add_adsorbate(slab, 'O', height=1.5, position='fcc')

# Visualize the structure
view(slab)

