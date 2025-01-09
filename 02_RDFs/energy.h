#include "FCCAnalyses/MCParticle.h"
//include std
#include <vector>
#include <iostream>
#include <cmath>
#include <typeinfo>

ROOT::VecOps::RVec<float> get_energy(const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: particles) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    float energy = tlv.E();
    if (energy > 10) {
      result.push_back(energy);
    }
  }
  return result;
}



ROOT::VecOps::RVec<float> get_InvarientMassLorentz(const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: particles) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);



    float invarientMass = tlv.M();


    float energy = tlv.E();
    if ((energy > 10) && (invarientMass > 10)) {
      result.push_back(invarientMass);
    }
  }
  return result;
}

//in theory we'd break up the following so itd be more modular but whatever
ROOT::VecOps::RVec<float> get_InvarientMass(const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles) {
  ROOT::VecOps::RVec<float> invarientMass;

  //create an empty vector to store muon energy
    std::vector<float> MuonEnergy;
    //create an empty vector to store anti-muon energy
    std::vector<float> AntiMuonEnergy;
    //create an empty vector to store the momentum of the muon which is a N7edm4hep8Vector3fE
    std::vector<ROOT::Math::XYZVector> MuonMomentum;
    //create an empty vector to store the momentum of the anti-muon which is a N7edm4hep8Vector3fE
    std::vector<ROOT::Math::XYZVector> AntiMuonMomentum;
    //std::cout << "Type of a: " << typeid(p.momentum).name() << std::endl;
  for (auto & p: particles) {

    //make sure vectors are empty
    if (MuonEnergy.size() > 0) {
      MuonEnergy.clear();
    }
    if (AntiMuonEnergy.size() > 0) {
      AntiMuonEnergy.clear();
    }
    if (MuonMomentum.size() > 0) {
      MuonMomentum.clear();
    }
    if (AntiMuonMomentum.size() > 0) {
      AntiMuonMomentum.clear();
    }

    if (p.PDG == 13) {
      MuonEnergy.push_back(sqrt(p.momentum.x*p.momentum.x + p.momentum.y*p.momentum.y + p.momentum.z*p.momentum.z + p.mass*p.mass));
      MuonMomentum.push_back(ROOT::Math::XYZVector(p.momentum.x, p.momentum.y, p.momentum.z));

    }
    if (p.PDG == -13) {
      AntiMuonEnergy.push_back(sqrt(p.momentum.x*p.momentum.x + p.momentum.y*p.momentum.y + p.momentum.z*p.momentum.z + p.mass*p.mass));
      AntiMuonMomentum.push_back(ROOT::Math::XYZVector(p.momentum.x, p.momentum.y, p.momentum.z));
    }
  }
  //get max muon energy
  float maxMuonEnergy = *std::max_element(MuonEnergy.begin(), MuonEnergy.end());
  //get max anti-muon energy
  float maxAntiMuonEnergy = *std::max_element(AntiMuonEnergy.begin(), AntiMuonEnergy.end());
  //get the index of the max muon energy
  int maxMuonIndex = std::distance(MuonEnergy.begin(), std::max_element(MuonEnergy.begin(), MuonEnergy.end()));
  //get the index of the max anti-muon energy
  int maxAntiMuonIndex = std::distance(AntiMuonEnergy.begin(), std::max_element(AntiMuonEnergy.begin(), AntiMuonEnergy.end()));
  //get the momentum of the muon with the max energy
  ROOT::Math::XYZVector maxMuonMomentum = MuonMomentum[maxMuonIndex];
  //get the momentum of the anti-muon with the max energy
  ROOT::Math::XYZVector maxAntiMuonMomentum = AntiMuonMomentum[maxAntiMuonIndex];

  //get the invarientMass where sqrt[(E1 + E2)^2 - [(p1x + p2x)^2 + (p1y + p2y)^2 + (p1z + p2z)^2]]:
  invarientMass.push_back(sqrt(pow((maxMuonEnergy + maxAntiMuonEnergy), 2) - pow((maxMuonMomentum + maxAntiMuonMomentum).R(), 2)));


  return invarientMass;
}