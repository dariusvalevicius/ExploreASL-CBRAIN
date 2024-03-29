#!/usr/bin/python3.10 -u
import subprocess
import os
import sys
import shutil
from parse_arguments import parse_arguments
from to_json import parse_list_to_dict
import json

######################## Run arg parser script #############################
print('===== Running CBRAIN wrapper for ExploreASL 1.9.0 =====')
print('Parsing arguments...')

args, params = parse_arguments(sys.argv[1:])

######################### Concatenate xASL Module Parameters ################################
# Create boolean arrays for modules
print('Parsing module inclusion parameters...')

import_modules = ""
process_modules = ""

if args.mode == "BIDS":

    import_modules = f"[0,0,{args.im_deface},1]"
    process_modules = f"[{args.pm_structural},{args.pm_asl},0]"

# if args.mode == "DICOM":

#     import_modules = f"[1]"
#     process_modules = f"[{args.pm_structural},{args.pm_asl},{args.pm_population}]"

# print('Import Modules: ' + import_modules)
# print('Process Modules: ' + process_modules)

############################ File management ##########################################

print('Preparing output directory...')
# input_path = os.path.abspath(args.input_folder)

# Set output root folder variable
# Strip extra folder layers that may be artifacts of "input_folder" prefixing
output_path = os.path.abspath(os.path.basename(os.path.normpath(args.output_folder)))
print('Data root directory: ' + output_path)

## BIDS dataset:
## Copy BIDS dataset (with dataset_description.json)
## to root/rawdata

if args.mode == "BIDS":

    dest_path = os.path.join(output_path, "rawdata")

    print('Copying input files...')
    print('Copying contents of ' + args.input_folder + ' to ' + dest_path)

    if os.path.isfile(os.path.join(args.input_folder, "dataset_description.json")):
        print("BIDS Dataset found. Copying...")
        shutil.copytree(args.input_folder, dest_path)
    else:
        raise Exception("BIDS ERROR: No dataset_description.json found in input directory. Is it a valid BIDS dataset?")

## DICOM:
## Should already have correct folder structure + all contained JSONs!
## User can figure out the complicated system from xASL docs
## Alternatively, we can add a parameter section for defining sourceStructure.json

# dicom_has_json = False

# if args.mode == "DICOM":

#     # Contains sourceStructure.json?
#     for dirpath, dirs, files in os.walk('src'): 
#         for filename in files:
#             if filename == "sourceStructure.json":
#                 dicom_has_json = True

#     shutil.copytree(args.input_folder, output_path)

################################ Create JSON configs ###############################

    
print("Creating config files...")

# Create dataPar.json
data_par = parse_list_to_dict(vars(params))

data_par_path = os.path.join(
    output_path, 'dataPar.json')

if os.path.isfile(data_par_path):
    print("Warning: dataPar.json already present in root directory. Overwriting.")

print('Writing dataPar.json...')
# os.makedirs(os.path.dirname(data_par_path), exist_ok=True)
with open(data_par_path, 'w') as f:
    json_object = json.dumps(data_par, indent=4)
    f.write(json_object)

# Create sourceStructure.json if applicable

# if args.mode =='DICOM' and not dicom_has_json:

#     # source_structure = {k: data_par[k] for k in ('folderHierarchy', 'tokenOrdering', 'tokenVisitAliases', 'tokenSessionAliases', 'tokenScanAliases', 'bMatchDirectories')}

#     source_structure = {}

#     for k in ['folderHierarchy', 'tokenOrdering', 'tokenVisitAliases', 'tokenSessionAliases', 'tokenScanAliases', 'bMatchDirectories']:
#         if k in data_par.keys():
#             source_structure[k] = data_par[k]

#     source_structure_path = os.path.join(output_path, 'sourceStructure.json')

#     print('Writing sourceStructure.json...')
#     with open(source_structure_path, 'w') as f:
#         json_object = json.dumps(source_structure, indent=4)
#         f.write(json_object)




###################### Run ExploreASL from bash starter script #########################
print('Running ExploreASL.')
print('=======================================================')

# Original call (in Bash):
# /bin/bash /opt/xasl/xASL_latest/run_xASL_latest.sh /opt/mcr/v97/ $pathDataRoot $IMPORTMODULES $PROCESSMODULES
# subprocess.run(['bash', '/opt/xASL/run_xASL_latest.sh',
#                             '/opt/matlabruntime/v911/', 
#                             output_path, import_modules, process_modules],
#                             check=True)

try:
    result = subprocess.run(['bash', 
                             '/opt/xASL/run_xASL_latest.sh',
                             '/opt/matlabruntime/v911/', 
                             output_path, import_modules, process_modules], 
                             stderr=subprocess.PIPE, check=True)
except subprocess.CalledProcessError as e:
    error_code = e.returncode
    error_message = e.stderr.decode().strip()
    raise Exception(f"Error {error_code}: {error_message}")

print('=======================================================')

# End of script
# This will only execute if subprocess.run completes successfully
# check=True will raise a CalledProcessError exception
print('ExploreASL task completed.')
print('Terminating...')
exit(0)