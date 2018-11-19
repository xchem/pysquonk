# pysquonk
A python wrapper around squonk RESTful services

## Setup

The setup is specific to your environment, and is configured in ```config.ini```. A template file fot this can be found at ```config_template```.ini

For more information on what is required, and how to set up squonk RESTful services on your own cluster, please contact tdudgeon@informaticsmatters.com

## Authorisation

You will need to get a token to do anything with the service. The autorisation class can be found in ```auth.py```.

To get a token, providing the info in ```config.ini``` is correct:

```
from auth import SquonkAuth

token = SquonkAuth().get_token()
```

This token should be valid for approx. 5 minutes. You will need a new one after this. 

## Services

All functions related to getting information about the available services can be found in ```service_info.py```

e.g:

```
from service_info import SquonkServiceInfo
from auth import SquonkAuth

# get a token for authorisation
token = SquonkAuth().get_token()

# list of service ids
service_ids = SquonkServiceInfo().list_service_ids(token=token)

# list info for 'pipelines.rdkit.sucos.basic'
info = SquonkServiceInfo().list_full_service_info(service_id='pipelines.rdkit.sucos.basic', token=token)

print(info)

>> {u'description': u'Generate 3D overlay using SuCOS in RDKit', u'optionDescriptors': [{u'description': u'Target molecule index (default is the first)', u'editable': True, u'label': u'Target mol index', u'visible': True, u'maxValues': 1, u'key': u'arg.target', u'minValues': 0, u'typeDescriptor': {u'type': u'java.lang.Integer', u'@class': u'org.squonk.options.SimpleTypeDescriptor'}, u'@class': u'org.squonk.options.OptionDescriptor', u'modes': [u'User']}], u'tags': [u'rdkit', u'alignment', u'sucos', u'3d', u'docker'], u'outputDescriptors': [{u'primaryType': u'org.squonk.dataset.Dataset', u'secondaryType': u'org.squonk.types.MoleculeObject', u'name': u'output', u'mediaType': u'application/x-squonk-dataset-molecule+json'}], u'executorClassName': u'org.squonk.execution.steps.impl.ThinDatasetDockerExecutorStep', u'name': u'RDKitSuCOS', u'inputDescriptors': [{u'primaryType': u'org.squonk.dataset.Dataset', u'secondaryType': u'org.squonk.types.MoleculeObject', u'name': u'input', u'mediaType': u'application/x-squonk-dataset-molecule+json'}, {u'primaryType': u'org.squonk.dataset.Dataset', u'secondaryType': u'org.squonk.types.MoleculeObject', u'name': u'target', u'mediaType': u'application/x-squonk-dataset-molecule+json'}], u'id': u'pipelines.rdkit.sucos.basic', u'icon': u'icons/filter_molecules.png'}

```

## Submitting a job

Now we know what info we need, we can submit a job. The job submission classes can be found in ```jobs.py```. 

The class to submit a job is called ```SquonkJob().submit_job_from_yaml()```. This requires a yml file containing all of the neccessary info for the job you want to submit. For the job info we looket at above, we know that we need a 'target' molecule (named target) and an sdf file of molecules to compare against it. An example of a yml file for this can be found in test_data/sucos.yml:

```
username: user101
service_name: pipelines.rdkit.sucos.basic
content_type: multipart/mixed
input_data:
  input:
    name: test_data/sucos_data/4e3g_lig.mol
    type: mol
    options:
      None
  target:
    name: test_data/sucos_data/mols.sdf
    type: sdf
    options:
      arg.target: 1
```

