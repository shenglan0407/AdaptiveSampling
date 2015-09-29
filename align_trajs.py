#---------------------------------------------------------------------
# Author: Shenglan Qiao <shenglan@stanford.edu>
# Contributors:
# Copyright (c) 2015, Stanford University
# All rights reserved.
# 
# This scripts aligns simulation trajectories by aligning the alpha-C in the following 
# residues: TRP109, THR110, ASP113, VAL114, VAL117, THR118, PHE193, SER203,
# SER207, TRP286, PHE289, PHE290, ASN293, ASN312, TYR316.

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import numpy as np
import os

import mdtraj as md

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------


sim_path = '/scratch/PI/rondror/MD_simulations/amber/b2AR_ligand_binding/alprenolol/ten_ligands/production/ten_ligands/reimaged_trajs/'
align_path = '/scratch/PI/rondror/MD_simulations/amber/b2AR_ligand_binding/alprenolol/ten_ligands/production/ten_ligands/aligned_trajs/'
topology = '/scratch/PI/rondror/MD_simulations/amber/b2AR_ligand_binding/alprenolol/ten_ligands/system.psf'

# all trajectories
sim_files = []
for this_file in os.listdir(sim_path):
    if this_file.endswith('.nc'):
        sim_files.append(this_file)

print ('We are using the first frame in the following trajectory to align the other ones:')
print sim_files[0]
ref_traj = md.load_frame(sim_path+sim_files[0],0, top = topology)

res_to_track = ['TRP109','THR110','ASP113','VAL114','VAL117','THR118','PHE193','SER203',\
'SER207','TRP286','PHE289','PHE290','ASN293','ASN312','TYR316']
ind_align_CAs = [atom.index for atom in ref_traj.topology.atoms if atom.name in ['CA'] and str(atom.residue) in res_to_track]



for this_sim_file in sim_files:
    print ("Aligning %s ..." % this_sim_file)
    this_traj = md.load(sim_path+this_sim_file,top = topology)
    this_traj.superpose(ref_traj,frame = 0, atom_indices = ind_align_CAs)
    this_traj.save_netcdf(align_path+this_sim_file)
