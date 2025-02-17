#!/bin/bash

# Arquivos de saída para cada ano
output_2018="missing_files_list_2018.txt"
output_2017="missing_files_list_2017.txt"
output_2016="missing_files_list_2016.txt"
output_2016_apv="missing_files_list_2016_apv.txt"

# Limpa os arquivos de saída existentes
> $output_2018
> $output_2017
> $output_2016
> $output_2016_apv

# Lista de datasets para 2017

datasets_2018=(
    # SPIN ZERO PHOTON FUSION #
    "/Monopole_SpinZero_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
)

datasets_2017=(
    # SPIN ZERO PHOTON FUSION #
    "/Monopole_SpinZero_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
)

# Lista de datasets para 2016
datasets_2016=(
    # SPIN ZERO PHOTON FUSION #
    "/Monopole_SpinZero_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    "/Monopole_SpinZero_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    "/Monopole_SpinZero_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
)

# Função para buscar arquivos e salvar no arquivo apropriado
get_files() {
    local dataset=$1
    local output_file=$2
    echo "Fetching files for dataset: $dataset"
    dasgoclient --query="file dataset=$dataset" --limit=0 >> $output_file
}

# Buscar arquivos para datasets de 2017
for dataset in "${datasets_2017[@]}"; do
    get_files $dataset $output_2017
done

for dataset in "${datasets_2018[@]}"; do
    get_files $dataset $output_2018
done

# Buscar arquivos para datasets de 2016
for dataset in "${datasets_2016[@]}"; do
    if [[ $dataset == *"APV"* ]]; then
        get_files $dataset $output_2016_apv
    else
        get_files $dataset $output_2016
    fi
done

echo "File fetching complete."
