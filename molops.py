import uuid
import json
from rdkit import Chem


def dict_from_mol(mol_string):
    json_dict = {'uuid': str(uuid.uuid1()),
                 'source': mol_string,
                 'type': 'mol'}

    return json_dict


def sdf_to_mol_dicts(sdf_file):
    suppl = Chem.SDMolSupplier(sdf_file)
    mol_json_list = []
    for mol in suppl:
        m = dict_from_mol(Chem.MolToMolBlock(mol))
        mol_json_list.append(m)

    return mol_json_list


def mol_to_mol_dict(mol_file):
    with open(mol_file, 'r') as f:
        mol_string = f.read()
    mol_json = dict_from_mol(mol_string)

    return mol_json


def dict_to_json_file(outfile, jdict):
    with open(outfile, 'w') as f:
        json.dump(jdict, f)

    return outfile
