import os
import pathlib
import random

import numpy as np
import selfies as sf
from rdkit import Chem
from scipy.stats import poisson

_dir = str(pathlib.Path(__file__).parent.resolve())

with open(os.path.join(_dir, "sf_tokens.txt"), "r") as f:
    _lines = f.read()
    f.close()

tokens = [line.strip().split(",")[0] for line in _lines]
weights = np.array([int(line.strip().split(",")[1]) for line in _lines])


def sample_sf_token(temperature: int = 1) -> str:
    log_weights = np.log(weights) / temperature
    new_weights = np.exp(log_weights)
    new_weights = new_weights / new_weights.sum()
    token = np.random.choice(tokens, 1, p=new_weights)[0]
    return token


smiles_to_sf_tokens = lambda smi: [i for i in sf.split_selfies(sf.encoder(smi))]
sf_tokens_to_smiles = lambda list_: Chem.CanonSmiles(
    sf.decoder("".join([i for i in list_]))
)

# random selection of list index
pick_index = lambda list_: random.randint(0, len(list_) - 1)


def insert_token(smi: str, temperature: int = 1) -> str:
    selfie_list = smiles_to_sf_tokens(smi)
    random_token = sample_sf_token(temperature=temperature)
    index = pick_index(selfie_list)
    selfie_list.insert(index, random_token)
    return sf_tokens_to_smiles(selfie_list)


def delete_token(smi: str) -> str:
    selfie_list = smiles_to_sf_tokens(smi)
    index = pick_index(selfie_list)
    selfie_list.pop(index)
    return sf_tokens_to_smiles(selfie_list)


def replace_token(smi: str, temperature: int = 1) -> str:
    selfie_list = smiles_to_sf_tokens(smi)
    index = pick_index(selfie_list)
    selfie_list[index] = sample_sf_token(temperature=temperature)
    return sf_tokens_to_smiles(selfie_list)


def permute_sf_tokens(smi: str, t: int = 0, temperature: int = 0) -> str:
    """
    t: number of permutation steps
    T: temperature
    """
    if t == 0:
        t = poisson.rvs(0.6) + 1
    for i in range(t):
        k = random.randint(0, 3)
    list_of_funcs = [replace_token, delete_token, insert_token]
    new_smi = list_of_funcs[k](smi)
    if new_smi != None and len(new_smi) > 2:
        return new_smi