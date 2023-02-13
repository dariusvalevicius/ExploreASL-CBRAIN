# Changelog

## Version 1.2.0 (TBD/02/2023)

Split into two versions: ExploreASL-DICOM and ExploreASL-BIDS. (explore-asl_master.json is a non-functioning parent of the two).

General changes:
- Renamed xasl\_wrapper.py to run\_xasl.py
- List type inputs are now lists in Boutiques
- Boolean type inputs are now flags in Boutiques (except module inclusion parameters)
- Amount of general input arguments greatly reduced

DICOM version:
- Takes SourceStructure arguments

BIDS version:
- Uses BoutiquesBidsSingleSubjectMaker module in Boutiques to standardize input to BIDS Dataset



## Version 1.1.2 (17/10/2022)

- Fixed issue #1 on BIDS single subject input
