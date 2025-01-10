'''
Compute the cross-section for LEP luminosity: analyze the result and understand its number.
Compute the cross-section for FCC luminosity: compare this result with the LEP cross-section.
Derive the formula for the statistical uncertainty on the cross-section: explore how uncertainties propagate in the calculation.
'''
#cross-section = n_{obs} - n_{bkg} / (L_{inst} * A * \epsilon)

luminosityLEP = 44.84 # LEP=44.84, FCC=100e6
luminosityFCC = 100*10**6
A = 0.931 #for both
epsilon = 1 #for both for now
normalizedYields = 71744
#use total number of events from simularion:
n_obs = 100000000
n_bkg = n_obs - normalizedYields

crossSectionLEP = (n_obs - n_bkg) / (luminosityLEP * A * epsilon)
print(f"Cross-section for LEP luminosity: {crossSectionLEP:.2f} pb")
crossSectionFCC = (n_obs - n_bkg) / (luminosityFCC * A * epsilon)
print(f"Cross-section for FCC luminosity: {crossSectionFCC} pb")


#derive formula for statistical uncertainty on the cross-section:
#uncertainty = sqrt(n_{obs} + n_{bkg}) / (L_{inst} * A * \epsilon)