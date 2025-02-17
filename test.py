import os
import sys
import argparse

# List of datasets generated with the command below (example for MuonEG). 
# dasgoclient --limit 0 --query 'dataset dataset=/MuonEG/*UL2016_MiniAODv1_NanoAODv2*/NANOAOD'

#======SETUP=======================================================================================
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version")
args = parser.parse_args()

if args.version != "A" and args.version != "B":
    print("Please, enter a valid version: A or B")
    sys.exit()

if args.version == "A":
    version = "A"
    tag = "v1"
elif args.version == "B":
    version = "B"
    tag = "v1"


campaign = "PromptReco-"+tag

basedir = "data_24/Run2024"+version+"/"
if os.path.isdir(basedir) is False:
    os.makedirs(basedir)

datasets = [
["Run2024A",         "/Muon0/Run2024A-" + campaign],
["Run2024B",         "/Muon0/Run2024B-" + campaign],
["Run2024C",         "/Muon0/Run2024C-" + campaign],
["Run2024D",         "/Muon0/Run2024D-" + campaign],
]

#/Muon0/Run2024B-PromptReco-v1/NANOAOD

for i in range(len(datasets)):
    file_name = basedir + datasets[i][0] + ".txt"
    for k in range(1):
       #print(datasets)
        ds_name = datasets[i][1] + "/NANOAOD"
        print(ds_name)
        if k == 0:
            command = "dasgoclient --limit 0 --query 'dataset dataset=" + ds_name + "' > " + "temp.txt"
        else:
            command = "dasgoclient --limit 0 --query 'dataset dataset=" + ds_name + "' >> " + "temp.txt"
        os.system(command)
    has_dataset = False
    k_lines = []
    with open("temp.txt", "r") as file:
        for line in file:
            pass
            has_dataset = True
            k_lines.append(line[0:-1])
    if has_dataset:
        for dataset_name in reversed(k_lines):
            command = "dasgoclient --limit 0 --query 'file dataset=" + dataset_name + "' > " + file_name
            os.system(command)
            NumLines = sum(1 for line in open(file_name))
            if NumLines > 0:
                print(dataset_name)
                break
    else:
        open(file_name, 'a').close()
        print(datasets[i][1] + " is not available!")
    os.system("rm temp.txt")
