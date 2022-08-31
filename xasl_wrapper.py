import subprocess
import os
import sys
import shutil
from parse_arguments import parse_arguments
from to_json import to_json


######################## Run arg parser script #############################
print('===== Running CBRAIN wrapper for ExploreASL 1.9.0 =====')
print('Parsing arguments...')

args, params = parse_arguments(sys.argv[1:])


######################### Concatenate xASL Module Parameters ################################
# Create boolean arrays for modules
# Semicolons (MATLAB vertical vectors) are used instead of spaces (horizontal vectors),
# because run_xASL_latest.sh will send the space-separated characters as separate shell arguments...
print('Parsing module inclusion parameters...')
import_modules = '[' + args.im_dcm2nii + ';' + args.im_nii2bids + \
    ';' + args.im_deface + ';' + args.im_bids2legacy + ']'
process_modules = '[' + args.pm_structural + ';' + \
    args.pm_asl + ';' + args.pm_population + ']'

print('Import Modules: ' + import_modules)
print('Process Modules: ' + process_modules)


############################ File management ##########################################


print('Preparing output directory...')
input_path = os.path.abspath(args.input_folder)

# Set output root folder variable
path_data_root = os.path.join(os.getcwd(), args.output_folder)
print('Data root directory: ' + path_data_root)

# Tentative output path, may be changed by conditionals
# Where input data will be copied to
dest_path = path_data_root


# Verify input folder structure based on input type and subject quantity:

print('Checking input folder structure...')
if args.input_type == "DICOM":
    sourcedata_path = os.path.join(input_path, 'sourcedata')
    if not os.path.exists(sourcedata_path) or not os.listdir(sourcedata_path):
        print('ERROR: DICOM input type selected but sourcedata folder is missing.')
        exit(1)


if args.input_type == "BIDS":

    rawdata_path = os.path.join(input_path, 'rawdata')
    if os.path.exists(rawdata_path) and os.listdir(rawdata_path):
        print('BIDS input type: Found rawdata data directory.')

    else:
        if args.subject_quantity == "Single_Subject":
            if not os.path.exists(os.path.join(input_path, 'perf')):
                print(
                    'ERROR: BIDS Single Subject selected but cannot find perfusion folder.')
                exit(1)
            else:
                dest_path = os.path.join(
                    dest_path, 'rawdata', args.input_folder)
        elif args.subject_quantity == "Multiple_Subjects":
            dest_path = os.path.join(dest_path, 'rawdata')

print('Copying input files...')
print('Copying contents of ' + input_path + ' to ' + dest_path)
shutil.copytree(input_path, dest_path)


# Copy dataset_description.json if separately provided
if args.dataset_description:
    print('Copying dataset_description.json...')
    shutil.copy(args.dataset_description, os.path.join(
        path_data_root, 'rawdata', 'dataset_description.json'))


################################ Create JSON config ###############################

print("Creating config file...")

data_par_path = os.path.join(
    path_data_root, 'dataPar.json')

if os.path.isfile(data_par_path):
    print("dataPar.json already present in data root directory. Skipping...")
else:
    json_object = to_json(vars(params))

    os.makedirs(os.path.dirname(data_par_path), exist_ok=True)
    with open(data_par_path, 'w') as f:
        f.write(json_object)


###################### Run ExploreASL from bash starter script #########################
print('Running ExploreASL.')
# Original call (in Bash):
# /bin/bash /opt/xasl/xASL_latest/run_xASL_latest.sh /opt/mcr/v97/ $pathDataRoot $IMPORTMODULES $PROCESSMODULES
exit_code = subprocess.call(['bash', '/opt/xASL/run_xASL_latest.sh',
                            '/opt/matlabruntime/v911/', path_data_root, import_modules, process_modules])

if (exit_code):
    print('ExploreASL entrypoint terminated with exit code 1.')
else:
    print('ExploreASL entrypoint terminated with exit code 0.')
    print('ExploreASL task completed.')


# End of script
print('Terminating...')
