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
# Semicolons (MATLAB vertical vectors) are used instead of spaces (horizontal vectors),
# because run_xASL_latest.sh will send the space-separated characters as separate shell arguments...
print('Parsing module inclusion parameters...')

import_modules = ""
process_modules = ""

if args.mode == "BIDS":

    import_modules = f"[0,0,{args.im_deface},1]"
    process_modules = f"[{args.pm_structural},{args.pm_asl},0]"

# if args.mode == "BIDS_Dataset":

#     import_modules = f"[0,0,{args.im_deface},1]"
#     process_modules = f"1"

# if args.mode == "DICOM":

#     import_modules = f"[1]"
#     process_modules = f"[{args.pm_structural},{args.pm_asl},{args.pm_population}]"

# print('Import Modules: ' + import_modules)
# print('Process Modules: ' + process_modules)

############################ File management ##########################################

print('Preparing output directory...')
# input_path = os.path.abspath(args.input_folder)

# Set output root folder variable
output_path = os.path.abspath(args.output_folder)
print('Data root directory: ' + output_path)

## BIDS dataset:
## Copy BIDS dataset (with dataset_description.json)
## to root/rawdata

if args.mode == "BIDS":

    dest_path = os.path.join(output_path, "rawdata")

    print('Copying input files...')
    print('Copying contents of ' + args.input_folder + ' to ' + dest_path)

    # For development purposes:
    # When running outside CBRAIN (e.g. directly in Docker), input will have one less layer
    # Check for dataset_description.json; if not present, add extra folder layer and copy dataset_description_json

    if os.path.isfile(os.path.join(args.input_folder, "dataset_description.json")):
        print("BIDS Dataset found.")
        shutil.copytree(args.input_folder, dest_path)
    else:
        print("BIDS Subject found. Copying dataset_description.json")
        shutil.copytree(args.input_folder, os.path.join(dest_path, args.input_folder))
        shutil.copy(args.dataset_description_json, dest_path)

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
# Original call (in Bash):
# /bin/bash /opt/xasl/xASL_latest/run_xASL_latest.sh /opt/mcr/v97/ $pathDataRoot $IMPORTMODULES $PROCESSMODULES
exit_code = subprocess.call(['bash', '/opt/xASL/run_xASL_latest.sh',
                            '/opt/matlabruntime/v911/', output_path, import_modules, process_modules])

if (exit_code):
    print('ExploreASL entrypoint terminated with exit code 1.')
else:
    print('ExploreASL entrypoint terminated with exit code 0.')
    print('ExploreASL task completed.')


# End of script
print('Terminating...')
