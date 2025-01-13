

#fraction = Acceptance value ; yield (total)
#1 = 0.9313999599999999 ; 71744.33
#0.75 = 0.931 ;
#0.5 - 0.931 ;
#0.25 = 0.931 ;
#0.1 = 0.931 ;


'''
n_s = w*N_s (since it is normalized by some weight w)
n_tot = w*N_tot (since it is normalized by some weight w)
er(A) = partial derivative of A wrt n_s * er(n_s) + partial derivative of A wrt n_tot * er(n_tot) [however there is binomial correlation between n_s and n_tot]
er(A) = sqrt(A*(1-A)/N_tot) [since n_s/n_tot = A]
'''
#given that acceptance is n_{sel} / n_{tot} = 0.931
#Calculate the statistical error on the Acceptance and include it as error bars in the plot:
#uncertainty = sqrt(acceptance*(1-acceptance)/total)
