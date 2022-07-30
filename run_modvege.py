#!/usr/bin env python3

# Mod Vege main code, had to rewrite most of the functions as the Java code was a complete mess
# This code runs a single geographical "Cell" (as the Java code was trying to do on a grid)
# This function *should* be self sustaining, nothing else needed.

import numpy as np

#Import the model function
from modvege import *

# Import ModVege read input files library:
#   params.csv
#   weather.csv
from lib_read_input_files import *

# ONLY FOR DEV
from lib_read_output_files import *

# Define the name of the input params file
input_params_csv='params.csv'
# Define the name of the input environment file
input_weather_csv='weather.csv'

def run_modvege(input_params_csv, input_weather_csv):
    """
    Pre-Process the inputs to run Mod Vege model as a function

    :param input_params_csv: Filename of the csv input parameters
    :param input_weather_csv: Filename of the csv input weather file
    """
    # Read Parameter files into array
    params = read_params(input_params_csv)

    # Read weather file into array
    # arr[0][0] = DOY[0] = 1
    # arr[0][1] = Temperature[0] = -0.84125
    # arr[0][2] = PARi[0] = 2.22092475
    # arr[0][3] = PP[0] = 0.119
    # arr[0][4] = PET[0] = 0.602689848
    # arr[0][5] = ETA[0] = 0.301344 # RS simulated
    # arr[0][6] = LAI[0] = 0.864162 # RS simulated
    # arr[0][7] = gcut_height[0] = 0.0 [default is 0.05 if cut]
    # arr[0][8] = grazing_animal_count[0] = 0 [default is 1 for test ]
    # arr[0][9] = grazing_avg_animal_weight[0] = 0 [ default is 400 for cow ]

    weather = read_weather(input_weather_csv)

    # ONLY FOR DEV
    out = read_out(out_csv)
    
    startdoy = 1
    enddoy = 365

    # Initialize the run and return arrays
    gv_b, dv_b, gr_b, dr_b, h_b, i_b, gro, abc, sumT, gva, gra, dva, dra, sea, ftm, env, pgr, atr = modvege(params, weather, startdoy, enddoy)
    
    # Print the output
    #print(output)
    
    ################################################  ###################
    # Definition of columns in out_cut.csv            Eq. from output run
    ################################################  ###################
    # 0 day
    # 1 Mean biomass                      (kg DM/ha)  gv_b+gr_b+dv_b+dr_b
    # 2 Mean green vegetative biomass     (kg DM/ha)  gv_b
    # 3 Mean green reproductive biomass   (kg DM/ha)  gr_b
    # 4 Mean dry vegetative biomass       (kg DM/ha)  dv_b
    # 5 Mean dry reproductive biomass     (kg DM/ha)  dr_b
    # 6 Harvested Biomass                 (kg DM/ha)  h_b
    # 7 Ingested Biomass                  (kg DM/ha)  i_b
    # 8 Mean GRO biomass                  (kg DM/ha)  gro
    # 9 Mean available biomass for cut    (kg DM/ha)  abc

    #PLOT
    out_doy = [out[i][0] for i in range(len(out)-1) ]
    out_gvb = [out[i][2] for i in range(len(out)-1) ]
    out_grb = [out[i][3] for i in range(len(out)-1) ]
    out_dvb = [out[i][4] for i in range(len(out)-1) ]
    out_drb = [out[i][5] for i in range(len(out)-1) ]
    out_hb = [out[i][6] for i in range(len(out)-1) ]
    out_ib = [out[i][7] for i in range(len(out)-1) ]
    out_gro = [out[i][8] for i in range(len(out)-1) ]
    out_abc = [out[i][9] for i in range(len(out)-1) ]

    import numpy as np
    import matplotlib.pyplot as plt

    plt.figure(figsize=(15,7))

    plt.subplot(331)
    plt.plot(out_doy,gv_b,'g-',label="gv_b")
    plt.plot(out_doy,out_gvb,'b-',label="out_gvb")
    plt.title('Green Vegetative biomass (kg DM/ha)')
    plt.legend()
    plt.grid()

    plt.subplot(332)
    plt.plot(out_doy,gr_b,'g-',label="gr_b")
    plt.plot(out_doy,out_grb,'b-',label="out_grb")
    plt.title('Green Reproductive biomass (kg DM/ha)')
    plt.legend()
    plt.grid()

    plt.subplot(333)
    plt.plot(out_doy,sumT,'g-',label="sumT")
    plt.plot(out_doy,gva,'b-',label="gv_age")
    plt.plot(out_doy,gra,'y-',label="gr_age")
    plt.plot(out_doy,dva,'c-',label="dv_age")
    plt.plot(out_doy,dra,'r-',label="dr_age")
    plt.title('Sum of Temperature (Celsius)')
    plt.legend()
    plt.grid()

    plt.subplot(334)
    plt.plot(out_doy,dv_b,'g-',label="dv_b")
    plt.plot(out_doy,out_dvb,'b-',label="out_dvb")
    plt.title('Dead Vegetative biomass (kg DM/ha)')
    plt.legend()
    plt.grid()

    plt.subplot(335)
    plt.plot(out_doy,dr_b,'g-',label="dr_b")
    plt.plot(out_doy,out_drb,'b-',label="out_drb")
    plt.title('Dead Reproductive biomass (kg DM/ha)')
    plt.legend()
    plt.grid()

    plt.subplot(336)
    plt.plot(out_doy,pgr,'m-',label="Pot. Growth")
    plt.plot(out_doy,gro,'g-',label="gro")
    plt.plot(out_doy,out_gro,'b-',label="out_gro")
    plt.title('GRO biomass (kg DM/ha)')
    plt.legend()
    plt.grid()

    plt.subplot(337)
    plt.plot(out_doy,abc,'g-',label="abc")
    plt.plot(out_doy,out_abc,'b-',label="out_abc")
    plt.title('Mean available biomass for cut (kg DM/ha)')
    plt.legend()
    plt.grid()

    # Harvested Biomass Plot
    plt.subplot(338)
    plt.plot(out_doy,h_b,'g-',label="h_b")
    plt.plot(out_doy,out_hb,'b-',label="out_hb")
    plt.title('Harvested biomass (kg DM/ha)')
    plt.legend()
    plt.grid()

    plt.subplot(339)
    plt.plot(out_doy,atr,'c-',label="a2r")
    plt.plot(out_doy,sea,'g-',label="Season")
    plt.plot(out_doy,ftm,'r-',label="Temperature")
    plt.plot(out_doy,env,'y-',label="Environmental")
    plt.title('ENV and other Factors')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

# run the main function
run_modvege(input_params_csv, input_weather_csv)
