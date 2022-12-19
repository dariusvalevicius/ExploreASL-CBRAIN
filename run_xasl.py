#!/usr/bin/python3.10 -u
import subprocess
import os
import sys
import shutil
from parse_arguments import parse_arguments
from to_json import parse_list_to_dict
import json


## New in this version (1.2.0?):
# - Split tool in 3 (BIDS Subject, BIDS Dataset, DICOM)
# - Updated descriptor with default values
# - List type inputs will now be lists in CBRAIN


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

if args.mode == "BIDS_Subject":

    import_modules = f"[0,0,{args.im_deface},1]"
    process_modules = f"[{args.pm_structural},{args.pm_asl},0]"

if args.mode == "BIDS_Dataset":

    import_modules = f"[0,0,{args.im_deface},1]"
    process_modules = f"1"

if args.mode == "DICOM":

    import_modules = f"[1]"
    process_modules = f"[{args.pm_structural},{args.pm_asl},{args.pm_population}]"

print('Import Modules: ' + import_modules)
print('Process Modules: ' + process_modules)

############################ File management ##########################################

print('Preparing output directory...')
# input_path = os.path.abspath(args.input_folder)

# Set output root folder variable
output_path = os.path.abspath(args.output_folder)
print('Data root directory: ' + output_path)

## BIDS Subject:
## Copy BIDS subject folder to root/rawdata
## Copy dataset_description.json to the same directory

if args.mode == "BIDS_Subject":

    dest_path = os.path.join(output_path, "rawdata")

    print('Copying input files...')
    print('Copying contents of ' + args.input_folder + ' to ' + dest_path)
    shutil.copytree(args.input_folder, dest_path)

    print('Copying dataset_description.json...')
    shutil.copy(args.dataset_description, dest_path)

## BIDS dataset:
## Copy BIDS dataset (with dataset_description.json)
## to root/rawdata

if args.mode == "BIDS_Dataset":

    dest_path = os.path.join(output_path, "rawdata")

    print('Copying input files...')
    print('Copying contents of ' + args.input_folder + ' to ' + dest_path)
    shutil.copytree(args.input_folder, dest_path)

## DICOM:
## Should already have correct folder structure + all contained JSONs!
## User can figure out the complicated system from xASL docs
## Alternatively, we can add a parameter section for defining sourceStructure.json

if args.mode == "DICOM":

    valid_dicom_input = False

    ## Do a bunch of checks!

    # Contains sourceStructure.json?
    for dirpath, dirs, files in os.walk('src'): 
        for filename in files:
            if filename == "sourceStructure.json":
                valid_dicom_input = True
    
    if not valid_dicom_input:
        raise Exception("")

    shutil.copytree(args.input_folder, output_path)

################################ Create JSON config ###############################
print("Creating config file...")
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
