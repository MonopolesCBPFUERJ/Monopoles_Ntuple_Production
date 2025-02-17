#!/usr/bin/env sh
#el7-cmssw
remoteFile=$1
processNum=$2
outputFile=/eos/user/t/tmenezes/Monopole_Ntuples/Central_Production/Uncleaned_test/NewUncleanRematch_MonoNtuple2018_MC_2000_${processNum}.root 
#outputFile=/eos/user/t/tmenezes/Monopole_Ntuples/Data/MET/2016/2016RunB/2016RunB_${processNum}.root
currentPath=$PWD
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/cern.ch/user/t/tmenezes/work/public/CMSSW_10_6_23/src && eval $(scram runtime -sh)
cd $currentPath
cmsRun /afs/cern.ch/user/t/tmenezes/work/public/CMSSW_10_6_23/src/ntuple_mc_2018_cfg.py inputFiles=${remoteFile} outputFile=${outputFile}
