import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep 

# Open the file
file = ROOT.TFile("/ceph/submit/data/group/cms/store/fccee/samples/winter2023/CLD_FullSim/wzp6_ee_mumuH_ecm240/mumuH_rec_16610_191.root")

# Get the tree of events
tree = file.Get("events")

# Create a histogram to store the energies
h = ROOT.TH1D("h", "Energy [GeV]", 300, 0, 1000)



events = 50



# for loop over the first 10 events, and print information about the MC particles
for i in range(1000):
    
    print("Processing event", i)
    tree.GetEntry(i)

    # get the MC particles for this event
    MCParticles = tree.MCParticles
    print("Number of MC particles:", len(MCParticles))
    
    
    muonMass = []
    muonMom = []
    antiMuonMass = []
    antiMuonMom = []
    antiMuonEnergy = []
    muonEnergy = []
        
        
    # loop over all particles in the event
    for j in range(len(MCParticles)):

        # print their information
        #print("MC Particle", j)
        #print("Momentum (px, py, pz):", MCParticles[j].momentum.x, MCParticles[j].momentum.y, MCParticles[j].momentum.z)
        #print("Charge:", MCParticles[j].charge)
        #print("PDG ID:", MCParticles[j].PDG)

        # calculate the energy
        energy = (MCParticles[j].momentum.x**2 + MCParticles[j].momentum.y**2 + MCParticles[j].momentum.z**2 + MCParticles[j].mass**2)**0.5
        #print("Energy:", energy)

        # if the particle has more than 10 GeV of energy, fill the histogram
        #if energy > 10:
            #h.Fill(energy)
        curID = MCParticles[j].PDG
        
        
        if MCParticles[j].PDG == 13:
            mass = MCParticles[j].mass
            muonMass.append(MCParticles[j].mass)
            muonMom.append(MCParticles[j].momentum)
            #muonMom = MCParticles[j].momentum
            #print(type(muonMass[j]))
            #muonEnergy.append((muonMom[j].x**2 + muonMom[j].y**2 + muonMom[j].z**2)**0.5 + muonMass**2)
            muonEnergy.append(energy)
            
        if MCParticles[j].PDG == -13:
            antimass = MCParticles[j].mass
            antiMuonMass.append(MCParticles[j].mass)
            antiMuonMom.append(MCParticles[j].momentum)
            #antiMuonMom = MCParticles[j].momentum
            #antiMuonEnergy.append((antiMuonMom[j].x**2 + antiMuonMom[j].y**2 + antiMuonMom[j].z**2)**0.5 + antiMuonMass**2)
            antiMuonEnergy.append(energy)
            

            
    #print maximum energy of muon
    print("Maximum energy of muon:", max(muonEnergy))
    #print maximum energy of anti-muon
    print("Maximum energy of anti-muon:", max(antiMuonEnergy))
    #h.Fill(max(muonEnergy))
    #h.Fill(max(antiMuonEnergy))
    '''
    print("Muon energy:", muonEnergy)
    print("Anti-muon energy:", antiMuonEnergy)
    print("Muon momentum:", muonMom)
    print("Anti-muon momentum:", antiMuonMom)
    '''
    #check if there is a pair of muon and anti-muon, if not remove the extra
    '''
    if len(muonEnergy) > len(antiMuonEnergy):
        muonEnergy.pop()
        muonMom.pop()
    if len(antiMuonEnergy) > len(muonEnergy):
        antiMuonEnergy.pop()
        antiMuonMom.pop()
    print("Muon energy:", muonEnergy)
    print("Anti-muon energy:", antiMuonEnergy)
    '''
    
    
    #get invarient mass of muon and anti-muon where we get the momentum of the max energy muon and anti-muon:
    invarientMass = ( (max(muonEnergy) + max(antiMuonEnergy))**2 
                     - (  (muonMom[muonEnergy.index(max(muonEnergy))].x + antiMuonMom[antiMuonEnergy.index(max(antiMuonEnergy))].x)**2 
                        + (muonMom[muonEnergy.index(max(muonEnergy))].y + antiMuonMom[antiMuonEnergy.index(max(antiMuonEnergy))].y)**2 
                        + (muonMom[muonEnergy.index(max(muonEnergy))].z + antiMuonMom[antiMuonEnergy.index(max(antiMuonEnergy))].z)**2 ) )**0.5
    
    
    #invarientMass = (max(muonEnergy) + max(antiMuonEnergy))**2 - (muonMom.index(max(muonEnergy)).x + antiMuonMom.index(max(antiMuonEnergy)).x)**2 - (muonMom.index(max(muonEnergy)).y + antiMuonMom.index(max(antiMuonEnergy)).y)**2 - (muonMom.index(max(muonEnergy)).z + antiMuonMom.index(max(antiMuonEnergy)).z)**2
    #invarientMass = (max(muonEnergy) + max(antiMuonEnergy))
    print("Invarient mass of muon and anti-muon:", invarientMass)
    h.Fill(invarientMass)



# draw the histogram, this is done using a Canvas
c = ROOT.TCanvas()
h.Draw()

# label the axes
h.GetXaxis().SetTitle("Energy [GeV]")
h.GetYaxis().SetTitle("Number of particles")


#make yscale log
c.SetLogy()

#set xrange
h.GetXaxis().SetRangeUser(50, 150)


# draw the canvas
c.Draw()

# save the plot to a file
c.SaveAs("energy.png")

# save the histogram to a .root file
file_out = ROOT.TFile("output.root", "RECREATE")
h.Write()
file_out.Close()

print("All done!")






# these set the default style of the plotting libraries to the CMS style
hep.style.use("CMS")
plt.style.use(hep.style.CMS)

# initialize a figure and axis using matplotlib
fig = plt.figure()
ax = fig.subplots()

# use mplhep to plot the histogram on the axis, add a nice label
hep.histplot(h, label="$e^+e^-\\to\mu^+\mu^-$", ax=ax)

ax.set_ylabel("Events")
ax.legend(loc=(1.01, 0), fontsize='x-small')
ax.set_yscale("log")
ax.set_xlabel("$E$ [GeV]")

#set x range
ax.set_xlim(60, 120)

# the finishing touch, add the experiment label!
# for now setting the luminosity to 1 as an example, since we didn't do any normalization
hep.label.exp_label(exp="FCC-ee", ax=ax, lumi=1, data=False, com=240)


# (the bbox_inches="tight" makes sure the labels are not cut off)
fig.savefig("energyplt.png", bbox_inches="tight")

print("All done 2!")