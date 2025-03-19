#!/bin/bash

# Check if a folder name is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <crab_folder_name>"
    exit 1
fi

# Assign the folder name from the argument
CRAB_FOLDER=$1

# Run the crab report command
crab report $CRAB_FOLDER

# Change to the results directory
#RESULTS_DIR="/afs/cern.ch/user/t/tmenezes/work/private/CRAB_MonopoleData/CMSSW_10_6_26/src/production/crab3/utilities/$CRAB_FOLDER/results"
#RESULTS_DIR="/afs/cern.ch/work/t/tmenezes/private/CRAB_MonopoleData/CMSSW_10_6_26/src/$CRAB_FOLDER/results"
RESULTS_DIR="/afs/cern.ch/work/t/tmenezes/private/CMSSW_10_6_20/src/$CRAB_FOLDER/results"
cd $RESULTS_DIR

# Set the PATH environment variable
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda3/bin:$PATH

# Run the brilcalc command
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i processedLumis.json
#brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i notFinishedLumis.json
