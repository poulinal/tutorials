import ROOT

import matplotlib.pyplot as plt
import mplhep as hep 


ROOT.EnableImplicitMT(1) #restrict to single thread


ROOT.gInterpreter.ProcessLine("""
#include "02_RDFs/energy.h"
"""
)

# Open the file
f = ROOT.TFile.Open("/ceph/submit/data/group/cms/store/fccee/samples/winter2023/CLD_FullSim/wzp6_ee_mumuH_ecm240/mumuH_rec_16610_191.root")

# Get the tree
tree = f.Get("events")

# Create the RDF
df = ROOT.RDataFrame(tree)

# Define the energy of the particles, and save if above 10 GeV
df = df.Define("Energy", "get_energy(MCParticles)")

df = df.Define("InvarientMassLorentz", "get_InvarientMassLorentz(MCParticles)")

df = df.Define("InvarientMass", "get_InvarientMass(MCParticles)")

# Fill the histogram with the calculated energies
# We defined 100 bins between 0 and 1000 GeV
#h = df.Histo1D(("MCParticles_Energies", "", *(100, 0, 1000)), "Energy")


h = df.Histo1D(("MCParticles_Energies", "", *(300, 0, 1000)), "InvarientMass")

# Draw the histogram
c = ROOT.TCanvas()
h.Draw()

# label the axes
h.GetXaxis().SetTitle("Energy [GeV]")
h.GetYaxis().SetTitle("Number of particles")


#make yscale log
c.SetLogy()

#set xrange
h.GetXaxis().SetRangeUser(50, 150)


c.Draw()

# save the histogram
c.SaveAs("pretty_energy.png")




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
fig.savefig("pretty_energyplt.png", bbox_inches="tight")