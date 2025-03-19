import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from Configuration.Eras.Era_Run2_2017_cff import Run2_2017
from Configuration.ProcessModifiers.run2_miniAOD_UL_preSummer20_cff import run2_miniAOD_UL_preSummer20

process = cms.Process('PAT',Run2_2017,run2_miniAOD_UL_preSummer20)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.PAT_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
#with open("28Feb_run319347_SKIM_files_test.txt", "r") as f:
#    root_files = [line.strip() for line in f if line.strip()]


options = VarParsing.VarParsing('analysis')
# Prevent re-registration of the variable by checking if it already exists
if not hasattr(options, 'inputFiles'):
    options.register('inputFiles',
                     '',
                     VarParsing.VarParsing.multiplicity.list,
                     VarParsing.VarParsing.varType.string,
                     "Input files")

options.parseArguments()


process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('file:Monopole_SpinHalf_DrellYan-M_2000.root'),
    fileNames = cms.untracked.vstring(options.inputFiles),
    secondaryFileNames = cms.untracked.vstring()
)


process.options = cms.untracked.PSet(

)


# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v35', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v33', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mc2017_realistic_v8', '')

# Path and EndPath definitions
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_HcalStripHaloFilter = cms.Path(process.HcalStripHaloFilter)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_hfNoisyHitsFilter = cms.Path(process.hfNoisyHitsFilter)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
#process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)  # DATA o ly
process.Flag_globalSuperTightHalo2016Filter = cms.Path(process.globalSuperTightHalo2016Filter)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_chargedHadronTrackResolutionFilter = cms.Path(process.chargedHadronTrackResolutionFilter)
process.Flag_globalTightHalo2016Filter = cms.Path(process.globalTightHalo2016Filter)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_BadChargedCandidateSummer16Filter = cms.Path(process.BadChargedCandidateSummer16Filter)  # DATA only
#process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)  # DATA only
process.Flag_BadPFMuonFilter = cms.Path(process.BadPFMuonFilter)
process.Flag_ecalBadCalibFilter = cms.Path(process.ecalBadCalibFilter)  # ensure that is ON for MC
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_BadChargedCandidateFilter = cms.Path(process.BadChargedCandidateFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_BadPFMuonSummer16Filter = cms.Path(process.BadPFMuonSummer16Filter) 
process.Flag_muonBadTrackFilter = cms.Path(process.muonBadTrackFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
process.Flag_BadPFMuonDzFilter = cms.Path(process.BadPFMuonDzFilter)
# process.endjob_step = cms.EndPath(process.endOfProcess)


#
#
#
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')

process.KFFittingSmootherWithOutliersRejectionAndRK.BreakTrajWith2ConsecutiveMissing = False
process.KFFittingSmootherWithOutliersRejectionAndRK.EstimateCut = 1000

## Track refitter specific stuff
from RecoTracker.TrackProducer.TrackRefitters_cff import *
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")

### unclean EE
process.uncleanEERecovered = cms.EDProducer(
    'UncleanSCRecoveryProducer',
    # input collections
    cleanBcCollection = cms.InputTag('multi5x5SuperClusters','multi5x5EndcapBasicClusters'),
    cleanScCollection = cms.InputTag('multi5x5SuperClusters','multi5x5EndcapSuperClusters'),

    uncleanBcCollection = cms.InputTag('multi5x5SuperClusters','uncleanOnlyMulti5x5EndcapBasicClusters'),
    uncleanScCollection = cms.InputTag('multi5x5SuperClusters','uncleanOnlyMulti5x5EndcapSuperClusters'),
    # names of collections to be produced:
    bcCollection = cms.string('uncleanEndcapBasicClusters'),
    scCollection = cms.string('uncleanEndcapSuperClusters'),
)

### Construct combined (clean and uncleanOnly Ecal clusters)
process.load("RecoEcal.EgammaClusterProducers.uncleanSCRecovery_cfi")
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
process.Monopoler = cms.EDAnalyzer(
    'MonoNtupleDumper',
    isData = cms.bool(False),
    Output = cms.string(options.outputFile),
    #Output = cms.string("14Mar_MC.root"),
    TriggerResults = cms.InputTag("TriggerResults","","HLT"),
    TriggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    GeneratorTag = cms.InputTag("genParticles",""),
    PrimaryVertices = cms.InputTag("offlinePrimaryVertices",""),
    EcalEBRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    EcalEERecHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    HBHERecHits = cms.InputTag("hbhereco",""),
    JetTag = cms.InputTag("ak4PFJets",""),
    ElectronTag = cms.InputTag("gedGsfElectrons",""),
    PhotonTag = cms.InputTag("photons",""),
    PFTag = cms.InputTag("particleFlow",""),
    METTag = cms.InputTag("pfMet",""),
    GenMETTag = cms.InputTag("genMetTrue",""),
    CaloMETTag = cms.InputTag("caloMet",""),
    bcClusterTag = cms.InputTag("hybridSuperClusters","uncleanOnlyHybridBarrelBasicClusters") ,
    ccClusterTag = cms.InputTag("hybridSuperClusters","hybridBarrelBasicClusters"),
    combClusterTag = cms.InputTag("uncleanSCRecovered","uncleanHybridBarrelBasicClusters") ,
    eeCleanTag = cms.InputTag("multi5x5SuperClusters","multi5x5EndcapBasicClusters"),
    eeUncleanTag = cms.InputTag("multi5x5SuperClusters","uncleanOnlyMulti5x5EndcapBasicClusters") ,
    eeCombTag = cms.InputTag("uncleanEERecovered","uncleanEndcapBasicClusters"),
    pileupInfoTag = cms.InputTag("addPileupInfo"),    
    PatJetTag = cms.InputTag("slimmedJets"),
    PatMETTag = cms.InputTag("slimmedMETs"),
    StripSeedLength = cms.uint32(3),
    ClusterLength = cms.uint32(5),
    SeedThreshold = cms.double(50.),
    TrackTag=cms.InputTag("TrackRefitter"),
    TrackSource=cms.string("TrackRefitter"),
    TrackChi2Cut=cms.untracked.double(7.5),
    TrackPtCut=cms.untracked.double(3.0),
    TrackDeDxCut=cms.untracked.double(0),
    TrackDefaultError=cms.untracked.double(0.05),
    TrackErrorFudge=cms.untracked.double(0.02),
    TrackHitOutput=cms.untracked.bool(True),
    ClustHitOutput = cms.untracked.bool(True)
)
process.ecalCombine_step = cms.Path(process.uncleanSCRecovered)
process.ecalCombineEE_step = cms.Path(process.uncleanEERecovered)
process.refit_step = cms.Path(process.MeasurementTrackerEvent * process.TrackRefitter)
process.mpl_step = cms.Path(process.Monopoler)




# Schedule definition

process.schedule = cms.Schedule(process.Flag_HBHENoiseFilter,
process.Flag_HBHENoiseIsoFilter,
process.Flag_CSCTightHaloFilter,
process.Flag_CSCTightHaloTrkMuUnvetoFilter,
process.Flag_CSCTightHalo2015Filter,
process.Flag_globalTightHalo2016Filter,
process.Flag_globalSuperTightHalo2016Filter,
process.Flag_HcalStripHaloFilter,
process.Flag_hcalLaserEventFilter,
process.Flag_EcalDeadCellTriggerPrimitiveFilter,
process.Flag_EcalDeadCellBoundaryEnergyFilter,
process.Flag_ecalBadCalibFilter,
process.Flag_goodVertices,
process.Flag_eeBadScFilter,
process.Flag_ecalLaserCorrFilter,
process.Flag_trkPOGFilters,
process.Flag_chargedHadronTrackResolutionFilter,
process.Flag_muonBadTrackFilter,
process.Flag_BadChargedCandidateFilter,
process.Flag_BadPFMuonFilter,
process.Flag_BadPFMuonDzFilter,
process.Flag_hfNoisyHitsFilter,
process.Flag_BadChargedCandidateSummer16Filter,
process.Flag_BadPFMuonSummer16Filter,
process.Flag_trkPOG_manystripclus53X,
process.Flag_trkPOG_toomanystripclus53X,
process.Flag_trkPOG_logErrorTooManyClusters,
process.Flag_METFilters,
process.ecalCombine_step,
process.ecalCombineEE_step,
process.refit_step,
process.mpl_step
# process.endjob_step,
)

process.schedule.associate(process.patTask)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllData imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
