# -*- coding: utf-8 -*-

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from CRABClient.UserUtilities import config
from http.client import HTTPException
from WMCore.Configuration import Configuration
import datetime
import re

# Defina o ano e o tipo de dados aqui
year = '2016APV'            # Defina o ano aqui
data_type = 'DATA'       # Use 'DATA' para dados reais ou 'MC' para Monte Carlo

config = config()

config.section_("General")
config.General.workArea = '17Feb_METReview_crab_EXOMONOPOLE_{data_type}_{year}/{era}'.format(data_type=data_type, year=year, era='{era}')
config.General.transferOutputs = True
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'

# Ajuste o psetName conforme necessário para DATA ou MC
if data_type == 'DATA':
    config.JobType.psetName = 'ntuple_mc_2018_forData_14Feb_cfg.py'
elif data_type == 'MC':
    if year == '2016':
        config.JobType.psetName = 'ntuple_mc_2016_cfg_METFilter.py'
    elif year == '2016APV':
        config.JobType.psetName = 'ntuple_mc_2016APV_cfg_METFilter.py'
    elif year == '2017':
        config.JobType.psetName = 'ntuple_mc_2017_cfg_METFilter.py'
    elif year == '2018':
        config.JobType.psetName = 'ntuple_mc_2018_cfg_METFilter.py'
    else:
        raise ValueError("Ano inválido. Escolha '2016', '2016APV', '2017' ou '2018'.")
else:
    raise ValueError("Tipo de dados inválido. Escolha 'DATA' ou 'MC'.")


config.JobType.outputFiles = ['output.root']
config.JobType.allowUndistributedCMSSW = True
#config.JobType.maxMemoryMB = 2500
#config.JobType.maxJobRuntimeMin = 540

config.section_("Data")
config.Data.inputDBS = 'global'

# Ajuste o método de splitting e unidades por trabalho com base no tipo de dados
if data_type == 'DATA':
    config.Data.splitting = 'LumiBased'
    config.Data.unitsPerJob = 13
elif data_type == 'MC':
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 1
    #config.Data.totalUnits = 1000  # Descomente para limitar o número de arquivos processados
else:
    raise ValueError("Tipo de dados inválido. Escolha 'DATA' ou 'MC'.")

config.Data.publication = True

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'

# Lista de datasets para DATA e MC

datasets_2016_MONO = [
    #'/SinglePhoton/Run2016F-EXOMONOPOLE-21Feb2020_UL2016-v1/USER',
    #'/SinglePhoton/Run2016G-EXOMONOPOLE-21Feb2020_UL2016-v1/USER',
    #'/SinglePhoton/Run2016H-EXOMONOPOLE-21Feb2020_UL2016-v1/USER',
    '/MET/Run2016F-EXOMONOPOLE-21Feb2020_UL2016-v1/USER',
    '/MET/Run2016F-EXOMONOPOLE-21Feb2020_UL2016-v1/USER',
    '/MET/Run2016F-EXOMONOPOLE-21Feb2020_UL2016-v1/USER'
]

datasets_MC_2016 = [
    # SPIN HALF PHOTON FUSION #
    "/Monopole_SpinHalf_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    # SPIN HALF DRELL YAN #
    ,"/Monopole_SpinHalf_DrellYan_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    # SPIN ZERO PHOTON FUSION #
    ,"/Monopole_SpinZero_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v3/GEN-SIM-RECO"
    # SPIN ZERO DRELL YAN #
    ,"/Monopole_SpinZero_DrellYan_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v2/GEN-SIM-RECO"

]


datasets_2016_apv_MONO = [
    #'/SinglePhoton/Run2016B-EXOMONOPOLE-21Feb2020_ver2_UL2016_HIPM-v1/USER',
    #'/SinglePhoton/Run2016B-EXOMONOPOLE-21Feb2020_ver1_UL2016_HIPM-v1/USER',
    #'/SinglePhoton/Run2016C-EXOMONOPOLE-21Feb2020_UL2016_HIPM-v1/USER',
    #'/SinglePhoton/Run2016D-EXOMONOPOLE-21Feb2020_UL2016_HIPM-v1/USER',
    #'/SinglePhoton/Run2016E-EXOMONOPOLE-21Feb2020_UL2016_HIPM-v1/USER',
    #'/SinglePhoton/Run2016F-EXOMONOPOLE-21Feb2020_UL2016_HIPM-v1/USER',
    #'/MET/Run2016B-EXOMONOPOLE-21Feb2020_ver2_UL201_HIPM-v1/USER',
    '/MET/Run2016C-EXOMONOPOLE-21Feb2020_UL2016_HIPM-v1/USER',
    #'/MET/Run2016D-EXOMONOPOLE-21Feb2020_UL2016_HIPM-v1/USER',
    #'/MET/Run2016E-EXOMONOPOLE-21Feb2020_UL2016_HIPM-v1/USER',
    #'/MET/Run2016F-EXOMONOPOLE-21Feb2020_UL2016_HIPM-v1/USER'
]

datasets_MC_2016APV = [
    # SPIN HALF PHOTON FUSION #
    "/Monopole_SpinHalf_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    # SPIN HALF DRELL YAN #
    ,"/Monopole_SpinHalf_DrellYan_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    # SPIN ZERO PHOTON FUSION #
    ,"/Monopole_SpinZero_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    # SPIN ZERO DRELL YAN #
    ,"/Monopole_SpinZero_DrellYan_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v2/GEN-SIM-RECO"

]

datasets_2017_MONO = [
    #'/SinglePhoton/Run2017C-EXOMONOPOLE-09Aug2019_UL2017-v1/USER',
    #'/SinglePhoton/Run2017E-EXOMONOPOLE-09Aug2019_UL2017-v1/USER',
    #'/SinglePhoton/Run2017D-EXOMONOPOLE-09Aug2019_UL2017-v1/USER',
    #'/SinglePhoton/Run2017F-EXOMONOPOLE-09Aug2019_UL2017-v1/USER',
    #'/SinglePhoton/Run2017B-EXOMONOPOLE-09Aug2019_UL2017-v1/USER',
    '/MET/Run2017B-EXOMONOPOLE-09Aug2019_UL2017_rsb-v1/USER',
    '/MET/Run2017C-EXOMONOPOLE-09Aug2019_UL2017_rsb-v1/USER',
    '/MET/Run2017D-EXOMONOPOLE-09Aug2019_UL2017_rsb-v1/USER',
    '/MET/Run2017E-EXOMONOPOLE-09Aug2019_UL2017_rsb-v1/USER',
    '/MET/Run2017F-EXOMONOPOLE-09Aug2019_UL2017_rsb-v1/USER'
]

datasets_MC_2017 = [
    # SPIN HALF PHOTON FUSION #
    "/Monopole_SpinHalf_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    # SPIN HALF DRELL YAN #
    ,"/Monopole_SpinHalf_DrellYan_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    # SPIN ZERO PHOTON FUSION #
    ,"/Monopole_SpinZero_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    # SPIN ZERO DRELL YAN #
    ,"/Monopole_SpinZero_DrellYan_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/GEN-SIM-RECO"
    
]

datasets_2018_MONO = [
    #'/EGamma/Run2018A-EXOMONOPOLE-12Nov2019_UL2018-v2/USER',
    #'/EGamma/Run2018B-EXOMONOPOLE-12Nov2019_UL2018-v2/USER',
    #'/EGamma/Run2018C-EXOMONOPOLE-12Nov2019_UL2018-v2/USER',
    #'/EGamma/Run2018D-EXOMONOPOLE-12Nov2019_UL2018-v6/USER',
    '/MET/Run2018A-EXOMONOPOLE-12Nov2019_UL2018_rsb-v1/USER',
    '/MET/Run2018B-EXOMONOPOLE-12Nov2019_UL2018_rsb-v1/USER',
    '/MET/Run2018C-EXOMONOPOLE-12Nov2019_UL2018_rsb-v1/USER',
    '/MET/Run2018D-EXOMONOPOLE-12Nov2019_UL2018_rsb-v1/USER'
]


first_datasets_MC_2018 = [
    #"/Monopole_SpinHalf_DrellYan_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    "/Monopole_SpinHalf_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    #,"/Monopole_SpinHalf_DrellYan_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    #,"/Monopole_SpinHalf_DrellYan_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    #,"/Monopole_SpinHalf_DrellYan_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    #,"/Monopole_SpinHalf_DrellYan_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    #,"/Monopole_SpinHalf_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    #,"/Monopole_SpinHalf_DrellYan_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
]


datasets_MC_2018 = [
    # SPIN HALF PHOTON FUSION #
    "/Monopole_SpinHalf_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    # SPIN HALF DRELL YAN #
    ,"/Monopole_SpinHalf_DrellYan_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinHalf_DrellYan_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    # SPIN ZERO PHOTON FUSION #
    ,"/Monopole_SpinZero_PhotonFusion_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_PhotonFusion_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    # SPIN ZERO DRELL YAN #
    ,"/Monopole_SpinZero_DrellYan_M-1000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-2000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-2500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-3000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-3500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-4000_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
    ,"/Monopole_SpinZero_DrellYan_M-4500_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/GEN-SIM-RECO"
]

# Mapeamento entre o ano e os arquivos LumiMask
lumi_masks = {
    '2016': 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt',
    '2016APV': 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt',
    '2017': 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt',
    '2018': 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
}


if data_type == 'DATA':
    if year == '2016':
        datasets = datasets_2016_MONO
    elif year == '2016APV':
        datasets = datasets_2016_apv_MONO
    elif year == '2017':
        datasets = datasets_2017_MONO
    elif year == '2018':
        datasets = datasets_2018_MONO
    else:
        raise ValueError("Ano inválido. Escolha 2016, 2016APV, 2017 ou 2018.")
    lumi_mask = lumi_masks[year]
elif data_type == 'MC':
    if year == '2016':
        datasets = datasets_MC_2016
    elif year == '2016APV':
        datasets = datasets_MC_2016APV
    elif year == '2017':
        datasets = datasets_MC_2017
    elif year == '2018':
        datasets = first_datasets_MC_2018
    else:
        raise ValueError("Datasets MC não disponíveis para o ano selecionado.")
    lumi_mask = None  # Não é necessário para MC
else:
    raise ValueError("Tipo de dados inválido. Escolha 'DATA' ou 'MC'.")

# Função para submeter a configuração CRAB
def submit(config):
    try:
        crabCommand("submit", config=config)
    except HTTPException as hte:
        print("Falha ao submeter a tarefa: %s" % (hte.headers))
    except ClientException as cle:
        print("Falha ao submeter a tarefa: %s" % (cle))

# Loop sobre os datasets
for dataset in datasets:
    # Extrair a era ou identificar o dataset
    if data_type == 'DATA':
        era_match = re.search(r'Run\d{4}[A-Z]', dataset)
        if not era_match:
            raise ValueError("Era não encontrada no dataset: {}".format(dataset))
        era = era_match.group(0)
    elif data_type == 'MC':
        # Extrair o nome do dataset para identificação
        dataset_name = dataset.split('/')[1]
        era = dataset_name
    else:
        raise ValueError("Tipo de dados inválido. Escolha 'DATA' ou 'MC'.")

    crab_config = Configuration()
    crab_config.section_("General")
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    crab_config.General.requestName = '14Feb_EXOMETReview_{data_type}_{year}_{era}'.format(data_type=data_type, year=year, era=era)

    crab_config.General.workArea = config.General.workArea.format(data_type=data_type, year=year, era=era)
    crab_config.General.transferOutputs = config.General.transferOutputs
    crab_config.General.transferLogs = config.General.transferLogs

    crab_config.section_("JobType")
    crab_config.JobType.pluginName = config.JobType.pluginName
    crab_config.JobType.psetName = config.JobType.psetName
    crab_config.JobType.outputFiles = config.JobType.outputFiles
    crab_config.JobType.allowUndistributedCMSSW = config.JobType.allowUndistributedCMSSW
    #crab_config.JobType.maxMemoryMB = config.JobType.maxMemoryMB
    #crab_config.JobType.maxJobRuntimeMin = config.JobType.maxJobRuntimeMin

    crab_config.section_("Data")
    crab_config.Data.inputDataset = dataset
    crab_config.Data.inputDBS = config.Data.inputDBS
    crab_config.Data.allowNonValidInputDataset = True
    crab_config.Data.splitting = config.Data.splitting
    crab_config.Data.unitsPerJob = config.Data.unitsPerJob
    #crab_config.Data.totalUnits = config.Data.totalUnits
    crab_config.Data.publication = config.Data.publication
    crab_config.Data.outputDatasetTag = '{data_type}_{year}'.format(data_type=data_type, year=year)
    crab_config.Data.outLFNDirBase = '/store/user/tmenezes/Feb_EXOMETReview_MagneticMonopole_{data_type}_{year}/{era}/'.format(data_type=data_type, year=year, era=era)

    if data_type == 'DATA':
        crab_config.Data.lumiMask = lumi_mask
    elif data_type == 'MC':
        pass  # Não precisa de lumiMask para MC

    crab_config.section_("Site")
    crab_config.Site.storageSite = config.Site.storageSite

    submit(crab_config)
