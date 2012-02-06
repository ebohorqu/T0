#!/usr/bin/env python
"""
_RunConfig_t_

Testing the RunConfig code

"""
import unittest
import threading
import logging
import time
import os

from WMQuality.TestInit import TestInit
from WMCore.DAOFactory import DAOFactory
from WMCore.Database.DBFactory import DBFactory
from WMCore.Configuration import loadConfigurationFile

from T0.RunConfig import RunConfigAPI


class RunConfigTest(unittest.TestCase):
    """
    _RunConfigTest_

    Testing the RunConfig code
    """

    def setUp(self):
        """
        _setUp_

        """
        self.testInit = TestInit(__file__)
        self.testInit.setLogging()
        self.testInit.setDatabaseConnection()

        self.testInit.setSchema(customModules = ["T0.WMBS"])

        self.hltkey = "/cdaq/physics/Run2011/3e33/v2.1/HLT/V2"
        self.hltConfig = None

        if os.environ.has_key('WMAGENT_CONFIG'):

            wmAgentConfig = loadConfigurationFile(os.environ["WMAGENT_CONFIG"])
            if hasattr(wmAgentConfig, "HLTConfDatabase"):

                connectUrl = getattr(wmAgentConfig.HLTConfDatabase, "connectUrl", None)

                dbFactory = DBFactory(logging, dburl = connectUrl, options = {})
                dbInterface = dbFactory.connect()

                daoFactory = DAOFactory(package = "T0.WMBS",
                                        logger = logging,
                                        dbinterface = dbInterface)

                getHLTConfigDAO = daoFactory(classname = "RunConfig.GetHLTConfig")
                self.hltConfig = getHLTConfigDAO.execute(self.hltkey, transaction = False)

                if self.hltConfig['process'] == None or len(self.hltConfig['mapping']) == 0:
                    raise RuntimeError, "HLTConfDB query returned no process or mapping"

            else:
                print "Your config is missing the HLTConfDatabase section"
                print "Using reference HLT config instead"

        else:
            print "You do not have WMAGENT_CONFIG in your environment"
            print "Using reference HLT config instead"

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        insertCMSSVersionDAO = daoFactory(classname = "RunConfig.InsertCMSSWVersion")
        insertCMSSVersionDAO.execute(binds = { 'VERSION' : "CMSSW_4_2_7" },
                                     transaction = False)

        insertRunDAO = daoFactory(classname = "RunConfig.InsertRun")
        insertRunDAO.execute(binds = { 'RUN' : 176161,
                                       'TIME' : int(time.time()),
                                       'HLTKEY' : self.hltkey },
                             transaction = False)

        insertLumiDAO = daoFactory(classname = "RunConfig.InsertLumiSection")
        insertLumiDAO.execute(binds = { 'RUN' : 176161,
                                        'LUMI' : 1 },
                              transaction = False)

        insertStreamDAO = daoFactory(classname = "RunConfig.InsertStream")
        insertStreamDAO.execute(binds = { 'STREAM' : "A" },
                                transaction = False)
        insertStreamDAO.execute(binds = { 'STREAM' : "Express" },
                                transaction = False)
        insertStreamDAO.execute(binds = { 'STREAM' : "HLTMON" },
                                transaction = False)

        insertStreamCMSSWVersionDAO = daoFactory(classname = "RunConfig.InsertStreamCMSSWVersion")
        insertStreamCMSSWVersionDAO.execute(binds = { 'RUN' : 176161,
                                                      'STREAM' : "A",
                                                      'VERSION' : "CMSSW_4_2_7" },
                                            transaction = False)
        insertStreamCMSSWVersionDAO.execute(binds = { 'RUN' : 176161,
                                                      'STREAM' : "Express",
                                                      'VERSION' : "CMSSW_4_2_7" },
                                            transaction = False)
        insertStreamCMSSWVersionDAO.execute(binds = { 'RUN' : 176161,
                                                      'STREAM' : "HLTMON",
                                                      'VERSION' : "CMSSW_4_2_7" },
                                            transaction = False)

        insertStreamerDAO = daoFactory(classname = "RunConfig.InsertStreamer")
        insertStreamerDAO.execute(binds = { 'RUN' : 176161,
                                            'LUMI' : 1,
                                            'STREAM' : "A",
                                            'LFN' : "/testLFN/A",
                                            'FILESIZE' : 100,
                                            'EVENTS' : 100,
                                            'TIME' : int(time.time()) },
                                  transaction = False)
        insertStreamerDAO.execute(binds = { 'RUN' : 176161,
                                            'LUMI' : 1,
                                            'STREAM' : "Express",
                                            'LFN' : "/testLFN/Express",
                                            'FILESIZE' : 100,
                                            'EVENTS' : 100,
                                            'TIME' : int(time.time()) },
                                  transaction = False)
        insertStreamerDAO.execute(binds = { 'RUN' : 176161,
                                            'LUMI' : 1,
                                            'STREAM' : "HLTMON",
                                            'LFN' : "/testLFN/HLTMON",
                                            'FILESIZE' : 100,
                                            'EVENTS' : 100,
                                            'TIME' : int(time.time()) },
                                  transaction = False)

        self.tier0Config = loadConfigurationFile("ExampleConfig.py")

        self.referenceRunInfo = [ { 'status': 1,
                                    'process': 'HLT',
                                    'reco_lock_timeout': 30,
                                    'reco_timeout': 60,
                                    'hltkey': self.hltkey,
                                    'acq_era': 'ExampleConfig_UnitTest' } ]

        self.referenceMapping = {}
        self.referenceMapping['A'] = {}
        self.referenceMapping['A']['BTag'] = []
        self.referenceMapping['A']['BTag'].append("HLT_BTagMu_DiJet110_Mu5_v10")
        self.referenceMapping['A']['BTag'].append("HLT_BTagMu_DiJet20_Mu5_v10")
        self.referenceMapping['A']['BTag'].append("HLT_BTagMu_DiJet40_Mu5_v10")
        self.referenceMapping['A']['BTag'].append("HLT_BTagMu_DiJet70_Mu5_v10")
        self.referenceMapping['A']['Commissioning'] = []
        self.referenceMapping['A']['Commissioning'].append("HLT_Activity_Ecal_SC7_v8")
        self.referenceMapping['A']['Commissioning'].append("HLT_BeamGas_BSC_v5")
        self.referenceMapping['A']['Commissioning'].append("HLT_BeamGas_HF_v6")
        self.referenceMapping['A']['Commissioning'].append("HLT_IsoTrackHB_v7")
        self.referenceMapping['A']['Commissioning'].append("HLT_IsoTrackHE_v8")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleEG12_v3")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleEG5_v3")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleJet16_v4")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleJet36_v4")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleMuOpen_DT_v4")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleMuOpen_v4")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1_Interbunch_BSC_v3")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1_PreCollisions_v3")
        self.referenceMapping['A']['Commissioning'].append("HLT_Mu5_TkMu0_OST_Jpsi_Tight_B5Q7_v9")
        self.referenceMapping['A']['Cosmics'] = []
        self.referenceMapping['A']['Cosmics'].append("HLT_BeamHalo_v6")
        self.referenceMapping['A']['Cosmics'].append("HLT_L1SingleMuOpen_AntiBPTX_v3")
        self.referenceMapping['A']['Cosmics'].append("HLT_L1TrackerCosmics_v4")
        self.referenceMapping['A']['Cosmics'].append("HLT_RegionalCosmicTracking_v7")
        self.referenceMapping['A']['DoubleElectron'] = []
        self.referenceMapping['A']['DoubleElectron'].append("HLT_DoubleEle10_CaloIdL_TrkIdVL_Ele10_CaloIdT_TrkIdVL_v3")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele17_CaloIdL_CaloIsoVL_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_Ele8_Mass30_v7")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_SC8_Mass30_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele22_CaloIdL_CaloIsoVL_Ele15_HFT_v1")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_Ele17_v1")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17_v6")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_CaloIdL_CaloIsoVL_Jet40_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_CaloIdL_CaloIsoVL_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_CaloIdL_TrkIdVL_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v6")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Photon20_CaloIdVT_IsoT_Ele8_CaloIdL_CaloIsoVL_v9")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_TripleEle10_CaloIdL_TrkIdVL_v9")
        self.referenceMapping['A']['DoubleMu'] = []
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu3_v10")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu45_v6")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu5_Acoplanarity03_v6")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu5_IsoMu5_v8")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu5_v1")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu6_Acoplanarity03_v1")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu6_v8")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu7_v8")
        self.referenceMapping['A']['DoubleMu'].append("HLT_L1DoubleMu0_v4")
        self.referenceMapping['A']['DoubleMu'].append("HLT_L2DoubleMu0_v7")
        self.referenceMapping['A']['DoubleMu'].append("HLT_L2DoubleMu23_NoVertex_v7")
        self.referenceMapping['A']['DoubleMu'].append("HLT_L2DoubleMu30_NoVertex_v3")
        self.referenceMapping['A']['DoubleMu'].append("HLT_Mu13_Mu8_v7")
        self.referenceMapping['A']['DoubleMu'].append("HLT_Mu17_Mu8_v7")
        self.referenceMapping['A']['DoubleMu'].append("HLT_Mu8_Jet40_v10")
        self.referenceMapping['A']['DoubleMu'].append("HLT_TripleMu5_v9")
        self.referenceMapping['A']['ElectronHad'] = []
        self.referenceMapping['A']['ElectronHad'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_HT150_v6")
        self.referenceMapping['A']['ElectronHad'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_Mass4_HT150_v3")
        self.referenceMapping['A']['ElectronHad'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_v3")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R005_MR200_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R025_MR200_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R029_MR200_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT25_v4")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT40_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_v2")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3_Jet20_v2")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_BTagIP_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_QuadCentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_BTagIP_v9")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v9")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_DiCentralJet30_v8")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_QuadCentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet30_v8")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_CentralJet25_PFMHT20_v2")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_CentralJet25_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3_Jet20_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_TrkIdT_CentralJet30_CentralJet25_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_TrkIdT_Jet35_Jet25_Deta3_Jet20_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele30_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_PFMHT25_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele30_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3p5_Jet25_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele8_CaloIdT_TrkIdT_DiJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele8_CaloIdT_TrkIdT_QuadJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele8_CaloIdT_TrkIdT_TriJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT200_DoubleEle5_CaloIdVL_MassJPsi_v3")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT300_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT40_v6")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT350_Ele30_CaloIdT_TrkIdT_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT350_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT45_v6")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT400_Ele60_CaloIdT_TrkIdT_v1")
        self.referenceMapping['A']['FEDMonitor'] = []
        self.referenceMapping['A']['FEDMonitor'].append("HLT_DTErrors_v2")
        self.referenceMapping['A']['HT'] = []
        self.referenceMapping['A']['HT'].append("HLT_DiJet130_PT130_v6")
        self.referenceMapping['A']['HT'].append("HLT_DiJet160_PT160_v6")
        self.referenceMapping['A']['HT'].append("HLT_FatJetMass750_DR1p1_Deta2p0_v2")
        self.referenceMapping['A']['HT'].append("HLT_FatJetMass850_DR1p1_Deta2p0_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT150_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT2000_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT200_AlphaT0p55_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT200_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT250_AlphaT0p53_v6")
        self.referenceMapping['A']['HT'].append("HLT_HT250_AlphaT0p55_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT250_DoubleDisplacedJet60_PromptTrack_v6")
        self.referenceMapping['A']['HT'].append("HLT_HT250_DoubleDisplacedJet60_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT250_MHT100_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT250_MHT90_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT250_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT300_AlphaT0p53_v6")
        self.referenceMapping['A']['HT'].append("HLT_HT300_AlphaT0p54_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT300_CentralJet30_BTagIP_PFMHT55_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT300_CentralJet30_BTagIP_PFMHT65_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT300_CentralJet30_BTagIP_v7")
        self.referenceMapping['A']['HT'].append("HLT_HT300_MHT80_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT300_MHT90_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT300_PFMHT55_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT300_PFMHT65_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT300_v9")
        self.referenceMapping['A']['HT'].append("HLT_HT350_AlphaT0p52_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT350_AlphaT0p53_v7")
        self.referenceMapping['A']['HT'].append("HLT_HT350_MHT70_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT350_MHT80_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT350_MHT90_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT350_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT400_AlphaT0p51_v7")
        self.referenceMapping['A']['HT'].append("HLT_HT400_AlphaT0p52_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT400_MHT80_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT400_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT450_AlphaT0p51_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT450_AlphaT0p52_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT450_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT500_JetPt60_DPhi2p94_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT500_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT550_JetPt60_DPhi2p94_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT550_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT600_JetPt60_DPhi2p94_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT600_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT650_v1")
        self.referenceMapping['A']['HT'].append("HLT_R014_MR150_v7")
        self.referenceMapping['A']['HT'].append("HLT_R020_MR150_v7")
        self.referenceMapping['A']['HT'].append("HLT_R020_MR550_v7")
        self.referenceMapping['A']['HT'].append("HLT_R023_MR550_v3")
        self.referenceMapping['A']['HT'].append("HLT_R025_MR150_v7")
        self.referenceMapping['A']['HT'].append("HLT_R025_MR450_v7")
        self.referenceMapping['A']['HT'].append("HLT_R029_MR450_v3")
        self.referenceMapping['A']['HT'].append("HLT_R033_MR350_v7")
        self.referenceMapping['A']['HT'].append("HLT_R036_MR350_v3")
        self.referenceMapping['A']['HT'].append("HLT_R038_MR250_v7")
        self.referenceMapping['A']['HT'].append("HLT_R042_MR250_v3")
        self.referenceMapping['A']['HcalHPDNoise'] = []
        self.referenceMapping['A']['HcalHPDNoise'].append("HLT_GlobalRunHPDNoise_v5")
        self.referenceMapping['A']['HcalHPDNoise'].append("HLT_L1Tech_HBHEHO_totalOR_v3")
        self.referenceMapping['A']['HcalHPDNoise'].append("HLT_L1Tech_HCAL_HF_single_channel_v1")
        self.referenceMapping['A']['HcalNZS'] = []
        self.referenceMapping['A']['HcalNZS'].append("HLT_HcalNZS_v7")
        self.referenceMapping['A']['HcalNZS'].append("HLT_HcalPhiSym_v8")
        self.referenceMapping['A']['HighPileUp'] = []
        self.referenceMapping['A']['HighPileUp'].append("HLT_60Jet10_v1")
        self.referenceMapping['A']['HighPileUp'].append("HLT_70Jet10_v1")
        self.referenceMapping['A']['HighPileUp'].append("HLT_70Jet13_v1")
        self.referenceMapping['A']['Jet'] = []
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve110_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve190_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve240_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve300_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve30_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve370_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve60_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet110_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet190_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet240_CentralJet30_BTagIP_v3")
        self.referenceMapping['A']['Jet'].append("HLT_Jet240_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet270_CentralJet30_BTagIP_v3")
        self.referenceMapping['A']['Jet'].append("HLT_Jet300_v5")
        self.referenceMapping['A']['Jet'].append("HLT_Jet30_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet370_NoJetID_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet370_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet60_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet800_v1")
        self.referenceMapping['A']['LogMonitor'] = []
        self.referenceMapping['A']['LogMonitor'].append("HLT_LogMonitor_v1")
        self.referenceMapping['A']['MET'] = []
        self.referenceMapping['A']['MET'].append("HLT_CentralJet80_MET100_v7")
        self.referenceMapping['A']['MET'].append("HLT_CentralJet80_MET160_v7")
        self.referenceMapping['A']['MET'].append("HLT_CentralJet80_MET65_v7")
        self.referenceMapping['A']['MET'].append("HLT_CentralJet80_MET80_v6")
        self.referenceMapping['A']['MET'].append("HLT_DiCentralJet20_BTagIP_MET65_v7")
        self.referenceMapping['A']['MET'].append("HLT_DiCentralJet20_MET100_HBHENoiseFiltered_v1")
        self.referenceMapping['A']['MET'].append("HLT_DiCentralJet20_MET80_v5")
        self.referenceMapping['A']['MET'].append("HLT_DiJet60_MET45_v7")
        self.referenceMapping['A']['MET'].append("HLT_L2Mu60_1Hit_MET40_v5")
        self.referenceMapping['A']['MET'].append("HLT_L2Mu60_1Hit_MET60_v5")
        self.referenceMapping['A']['MET'].append("HLT_MET100_HBHENoiseFiltered_v6")
        self.referenceMapping['A']['MET'].append("HLT_MET100_v7")
        self.referenceMapping['A']['MET'].append("HLT_MET120_HBHENoiseFiltered_v6")
        self.referenceMapping['A']['MET'].append("HLT_MET120_v7")
        self.referenceMapping['A']['MET'].append("HLT_MET200_HBHENoiseFiltered_v6")
        self.referenceMapping['A']['MET'].append("HLT_MET200_v7")
        self.referenceMapping['A']['MET'].append("HLT_MET400_v2")
        self.referenceMapping['A']['MET'].append("HLT_MET65_HBHENoiseFiltered_v5")
        self.referenceMapping['A']['MET'].append("HLT_MET65_v4")
        self.referenceMapping['A']['MET'].append("HLT_PFMHT150_v12")
        self.referenceMapping['A']['MinimumBias'] = []
        self.referenceMapping['A']['MinimumBias'].append("HLT_JetE30_NoBPTX3BX_NoHalo_v8")
        self.referenceMapping['A']['MinimumBias'].append("HLT_JetE30_NoBPTX_NoHalo_v8")
        self.referenceMapping['A']['MinimumBias'].append("HLT_JetE30_NoBPTX_v6")
        self.referenceMapping['A']['MinimumBias'].append("HLT_JetE50_NoBPTX3BX_NoHalo_v3")
        self.referenceMapping['A']['MinimumBias'].append("HLT_Physics_v2")
        self.referenceMapping['A']['MinimumBias'].append("HLT_PixelTracks_Multiplicity100_v7")
        self.referenceMapping['A']['MinimumBias'].append("HLT_PixelTracks_Multiplicity80_v7")
        self.referenceMapping['A']['MinimumBias'].append("HLT_Random_v1")
        self.referenceMapping['A']['MinimumBias'].append("HLT_ZeroBias_v4")
        self.referenceMapping['A']['MuEG'] = []
        self.referenceMapping['A']['MuEG'].append("HLT_DoubleMu5_Ele8_CaloIdL_TrkIdVL_v10")
        self.referenceMapping['A']['MuEG'].append("HLT_DoubleMu5_Ele8_CaloIdT_TrkIdVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu15_DoublePhoton15_CaloIdL_v10")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu15_Photon20_CaloIdL_v10")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu17_Ele8_CaloIdL_v9")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu5_DoubleEle8_CaloIdT_TrkIdVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu5_Ele8_CaloIdT_CaloIsoVL_v1")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Ele8_CaloIdL_TrkIdVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu8_Ele17_CaloIdL_v9")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu8_Photon20_CaloIdVT_IsoT_v9")
        self.referenceMapping['A']['MuHad'] = []
        self.referenceMapping['A']['MuHad'].append("HLT_DoubleMu5_HT150_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_DoubleMu5_Mass4_HT150_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_HT250_Mu15_PFMHT40_v4")
        self.referenceMapping['A']['MuHad'].append("HLT_HT300_Mu15_PFMHT40_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_HT300_Mu5_PFMHT40_v8")
        self.referenceMapping['A']['MuHad'].append("HLT_HT350_Mu5_PFMHT45_v8")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_CentralJet30_BTagIP_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_CentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_DiCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_QuadCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_TriCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu20_DiCentralJet34_v3")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu10_R005_MR200_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu10_R025_MR200_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu10_R029_MR200_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu12_eta2p1_DiCentralJet20_BTagIP3D1stTrack_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu12_eta2p1_DiCentralJet20_DiBTagIP3D1stTrack_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu12_eta2p1_DiCentralJet30_BTagIP3D_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_CentralJet30_BTagIP_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_CentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_DiCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_QuadCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_TriCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu40_HT200_v4")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_DiJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_HT150_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Mass4_HT150_v6")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_QuadJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_TriJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu60_HT200_v1")
        self.referenceMapping['A']['MuOnia'] = []
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Jpsi_Muon_v7")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Jpsi_NoVertexing_v3")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Jpsi_v6")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Upsilon_Muon_v7")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Upsilon_v6")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon10_Jpsi_Barrel_v6")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon11_PsiPrime_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon13_Jpsi_Barrel_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon6_LowMass_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon7_Upsilon_Barrel_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon9_PsiPrime_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon9_Upsilon_Barrel_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu4_Dimuon4_Bs_Barrel_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu4_Dimuon6_Bs_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu4_Jpsi_Displaced_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu4p5_LowMass_Displaced_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu5_Jpsi_Displaced_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu5_LowMass_Displaced_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Mu5_L2Mu2_Jpsi_v9")
        self.referenceMapping['A']['MuOnia'].append("HLT_Mu5_Track2_Jpsi_v9")
        self.referenceMapping['A']['MuOnia'].append("HLT_Mu7_Track7_Jpsi_v10")
        self.referenceMapping['A']['MultiJet'] = []
        self.referenceMapping['A']['MultiJet'].append("HLT_CentralJet46_CentralJet38_CentralJet20_DiBTagIP3D_v1")
        self.referenceMapping['A']['MultiJet'].append("HLT_CentralJet46_CentralJet38_DiBTagIP3D_v3")
        self.referenceMapping['A']['MultiJet'].append("HLT_CentralJet60_CentralJet53_DiBTagIP3D_v2")
        self.referenceMapping['A']['MultiJet'].append("HLT_DiCentralJet36_BTagIP3DLoose_v1")
        self.referenceMapping['A']['MultiJet'].append("HLT_DoubleJet30_ForwardBackward_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_DoubleJet60_ForwardBackward_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_DoubleJet70_ForwardBackward_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_DoubleJet80_ForwardBackward_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_EightJet120_v1")
        self.referenceMapping['A']['MultiJet'].append("HLT_ExclDiJet60_HFAND_v6")
        self.referenceMapping['A']['MultiJet'].append("HLT_ExclDiJet60_HFOR_v6")
        self.referenceMapping['A']['MultiJet'].append("HLT_L1DoubleJet36Central_v4")
        self.referenceMapping['A']['MultiJet'].append("HLT_L1ETM30_v4")
        self.referenceMapping['A']['MultiJet'].append("HLT_L1MultiJet_v4")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet40_IsoPFTau40_v12")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet40_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet45_IsoPFTau45_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet50_DiJet40_v1")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet50_Jet40_Jet30_v3")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet70_v6")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet80_v1")
        self.referenceMapping['A']['Photon'] = []
        self.referenceMapping['A']['Photon'].append("HLT_DoubleEle33_CaloIdL_v5")
        self.referenceMapping['A']['Photon'].append("HLT_DoubleEle45_CaloIdL_v4")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton33_HEVT_v4")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton38_HEVT_v3")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton40_MR150_v6")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton40_R014_MR150_v6")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton5_IsoVL_CEP_v7")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton60_v4")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton80_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon135_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon200_NoHE_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon20_CaloIdVL_IsoL_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon20_R9Id_Photon18_R9Id_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon225_NoHE_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_CaloIdXL_IsoXL_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_R9Id_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_Photon18_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_R9Id_Photon18_CaloIdXL_IsoXL_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_R9Id_Photon18_R9Id_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon30_CaloIdVL_IsoL_v9")
        self.referenceMapping['A']['Photon'].append("HLT_Photon30_CaloIdVL_v8")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_R9Id_v3")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_v5")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_CaloIdVL_Photon22_CaloIdVL_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_Photon22_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_R9Id_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_R9Id_Photon22_R9Id_v3")
        self.referenceMapping['A']['Photon'].append("HLT_Photon400_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon44_CaloIdL_Photon34_CaloIdL_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon48_CaloIdL_Photon38_CaloIdL_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon50_CaloIdVL_IsoL_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon50_CaloIdVL_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon75_CaloIdVL_IsoL_v8")
        self.referenceMapping['A']['Photon'].append("HLT_Photon75_CaloIdVL_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon90_CaloIdVL_IsoL_v5")
        self.referenceMapping['A']['Photon'].append("HLT_Photon90_CaloIdVL_v4")
        self.referenceMapping['A']['PhotonHad'] = []
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon30_CaloIdVT_CentralJet20_BTagIP_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R005_MR150_v5")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R017_MR500_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R023_MR350_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R029_MR250_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R042_MR200_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon55_CaloIdL_R017_MR500_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon55_CaloIdL_R023_MR350_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon55_CaloIdL_R029_MR250_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon55_CaloIdL_R042_MR200_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon70_CaloIdL_HT400_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon70_CaloIdL_HT500_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon70_CaloIdL_MHT110_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon70_CaloIdL_MHT90_v3")
        self.referenceMapping['A']['SingleElectron'] = []
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele100_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v3")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele25_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_v5")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele27_WP80_PFMT50_v4")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele32_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v5")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v7")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele32_WP70_PFMT50_v4")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele65_CaloIdVT_TrkIdT_v4")
        self.referenceMapping['A']['SingleMu'] = []
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu15_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu15_v14")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu17_v14")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu20_v9")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu24_eta2p1_v3")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu24_v9")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu30_eta2p1_v3")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu34_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_L1SingleMu10_v4")
        self.referenceMapping['A']['SingleMu'].append("HLT_L1SingleMu20_v4")
        self.referenceMapping['A']['SingleMu'].append("HLT_L2Mu10_v6")
        self.referenceMapping['A']['SingleMu'].append("HLT_L2Mu20_v6")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu100_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu12_v8")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu15_v9")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu20_v8")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu24_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu24_v8")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu30_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu30_v8")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu40_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu40_v6")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu5_v10")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu60_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu8_v8")
        self.referenceMapping['A']['Tau'] = []
        self.referenceMapping['A']['Tau'].append("HLT_DoubleIsoPFTau45_Trk5_eta2p1_v3")
        self.referenceMapping['A']['Tau'].append("HLT_IsoPFTau40_IsoPFTau30_Trk5_eta2p1_v3")
        self.referenceMapping['A']['Tau'].append("HLT_MediumIsoPFTau35_Trk20_MET60_v1")
        self.referenceMapping['A']['Tau'].append("HLT_MediumIsoPFTau35_Trk20_MET70_v1")
        self.referenceMapping['A']['Tau'].append("HLT_MediumIsoPFTau35_Trk20_v1")
        self.referenceMapping['A']['TauPlusX'] = []
        self.referenceMapping['A']['TauPlusX'].append("HLT_Ele18_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_Ele18_CaloIdVT_TrkIdT_MediumIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_HT300_DoubleIsoPFTau10_Trk3_PFMHT40_v8")
        self.referenceMapping['A']['TauPlusX'].append("HLT_HT350_DoubleIsoPFTau10_Trk3_PFMHT45_v8")
        self.referenceMapping['A']['TauPlusX'].append("HLT_IsoMu15_LooseIsoPFTau15_v9")
        self.referenceMapping['A']['TauPlusX'].append("HLT_IsoMu15_eta2p1_LooseIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_IsoMu15_eta2p1_MediumIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_IsoMu15_eta2p1_TightIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_Mu15_LooseIsoPFTau15_v9")
        self.referenceMapping['A']['TauPlusX'].append("HLT_QuadJet50_IsoPFTau50_v1")
        self.referenceMapping['ALCAP0'] = {}
        self.referenceMapping['ALCAP0']['AlCaP0'] = []
        self.referenceMapping['ALCAP0']['AlCaP0'].append("AlCa_EcalEta_v9")
        self.referenceMapping['ALCAP0']['AlCaP0'].append("AlCa_EcalPi0_v10")
        self.referenceMapping['ALCAPHISYM'] = {}
        self.referenceMapping['ALCAPHISYM']['AlCaPhiSym'] = []
        self.referenceMapping['ALCAPHISYM']['AlCaPhiSym'].append("AlCa_EcalPhiSym_v7")
        self.referenceMapping['Calibration'] = {}
        self.referenceMapping['Calibration']['TestEnablesEcalHcalDT'] = []
        self.referenceMapping['Calibration']['TestEnablesEcalHcalDT'].append("HLT_DTCalibration_v1")
        self.referenceMapping['Calibration']['TestEnablesEcalHcalDT'].append("HLT_EcalCalibration_v2")
        self.referenceMapping['Calibration']['TestEnablesEcalHcalDT'].append("HLT_HcalCalibration_v2")
        self.referenceMapping['EcalCalibration'] = {}
        self.referenceMapping['EcalCalibration']['EcalLaser'] = []
        self.referenceMapping['EcalCalibration']['EcalLaser'].append("HLT_EcalCalibration_v2")
        self.referenceMapping['Express'] = {}
        self.referenceMapping['Express']['ExpressPhysics'] = []
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_DoubleEle45_CaloIdL_v4")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_DoubleMu45_v6")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_DoublePhoton80_v2")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_EightJet120_v1")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Ele100_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v3")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v8")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Ele65_CaloIdVT_TrkIdT_v4")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_HT2000_v2")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Jet370_v6")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Jet800_v1")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_MET200_v7")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_MET400_v2")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Mu100_eta2p1_v1")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Mu17_Mu8_v7")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Photon400_v2")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Photon75_CaloIdVL_IsoL_v8")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_ZeroBias_v4")
        self.referenceMapping['HLTMON'] = {}
        self.referenceMapping['HLTMON']['OfflineMonitor'] = []
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_EcalEta_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_EcalPhiSym_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_EcalPi0_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_RPCMuonNoHits_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_RPCMuonNoTriggers_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_RPCMuonNormalisation_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_60Jet10_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_70Jet10_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_70Jet13_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Activity_Ecal_SC7_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BTagMu_DiJet110_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BTagMu_DiJet20_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BTagMu_DiJet40_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BTagMu_DiJet70_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BeamGas_BSC_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BeamGas_HF_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BeamHalo_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet46_CentralJet38_CentralJet20_DiBTagIP3D_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet46_CentralJet38_DiBTagIP3D_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet60_CentralJet53_DiBTagIP3D_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet80_MET100_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet80_MET160_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet80_MET65_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet80_MET80_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DTErrors_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiCentralJet20_BTagIP_MET65_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiCentralJet20_MET100_HBHENoiseFiltered_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiCentralJet20_MET80_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiCentralJet36_BTagIP3DLoose_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJet130_PT130_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJet160_PT160_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJet60_MET45_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve110_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve190_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve240_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve300_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve30_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve370_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve60_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Jpsi_Muon_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Jpsi_NoVertexing_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Jpsi_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Upsilon_Muon_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Upsilon_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon10_Jpsi_Barrel_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon11_PsiPrime_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon13_Jpsi_Barrel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon6_LowMass_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon7_Upsilon_Barrel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon9_PsiPrime_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon9_Upsilon_Barrel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle10_CaloIdL_TrkIdVL_Ele10_CaloIdT_TrkIdVL_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle33_CaloIdL_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle45_CaloIdL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_HT150_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_Mass4_HT150_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleIsoPFTau45_Trk5_eta2p1_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleJet30_ForwardBackward_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleJet60_ForwardBackward_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleJet70_ForwardBackward_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleJet80_ForwardBackward_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu3_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu45_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu4_Dimuon4_Bs_Barrel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu4_Dimuon6_Bs_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu4_Jpsi_Displaced_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu4p5_LowMass_Displaced_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Acoplanarity03_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Ele8_CaloIdL_TrkIdVL_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Ele8_CaloIdT_TrkIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_HT150_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_IsoMu5_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Jpsi_Displaced_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_LowMass_Displaced_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Mass4_HT150_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu6_Acoplanarity03_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu6_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu7_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton33_HEVT_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton38_HEVT_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton40_MR150_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton40_R014_MR150_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton5_IsoVL_CEP_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton60_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton80_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_EightJet120_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele100_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R005_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R025_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R029_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT25_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT40_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele17_CaloIdL_CaloIsoVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_Ele8_Mass30_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_SC8_Mass30_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele18_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele18_CaloIdVT_TrkIdT_MediumIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3_Jet20_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele22_CaloIdL_CaloIsoVL_Ele15_HFT_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_BTagIP_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_QuadCentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_BTagIP_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_DiCentralJet30_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_QuadCentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet30_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_CentralJet25_PFMHT20_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_CentralJet25_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3_Jet20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_TrkIdT_CentralJet30_CentralJet25_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_TrkIdT_Jet35_Jet25_Deta3_Jet20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_WP80_PFMT50_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele30_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_PFMHT25_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele30_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3p5_Jet25_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_Ele17_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_WP70_PFMT50_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele65_CaloIdVT_TrkIdT_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdL_CaloIsoVL_Jet40_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdL_CaloIsoVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdL_TrkIdVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdT_TrkIdT_DiJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdT_TrkIdT_QuadJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdT_TrkIdT_TriJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_ExclDiJet60_HFAND_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_ExclDiJet60_HFOR_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_FatJetMass750_DR1p1_Deta2p0_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_FatJetMass850_DR1p1_Deta2p0_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_GlobalRunHPDNoise_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT150_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT2000_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT200_AlphaT0p55_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT200_DoubleEle5_CaloIdVL_MassJPsi_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT200_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_AlphaT0p53_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_AlphaT0p55_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_DoubleDisplacedJet60_PromptTrack_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_DoubleDisplacedJet60_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_MHT100_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_MHT90_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_Mu15_PFMHT40_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_AlphaT0p53_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_AlphaT0p54_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_CentralJet30_BTagIP_PFMHT55_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_CentralJet30_BTagIP_PFMHT65_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_CentralJet30_BTagIP_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_DoubleIsoPFTau10_Trk3_PFMHT40_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT40_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_MHT80_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_MHT90_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_Mu15_PFMHT40_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_Mu5_PFMHT40_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_PFMHT55_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_PFMHT65_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_AlphaT0p52_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_AlphaT0p53_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_DoubleIsoPFTau10_Trk3_PFMHT45_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_Ele30_CaloIdT_TrkIdT_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT45_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_MHT70_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_MHT80_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_MHT90_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_Mu5_PFMHT45_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_AlphaT0p51_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_AlphaT0p52_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_Ele60_CaloIdT_TrkIdT_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_MHT80_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT450_AlphaT0p51_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT450_AlphaT0p52_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT450_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT500_JetPt60_DPhi2p94_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT500_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT550_JetPt60_DPhi2p94_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT550_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT600_JetPt60_DPhi2p94_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT600_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT650_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HcalNZS_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HcalPhiSym_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_LooseIsoPFTau15_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_eta2p1_LooseIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_eta2p1_MediumIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_eta2p1_TightIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_v14")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_CentralJet30_BTagIP_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_CentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_DiCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_QuadCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_TriCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_v14")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu20_DiCentralJet34_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu20_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu24_eta2p1_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu24_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu30_eta2p1_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu34_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoPFTau40_IsoPFTau30_Trk5_eta2p1_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoTrackHB_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoTrackHE_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet110_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet190_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet240_CentralJet30_BTagIP_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet240_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet270_CentralJet30_BTagIP_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet300_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet30_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet370_NoJetID_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet370_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet60_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet800_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_JetE30_NoBPTX3BX_NoHalo_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_JetE30_NoBPTX_NoHalo_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_JetE30_NoBPTX_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_JetE50_NoBPTX3BX_NoHalo_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1DoubleJet36Central_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1DoubleMu0_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1ETM30_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1MultiJet_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleEG12_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleEG5_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleJet16_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleJet36_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMu10_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMu20_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMuOpen_AntiBPTX_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMuOpen_DT_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMuOpen_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1Tech_HBHEHO_totalOR_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1Tech_HCAL_HF_single_channel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1TrackerCosmics_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1_Interbunch_BSC_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1_PreCollisions_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2DoubleMu0_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2DoubleMu23_NoVertex_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2DoubleMu30_NoVertex_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2Mu10_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2Mu20_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2Mu60_1Hit_MET40_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2Mu60_1Hit_MET60_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_LogMonitor_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET100_HBHENoiseFiltered_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET100_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET120_HBHENoiseFiltered_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET120_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET200_HBHENoiseFiltered_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET200_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET400_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET65_HBHENoiseFiltered_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET65_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MediumIsoPFTau35_Trk20_MET60_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MediumIsoPFTau35_Trk20_MET70_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MediumIsoPFTau35_Trk20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu100_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu10_R005_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu10_R025_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu10_R029_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu12_eta2p1_DiCentralJet20_BTagIP3D1stTrack_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu12_eta2p1_DiCentralJet20_DiBTagIP3D1stTrack_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu12_eta2p1_DiCentralJet30_BTagIP3D_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu12_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu13_Mu8_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu15_DoublePhoton15_CaloIdL_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu15_LooseIsoPFTau15_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu15_Photon20_CaloIdL_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu15_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_Ele8_CaloIdL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_Mu8_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_CentralJet30_BTagIP_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_CentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_DiCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_QuadCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_TriCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu20_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu24_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu24_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu30_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu30_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu40_HT200_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu40_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu40_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_DiJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_DoubleEle8_CaloIdT_TrkIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Ele8_CaloIdT_CaloIsoVL_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Ele8_CaloIdL_TrkIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_HT150_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Mass4_HT150_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_L2Mu2_Jpsi_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_QuadJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_TkMu0_OST_Jpsi_Tight_B5Q7_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Track2_Jpsi_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_TriJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu60_HT200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu60_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu7_Track7_Jpsi_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_Ele17_CaloIdL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_Jet40_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_Photon20_CaloIdVT_IsoT_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_PFMHT150_v12")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon135_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon200_NoHE_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon20_CaloIdVL_IsoL_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon20_CaloIdVT_IsoT_Ele8_CaloIdL_CaloIsoVL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon20_R9Id_Photon18_R9Id_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon225_NoHE_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_CaloIdXL_IsoXL_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_R9Id_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_Photon18_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_R9Id_Photon18_CaloIdXL_IsoXL_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_R9Id_Photon18_R9Id_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon30_CaloIdVL_IsoL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon30_CaloIdVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon30_CaloIdVT_CentralJet20_BTagIP_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_R9Id_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_CaloIdVL_Photon22_CaloIdVL_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_Photon22_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_R9Id_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_R9Id_Photon22_R9Id_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon400_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R005_MR150_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R017_MR500_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R023_MR350_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R029_MR250_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R042_MR200_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon44_CaloIdL_Photon34_CaloIdL_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon48_CaloIdL_Photon38_CaloIdL_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon50_CaloIdVL_IsoL_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon50_CaloIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon55_CaloIdL_R017_MR500_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon55_CaloIdL_R023_MR350_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon55_CaloIdL_R029_MR250_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon55_CaloIdL_R042_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon70_CaloIdL_HT400_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon70_CaloIdL_HT500_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon70_CaloIdL_MHT110_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon70_CaloIdL_MHT90_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon75_CaloIdVL_IsoL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon75_CaloIdVL_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon90_CaloIdVL_IsoL_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon90_CaloIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Physics_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_PixelTracks_Multiplicity100_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_PixelTracks_Multiplicity80_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet40_IsoPFTau40_v12")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet40_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet45_IsoPFTau45_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet50_DiJet40_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet50_IsoPFTau50_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet50_Jet40_Jet30_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet70_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet80_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R014_MR150_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R020_MR150_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R020_MR550_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R023_MR550_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R025_MR150_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R025_MR450_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R029_MR450_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R033_MR350_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R036_MR350_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R038_MR250_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R042_MR250_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Random_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_RegionalCosmicTracking_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_TripleEle10_CaloIdL_TrkIdVL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_TripleMu5_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_ZeroBias_v4")
        self.referenceMapping['NanoDST'] = {}
        self.referenceMapping['NanoDST']['L1Accept'] = []
        self.referenceMapping['NanoDST']['L1Accept'].append("DST_Physics_v2")
        self.referenceMapping['RPCMON'] = {}
        self.referenceMapping['RPCMON']['RPCMonitor'] = []
        self.referenceMapping['RPCMON']['RPCMonitor'].append("AlCa_RPCMuonNoHits_v6")
        self.referenceMapping['RPCMON']['RPCMonitor'].append("AlCa_RPCMuonNoTriggers_v6")
        self.referenceMapping['RPCMON']['RPCMonitor'].append("AlCa_RPCMuonNormalisation_v6")
        self.referenceMapping['TrackerCalibration'] = {}
        self.referenceMapping['TrackerCalibration']['TestEnablesTracker'] = []
        self.referenceMapping['TrackerCalibration']['TestEnablesTracker'].append("HLT_TrackerCalibration_v2")

        # remember for later
        self.getRunInfoDAO = daoFactory(classname = "RunConfig.GetRunInfo")
        self.getStreamDatasetTriggersDAO = daoFactory(classname = "RunConfig.GetStreamDatasetTriggers")
        self.getStreamDatasetsDAO = daoFactory(classname = "RunConfig.GetStreamDatasets")
        self.getStreamStylesDAO = daoFactory(classname = "RunConfig.GetStreamStyles")
        self.getRepackConfigDAO = daoFactory(classname = "RunConfig.GetRepackConfig")
        self.getExpressConfigDAO = daoFactory(classname = "RunConfig.GetExpressConfig")
        self.getRecoConfigDAO = daoFactory(classname = "RunConfig.GetRecoConfig")
        self.getPhEDExConfigDAO = daoFactory(classname = "RunConfig.GetPhEDExConfig")
        self.getPromptSkimConfigDAO = daoFactory(classname = "RunConfig.GetPromptSkimConfig")

        return

    def tearDown(self):
        """
        _tearDown_

        """
        self.testInit.clearDatabase()

        return

    def test00(self):
        """
        _test00_

        Test configureRun and configureRunStream methods
        by calling them the same way as from Tier0Feeder

        """
        myThread = threading.currentThread()

        RunConfigAPI.configureRun(self.tier0Config, 176161, self.hltConfig,
                                  { 'process' : "HLT",
                                    'mapping' : self.referenceMapping })

        runInfo = self.getRunInfoDAO.execute(176161,
                                             transaction = False)

        self.assertEqual(runInfo, self.referenceRunInfo,
                         "ERROR: run info does not match reference")

        mapping = self.getStreamDatasetTriggersDAO.execute(176161,
                                                           transaction = False)

        self.assertEqual(sorted(mapping.keys()), sorted(self.referenceMapping.keys()),
                         "ERROR: streams do not match reference") 
        for stream in mapping.keys():
            self.assertEqual(sorted(mapping[stream].keys()), sorted(self.referenceMapping[stream].keys()),
                             "ERROR: primary datasets do not match reference")
            for primds in mapping[stream].keys():
                self.assertEqual(sorted(mapping[stream][primds]), sorted(self.referenceMapping[stream][primds]),
                                 "ERROR: trigger paths do not match reference")

        RunConfigAPI.configureRunStream(self.tier0Config, 176161, "A")
        RunConfigAPI.configureRunStream(self.tier0Config, 176161, "Express")
        RunConfigAPI.configureRunStream(self.tier0Config, 176161, "HLTMON")

        datasets = self.getStreamDatasetsDAO.execute(176161, "A",
                                                     transaction = False)

        for primds in datasets:
            if not primds.endswith("-Error"):
                self.assertTrue(('%s-Error' % primds) in datasets,
                                "ERROR: error datasets for bulk not setup correctly")

        datasets = self.getStreamDatasetsDAO.execute(176161, "Express",
                                                     transaction = False)

        self.assertTrue('StreamExpress' in datasets,
                        "ERROR: special express datasets not setup correctly")
        for primds in datasets:
            if not primds.endswith("-Error"):
                self.assertFalse(('%s-Error' % primds) in datasets,
                                "ERROR: error datasets for express setup incorrectly")

        datasets = self.getStreamDatasetsDAO.execute(176161, "HLTMON",
                                                     transaction = False)

        self.assertTrue('StreamHLTMON' in datasets,
                        "ERROR: special express datasets not setup correctly")
        for primds in datasets:
            if not primds.endswith("-Error"):
                self.assertFalse(('%s-Error' % primds) in datasets,
                                "ERROR: error datasets for express setup incorrectly")

        streamStyles = self.getStreamStylesDAO.execute(176161,
                                                       transaction = False)

        self.assertEquals(streamStyles['A'], "Bulk",
                          "ERROR: stream A is not Bulk style")
        self.assertEquals(streamStyles['Express'], "Express",
                          "ERROR: stream Express is not Express style")
        self.assertEquals(streamStyles['HLTMON'], "Express",
                          "ERROR: stream HLTMON is not Express style")

        repackConfig = self.getRepackConfigDAO.execute(176161, "A",
                                                       transaction = False)

        self.assertEqual(repackConfig['proc_ver'], "v1",
                         "ERROR: wrong processing version for stream A")

        self.assertEqual(repackConfig['cmssw'], "CMSSW_4_2_7",
                         "ERROR: wrong CMSSW version for stream A")

        expressConfig = self.getExpressConfigDAO.execute(176161, "Express",
                                                         transaction = False)

        self.assertEqual(expressConfig['proc_ver'], "v2" ,
                         "ERROR: wrong processing version for stream Express")

        self.assertEqual(expressConfig['cmssw'], "CMSSW_4_2_8_patch6" ,
                         "ERROR: wrong CMSSW version for stream Express")

        writeTiers = expressConfig['write_tiers'].split(',')
        self.assertEqual(set(writeTiers), set([ "FEVT", "ALCARECO", "DQM" ]),
                         "ERROR: wrong data tiers for stream Express")

        writeSkims = []
        if expressConfig['write_skims'] != None:
            writeSkims = expressConfig['write_skims'].split(',')
        self.assertEqual(set(writeSkims), set([ "SiStripCalZeroBias", "PromptCalibProd" ]),
                         "ERROR: wrong alca skims for stream Express")

        self.assertEqual(expressConfig['global_tag'], "GlobalTag1" ,
                         "ERROR: wrong global tag for stream Express")

        self.assertEqual(expressConfig['scenario'], "pp" ,
                         "ERROR: wrong scenario for stream Express")

        expressConfig = self.getExpressConfigDAO.execute(176161, "HLTMON",
                                                         transaction = False)

        self.assertEqual(expressConfig['proc_ver'], "v3" ,
                         "ERROR: wrong processing version for stream HLTMON")

        self.assertEqual(expressConfig['cmssw'], "CMSSW_4_2_8_patch7" ,
                         "ERROR: wrong CMSSW version for stream HLTMON")

        writeTiers = expressConfig['write_tiers'].split(',')
        self.assertEqual(set(writeTiers), set([ "FEVTHLTALL" ]),
                         "ERROR: wrong data tiers for stream HLTMON")

        writeSkims = []
        if expressConfig['write_skims'] != None:
            writeSkims = expressConfig['write_skims'].split(',')
        self.assertEqual(set(writeSkims), set([]),
                         "ERROR: wrong alca skims for stream HLTMON")

        self.assertEqual(expressConfig['global_tag'], "GlobalTag2" ,
                         "ERROR: wrong global tag for stream HLTMON")

        self.assertEqual(expressConfig['scenario'], "cosmics" ,
                         "ERROR: wrong scenario for stream HLTMON")

        
        datasets = self.getStreamDatasetsDAO.execute(176161, "A",
                                                     transaction = False)
        recoConfigs = self.getRecoConfigDAO.execute(176161, "A",
                                                   transaction = False)

        self.assertEquals(datasets, set(recoConfigs.keys()),
                          "ERROR: problems retrieving reco configs for stream A")

        for primds, recoConfig in recoConfigs.items():

            if primds == "Cosmics" or primds == "Cosmics-Error":

                if primds == "Cosmics":
                    self.assertEquals(recoConfig['do_reco'], 1,
                                      "ERROR: problem in reco configuration")
                else:
                    self.assertEquals(recoConfig['do_reco'], 0,
                                      "ERROR: problem in reco configuration")

                self.assertEquals(recoConfig['cmssw'], "CMSSW_4_2_8_patch2",
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['reco_split'], 100,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['write_reco'], 1,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['write_aod'], 1,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['write_dqm'], 1,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['proc_ver'], "v5",
                                  "ERROR: problem in reco configuration")

                writeSkims = []
                if recoConfig['write_skims'] != None:
                    writeSkims = recoConfig['write_skims'].split(',')
                self.assertEquals(set(writeSkims), set([ "Skim1", "Skim2", "Skim3" ]),
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['global_tag'], "GlobalTag4",
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['scenario'], "cosmics",
                                  "ERROR: problem in reco configuration")

            elif primds == "MinimumBias" or primds == "MinimumBias-Error":

                self.assertEquals(recoConfig['do_reco'], 0,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['cmssw'], "CMSSW_4_2_8_patch3",
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['reco_split'], 200,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['write_reco'], 0,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['write_aod'], 0,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['write_dqm'], 0,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['proc_ver'], "v6",
                                  "ERROR: problem in reco configuration")

                writeSkims = []
                if recoConfig['write_skims'] != None:
                    writeSkims = recoConfig['write_skims'].split(',')
                self.assertEquals(set(writeSkims), set([]),
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['global_tag'], "GlobalTag5",
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['scenario'], "pp",
                                  "ERROR: problem in reco configuration")

            else:

                self.assertEquals(recoConfig['do_reco'], 0,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['cmssw'], "CMSSW_4_2_8_patch1",
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['reco_split'], 2000,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['write_reco'], 1,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['write_aod'], 1,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['write_dqm'], 1,
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['proc_ver'], "v4",
                                  "ERROR: problem in reco configuration")

                writeSkims = []
                if recoConfig['write_skims'] != None:
                    writeSkims = recoConfig['write_skims'].split(',')
                self.assertEquals(set(writeSkims), set([]),
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['global_tag'], "GlobalTag3",
                                  "ERROR: problem in reco configuration")
            
                self.assertEquals(recoConfig['scenario'], "pp",
                                  "ERROR: problem in reco configuration")
                
        
        phedexConfigs = self.getPhEDExConfigDAO.execute(176161, "A",
                                                        transaction = False)

        self.assertEquals(datasets, set(phedexConfigs.keys()),
                          "ERROR: problems retrieving PhEDEx configs for stream A")

        for primds, phedexConfig in phedexConfigs.items():

            if primds == "Cosmics":

                self.assertEquals(set(phedexConfig.keys()), set([ "Node2", "Node3" ]),
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node2']['custodial'], 1,
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node2']['request_only'], "y",
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node2']['priority'], "high",
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node3']['custodial'], 0,
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node3']['request_only'], "n",
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node3']['priority'], "high",
                                  "ERROR: problem in phedex configuration")

            elif primds == "Cosmics-Error":

                self.assertEquals(set(phedexConfig.keys()), set([ "Node3" ]),
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node3']['custodial'], 0,
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node3']['request_only'], "n",
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node3']['priority'], "high",
                                  "ERROR: problem in phedex configuration")

            elif primds == "MinimumBias":

                self.assertEquals(set(phedexConfig.keys()), set([ "Node4", "Node5" ]),
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node4']['custodial'], 1,
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node4']['request_only'], "n",
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node4']['priority'], "normal",
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node5']['custodial'], 0,
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node5']['request_only'], "n",
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node5']['priority'], "high",
                                  "ERROR: problem in phedex configuration")

            elif primds == "MinimumBias-Error":

                self.assertEquals(set(phedexConfig.keys()), set([ "Node5" ]),
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node5']['custodial'], 0,
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node5']['request_only'], "n",
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node5']['priority'], "high",
                                  "ERROR: problem in phedex configuration")

            else:

                self.assertEquals(set(phedexConfig.keys()), set([ "Node1" ]),
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node1']['custodial'], 0,
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node1']['request_only'], "n",
                                  "ERROR: problem in phedex configuration")

                self.assertEquals(phedexConfig['Node1']['priority'], "high",
                                  "ERROR: problem in phedex configuration")

        promptSkimConfigs = self.getPromptSkimConfigDAO.execute(176161, "A",
                                                                transaction = False)

        self.assertEquals(set(promptSkimConfigs.keys()), set([ "Cosmics", "MinimumBias" ]),
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(set(promptSkimConfigs['Cosmics'].keys()), set([ "RECO" ]),
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(set(promptSkimConfigs['MinimumBias'].keys()), set([ "AOD" ]),
                          "ERROR: problem in promptskim configuration")

        promptSkimConfig = promptSkimConfigs['Cosmics']['RECO']

        self.assertEquals(set(promptSkimConfig.keys()), set([ "Skim1" ]),
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim1']['node'], "Node2",
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim1']['cmssw'], "CMSSW_4_2_8_patch4",
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim1']['two_file_read'], 1,
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim1']['proc_ver'], "v7",
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim1']['global_tag'], "GlobalTag6",
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim1']['config_url'], "exampleurl1",
                          "ERROR: problem in promptskim configuration")

        promptSkimConfig = promptSkimConfigs['MinimumBias']['AOD']

        self.assertEquals(set(promptSkimConfig.keys()), set([ "Skim2" ]),
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim2']['node'], "Node6",
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim2']['cmssw'], "CMSSW_4_2_8_patch5",
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim2']['two_file_read'], 0,
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim2']['proc_ver'], "v8",
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim2']['global_tag'], "GlobalTag7",
                          "ERROR: problem in promptskim configuration")

        self.assertEquals(promptSkimConfig['Skim2']['config_url'], "exampleurl2",
                          "ERROR: problem in promptskim configuration")

        #
        # no DAO for this check because the query is only used here
        #
        results = myThread.dbi.processData("""SELECT run_stream_fileset_assoc.run_id,
                                                     stream.name,
                                                     wmbs_fileset.name
                                              FROM run_stream_fileset_assoc
                                              INNER JOIN wmbs_fileset ON
                                                wmbs_fileset.id = run_stream_fileset_assoc.fileset
                                              INNER JOIN wmbs_subscription ON
                                                wmbs_subscription.fileset = wmbs_fileset.id
                                              INNER JOIN stream ON
                                                stream.id = run_stream_fileset_assoc.stream_id
                                              ORDER BY run_stream_fileset_assoc.run_id,
                                                       stream.name,
                                                       wmbs_fileset.name
                                              """, transaction = False)[0].fetchall()

        self.assertEqual(results[0][0], 176161,
                         "ERROR: problem in setting up run/stream fileset/subscription")
        self.assertEqual(results[1][0], 176161,
                         "ERROR: problem in setting up run/stream fileset/subscription")
        self.assertEqual(results[2][0], 176161,
                         "ERROR: problem in setting up run/stream fileset/subscription")
        self.assertEqual(results[0][1], "A",
                         "ERROR: problem in setting up run/stream fileset/subscription")
        self.assertEqual(results[1][1], "Express",
                         "ERROR: problem in setting up run/stream fileset/subscription")
        self.assertEqual(results[2][1], "HLTMON",
                         "ERROR: problem in setting up run/stream fileset/subscription")
        self.assertEqual(results[0][2], "Run176161_StreamA",
                         "ERROR: problem in setting up run/stream fileset/subscription")
        self.assertEqual(results[1][2], "Run176161_StreamExpress",
                         "ERROR: problem in setting up run/stream fileset/subscription")
        self.assertEqual(results[2][2], "Run176161_StreamHLTMON",
                         "ERROR: problem in setting up run/stream fileset/subscription")

        return

if __name__ == '__main__':
    unittest.main()