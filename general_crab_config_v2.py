import subprocess
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from CRABClient.UserUtilities import config
from httplib import HTTPException
import datetime


# --- User options: list of (input_dir, output_dir) pairs ---
input_output_pairs = [
    (
        "/store/user/srimanob/monopole/13TeV/Legacy-RECO-MonopoleSimHits-v2/2018-2500-SpinHalf-NoPU",
        "/store/user/tmenezes/MM_MC_2018_G4SimHits/2500_SpinHalf_NoPU/"
    ),
    (
        "/store/user/srimanob/monopole/13TeV/Legacy-RECO-MonopoleSimHits-v2/2018-4000-SpinHalf-NoPU",
        "/store/user/tmenezes/MM_MC_2018_G4SimHits/4000_SpinHalf_NoPU/"
    )
]

pset = "ntuple_MC2018ul_runPAT.py"


# --- Retrieve EOS ROOT files ---
def get_eos_root_files(eos_path):
    cmd = ["xrdfs", "root://eoscms.cern.ch", "ls", eos_path]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise RuntimeError("Failed to list EOS directory {0}: {1}".format(eos_path, err))
        eos_listing = out.splitlines()
    except Exception as e:
        raise RuntimeError("Error retrieving EOS listing: {0}".format(e))

    root_files = [
        "root://eoscms.cern.ch/{0}".format(line) for line in eos_listing if line.endswith(".root")
    ]
    if not root_files:
        raise RuntimeError("No ROOT files found in {0}".format(eos_path))
    return root_files


# --- Prepare CRAB Config ---
def create_crab_config(files, output_dir, tag):
    crab_cfg = config()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    crab_cfg.General.requestName = '{0}_{1}'.format(tag, timestamp)
    crab_cfg.General.workArea = 'crab_{0}'.format(tag)
    crab_cfg.General.transferOutputs = True
    crab_cfg.General.transferLogs = True

    crab_cfg.JobType.pluginName = 'Analysis'
    crab_cfg.JobType.psetName = pset
    crab_cfg.JobType.outputFiles = ['output.root']
    crab_cfg.JobType.allowUndistributedCMSSW = True

    crab_cfg.Data.userInputFiles = files
    crab_cfg.Data.splitting = 'FileBased'
    crab_cfg.Data.unitsPerJob = 1
    crab_cfg.Data.publication = False
    crab_cfg.Data.outputDatasetTag = tag
    crab_cfg.Data.outLFNDirBase = output_dir

    crab_cfg.Site.storageSite = 'T3_CH_CERNBOX'

    return crab_cfg


# --- Submit CRAB Job ---
def submit_crab_config(crab_cfg):
    try:
        crabCommand("submit", config=crab_cfg)
    except HTTPException as hte:
        print "HTTPException during submission: {0}".format(hte)
    except ClientException as cle:
        print "ClientException during submission: {0}".format(cle)


# --- Main execution ---
if __name__ == "__main__":
    for eos_dir, output_dir in input_output_pairs:
        print "\nRetrieving ROOT files from: {0}".format(eos_dir)
        files = get_eos_root_files(eos_dir)
        print "Found {0} ROOT files.".format(len(files))

        # Create a unique tag from the EOS directory name for bookkeeping
        tag_suffix = eos_dir.rstrip("/").split("/")[-1]
        tag = "monopole_UL18_{0}".format(tag_suffix)

        print "Submitting CRAB job with tag: {0} to output directory: {1}".format(tag, output_dir)
        crab_cfg = create_crab_config(files, output_dir, tag)
        submit_crab_config(crab_cfg)

