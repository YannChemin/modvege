import numpy as np

# ModVege is using 4 parts:
# Green Vegetative  (GV)
# Green Reproductive(GR)
# Dead Vegetative   (DV)
# Dead Reproductive (DR)

#########################################################
# Definition of input parameters
#########################################################
#ST1	        Onset of reproductive growth (degreeday)
#ST2	        End of reproductive growth (degreeday)
#INcell	        Initial Nutritional index of cell -NNI
#WHC	        Soil water-holding capacity (mm)
#WR	            Soil water reserve (mm)
#minSEA	        Growth increase in winter
#maxSEA	        Growth increase in summer
#W_GV	        Initial Biomass of GV (kg ha-1)
#alpha_PAR	    Light Extinction Coefficient
#T0	            Temperature threshold: photosynthesis activation (degC)
#T1	            Temp threshold: stable growth (degC)
#T2	            Temp threshold: growth decline (degC)
#beta_T	        Decrease in LUE after T2
#b_IN	        Impact of IN on LUE at IN=0
#SLA	        Specific leaf area (m2 g-1)
#LLS	        Leaf lifespan (degreeday)
#rho_GV	        Volume GV (g m-3)
#percentLAM	    Fraction of leaf of laminae in GV
#W_GR	        Biomass of GR (kg ha-1)
#a_IN	        Value of ALLOC at IN=0
#max_fIN	    Max of fNI
#rho_GR	        Volume GR (g m-3)
#W_DV	        Biomass of DV (kg ha-1)
#K_DV	        Senescence coefficient DV (degreeday)
#Kl_DV	        Abscission coefficient DV (degreeday)
#rho_DV	        Volume DV (g m-3)
#W_DR	        Biomass of DR (kg ha-1)
#K_DR	        Senescence coefficient DR (degreeday)
#Kl_DR	        Abscission coefficient DR (degreeday)
#rho_DR	        Volume DR (g m-3)
#init_AGE_GV	Initial value of age GV
#init_AGE_GR	Initial value of age VR
#init_AGE_DV	Initial value of age DV
#init_AGE_DR	Initial value of age DR
#RUEmax	        Maximum radiation use efficiency (g MJ-1)
#gammaGV	    Respiratory C loss during senescence (DV)
#gammaGR	    Respiratory C loss during senescence (DR)
#maxOMDgv	    maximum OMD green veg
#minOMDgv	    minimum OMD green veg
#maxOMDgr	    maximum OMD green rep
#minOMDgr	    minimum OMD green rep
#meanOMDdv	    mean OMD dry veg (digestibility of dead part is constant)
#meanOMDdr	    mean OMD dry rep (digestibility of dead part constant)
#cellSurface    Pixel area [Ha]

#file='params.csv'

def read_params(file):
    """
    Read the input parameters file

    :param file: the input file named param.csv
    :return arr: the returning array of [DOY, Temperature, PARi, PP, PET]
    """
    arr = np.genfromtxt(file, delimiter=",", dtype=float, usecols=(-1))
    return(arr)

#########################################################
# Definition of input parameters
#########################################################
#DOY	        Day Of Year
#Temperature    temperature (degree celsius)
#PARi           photosynthetic radiation incident (MJ.m-2)
#PP             Precipitation (mm)
#PET            Potential ET (mm/day)
#ETA            Actual ET from Remote Sensing (mm/day)
#LAI            Leaf Area Index from Remote Sensing (cm2/cm2) 
#gcut           Grass cut event cutHeight (m)
#grazing        Grazing animal count (-)
#grazingw       Grazing average animal weight (kg)

#file='weather.csv'

def read_weather(file):
    """
    Read the weather csv file 

    :param file: the input file named weather.csv
    :return arr: the returning array of [DOY, Temperature, PARi, PP, PET]
    """
    arr = np.genfromtxt(file, delimiter=",", skip_header=0, names=True)
    return(arr)

