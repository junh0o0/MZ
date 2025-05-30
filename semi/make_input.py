import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.build import molecule,surface,sort,make_supercell
from scipy.spatial.distance import cdist


num_o2 = 25
min_dist = 3.0 
z_range = (10, 15)


slab = read("cl_si.data",format='lammps-data')
cell = slab.get_cell()
added_positions = []

def rotation_matrix_z(angle):
    return np.array([[np.cos(angle), -np.sin(angle), 0],
                     [np.sin(angle),  np.cos(angle), 0],
                     [0,              0,             1]])

def random_rotation_matrix():
    rand = np.random.rand(3)
    theta, phi, z = 2*np.pi*rand[0], 2*np.pi*rand[1], rand[2]
    r = np.sqrt(z)
    V = np.array([r*np.cos(phi), r*np.sin(phi), np.sqrt(1-z)])
    H = np.eye(3) - 2*np.outer(V, V)
    R = np.dot(H, rotation_matrix_z(theta))
    return R


def is_far_enough(new_pos, existing, min_dist):
    if len(existing) == 0:
        return True
    dists = np.linalg.norm(existing - new_pos, axis=1)
    return np.all(dists > min_dist)



def add_random_o2s(slab, n_o2=10, z_min=10, z_max=20):
    cell = slab.get_cell()
    new_atoms = slab.copy()
    for _ in range(n_o2):
        o2 = molecule('O2')
        o2.positions -= o2.get_center_of_mass()
        R = random_rotation_matrix()
        o2.positions = np.dot(o2.positions, R.T)

        x = np.random.uniform(0, cell[0, 0])
        y = np.random.uniform(0, cell[1, 1])
        z = np.random.uniform(z_min, z_max)
        o2.positions += np.array([x, y, z])

        new_atoms += o2
    return new_atoms


for _ in range(num_o2):
    for attempt in range(100):
        x = np.random.uniform(0, cell[0, 0])
        y = np.random.uniform(0, cell[1, 1])
        z = np.random.uniform(*z_range)
        com = np.array([x, y, z])
        if is_far_enough(com, np.array(added_positions), min_dist):
            o2 = molecule("O2")
            o2.positions -= o2.get_center_of_mass()
            R = random_rotation_matrix()
            o2.positions = np.dot(o2.positions,R.T)
            o2.positions += com
            
            slab += o2
            added_positions.append(com)
            break
    else:
        print('1')