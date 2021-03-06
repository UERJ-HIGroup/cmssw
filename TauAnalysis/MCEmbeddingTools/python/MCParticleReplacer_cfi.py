import FWCore.ParameterSet.Config as cms

from Configuration.Generator.PythiaUESettings_cfi import *
from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *

# Note: currently this is just a sketch and should not be used

newSource = cms.EDProducer("MCParticleReplacer",
    src                = cms.InputTag("selectedMuons"),
    beamSpotSrc        = cms.InputTag("dummy"),
    primaryVertexLabel = cms.InputTag("dummy"),
    hepMcSrc           = cms.InputTag("generator"),

    algorithm = cms.string("ParticleGun"), # "ParticleGun", "ZTauTau"
    hepMcMode = cms.string("new"),         # "new" for new HepMCProduct with taus and decay products,
                                           # "replace" for replacing muons in the existing HepMCProcuct
    verbose = cms.bool(False),

    ParticleGun = cms.PSet(
        gunParticle	      = cms.int32(15),
        particleOrigin        = cms.string("muonReferencePoint"), # "primaryVertex", "muonReferencePoint"
        forceTauPolarization  = cms.string("W"), # "W", "H+", "h", "H", "A"
        forceTauDecay	      = cms.string("none"), # "none", "hadrons", "1prong", "3prong"
        forceTauPlusHelicity  = cms.int32(0),
        forceTauMinusHelicity = cms.int32(0),
        generatorMode = cms.string("Tauola"),  # "Tauola", "Pythia" (not implemented yet)
        ExternalDecays = cms.PSet(
            Tauola = cms.PSet(
                TauolaPolar,
                TauolaDefaultInputCards
            ),
            parameterSets = cms.vstring('Tauola')
        ),
        PythiaParameters = cms.PSet(
            pythiaUESettingsBlock,
            pgunTauolaParameters = cms.vstring(["MDME(%d,1)=0" % x for x in range(89, 143)]),
            parameterSets = cms.vstring("pythiaUESettings")
        ),
    ),

    ZTauTau = cms.PSet(
                    TauolaOptions = cms.PSet(
                                TauolaPolar,
                                InputCards = cms.PSet
                                        (
                                            pjak1 = cms.int32(0),
                                            pjak2 = cms.int32(0),
                                            mdtau = cms.int32(102)
                                        )
                                ),
        filterEfficiency = cms.untracked.double(1.0),
        pythiaHepMCVerbosity = cms.untracked.bool(False),
        generatorMode = cms.string("Tauola"),  # "Tauola", "Pythia" (not implemented yet)

    )

)

# Disable tau decays in Pythia for particle gun
def customise(process):
    if process.newSource.generatorMode.value() != "Pythia" and abs(process.newSource.ParticleGun.gunParticle.value()) == 15:
        process.newSource.ParticleGun.PythiaParameters.parameterSets.append("pgunTauolaParameters")
