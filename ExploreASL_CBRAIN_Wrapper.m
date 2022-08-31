function ExploreASL_CBRAIN_Wrapper(varargin)

%% Arg parser
p = inputParser;

addParameter(p, 'DatasetRoot', '');
% Import module array
%addParameter(p, 'ImportModules', [0,0,0,1]);
addParameter(p, 'ImportModules_DCM2NII', 0);
addParameter(p, 'ImportModules_NII2BIDS', 0);
addParameter(p, 'ImportModules_DEFACE', 0);
addParameter(p, 'ImportModules_BIDS2LEGACY', 0);
% Process Module array
%addParameter(p, 'ProcessModules', [1,1,0]);
addParameter(p, 'ProcessModules_STRUCTURAL', 0);
addParameter(p, 'ProcessModules_ASL', 0);
addParameter(p, 'ProcessModules_POPULATION', 0);

% These parameters not needed
%addParameter(p, 'bImportData', 1);
%ddParameter(p, 'bProcessData', 1);
%addParameter(p, 'bLoadData', 1);

%% 
%{
addParameter(p, 'studyID', 'test');
addParameter(p, 'visitNames', {});
addParameter(p, 'sessionNames', {});
addParameter(p, 'folderHierarchy',{'^(.)+$';'^(asl|T1w|m0scan)$'} );
addParameter(p, 'tokenOrdering', [1, 0, 2]);
addParameter(p, 'tokenScanAliases', {'^asl$' ,'ASL4D' ; '^T1w$' ,'T1w'; '^m0scan$'  ,'M0' });


addParameter(p, 'SESSIONS', 'ASL_1');

%}

%% Dataset Parameters
% Dataset Parameters
% x.[...]
% x.D.ROOT
%addParameter(p, 'D__ROOT', 'pwd');
%addParameter(p, 'SESSIONS', 'ASL_1');
% x.sessions.options
%addParameter(p, 'session__options', '');


%## DATASET PARAMETERS
% x.datastet.[...]
addParameter(p, 'name', 'study_name');
addParameter(p, 'subjectRegexp' , "^\d{3}$") ; 
% addParameter(p, 'exclusion', '');
% addParameter(p, 'ForceInclusionList' ,1);


%## M0 PARAMETERS and OPTIONS
% x.modules.asl.[...]
addParameter(p,'M0_conventionalProcessing' ,0);
addParameter(p,'M0_GMScaleFactor' ,1);
% Vector arguments:
addParameter(p,'M0PositionInASL4D' ,'');
addParameter(p,'DummyScanPositionInASL4D' ,'');


%## SEQUENCE PARAMETERS (all are inputs)
% x.Q.[...]
addParameter(p,'M0' ,'separate_scan');
addParameter(p,'BackgroundSuppressionNumberPulses' ,0);
addParameter(p,'BackgroundSuppressionPulseTime' ,'');
addParameter(p,'PresaturationTime' ,'');
addParameter(p,'readoutDim' ,'3D');
addParameter(p,'Vendor' ,'Siemens');
addParameter(p,'Sequence' ,'2D_EPI');
addParameter(p,'LabelingType' ,'CASL');
addParameter(p,'Initial_PLD' ,1500);
addParameter(p,'LabelingDuration' ,1500);
addParameter(p,'SliceReadoutTime' ,'shortestTR');



%## QUANTIFICATION PARAMETERS
% x.Q.[...]
addParameter(p,'bUseBasilQuantification' ,0);
addParameter(p,'Lambda' ,0.9);
addParameter(p,'T2art' ,50);
addParameter(p,'BloodT1' ,1650);
addParameter(p,'TissueT1' ,1240);
addParameter(p,'nCompartments' ,1);
addParameter(p,'ApplyQuantification' ,'1 1 1 1 1');
addParameter(p,'SaveCBF4D' ,0);


%## GENERAL PROCESSING PARAMETERS
% x.setting.[...]
addParameter(p,'Quality' ,1);
addParameter(p,'DELETETEMP' ,1);
addParameter(p,'SkipIfNoFlair' ,0);
addParameter(p,'SkipIfNoASL' ,0);
addParameter(p,'SkipIfNoM0' ,0);



%## STRUCTURAL PROCESSING PARAMETERS
% x.modules.[...]
addParameter(p,'bRunLongReg' ,0);
addParameter(p,'bRunDARTEL' ,0);
addParameter(p,'structural__bSegmentSPM12' ,0);
addParameter(p,'structural__bHammersCAT12' ,0);
addParameter(p,'structural__bFixResolution' ,0);


%## ASL PROCESSING PARAMETERS
% x.modules.asl.[...]
addParameter(p,'motionCorrection' ,1);
addParameter(p,'SpikeRemovalThreshold' ,0.01);
addParameter(p,'bRegistrationContrast' ,2);
addParameter(p,'bAffineRegistration' ,0);
addParameter(p,'bDCTRegistration' ,0);
addParameter(p,'bRegisterM02ASL' ,0);
addParameter(p,'bUseMNIasDummyStructural' ,0);
addParameter(p,'bPVCNativeSpace' ,0);
addParameter(p,'PVCNativeSpaceKernel' ,'');
addParameter(p,'bPVCGaussianMM' ,0);
addParameter(p,'bMakeNIfTI4DICOM' ,1);



%## MASKING & ATLAS PARAMETERS
% x.S.[...]
addParameter(p,'bMasking' ,'1 1 1 1');
%addParameter(p,'Atlases' ,{'TotalGM','DeepWM'});
%addParameter(p,'SetsName' ,{'session'  'LongitudinalTimePoint'  'SubjectNList'  'Site'});
%addParameter(p,'SetsOptions' ,{'ASL_1'   'TimePoint_1'  'SubjectNList'  'SingleSite'});
%addParameter(p,'SetsID' ,'1 1 1 1');
%addParameter(p,'Sets1_2Sample' ,'1 1 1 2';
%addParameter(p,'iSetLong_TP' ,2);
%addParameter(p,'iSetSite' ,4);


% Parse args
parse(p, varargin{:});

DatasetRoot = p.Results.DatasetRoot;

% Assign variables to struct
% study parameters
% x.[...]
x.D.ROOT = DatasetRoot;
%x.SESSIONS = p.Results.SESSIONS;
%x.sessions.options = p.Results.session__options;

% dataset parameters
% x.dataset.[...]
x.dataset.name = p.Results.name;
x.dataset.subjectRegexp = p.Results.subjectRegexp;

% M0 parameters
% x.modules.asl.[...]
x.modules.asl.M0_conventionalProcessing = p.Results.M0_conventionalProcessing;
x.modules.asl.M0_GMScaleFactor = p.Results.M0_GMScaleFactor;

M0PositionInASL4D = parse_vector_arg(p.Results.M0PositionInASL4D, [0, 1, 2]);
x.modules.asl.M0PositionInASL4D = M0PositionInASL4D;

DummyScanPositionInASL4D = parse_vector_arg(p.Results.DummyScanPositionInASL4D, [0, 1, 2]);
x.modules.asl.DummyScanPositionInASL4D = DummyScanPositionInASL4D;

% Sequence parameters
% x.Q.[...]
x.Q.M0 = p.Results.M0;
x.Q.BackgroundSuppressionNumberPulses = p.Results.BackgroundSuppressionNumberPulses;

BackgroundSuppressionPulseTime = parse_vector_arg(p.Results.BackgroundSuppressionPulseTime, [0:10]);
x.Q.BackgroundSuppressionPulseTime = BackgroundSuppressionPulseTime;
x.Q.PresaturationTime = p.Results.PresaturationTime;
x.Q.readoutDim = p.Results.readoutDim;
x.Q.Vendor = p.Results.Vendor;
x.Q.Sequence = p.Results.Sequence;
x.Q.LabelingType = p.Results.LabelingType;
x.Q.Initial_PLD = p.Results.Initial_PLD;
x.Q.LabelingDuration = p.Results.LabelingDuration;
x.Q.SliceReadoutTime = p.Results.SliceReadoutTime;

% Quantification parameters
% x.Q.[...]
x.Q.bUseBasilQuantification = p.Results.bUseBasilQuantification;
x.Q.Lambda = p.Results.Lambda;
x.Q.T2art = p.Results.T2art;
x.Q.BloodT1 = p.Results.BloodT1;
x.Q.TissueT1 = p.Results.TissueT1;
x.Q.nCompartments = p.Results.nCompartments;

ApplyQuantification = parse_vector_arg(p.Results.ApplyQuantification, [5]);
x.Q.ApplyQuantification = ApplyQuantification;
x.Q.SaveCBF4D = p.Results.SaveCBF4D;

% General processing parameters;
% x.settings.[...]
x.settings.Quality = p.Results.Quality;
x.settings.DELETETEMP = p.Results.DELETETEMP;
x.settings.SkipIfNoFlair = p.Results.SkipIfNoFlair;
x.settings.SkipIfNoASL = p.Results.SkipIfNoASL;
x.settings.SkipIfNoM0 = p.Results.SkipIfNoM0;

% Structural processing parameters
% x.modules.[...]
x.modules.bRunLongReg = p.Results.bRunLongReg;
x.modules.bRunDARTEL = p.Results.bRunDARTEL;
x.modules.structural.bSegmentSPM12 = p.Results.structural__bSegmentSPM12;
x.modules.structural.bHammersCAT12 = p.Results.structural__bHammersCAT12;
x.modules.structural.bFixResolution = p.Results.structural__bFixResolution;


% ASL Processing Parameters
% x.modules.asl.[...]
x.modules.asl.motionCorrection = p.Results.motionCorrection;
x.modules.asl.SpikeRemovalThreshold = p.Results.SpikeRemovalThreshold;
x.modules.asl.bRegistrationContrast = p.Results.bRegistrationContrast;
x.modules.asl.bAffineRegistration = p.Results.bAffineRegistration;
x.modules.asl.bDCTRegistration = p.Results.bDCTRegistration;
x.modules.asl.bRegisterM02ASL = p.Results.bRegisterM02ASL;
x.modules.asl.bUseMNIasDummyStructural = p.Results.bUseMNIasDummyStructural;
x.modules.asl.bPVCNativeSpace = p.Results.bPVCNativeSpace;
x.modules.asl.PVCNativeSpaceKernel = p.Results.PVCNativeSpaceKernel;
x.modules.asl.bPVCGaussianMM = p.Results.bPVCGaussianMM;
x.modules.asl.bMakeNIfTI4DICOM = p.Results.bMakeNIfTI4DICOM;

% masking and atlas parameters
% x.S.[...]
bMasking = parse_vector_arg(p.Results.bMasking, [1, 4]);
x.S.bMasking = bMasking;
%x.S.Atlases = p.Results.Atlases;

% Write to JSON file

json_txt = jsonencode(x);


if (~isfolder(DatasetRoot))
    mkdir(DatasetRoot);
end


json_filename = fullfile(DatasetRoot, 'studyPar.json');

fid = fopen(json_filename, 'w');
fprintf(fid, '%s', json_txt);
fclose(fid);




% Make main input array

ImportModules = [p.Results.ImportModules_DCM2NII, p.Results.ImportModules_NII2BIDS, ...
    p.Results.ImportModules_DEFACE, p.Results.ImportModules_BIDS2LEGACY];

ProcessModules = [p.Results.ProcessModules_STRUCTURAL, p.Results.ProcessModules_ASL, ...
    p.Results.ProcessModules_POPULATION];



% Call main exploreASL function
ExploreASL_Master('DatasetRoot', DatasetRoot, 'ImportModules', ImportModules, 'ProcessModules', ProcessModules); 



end


function [arr] = parse_vector_arg(arg, numel)
    % arg is input vector as a string
    % numel is an array of valid numbers of elements

    arr = split(arg);
    % Check length
    if (~ismember(length(arr), numel))
        msg = "Error: Vector argument is not the right length.";
        error(msg);
    end
    
    %arr = str2double(arr);
   
end





