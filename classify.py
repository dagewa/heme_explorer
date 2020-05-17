#!/usr/bin/env ccp4-python
from __future__ import print_function
import gemmi
from glob import glob
import sys
import os

def distance_between_two_atoms(structure, atom1, atom2):

    try:
        model = structure[0]
    except IndexError:
        raise ValueError("Can't find atoms")
    chain = model[0]
    residue = chain[0]

    a1 = residue.find_atom(atom1, "*")
    a2 = residue.find_atom(atom2, "*")

    if a1 is None or a2 is None:
        raise ValueError("Can't find atoms")
    return a1.pos.dist(a2.pos)


if __name__ == "__main__":

    cif_dir = sys.argv[1]
    cif_files = glob(os.path.join(cif_dir, "*.cif"))

    print("Filename CBC-CMC CBB-CMB")
    for cif_file in cif_files:
        fname = os.path.basename(cif_file)
        try:
            heme = gemmi.read_structure(cif_file)
        except Exception:
            print(fname, "Can't read file")
            continue

        # TODO here want to check that the vinyl with atom CBB is furthest from
        # a propionate (2 methyls between it and propionate whereas CBC has 1
        # methyl between it and propionate)

        try:
            d1 = distance_between_two_atoms(heme, "CBC", "CMC")
            d2 = distance_between_two_atoms(heme, "CBB", "CMB")
            print(fname, d1, d2)
        except ValueError as e:
            print(cif_file, e)
