"""
    The script uses the fastapi-code-generator that creates a FastAPI application from an openapi file.
    For more details on using fastapi-code-generator, see the following documentation: 
    https://koxudaxi.github.io/fastapi-code-generator/?ref=morioh.com&utm_source=morioh.com
"""

import os
from pyutil import filereplace


# Specification path
INPUT_SPEC = "specific-provisioner/interface-specification.yml"

# Code output path
PATH_FOLDER = "specific-provisioner/src/"

# Path of the main program related to the API
PATH_MAIN = "specific-provisioner/src/main.py"

os.system(f"fastapi-codegen --input {INPUT_SPEC} --output {PATH_FOLDER}")

# To avoid possible errors when importing the module related to models
# (default: models.py), we replace '.models' with 'models' in the import 
# of main.py using a functionality of the pyutil library
filereplace(PATH_MAIN, ".models", "models")
