import os
import sys
import argparse


#dasgoclient --limit 0 --query 'dataset dataset=/Muon0/Run2024*/NANOAOD'
#/afs/cern.ch/user/t/tmenezes/work/private/Monopole_Ntuples_fromsun51027/merges

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version")
args = parser.parse_args()

tag = ""


#dasgoclient --query 'dataset dataset=/Muon0/Run2024*/NANOAOD'

if args.version != "A" and args.version != "B" and args.version != "C" and args.version != "D":
    print("Please, enter a valid version: A, B, C or D")   
    sys.exit()


if args.version == "A":
    version = "A"
elif args.version == "B":
    version = "B"
elif args.version == "C":
    version = "C"
elif args.version == "D":
    version = "D"

campaign = "PromptReco-v1"

datasets = [
["Muon0",   "/Muon0/Run2024"+version+"-" + campaign],

] 

# =/Muon0/Run2024*/NANOAOD'

basedir = "data24/Run2024"+version+"/"
#mkdir -p basedir

if not os.path.exists(basedir):
    os.makedirs(basedir)

for i in range(len(datasets)):
    file_name = basedir + datasets[i][0] + ".txt"
    for k in range(9):
        ds_name = datasets[i][1] + "-v" + str(k+1) + "/NANOAOD"
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