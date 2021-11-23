#!/usr/bin/env python
# Copyright 2021 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Relax AlphaFold protein structure prediction script."""
import json
import os
#import pathlib
import pickle
#import random
#import shutil
import sys
import time
#from typing import Dict, Union, Optional

#from absl import app
#from absl import flags
from absl import logging
from alphafold.common import protein
#from alphafold.common import residue_constants
#from alphafold.data import pipeline
#from alphafold.data import pipeline_multimer
#from alphafold.data import templates
#from alphafold.data.tools import hhsearch
#from alphafold.data.tools import hmmsearch
#from alphafold.model import config
#from alphafold.model import model
from alphafold.relax import relax
import numpy as np

#from alphafold.model import data
# Internal import (7716).

logging.set_verbosity(logging.INFO)





MAX_TEMPLATE_HITS = 20
RELAX_MAX_ITERATIONS = 0
RELAX_ENERGY_TOLERANCE = 2.39
RELAX_STIFFNESS = 10.0
RELAX_EXCLUDE_RESIDUES = []
RELAX_MAX_OUTER_ITERATIONS = 3



def main():
    amber_relaxer = relax.AmberRelaxation(
    max_iterations=RELAX_MAX_ITERATIONS,
    tolerance=RELAX_ENERGY_TOLERANCE,
    stiffness=RELAX_STIFFNESS,
    exclude_residues=RELAX_EXCLUDE_RESIDUES,
    max_outer_iterations=RELAX_MAX_OUTER_ITERATIONS)
    # Load the model outputs.
    result_output_path = os.path.join(output_dir, f'result_{model_name}.pkl')
    model_name=get_model_name_from_pkl(result_out_path)
    with open(result_output_path, 'rb') as f:
      prediction_results=pickle.load(f)
      plddt = prediction_result['plddt']
      ranking_confidences[model_name] = prediction_result['ranking_confidence']
      # Add the predicted LDDT in the b-factor column.
      # Note that higher predicted LDDT value means higher model confidence.
      plddt_b_factors = np.repeat(
        plddt[:, None], residue_constants.atom_type_num, axis=-1)
      unrelaxed_protein = protein.from_prediction(
        features=processed_feature_dict,
        result=prediction_result,
        b_factors=plddt_b_factors,
        remove_leading_feature_dimension=not model_runner.multimer_mode)

      unrelaxed_pdbs[model_name] = protein.to_pdb(unrelaxed_protein)
      #      unrelaxed_pdb_path = os.path.join(output_dir, f'unrelaxed_{model_name}.pdb')
      #      with open(unrelaxed_pdb_path, 'w') as f:
      #        f.write(unrelaxed_pdbs[model_name])
      t_0 = time.time()
      relaxed_pdb_str, _, _ = amber_relaxer.process(prot=unrelaxed_protein)
      timings[f'relax_{model_name}'] = time.time() - t_0
      relaxed_pdbs[model_name] = relaxed_pdb_str
      # Save the relaxed PDB.
      relaxed_output_path = os.path.join(
          output_dir, f'relaxed_{model_name}.pdb')
      with open(relaxed_output_path, 'w') as f:
        f.write(relaxed_pdb_str)



if __name__ == '__main__':
  main()
