import argparse


def parse_arguments(argv):

    # Create a new namespace to hold optional params for studyPar.json
    class Params:
        pass
    params = Params()

    # Creat argparser
    p = argparse.ArgumentParser(description="test")

    ################################## Arguments #########################################
    # Custom I/O parameters
    p.add_argument('--mode', type=str,
                   help="Which CBRAIN tool is being used? 1. DICOM 2. BIDS")

    p.add_argument('--input_folder', type=str,  # required=True,
                   help="Data folder to be processed. Can be single-subject or multi-subject, in DICOM, BIDS, or xASL Legacy format.\nNOTE: For the Structural and ASL process modules, a CBCSV can be used to process multiple subjects. For the Population module, all subjects must be included in one file collection.")
    p.add_argument('--output_folder', type=str,
                   help="Output folder name using input and output suffix.")
    # p.add_argument('--input_type', type=str,
    #                help="The format of the input dataset.\nNOTE: For DICOM input, folder structure must adhere to a convention set by ExploreASL. See their documentation for details.")
    # p.add_argument('--subject_quantity', type=str,
    #                help="Whether the input dataset contains one subject or multiple subjects' data.\nNOTE: If using a CBCSV to run multiple subjects in parallel, select 'Single_Subject'.")
    # p.add_argument('--dataset_description_json', type=str,
                #    help="dataset_description.json must be provided if not present in the input folder.")
    # p.add_argument('--source_structure', type=str,
    #                help="Config file defining structure of DICOM directory. Only required for DICOM. See ExploreASL documentation for details.\nNOTE: This field is not required if sourceStructure.json is included in the input folder (at root level).")
    # p.add_argument('--study_par', type=str,
    #                help="Config file containing study description fields. Recommended for DICOM input. See ExploreASL documentation for details.")
    # p.add_argument('--parameter_behaviour', type=str,
    #                help="If there is already a dataPar.json present in the input directory, do you wish to keep the original, overwrite, merge with priority to the original, or merge with priority to the new parameters?")

    # Import Modules
    p.add_argument('--im_dcm2nii', type=str, default=0,
                   help="Boolean: Use the DICOM to NIfTI import module")
    p.add_argument('--im_nii2bids', type=str, default=0,
                   help="Boolean: Use the NIfTI to BIDS import module")
    p.add_argument('--im_deface', type=str, default=0,
                   help="Boolean: Use the defacing import module")
    p.add_argument('--im_bids2legacy', type=str, default=0,
                   help="Boolean: Use the BIDS to xASL Legacy import module")

    # Process Modules
    p.add_argument('--pm_structural', type=str, default=0,
                   help="Boolean: Use the structural process module")
    p.add_argument('--pm_asl', type=str, default=0,
                   help="Boolean: Use the ASL process module")
    p.add_argument('--pm_population', type=str, default=0,
                   help="Boolean: Use the population process module\nNOTE: Input folder must be a collection containing all subject data.")

    # Parse above arguments into args object
    # Save the rest for later
    args, rest = p.parse_known_args(argv)

    ############### SourceStructure.json arguments ###################

    # p.add_argument('--folderHierarchy', type=str,  # required=True,
    #                help="This specifies the names of all directories at all levels.\nExample: \"^(\\d{\3}).*\", \"^Session([12])$\",\"^(PSEUDO_10_min|T1-weighted|M0)$\"")
    # p.add_argument('--tokenOrdering', type=str,  # required=True,
    #                help="Tokens (parts of the directory names) were extracted according to the regular expressions above. Here we decide how the tokens are used.\nThis is specified by \"tokenOrdering\": [patientName, SessionName, ScanName]\nExample: \"tokenOrdering\": [2 0 1 3]; = second token is used for patient name, first for session name, third for scan name\n\"tokenOrdering\": [2 1 0 3]; = second token is used for patient name, first for visit name, third for scan name")
    # p.add_argument('--tokenVisitAliases', type=str,  # required=True,
    #                help="If multiple visits are present - use the following notation to mark them:\n\"tokenVisitAliases\":[\"session_1\",\"1\",\"session_2\",\"2\",\"session_3\",\"3\",\"session_4\",\"4\",\"session_5\",\"5\",\"session_6\",\"6\",\"session_7\",\"7\"]")
    # p.add_argument('--tokenSessionAliases', type=str,  # required=True,
    #                help="The second token defines the name of the session. The token was extracted using a regular expression *^Session([12])$*. This can represent a string Session1 or Session2. And either 1 or 2 is taken as the token.\nIn the session-aliases, each row represents one session name. The first column is the regular expression for the token, the second column gives the final name.\n^1$ ASL_1\n^2$ ASL_2\nHere, the token name ^1$ - that is a string equaling to \"1\" is replaced in the analysis folder by the session name ASL_1.\nExample: \"tokenSessionAliases\": [\"^1$\", \"ASL_1\", \"^2$\", \"ASL_2\"],")
    # p.add_argument('--tokenScanAliases', type=str,  # required=True,
    #                help="")
    # p.add_argument('--bMatchDirectories', action="store_true",
    #                help="Set to true if it should look for directories and DICOM files inside them. Set to false when directly separate files are identified by the folder-hierarchy string.")
    

    ################ DataPar.json arguments #######################

    # Study Parameters
    p.add_argument('--x__SESSIONS', type=str,
                   help="Use this to define sessions.\nExample ('.json' file): [\"ASL_1\",\"ASL_2\"]\nDEFAULT = {'ASL_1'}")
    p.add_argument('--x__session__options', type=str,
                   help="This is how the sessions will be called, example: {'baseline' 'drug'}.\nFor FEAST, this should be {'crushed' 'non-crushed'}.")

    # Dataset Parameters
    p.add_argument('--x__dataset__subjectRegexp', type=str,
                   help="String with regular expression for ExploreASL to find subjects by foldername, example: ^\d{\3}$ for three digits")
    p.add_argument('--x__dataset__exclusion', type=str,
                   help="Cell with list of subjects to exclude, example: {'005' '018'}\nDEFAULT = empty")
    p.add_argument('--x__dataset__ForceInclusionList', type=str,
                   help="Use this field if you want to use a selection of subjects rather than taking all available subjects from directories\nExample: load(fullfile(x.D.ROOT,'LongitudinalList.mat')).\nDEFAULT = use all subjects")

    # M0 Parameters and Options
    p.add_argument('--x__modules__asl__M0_conventionalProcessing', action="store_true",
                   help="Boolean - use the conventional M0 processing (per consensus paper), \noptions: 1 = standard processing, 0 = new image processing (improved masking & smoothing).\nDEFAULT = 0")
    p.add_argument('--x__modules__asl__M0_GMScaleFactor', action="store_true",
                   help="Add additional scale factor to multiply the M0 image by \nThis can be useful when you have background suppression but no control/M0 image without background suppression. If you then know the M0 scalefactor for the GM, you can use the control image as M0 and use this parameter to scale back what was suppressed by background suppression. Note that there is no option for separate tissue scaling (e.g. WM & GM), because ExploreASL pragmatically smooths the M0 a lot, assuming that head motion and registration between M0 & ASL4D will differ between patients and controls.\nDEFAULT = 1")
    p.add_argument('--x__modules__asl__M0PositionInASL4D', type=str,
                   help="A vector of integers that indicates the position of M0 in TimeSeries, if it is integrated by the Vendor in the DICOM export. Will move this from ASL4D.nii to M0.nii Note that the x.modules.asl.M0PositionInASL4D parameter is independent from the x.Q.M0 parameter choice. Example for Philips 3D GRASE = '[1 2]' (first control-label pair). Example for Siemens 3D GRASE = 1 first image. Example for GE 3D spiral = 2 where first image is PWI & last = M0. Empty vector should be given (= [] or = null (in JSON)) if no action is to be taken and nothing is removed.\nDEFAULT = [] (no M0 in timeseries)")
    p.add_argument('--x__modules__asl__DummyScanPositionInASL4D', type=str,
                   help="A vector of integers that indicates the position of Dummy scans in TimeSeries if they are integrated by the Vendor in the DICOM export. This allows to remove the dummy scans or noise scans that are part of the Timeseries. A new ASL4D.nii is saved with dummy scans removed and the original is backed-up. Works in a similar way as M0PositionInASL4D, both can be entered at the same time and both indicate the original position in the Timeseries independend of each other. Example for Siemens 2D EPI = [79 80] Skip the control-label pair used for noise measurements. Example for certain Siemens 3D GRASE = 2 Skip the first dummy control image. Empty vector should be given (= [] or = null (in JSON)) if no action is to be taken and nothing is removed.\nDEFAULT = [] (no M0 in timeseries)")

    # Sequence parameters
    p.add_argument('--x__Q__M0', type=str,
                   help="Choose which M0 option to use: 'separate_scan' = for a separate M0 NIfTI (needs to be in the same folder called M0.nii), 3.7394*10^6 = single M0 value to use, 'UseControlAsM0' = will copy the mean control image as M0.nii and process as if it was a separately acquired M0 image (taking TR etc from the ASL4D.nii). Make sure that no background suppression was used, otherwise this option is invalid.")
    p.add_argument('--x__Q__BackgroundSuppressionNumberPulses', type=int,
                   help="Used to estimate decrease of labeling efficiency. Options: 0 = (no background suppression), 2 = labeling efficiency factor 0.83 (e.g. Philips 2D EPI & Siemens 3D GRASE), 4 = labeling efficiency factor 0.81 (e.g. Philips 3D GRASE), 5 = labeling efficiency factor 0.75 (e.g. GE 3D spiral).")
    p.add_argument('--x__Q__BackgroundSuppressionPulseTime', type=str,
                   help="Vector containing timing, in ms, of the background suppression pulses before the start of the readout (per BIDS)\nREQUIRED when x.Q.UseControlAsM0 & x.Q.BackgroundSuppressionNumberPulses>0.")
    p.add_argument('--x__Q__PresaturationTime', type=float,
                   help="Time in ms before the start of the readout, scalar, when the slice has been saturated (90 degree flip) this has to come before all the bSup pulses, but doesn't need to be always specified. Defaults to PLD (PASL) or PLD+LabDur ((P)CASL).")
    p.add_argument('--x__Q__readoutDim', type=str,
                   help="String specifying the readout type. Options: '2D' for slice-wise readout, '3D' for volumetric readout.")
    p.add_argument('--x__Q__Vendor', type=str,
                   help="String containing the Vendor used. This parameter is used to apply the Vendor-specific scale factors, \noptions: 'GE_product', 'GE_WIP', 'Philips', 'Siemens'.")
    p.add_argument('--x__Q__Sequence', type=str,
                   help="String containing the sequence used. Options: '3D_spiral', '3D_GRASE', '2D_EPI'.")
    p.add_argument('--x__Q__LabelingType', type=str,
                   help="String containing the labeling strategy used. Options: 'PASL' (pulsed Q2-TIPS), 'CASL' (CASL/PCASL). Note: pulsed without Q2TIPS cannot be reliably quantified because the bolus width cannot be identified CASL & PCASL are both continuous ASL methods, identical quantification.")
    p.add_argument('--x__Q__Initial_PLD', type=str,
                   help="Value of PLD (ms), for 3D this is fixed for whole brain, for 2D this is the PLD of first acquired slice, example: 1800.")
    p.add_argument('--x__Q__LabelingDuration', type=float,
                   help="Value of labeling duration (ms), example: 1800.")
    p.add_argument('--x__Q__SliceReadoutTime', type=str,
                   help="Value (ms) of time added to the PLD after reading out each slice, example: 31. Other option = 'shortestTR'; shortest TR enabled gives each sequence the minimal TR. This enables calculating slice delay per subject.")

    # Quantification Parameters
    p.add_argument('--x__Q__bUseBasilQuantification', type=int,
                   help="True for using BASIL quantification in addition to ExploreASL's quantification.")
    p.add_argument('--x__Q__Lambda', type=float, default=0.9,
                   help="Brain/blood water coefficient (mL 1H/ mL blood). Example: 0.32 (for GSP phantom).\nDEFAULT = 0.9")
    p.add_argument('--x__Q__T2art', type=float, default=50,
                   help="T2* of arterial blood, only used when no M0 image (ms).\nDEFAULT = 50 @ 3T")
    p.add_argument('--x__Q__BloodT1', type=float, default=1650,
                   help="T1 relaxation time of arterial blood (ms). Defaults (Alsop MRM 2014), 1800 for GSP phantom.\nDEFAULT = 1650 @ 3T")
    p.add_argument('--x__Q__TissueT1', type=float, default=1240,
                   help="T1 relaxation time of GM tissue (ms). Defaults (Alsop MRM 2014).\nDEFAULT=1240 @ 3T")
    p.add_argument('--x__Q__nCompartments', type=int, default=1,
                   help="Number of modeled compartments for quantification. Options: 1 = a single-compartment quantification model (default by concensus paper), 2 = a dual-compartment quantification model.\nDEFAULT = 1")
    p.add_argument('--x__Q__ApplyQuantification', type=str,
                   help="A vector of 1x5 logical values specifying which types on quantified images should be calculated and saved. Fields: 1) Apply ScaleSlopes ASL4D (xASL_wrp_Quantify, future at dcm2niiX stage), 2) Apply ScaleSlopes M0 (xASL_quant_M0, future at dcm2niiX stage), 3) Convert PWI a.u. to label (xASL_wrp_Quantify, future at xASL_wrp_Reslice?), 4) Quantify M0 a.u. (xASL_quant_M0, corrects for incomplete T1 relaxation), 5) Perform division by M0. Examples: ASL4D is an already quantified CBF image, disable all quantification '[0 0 0 0 0]'. To compare label but not CBF (e.g. label in vessels or sinus vs tissue): [1 1 1 1 0]'. Note that the output always goes to CBF.nii.\nDEFAULT = '[1 1 1 1 1]' = all enabled")
    p.add_argument('--x__Q__SaveCBF4D', action="store_true",
                   help="Boolean, true to also save 4D CBF timeseries, if ASL4D had timeseries.\nDEFAULT=false")

    # ASL Processing Parameters
    p.add_argument('--x__modules__asl__motionCorrection', action="store_true",
                   help="Boolean to perform motion correction in case of timeseries. Options: 1 = on, 0 = off.\nDEFAULT = 1")
    p.add_argument('--x__modules__asl__SpikeRemovalThreshold', type=float, default=0.01,
                   help="Minimal t-stat improval needed to remove motion spikes. Examples: 1 = effectively disabling spike removal.\nDEFAULT = 0.01")
    p.add_argument('--x__modules__asl__bRegistrationContrast', type=int, default=2,
                   help="Specifies the image contrast used for registration: 0 = Control->T1w, 1 = CBF->pseudoCBF from template/pGM+pWM (skip if sCoV>0.667), 2 = automatic (mix of both), 3 = option 2 & force CBF->pseudoCBF irrespective of sCoV.\nDEFAULT = 2")
    p.add_argument('--x__modules__asl__bAffineRegistration', type=int, default=0,
                   help="Specifies if the ASL-T1w rigid-body registration is followed up by an affine registration: 0 = affine registration disabled, 1 = affine registration enabled, 2 = affine registration automatically chosen based on spatial CoV of PWI.\nDEFAULT = 0")
    p.add_argument('--x__modules__asl__bDCTRegistration', type=int, default=0,
                   help="Specifies if to include the DCT registration on top of Affine, all other requirements for affine are thus also taken into account the x.modules.asl.bAffineRegistration must be >0 for DCT to run: 0 = DCT registration disabled 1 = DCT registration enabled if affine enabled and conditions for affine passed, 2 = DCT enabled as above, but use PVC on top of it to get the local intensity scaling right.\nDEFAULT = 0")
    p.add_argument('--x__modules__asl__bRegisterM02ASL', action="store_true",
                   help="Boolean specifying whether M0 is registered to mean_control image (or T1w if no control image exists). It can be useful to disable M0 registration if the ASL registration is done based on the M0, and little motion is expected between the M0 and ASL acquisition. If no separate M0 image is available, this parameter will have no effect. This option is disabled automatically for 3D spiral: 0 = M0 registration disabled, 1 = M0 registration enabled (DEFAULT).\nDEFAULT = 0")
    p.add_argument('--x__modules__asl__bUseMNIasDummyStructural', action="store_true",
                   help="When structural (e.g. T1w) data is missing, copy population-average MNI templates as dummy structural templates. With this option, the ASL module copies the structural templates to fool the pipeline, resulting in ASL registration to these templates. While the rigid-body parameters might still be found somewhat correctly, with this option it is advised to enable affine registration for ASL as well, since ASL and these dummy structural images will differ geometrically. When disabled, an error will be issued instead when the structural image are missing. 1 = enabled, 0 = disabled.\nDEFAULT = 0")
    p.add_argument('--x__modules__asl__bPVCNativeSpace', action="store_true",
                   help="Performs partial volume correction (PVC) in ASL native space using the GM and WM maps obtained from previously segmented T1-weighted images. Skipped with warning when those maps do not exist and are not resampled to the ASL space. PVC can take several minutes for larger scans (e.g. 128x128x30), so it is deactivated by default. 1 = enabled, 0 = disabled.\nDEFAULT = 0")
    p.add_argument('--x__modules__asl__PVCNativeSpaceKernel', type=str,
                   help="Kernel size for the ASL native space PVC. This is ignored when x.modules.asl.bPVCNativeSpace is set to 0. Equal weighting of all voxels within the kernel is assumed. 3D kernel can be used, but any of the dimension can be also set to 1. Only odd number of voxels can be used in each dimension (e.g. [3 7 5] not [2 3 1]).\nDEFAULT = [5 5 1] for bPVCGaussianMM==0, [10 10 4] for bPVCGaussianMM==1")
    p.add_argument('--x__modules__asl__bPVCGaussianMM', action="store_true",
                   help="If set to 1, PV-correction with a Gaussian weighting is used instead of the equal weights of all voxels in the kernel ('flat' kernel) as per Asllani's original method. Ignored when x.modules.asl.bPVCNativeSpace is set to 0. Unlike with the flat kernel when the size is defined in voxels, here the FWHM of the Gaussian in mm is defined in each dimension. The advantage is twofold - continuous values can be added and a single value can be entered which is valid for datasets with different voxel-sizes without having a kernel of different effective size.1 = enabled, use Gaussian kernel with FWHM in mm given in PVCNativeSpaceKernel, 0 = disabled, use 'flat' kernel with voxels given in PVCNativeSpaceKernel.\nDEFAULT = 0")
    p.add_argument('--x__modules__asl__bMakeNIfTI4DICOM', action="store_true",
                   help="Boolean to output CBF native space maps resampled and/or registered to the original T1w/ASL, and contrast adapted and in 12 bit range allowing to convert the NIfTI to a DICOM file, e.g. for implementation in PACS or other DICOM archives. If set to true, an additional CBF image will be created with modifications that allow it to be easily implemented back into a DICOM for e.g. PACS: 1. Remove peak & valley signal, remove NaNs, rescale to 12 bit integers, apply original orientation (2 copies saved, with original ASL and T1w orientation).")

    # Structural Processing Parameters
    p.add_argument('--x__modules__bRunLongReg', action="store_true",
                   help="Run longitudinal registration.\nDEFAULT = 0")
    p.add_argument('--x__modules__bRunDARTEL', action="store_true",
                   help="Run between-subject registration/create templates.\nDEFAULT = 0")
    p.add_argument('--x__modules__structural__bSegmentSPM12', action="store_true",
                   help="Boolean to specify if SPM12 segmentation is run instead of CAT12. Options: 1 = run SPM12, 0 = run CAT12.\nDEFAULT = 0")
    p.add_argument('--x__modules__structural__bHammersCAT12', action="store_true",
                   help="Boolean specifying if CAT12 should provide Hammers volumetric ROI results.\nDEFAULT = 0")
    p.add_argument('--x__modules__structural__bFixResolution', action="store_true",
                   help="Resample to a resolution that CAT12 accepts.\nDEFAULT = 0")

    # General processing parameters
    p.add_argument('--x__settings__Quality', action="store_true",
                   help="Boolean specifying on which quality the pipeline should be run, options: 1 = normal quality, 0 = lower quality, fewer iterations and lower resolution of processing for a fast try-out.\nDEFAULT = 1")
    p.add_argument('--x__settings__DELETETEMP', action="store_true",
                   help="Boolean for removing the temporary files. Options: 0 = keeping all files, 1 = delete temporary files created by the pipeline.\nDEFAULT = 1")
    p.add_argument('--x__settings__SkipIfNoFlair', action="store_true",
                   help="Boolean to skip processing of subjects that do not have a FLAIR image. These parameters can be useful when some data is still complete, but one would like to start image processing already. Options: 1 = skip processing of a subject that does not have a FLAIR image 0 = do not skip anything.\nDEFAULT = 0")
    p.add_argument('--x__settings__SkipIfNoASL', action="store_true",
                   help="Boolean to skip processing of subjects that do not have a ASL image. Options: 1 = skip processing of a subject that does not have a ASL image, 0 = do not skip anything.\nDefault = 0")
    p.add_argument('--x__settings__SkipIfNoM0', action="store_true",
                   help="Boolean to skip processing of subjects that do not have a M0 image. Options: 1 = skip processing of a subject that does not have a M0 image, 0 = do not skip anything.\nDEFAULT = 0")
    p.add_argument('--x__settings__stopAfterErrors', type=float,
                   help="Number of allowed errors before job iteration is stopped\nDEFAULT = inf")
    p.add_argument('--x__settings__bLesionFilling', action="store_true",
                   help="Boolean for lesion filling in structural module (submodule 5).\nDEFAULT = true")
    p.add_argument('--x__settings__bAutoACPC', action="store_true",
                   help="Boolean whether center of mass alignment should be performed before SPM registration.\nDEFAULT = true")

    # Masking & Atlas Parameters
    p.add_argument('--x__S__bMasking', type=str,
                   help="Vector specifying if we should mask a ROI with a subject-specific mask (1 = yes, 0 = no): [1 0 0 0] = susceptibility mask (either population-or subject-wise), [0 1 0 0] = vascular mask (only subject-wise), [0 0 1 0] = subject-specific tissue-masking (e.g. pGM>0.5), [0 0 0 1] = WholeBrain masking (used as memory compression) [0 0 0 0] = no masking at all, [1 1 1 1] = apply all masks, Can also be used as boolean, where 1 = [1 1 1 1], 0 = [0 0 0 0]. Can be useful for e.g. loading lesion masks outside the GM.\nDEFAULT = 1")
    p.add_argument('--x__S__Atlases', type=str,
                   help="Vector specifying the atlases which should be used within the population module. Default definition within the Population Module: x.S.Atlases = {'TotalGM','DeepWM'}. Available atlases: Free atlases: TotalGM: Mask of the entire GM, TotalWM: Mask of the entire WM, DeepWM: Mask of the deep WM, WholeBrain: Mask of the entire brain, MNI_Structural: MNI cortical atlas, Tatu_ACA_MCA_PCA: Original vascular territories by Tatu et al.', Tatu_ICA_PCA: Tatu - only ICA and PCA, Tatu_ICA_L_ICA_R_PCA, Tatu_ACA_MCA_PCA_Prox_Med_Dist: Tatu separated to distal/medial/proximal of ACA/MCA/PCA, Mindboggle_OASIS_DKT31_CMA: Mindboggle-101 cortical atlas. Free for non-commercial use only: HOcort_CONN: Harvard-Oxford cortical atlas, HOsub_CONN: Harvard-Oxford subcortical atlas, Hammers: Alexander Hammers's brain atlas, HammersCAT12: Hammers atlas adapted to DARTEL template of IXI550 space, Thalamus: Harvad-Oxford thalamus atlas.\nDEFAULT={'TotalGM','DeepWM'}")

    # Parse config file paramaters into params object
    params, rest = p.parse_known_args(rest)

    ###########################
    # Non-xASL: Flag for creating a boutiques descriptor from python argparser
    p.add_argument('--create_descriptor', action='store_true',
                   help="For development: Create a boutiques descriptor")

    dev_args = p.parse_args(rest)

    if dev_args.create_descriptor:
        import boutiques.creator as bc
        newDescriptor = bc.CreateDescriptor(p, execname="blah")
        newDescriptor.save("xASL_generated_descriptor.json")
        quit()

    # Return arg objects

    return args, params

    ########################################################################################


def split_list_arg(args):
    for arg in args:
        if type(arg) == str and "," in arg:
            arg = arg.split(",")
            print(arg)


################### Testing ##############################
if __name__ == "__main__":

    import sys
    args, params = parse_arguments(sys.argv[1:])

    from to_json import parse_list_to_dict
    import json

    json_object = parse_list_to_dict(vars(params))

    print(json_object)
    with open('test-config.json', 'w') as f:
        json_object = json.dumps(json_object, indent=4)
        f.write(json_object)
