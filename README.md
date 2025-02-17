# Monopole-Script
These files are in lxplus.  
CMS release version : CMSSW_10_6_23   
Set up enviroment before running the script  
```
cmsrel CMSSW_10_6_23  
cd CMSSW_10_6_23/src  
git clone git@github.com:sun51027/Monopole-Script.git  
mv Monopole-Script/* . 
rm -rf SimGeneral 
scram b -j 4
``` 
Note: If you just want to generate Ntuple rather than study systematic uncertainty, you have to remove "SimGeneral". If you want to study systematic uncertainty, please see Systematic Uncertainty part.
## Monopole Analysis
**To generate ntuple locally:**  
 `scarm b `  
 `cmsRun ntuple_mc_YEAR_cfg.py inputFiles=file:input.root maxEvents=-1 outputFile=output.root `  

Note: I recommend not to do this first, since all files in this repository were defaulted to be used for "Condor", see below topic. If you just want to run one file for test, you have to cancel the comments in these lines:
```c
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)
Output = cms.string(options.outputFile)
```
**To submit jobs onto Condor:**  

Please try to understand how submit.sh and tmpSUB.SUB work with relation to ntuple_mc_YEAR_cfg.py (the default year is 2018, mass 1000GeV), and change your own AFS (real)path in the *submit.sh* and *tmpSUB.SUB* before you submit jobs. For example,  

/afs/cern.ch/user/l/lshih/CMSSW_10_6_23/src -> /afs/cern.ch/user/m/maisway/CMSSW_10_6_23/src  
(There are 8 address need to be changed in these two codes)

You also have to create new folder for condor Output, Error, Log messages from condor job.
```
mkdir condor
cd condor
mkdir output errors stdout
cd -
```
 
Load the RECO files in Phat's eos space(current path):  
/eos/cms/store/user/srimanob/monopole/13TeV/Legacy-RECO-v2/  
Note:Skip this step when you run this script first time, since "remoteFileList.txt" in this package has 2018 1000GeV RECO files by default.  
`realpath /eos/cms/store/user/srimanob/monopole/13TeV/Legacy-RECO-v2/YEAR-MASS/* >> remoteFileList.txt`

Add "file:" in front of all lines (*see remoteFileList.txt for example*)  
Note that there are some DeltaRayOff sample in 2018-1000,2000,3000,4000 and 2016-1000,2000. Please remote DeltaRayOff samples in remoteFileList.txt before you submit jobs.

Submit jobs:

`condor_submit tmpSUB.SUB`  

Check the status of your jobs:

`condor_q`  

## Systematic Uncertainty

Load particular packages from CMSSW_RELEASE_BASE and compile:

`cp $CMSSW_RELEASE_BASE/src/{RecoParticleFlow,Configuration,SimGeneral} ~/CMSSW_10_6_23/src`

`scram b -j 4`

As long as structure in your workspace  is the same as the CMSSW_BASE, it will run the your local files first when `cmsRun`.
Note that I have modified SiStripSimParameters_cfi.py in SimGeneral, you can just copy my SiStripSimParameters_cfi.py to use. 
The usage see below:

**To modify the Dedx crosstalk effect with 10% (for X0 or X1 or X2):**

`vim SimGeneral/MixingModule/python/SiStripSimParameters_cfi.py`

We only choose to change X0 up and down with 10% for systematic study, so you only need to comment the default numbers and open the X0(up or down).


**To switch OFF the spike algorithm (for Ecal sysematic uncertainty):**

`vim RecoParticleFlow/PFClusterProducer/python/particleFlowRecHitECAL_cfi.py`

switch True to False for these lines:
      timingCleaning = cms.bool(True),
      topologicalCleaning = cms.bool(True),


Useful condor tutorial:  
https://batchdocs.web.cern.ch/local/quick.html  

## Run on Data

Just to test if cmsRun can be successful in local.

Download  ntuple_mc_2018_forData_cfg.py and latest MonoNtupleDumper.cc first.

```
scram b -j 4 
xrdcp root://cmsxrootd.fnal.gov//store/data/Run2018A/EGamma/USER/EXOMONOPOLE-12Nov2019_UL2018-v2/270007/7F10EF9D-BDF9-074B-8216-834602DE11C3.root .
cmsRun ntuple_mc_2018_forData_cfg.py inputFiles=file:7F10EF9D-BDF9-074B-8216-834602DE11C3.root
````
Still finding the problem with CRAB....
