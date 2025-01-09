import uproot
import hist
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep 

# open a .root file containing histograms
file = uproot.open("output.root")

# print the contents of the file
print(file.keys())

# read in the histogram
h = file["h"]

# this shold be a TH1D object, since we created it with ROOT
print(h)






# let's convert the uproot obeject it to hist histogram
h = h.to_hist()

# print the hist object
print(h)


h1D = hist.Hist.new.Reg(100, 0, 200, name="momentum", label="$p$ [GeV]").Weight()
h2D = hist.Hist.new.Reg(100, 0, 200, name="momentum", label="$p$ [GeV]").Reg(100, 0, 6.28, name="phi", label="$\phi$").Weight()

#h1D.fill(100) # this means: we count one event with 100 GeV of energy
#h2D.fill(130, 1.4) # this means: we count one event with 130 GeV of energy, angle angle of 1.4 








# generate some fake data: 10000 events with Gaussian-distributed energy peaked at 50 with variance 10, and unfiromly-distributed azimuthal angle
energies = np.random.normal(size=10000, loc=50, scale=10)
angles = np.random.uniform(size=10000, low=0, high=6.28)

# fill histograms
h1D.fill(energies)
h2D.fill(energies, angles)

centers_1D = h1D.axes[0].centers
edges_1D = h1D.axes[0].edges
counts_1D = h1D.values()
uncert_1D = np.sqrt(h1D.variances())

print("1D histogram bin centers", centers_1D)
print("1D histogram bin edges", edges_1D)
print("1D histogram counts", counts_1D)
print("1D histogram uncertanties", uncert_1D)
''''''
edges_2D_axis0 = h1D.axes[0].edges
edges_2D_axis1 = h1D.axes[1].edges
counts_2D = h2D.values()
uncert_2D = np.sqrt(h2D.variances())

print("2D histogram bin edges of axis 0", edges_2D_axis0)
print("2D histogram bin edges of axis 1", edges_2D_axis1)
print("2D histogram counts", counts_2D)
print("2D histogram uncertanties", uncert_2D)

print(h1D[0.0j:100.0j]) # returns a new histogram, which is the old histogram with only bins between 0 and 100.
print(h1D[0:100]) # returns a new histogram, which is the old histogram with only the first 100 bins.

n_total = h1D[::sum]
n_above_100gev = h1D[100j::sum]

h2D[10j:50j, 0.0j:3.14j] # slice between 10 and 50 GeV in energy, and 0 to 3.14 in phi







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

# the finishing touch, add the experiment label!
# for now setting the luminosity to 1 as an example, since we didn't do any normalization
hep.label.exp_label(exp="FCC-ee", ax=ax, lumi=1, data=False, com=240)

# (the bbox_inches="tight" makes sure the labels are not cut off)
fig.savefig("pretty_energy.pdf", bbox_inches="tight")