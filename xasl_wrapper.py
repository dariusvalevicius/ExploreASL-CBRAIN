from importlib import import_module
import json
import array as arr
import argparse as argp
import subprocess
import os
import sys
import shutil


# 1. Parse arguments into variables using argparse
# 2. Create JSON-like structure using dict and array
# 3. Write structure to JSON
# 4. Run xasl's 'run.sh'

print('===== Running CBRAIN wrapper for ExploreASL 1.9.0 =====')
print('Parsing arguments...')

p = argp.ArgumentParser(
    description='CBRAIN wrapper for ExploreASL. Main function is to allow argument inputs from the command line rather than JSON config file.')

########################################################################################
## Custom I/O parameters
p.add_argument('--input_folder', type=str)
p.add_argument('--output_folder', type=str)
p.add_argument('--input_type', type=str)
p.add_argument('--input_subject_quantity', type=str)

## Dataset parameters
p.add_argument('--dataset_root', type=str, default='')

## Import Modules
p.add_argument('--im_dcm2nii', type=str, default='0')
p.add_argument('--im_nii2bids', type=str, default='0')
p.add_argument('--im_deface', type=str, default='0')
p.add_argument('--im_bids2legacy', type=str, default='0')

## Process Modules
p.add_argument('--pm_structural', type=str, default='0')
p.add_argument('--pm_asl', type=str, default='0')
p.add_argument('--pm_population', type=str, default='0')
########################################################################################

args = p.parse_args(sys.argv[1:])


## Copy input to folder that xASL expects it to be in
print('Preparing input directory...')
shutil.copytree(args.input_folder, '/data/incoming')


## Create boolean arrays for modules
print('Parsing module inclusion parameters...')
import_modules = '[' + args.im_dcm2nii + ';' + args.im_nii2bids + ';' + args.im_deface + ';' + args.im_bids2legacy + ']'
process_modules = '[' + args.pm_structural + ';' + args.pm_asl + ';' + args.pm_population + ']'

# import_modules = "1"
# process_modules = "1"

print('Import Modules: ' + import_modules)
print('Process Modules: ' + process_modules)


## Set necessary environment variables
print('Setting environment variables for xASL execution...')
os.environ["DATASETROOT"] = args.dataset_root
os.environ["IMPORTMODULES"] = import_modules
os.environ["PROCESSMODULES"] = process_modules


## Run ExploreASL from bash entrypoint script
print('Running ExploreASL.')
exit_code = subprocess.call('/opt/run.sh')

if(exit_code):
    print('ExploreASL entrypoint terminated with exit code 1.')

else:
    print('ExploreASL entrypoint terminated with exit code 0.')

    ## Copy output data to CBRAIN's output volume
    print('Preparing output directory...')
    if os.path.exists(args.output_folder) and os.path.isdir(args.output_folder):
        shutil.rmtree(args.output_folder)
    shutil.copytree('/data/outgoing', args.output_folder)

    print('ExploreASL task completed.')


## End of script
print('Terminating...')


###########################
## Code snippets

# run -e DATASETROOT=MY-BIDS-DATASET
#        -e IMPORTMODULES=1 -e PROCESSMODULES=1
#        -v /home/.../incoming:/data/incoming
#        -v /home/.../outgoing:/data/outgoing xasl:1.7.0



# ########################################################################################
# ##
# p.add_argument('--studyID', type=str, const='test')
# p.add_argument('--visitNames', type=list, const='test')
# p.add_argument('--studyID', type=str, const='test')
# p.add_argument('--studyID', type=str, const='test')
# p.add_argument('--studyID', type=str, const='test')
# ########################################################################################

# ########################################################################################
# ## Dataset Parameters

# ########################################################################################
