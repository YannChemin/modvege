import numpy as np

# This is used only for development, to remove for operational mode

##############################################
# Definition of columns in out_cut.csv
##############################################
# day
# Mean biomass                      (kg DM/ha)
# Mean green vegetative biomass     (kg DM/ha)
# Mean green reproductive biomass   (kg DM/ha)
# Mean dry vegetative biomass       (kg DM/ha)
# Mean dry reproductive biomass     (kg DM/ha)
# Harvested Biomass                 (kg DM/ha)
# Ingested Biomass                  (kg DM/ha)
# Mean GRO biomass                  (kg DM/ha)
# Mean available biomass for cut    (kg DM/ha)

out_csv='out_cut.csv'

def read_out(out_csv):
    arr = np.genfromtxt(out_csv, delimiter=",", skip_header=0, names=True)
    return(arr)

