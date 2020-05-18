#!/usr/bin/env ccp4-python
from __future__ import print_function
import gemmi
from glob import glob
import sys
import os

def extract_residue(structure):

    try:
        model = structure[0]
    except IndexError:
        raise ValueError("Can't find atoms")
    chain = model[0]
    residue = chain[0]

    return residue

def distance_between_two_atoms(residue, atom1, atom2):

    a1 = residue.find_atom(atom1, "*")
    a2 = residue.find_atom(atom2, "*")

    if a1 is None or a2 is None:
        raise ValueError("Can't find atoms")
    return a1.pos.dist(a2.pos)

def iron_position(residue):

    fe = residue.find_atom("FE", "*")
    if fe is None:
        raise ValueError("Can't find iron")

    return fe.pos.x, fe.pos.y, fe.pos.z


if __name__ == "__main__":

    cif_dir = sys.argv[1]
    cif_files = glob(os.path.join(cif_dir, "*.cif"))

    print("Filename CBC-CMC CBB-CMB Fe.x Fe.y Fe.z")
    for cif_file in cif_files:
        fname = os.path.basename(cif_file)
        try:
            heme_structure = gemmi.read_structure(cif_file)
        except Exception:
            print(fname, "Can't read file")
            continue

        try:
            heme_res = extract_residue(heme_structure)
        except ValueError as e:
            print(fname, e)

        # TODO here want to check that the vinyl with atom CBB is furthest from
        # a propionate (2 methyls between it and propionate whereas CBC has 1
        # methyl between it and propionate)

        try:
            d1 = distance_between_two_atoms(heme_res, "CBC", "CMC")
            d2 = distance_between_two_atoms(heme_res, "CBB", "CMB")
            d1_d2 = ("{:.6f} " * 2).format(d1, d2)
        except ValueError as e:
            d1_d2 = str(e)

        try:
            fe_xyz = iron_position(heme_res)
            fe_xyz = ("{:.4f} " * 3).format(*fe_xyz)
        except ValueError as e:
            fe_xyz = str(e)

        print(fname, d1_d2, fe_xyz)
