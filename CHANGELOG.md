# Changelog

## Version 1.2.0 (TBD/02/2023)

Created new tool ExploreASL-BIDS, which takes only BIDS subjects as input. DICOM functionality is now deprecated.
This was to reduce the number of input parameters to something manageable, and to avoid the complexity of the DICOM import module.
Users should convert their DICOM data to BIDS format offline and upload this to CBRAIN for processing.

General changes:
- Renamed xasl\_wrapper.py to run\_xasl.py
- List type inputs are now lists in Boutiques
- Boolean type inputs are now flags in Boutiques (except module inclusion parameters)
- Amount of general input arguments greatly reduced

BIDS version:
- Uses BoutiquesBidsSingleSubjectMaker module in Boutiques to standardize input to BIDS Dataset
- Does not support population/BIDS datset processing yet!



## Version 1.1.2 (17/10/2022)

- Fixed issue #1 on BIDS single subject input
