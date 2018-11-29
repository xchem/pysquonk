import uuid
import json
import gzip
from rdkit import Chem


def dict_from_mol(mol_string):
    """Take a molecule block, in a string, and write it to a dictionary in the correct format for squonk."""
    json_dict = {'uuid': str(uuid.uuid1()),
                 'source': mol_string,
                 'format': 'mol'}

    return json_dict


def sdf_to_mol_dicts(sdf_file):
    """Take an SDMolFile and convert into a list of dicts containing individual molecules in the correct format for 
    squonk."""
    suppl = Chem.SDMolSupplier(sdf_file)
    mol_json_list = []
    for mol in suppl:
        m = dict_from_mol(Chem.MolToMolBlock(mol))
        mol_json_list.append(m)

    return mol_json_list


def mol_to_mol_dict(mol_file):
    """Take a mol file, and pass to dict_from_mol, to create a dictionary in the correct format for squonk."""
    with open(mol_file, 'r') as f:
        mol_string = f.read()
    mol_json = dict_from_mol(mol_string)

    return mol_json


def dict_to_json_file(outfile, jdict):
    """Take a dictionary, or list of dictionaries (jdict) and an outfile (outfile) and write jdict to gzipped outfile."""
    with open(outfile, 'w') as f:
        json.dump(json.dumps(jdict), f)

    return outfile


