# PF Photon ID Validation for Run3
As a part of CMS service task for [EGM POG](https://cms-egamma.github.io/), I worked on a NN based photon ID for PF photons in 2021, based on the MC generated in the Run3Summer21 campaign. I am validating the models in the Run3Summer23 campaign for photon candidates in the high-eta (forward) region, with `2.4 < abs(eta) < 3.0`.

## Information on the trained models
Four models are trained with the same architecture, two for barrel and two for endcap photons (non-weighted and pt-weighted in each case). The technical details are given below:
```
Model architecture: 128/64/64/32/16/1
Activation: 'relu' (except for the last layer, where it is 'sigmoid')
kernel_initializer='he_normal' (not applied on the last layer)
optimizer='adam'
loss='binary_crossentropy',
metrics=['accuracy']
```
These four models are kept in `TrainedModels/` in h5 and pb format, with the scaling parameters and training-vs-testing plots.

### Training dataset
The following samples were used for picking the photons candidates (all reco photons above 10 GeV) which may or may not pass the existing PF Photon ID).

#### Signal photons:
Signal photons are prompt, and they match with a gen-photon with a dR cone of radius 0.3. The following Gamma-Jet samples are used to pick these signal photons.
- `/GJet_Pt-10to40_DoubleEMEnriched_TuneCP5_14TeV_Pythia8/*`
- `/GJet_Pt-40toInf_DoubleEMEnriched_TuneCP5_14TeV_Pythia8/*`

#### Backgrounds (fakes)
QCD and TauGun samples were used to pick backgrounds as listed below. These are either fakes, or FSR/ISR photons, or in case of the TauGun sample, most likely coming from pion decays. The fakes are not supposed to match any gen-photons within a dR cone of radius 0.3. The candidates which match with any gen-photon are required to be not prompt.
  - `/QCD_Pt-80to120_EMEnriched_TuneCP5_14TeV_pythia8/*`
  - `/QCD_Pt-120to170_EMEnriched_TuneCP5_14TeV_pythia8/*`
  - `/QCD_Pt-170to300_EMEnriched_TuneCP5_14TeV_pythia8/*`
  - `QCD_Pt-300toInf_EMEnriched_TuneCP5_14TeV_pythia8/*`
  - `/TauGun_Pt-15to500_14TeV-pythia8/*`
 
where *=`Run3Summer21MiniAOD-FlatPU0to70_120X_mcRun3_2021_realistic_v5-v2/MINIAODSIM`
 
### Training variables
The photon variables that were fed into the models are listed below. The scaling parameters for these input variables are summarized in the `model_info.json` file.
- hadTowOverEm
- trkSumPtHollowConeDR03
- ecalRecHitSumEtConeDR03
- SigmaIEtaIEta3x3 
- SigmaIEtaIEtaFull5x5
- SigmaIEtaIPhiFull5x5
- EcalPFClusterIso
- HcalPFClusterIso
- hasPixelSeed
- R9Full5x5
- hcalTowerSumEtConeDR03

*Note: The same order has to maintained while feeding these variables to the neural network.*

### Working points chosen by EGM

## Validation
Keeping the definition of signal and background the same, I am using the following datasets to extract the photon candidates.
- `/GJet_PT-10to40_DoubleEMEnriched_TuneCP5_13p6TeV_pythia8/*`
- `/GJet_PT-40_DoubleEMEnriched_TuneCP5_13p6TeV_pythia8/*`
- `/QCD_PT-80to120_EMEnriched_TuneCP5_13p6TeV_pythia8/*`
- `/QCD_PT-120to170_EMEnriched_TuneCP5_13p6TeV_pythia8/*`
- `/QCD_PT-170to300_EMEnriched_TuneCP5_13p6TeV_pythia8/*`
- `/QCD_PT-300toInf_EMEnriched_TuneCP5_13p6TeV_pythia8/*`
- `/TauGun_E-10to100_13p6TeV_pythia8/*`
- `/TauGun_E-100to3000_13p6TeV_pythia8/*`

where *= `Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM`
The models, the training variables and their scaling parameters are picked using the `model_info.json` file. 

### Preparing the Run3Summer23 dataset from MiniAOD
I am using a mini-AOD to ntuple maker tool to write photon branches that I need into root files. This tool can be found [here](https://github.com/phazarik/MiniAOD-NtupleMaker). After the root files are generated, these are turned into flat csv files (with each entry representing a photon) using `root2csv.py`. These csv files are read into the jupyter notebook as pandas dataframes.

The details of the validation are available in the notebook.