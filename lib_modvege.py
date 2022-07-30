import numpy as np

def getAverageHeight(biomass, bulkDensity):
    """
    Return the height
    @param biomass biomass
    @param bulkDensity bulk density
    @return the average height
    """
    return biomass/(bulkDensity)
    
def avDefoliationBiomass(biomass, cutHeight, bulkDensity) :
    """
    Estimate av biomass for ingestion
    @param biomass av biomass
    @param cutHeight default cut height in cutEvent
    @param bulkDensity bulk density
    @return av biomass for ingestion
    """
    biomassAfterCut = cutHeight*bulkDensity*10
    return max(0, biomass - biomassAfterCut)
    
def exeDefoliation(biomass, cut_biomass, area):
    """
    Defoliation method
    @param biomass av biomass
    @param cut_biomass biomass removed by cut
    @param area area studied (i.e. pixel area)
    @return updated biomass after defoliation
    """
    biomass = biomass - cut_biomass/area
    if(biomass < 0 | np.isnan(biomass)):
        biomass = 0
    return(biomass)
    
def exeCut(cutHeight, bulkDensity, biomass):
    """
    Realize a cut in order that the average height is under cutHeight.
    This height is calculated by using the bulkDensity given in parameter
    \f[
    biomass_:afterCut = height_:cut * 10 * bulk_:density
    biomass_:harvested = biomass_:beforeCut-biomass_:afterCut
    \f]
    @param cutHeight the average height after the cut in m
    @param bulkDensity the bulk density (biomass after cut = height * 10 * bulk density)
    @return the biomass taken in kg DM / m^2
    """
    biomassAfterCut = cutHeight*bulkDensity*10
    if(biomassAfterCut < biomass):
        takenBiomass = biomass - biomassAfterCut;
        return(takenBiomass, biomassAfterCut)
    else:
        return(0,biomass)
    
def exeDefoliationByBiomass(biomass, biomassToIngest):
    """
    Realize a defoliation by providing the biomass to remove.
    @param biomass av biomass
    @param biomassToIngest the biomass to remove
    @return the biomass left kg DM / m^2
    """
    biomass -= biomassToIngest
    return(biomassToIngest)
    

# Dry Vegetative Functions
def dv_update(gv_gamma,gv_senescent_biomass,lls,kldv,temperature,dv_biomass,dv_avg_age):
    """
    Update DV
    \f[
    growthBiomass_{DV}(t)=(1-\sigma_{GV}) \times senescentBiomass_{GV}(t)
    \f]
     \f[
    abscissionBiomass_{DV}= 
    \begin{cases}
    Kl_{DV} \times  biomass_{DV} \times T \times f(age_{DV}) & \text{if } T >0
    \\ 0 & \text{if } T \leq 0
    \end{cases}
    \f]
    \f[
    age_{DV}(t)=
    \begin{cases} 
    (age_{DV}(t-1)+T) \times \frac{biomass_{DV}(t-1)-senescentBiomass_{DV}(t)-cutBiomass_{DV}(t)}{biomass_{DV}(t-1)+growthBiomass_{DV}(t)-senescentBiomass_{DV}(t)-cutBiomass_{DV}(t)} & \text {if } T > 0
    \\ age_{DV}(t-1) &\text {if } T \leq 0
    \end{cases}
    \f]
    \f[
    biomass_{DV}(t)=biomass_{DV}(t-1)+growthBiomass_{DV}(t)-abscissionBiomass_{DV}(t)
    \f]
    @param gv_gamma Respiratory C loss during senescence (DV) (1-gv_gamma=dv_gamma)
    @param gv_senescent_biomass senescene of compartment GV
    @param lls Leaf lifespan (degreeday)
    @param kldv Abscission coefficient DV (degreeday)
    @param temperature temperature
    @param dv_biomass av DV biomass
    @param dv_avg_age the average DV age
    @return the Dry Vegetation biomass
    @return the average DV age
    """
    abscissionBiomass = mk_dv_abscission(kldv,dv_biomass,temperature,dv_avg_age,lls)
    dv_biomass -= abscissionBiomass
    # at this point the biomass include cut, ingestion and abscission, not growth
    growthBiomass = (1.0-gv_gamma) * gv_senescent_biomass
    if(dv_biomass+growthBiomass > 0):
        dv_avg_age = (max(0, temperature) + dv_avg_age) * (dv_biomass/(dv_biomass+growthBiomass))
    else:
        dv_avg_age = 0
        
    dv_biomass += growthBiomass
    return(dv_biomass, dv_avg_age)

def mk_dv_abscission(kldv,dv_biomass,temperature,dv_avg_age,lls):
    """
    Compute abscission biomass
    @param lls Leaf lifespan (degreeday)
    @param kldv Abscission coefficient DV (degreeday) (Ducroq,1996)
    @param temperature temperature
    @param dv_biomass av biomass
    @param dv_avg_age the average DV age
    @return abscissionBiomass the abscission biomass  
    """
    #method to compute the age of DV for computing abcission of DV
    if (dv_avg_age/lls < 1.0/3.0):
        age = 1
    elif (dv_avg_age/lls < 2.0/3.0):
        age = 2
    else: 
        age = 3
    # Compute the abscission for Dead Vegetative part 
    if(temperature > 0):
        return(kldv*dv_biomass*temperature*age)
    else:
        return(0)

# Dead Reproductive Functions
def dr_update(gr_gamma,gr_senescent_biomass,st1,st2,temperature,kldr,dr_biomass,dr_avg_age):
    """
    Update compartment Dead Reproductive
    \f[
    growthBiomass_{DR}(t)=(1-\sigma_{GR}) \times senescentBiomass_{GR}(t)
    \f]
     \f[
    abscissionBiomass_{DR}= 
    \begin{cases}
    Kl_{DR} \times  biomass_{DR} \times T \times f(age_{DR}) & \text{if } T > 0
    \\ 0 & \text{if } T \leq 0
    \end{cases}
    \f]
    \f[
    age_{DR}(t)=
    \begin{cases} 
    (age_{DR}(t-1)+T) \times \frac{biomass_{DR}(t-1)-senescentBiomass_{DR}(t)-cutBiomass_{DR}(t)}{biomass_{DR}(t-1)+growthBiomass_{DR}(t)-senescentBiomass_{DR}(t)-cutBiomass_{DR}(t)} & \text {if } T > 0
    \\ age_{DR}(t-1) &\text {if } T \leq 0
    \end{cases}
    \f]
    \f[
    biomass_{DR}(t)=biomass_{DR}(t-1)+growthBiomass_{DR}(t)-abscissionBiomass_{DR}(t)
    \f]
    @param gr_gamma a parameter to compute growth of DR (1-gr_gamma)=dr_gamma
    @param gr_senescent_biomass Senescence of GR, computed in GR
    @param st1 sum of temperature at the beginning
    @param st2 sum of temperature in the end
    @param temperature temperature
    @param kldr basic rates of abscission in DR
    @param dr_biomass av DR biomass
    @param dr_avg_age the average DR age
    @return dr_biomass updated biomass for DR
    @return dr_avg_age the average DR age
    """
    abscissionBiomass = mk_dr_abscission(kldr,dr_biomass,temperature,dr_avg_age,st1,st2)
    dr_biomass -= abscissionBiomass
    # at this point the biomass include cut, ingestion and abscission, not growth
    growthBiomass = (1-gr_gamma)*gr_senescent_biomass
    if(dr_biomass+growthBiomass > 0):
        #print(temperature,dr_avg_age,dr_biomass,growthBiomass)
        dr_avg_age = max(0, temperature) + dr_avg_age*dr_biomass/(dr_biomass+growthBiomass)
    else:
        dr_avg_age = 0
                
    dr_biomass += growthBiomass
    return(dr_biomass, dr_avg_age)

def mk_dr_abscission(kldr,dr_biomass,temperature,dr_avg_age,st1,st2):
    """
    Compute abscission biomass
    @param kldr basic rates of abscission in DR (Ducroq,1996)
    @param biomass av biomass
    @param temperature temperature
    @param dr_avg_age the average DR age
    @param st1 sum of temperature at the beginning
    @param st2 sum of temperature in the end
    @return abscissionBiomass the abscission biomass  
    """
    #method to compute the age of DR for computing abscission of DR
    if (dr_avg_age/(st2-st1) < 1.0/3.0):
        age = 1
    elif (dr_avg_age/(st2-st1) < 2.0/3.0): 
        age = 2
    else:
        age = 3
    # Compute abscission for Dead Reproductive 
    if(temperature > 0):
        #print(kldr,dr_biomass,temperature,age)
        return(kldr*dr_biomass*temperature*age)
    else:
        return(0)
    
# Green Vegetative Functions
def gv_update(gro, a2r, lls, temperature, kdv, t0, gv_biomass, gv_avg_age):
    """
    Update Green Vegetation
    \f[
    growthBiomass_{GV}=  
    \begin{cases} 
    0& \text {if } T \leq 0
    \\ GRO \times (1-a2rRep) & \text {if } T > 0
    \end{cases}
    \f]
    \f[
    senescentBiomass_{GV}= k_{GV} \times  biomass_{GV} \times \left | T \right | \times
    \begin{cases} 
    f(age_{GV})& \text {if } T > T_{0}
    \\ 0 & \text {if } 0 \leq T \leq T_{0}
    \\ 1 & \text {if } T < 0
    \end{cases}
    \f]
    \f[
    age_{GV}(t)=
    \begin{cases} 
    (age_{GV}(t-1)+T) \times \frac{biomass_{GV}(t-1)-senescentBiomass_{GV}(t)-cutBiomass_{GV}(t)}{biomass_{GV}(t-1)+growthBiomass_{GV}(t)-senescentBiomass_{GV}(t)-cutBiomass_{GV}(t)} & \text {if } T > 0
    \\ age_{GV}(t-1) &\text {if } T \leq 0
    \end{cases}
    \f]
    \f[
    biomass_{GV}(t)=biomass_{GV}(t-1)+growthBiomass_{GV}(t)-senescentBiomass_{GV}(t)
    \f]
    @param GRO in Jouven_2006a.pdf, total growth
    @param a2r Allocate to reproductive (REP in Jouven_2006a.pdf, reproductive function)
    @param lls Leaf lifespan (degreeday)
    @param temperature Temperature
    @param kdv Senescence coefficient DV (degreeday)
    @param t0 minimum temperature for growth
    @param gv_avg_age the average GV age
    @return biomass Updated biomass
    @return gv_avg_age average GV age
    """
    senescentBiomass = mk_gv_senescence(kdv, gv_biomass, temperature, t0, lls, gv_avg_age)
    gv_biomass -= senescentBiomass
    # at this point the biomass include cut, ingestion and scenescence, not growth
    if (temperature > t0):
        growthBiomass = gro*(1-a2r)
    else:
        growthBiomass = 0
   
    if(gv_biomass+growthBiomass > 0):
        gv_avg_age = (max(0, temperature) + gv_avg_age) * (gv_biomass/(gv_biomass+growthBiomass))
    else:
        gv_avg_age = 0

    gv_biomass += growthBiomass
    return(gv_biomass, gv_avg_age, senescentBiomass)

def mk_gv_senescence(kgv,gv_biomass,temperature,t0,lls,gv_avg_age):
    """
    Extract about 2-6% (kDV=0.002, T=10C, gv_fAge=[1-3]) of gv_biomass as senescent
    
    @param kGV Senescence coefficient (degreeday) (Ducroq,1996)
    @param gv_biomass the Green Vegetation biomass
    @param temperature Temperature
    @param t0 minimum temperature for growth
    @param lls Leaf lifespan (degreeday)
    @param gv_avg_age the average GV age
    @return senescentBiomass the biomass that is senescent
    """
    #method to compute the age of GV for computing senescene of GV
    if (gv_avg_age/lls < 1.0/3.0):
        age = 1
    elif (gv_avg_age/lls < 1):
        age = 3 * gv_avg_age / lls
    else: 
        age = 3
    # Compute senescence of GV
    if(temperature > t0):
        return(kgv*gv_biomass*temperature*age)
    elif(temperature < 0):
        return(kgv*gv_biomass*abs(temperature))
    else:
        return(0)

# Green Reproductive Functions
def gr_update(temperature, a2r, gro, st1, st2, kdr, lls, rhogr, t0, gr_biomass, gr_avg_age):
    """
    Update Green Reproductive
    \f[
    growthBiomass_{GR}=  
    \begin{cases} 
    0& \text {if } T \leq 0
    \\ GRO \times a2rRep & \text {if } T > 0
    \end{cases}
    \f]
    \f[
    senescentBiomass_{GR}= k_{GR} \times biomass_{GR} \times \left | T \right | \times
    \begin{cases} 
    f(age_{RV})& \text {if } T > T_{0}
    \\ 0 & \text {if } 0 \leq T \leq T_{0}
    \\ 1 & \text {if } T < 0
    \end{cases}
    \f]
    \f[
    age_{GR}(t)=
    \begin{cases} 
    (age_{GR}(t-1)+T) \times \frac{biomass_{GR}(t-1)-senescentBiomass_{GR}(t)-cutBiomass_{GR}(t)}{biomass_{GR}(t-1)+growthBiomass_{GR}(t)-senescentBiomass_{GR}(t)-cutBiomass_{GR}(t)} & \text {if } T > 0
    \\ age_{GR}(t-1) &\text {if } T \leq 0
    \end{cases}
    \f]
    \f[
    biomass_{GR}(t)=biomass_{GR}(t-1)+growthBiomass_{GR}(t)-senescentBiomass_{GR}(t)
    \f]
    @param temperature temperature
    @param a2r allocate to reproductive (REP in Jouven_2006a.pdf, reproductive function)
    @param GRO in Jouven_2006a.pdf, total growth
    @param st1 Onset of reproductive growth (degreeday)
    @param st2 End of reproductive growth (degreeday)
    @param kdr basic rates of  in compartment GR
    @param lls Leaf lifespan (degreeday)
    @param rhogr Volume GR (g m-3)
    @param t0 minimum temperature for growth
    @param gr_biomass the av GR biomass
    @param gr_avg_age the average GR age
    @return gr_biomass Updated GR biomass
    @return gr_avg_age the average GR age
    """
    senescentBiomass = mk_gr_senescence(kdr,gr_biomass,temperature,t0,lls,gr_avg_age,st1,st2)
    gr_biomass -= senescentBiomass
    #print("senescentBiomass: = %.2f" % (senescentBiomass))
    # at this point the biomass include cut, ingestion and scenescence, not growth
    if (temperature > t0):
        growthBiomass = gro*(a2r)
        #print("growthBiomass: t>t0 = %.2f" % (growthBiomass))
    else:
        growthBiomass = 0
        #print("growthBiomass: t<t0 = %.2f" % (growthBiomass))

    if(gr_biomass+growthBiomass > 0):
        gr_avg_age = (max(0, temperature) + gr_avg_age) * (gr_biomass/(gr_biomass+growthBiomass))
    else:
        gr_avg_age = 0

    gr_biomass += growthBiomass
    return(gr_biomass, gr_avg_age, senescentBiomass)
    
def mk_gr_senescence(kdr,gr_biomass,temperature,t0,lls,gr_avg_age,st1,st2): 
    """
    @param kGV Senescence coefficient DV (degreeday)
    @param temperature Temperature
    @param lls Leaf lifespan (degreeday)
    @param t0 minimum temperature for growth
    @param gr_avg_age the average GR age
    @param gr_biomass the biomass available for GR 
    @param st1 Onset of reproductive growth (degreeday)
    @param st2 End of reproductive growth (degreeday)
    @return senescentBiomass the senescent biomass
    """
    #method to compute the age of GR for computing senescene of GR
    if(gr_avg_age/(st2-st1) < 1.0/3.0):
        age = 1
    elif(gr_avg_age/(st2-st1) < 1.0):
        age = (3*gr_avg_age/(st2-st1))
    else:
        age = 3
    # Compute senescence of GV
    if(temperature > t0):
        # T=10C kdr=0.001 gr_fAge=[1-3] => 1-3% of gr_biomass
        return(kdr*gr_biomass*temperature*age)
    elif(temperature < 0):
        return(kdr*gr_biomass*abs(temperature))
    else:
       return(0)

###########################################################################################
# Nutrition Index                   #double ni
# water reserves WR                 #double waterReserve
# Compartment green vegetative      #CompartmentGreenVegetative cGV
# Compartment green reproductive    #CompartmentGreenReproductive cGR
# Compartment dry vegetative        #CompartmentDryVegetative cDV
# Compartment dry reproductive      #CompartmentDryReproductive cDR
# Indicate if the cell was previously cut during a certain period   #boolean isCut
# Cut tag shows if there is a cut event                             #boolean isHarvested
# Cut tag shows if there is a grazed event                          #boolean isGrazed
# Sum of GRO                        #double sumGRO
# GRO                               #double gro

def getHeight(gv_avg_h, gr_avg_h, dv_avg_h, dr_avg_h):
    """
    Return the height of this cell
    @return the maximum height of the 4 cs
    """
    return max(max(gv_avg_h, gr_avg_h),np.max(dv_avg_h, dr_avg_h))

def cut(cutHeight, rhogv, rhodv, rhogr, rhodr, gvb, dvb, grb, drb, cellSurface, isHarvested):
    """
    Realize the harvest on each c. If the amount of cut biomass is not null, then the flag isHarvested is set to True
    \f[
    biomass_:harvested = \sum_:cell \in Plot \sum_:c \in cell biomassHarvested_:c
    \f]
    @param cutHeight the height of the cut (m)
    @param rhogv rho green vegetation
    @param rhodv rho dry vegetation
    @param rhogr rho green reproduction
    @param rhodr rho dry reproduction
    @param gvb  the biomass of Green Vegetation
    @param dvb  the biomass of Dry Vegetation
    @param grb  the biomass of Green Reproductive
    @param drb  the biomass of Dry Reproductive
    @param cellSurface Surface of the pixel (Ha)
    @param isHarvested Status flag indicating harvest happened
    @return isHarvested Status flag indicating harvest happened
    @return the total amount of biomass cut (in kg DM)
    @return the amount of GV biomass cut (in kg DM)
    @return the amount of DV biomass cut (in kg DM)
    @return the amount of GR biomass cut (in kg DM)
    @return the amount of DR biomass cut (in kg DM)
    """
    # exeCut returns harvested biomass in [kg DM m-2]
    gv_h, gv_b = exeCut(rhogv, cutHeight, gvb)
    dv_h, dv_b = exeCut(rhodv, cutHeight, dvb)
    gr_h, gr_b = exeCut(rhogr, cutHeight, grb)
    dr_h, dr_b = exeCut(rhodr, cutHeight, drb)

    # sum of harvested biomass [kg DM m-2]
    sumBiomassHarvested = gv_h + dv_h + gr_h + dr_h

    if(sumBiomassHarvested > 0):
        isHarvested = True

    return(isHarvested,sumBiomassHarvested*cellSurface, gv_b, dv_b, gr_b, dr_b)

def mk_env(meanTenDaysT, t0, t1, t2, sumT, ni, pari, alphapar, pet, waterReserve, waterHoldingCapacity):
    """
    Environemental stress
    @param meanTenDaysT the mean of the ten days of temperature
    @param t0 minimum temperature for growth
    @param t1 sum of temperature at the beginning (growth activation threshold)
    @param t2 sum of temperature in the end (growth decline threshold)
    @param sumT sum of temperatures
    @param ni Nutritional index of pixel -NNI
    @param pari Photosynthetic radiation incident (PARi)
    @param alphapar the Light Use Interception
    @param pet potential evapotranspiration
    @param waterReserve reserve of water in the soil
    @param waterHoldingCapacity capacity of the soil to hold a certain volume of water
    @return the environmental stress
    """
    return(fTemperature(meanTenDaysT, t0, t1, t2, sumT) * ni * fPARi(pari, alphapar) * fWaterStress(waterReserve, waterHoldingCapacity, pet))

def getTotalBiomass(gv_biomass, dv_biomass, gr_biomass, dr_biomass):
    """
    Return the total biomass of the cell (by adding the biomass of the 4 cs)
    @param gv_biomass the Green Vegetation biomass
    @param dv_biomass the Dry Vegetation biomass
    @param gr_biomass the Green Reproduction biomass
    @param dr_biomass the Dry Reproduction biomass
    @return total biomass
    """
    return (gv_biomass + dv_biomass + gr_biomass + dr_biomass)

def fTemperature(meanTenDaysT, t0, t1, t2, sumT):
    """
    f of temperature to compute ENV
    \f[
    f(T)=\begin:cases
    0                         & \text:if  T < T_0 \lor  T \geq 40 \\
    \frac:(T-T_0):(T_1-T_0) & \text:if  T_0 \leq T < T_1        \\
    1                         & \text:if  T_1 \leq T < T_2        \\
    \frac:(40-T):(40-T_2)   & \text:if  T_2 \leq T < 40
    \end:cases
    \f]
    @param meanTenDaysT the mean of the ten days of temperature
    @param t0 minimum temperature for growth
    @param t1 sum of temperature at the beginning (growth activation threshold)
    @param t2 sum of temperature in the end (growth decline threshold)
    @param sumT sum of temperatures
    @return the value given by the temperature f
    """
    if(meanTenDaysT < t0 or meanTenDaysT >= 40):
        return 0
    elif (meanTenDaysT >= t0 and meanTenDaysT < t1):
        return (meanTenDaysT - t0) / (t1 - t0)
    elif(meanTenDaysT >= t1 and meanTenDaysT < t2):
        return 1
    else:
        return (40 - meanTenDaysT) / (40 - t2)

def fsea(maxsea, minsea, sumT, st2, st1):
    """
    Function for seasonality (SEA) to compute the Potential Growth
    \f[
    f(SEA)=
    \begin:cases
    min_:SEA & \text:if  ST < 200 \lor ST_2 \leq ST \\
    min_:SEA + (max_:SEA - min_:SEA) * \frac:ST-200:ST_1-400 & \text:if  200 \leq ST < ST_1 - 200 \\
    max_:SEA &\text:if  ST_1 - 200 \leq ST < ST_1 - 100 \\
    max_:SEA + (min_:SEA - max_:SEA) * \frac:ST-ST_1 + 100:ST_2 - ST_1 +100 &\text:if  ST_1 - 100 \leq ST < ST_2
    \end:cases
    \f]
    @param maxsea growth increase in summer
    @param minsea growth increase in winter
    @param sumT sum of temperature
    @param st1 sum of temperature at the beginning of growth
    @param st2 sum of temperature in the end of growth
    @return the value given by the sea f
    """
    if(sumT < 200 or sumT >= st2):
        return minsea
    elif ( sumT < st1 - 200):
        return minsea+(maxsea-minsea)*(sumT-200) / (st1 - 400)
    elif (sumT < st1 - 100):
        return maxsea
    else:
        return maxsea+(minsea-maxsea)*(sumT - st1 + 100) / (st2 - st1 + 100)

def fPARi(pari, alphapar):
    """
    Function of PAR insterception (PARi) to compute ENV
    \f[
    f(PAR_:i)=
    \begin:cases
    1                          & \text:if  PAR_:i < 5 \\
    1-\alpha_:PAR*(PAR_:i-5) & \text:if  PAR_:i \geq 5
    \end:cases
    \f]
    @param pari Photosynthetic radiation incident (PARi)
    @param alphapar the Light Use Interception
    @return the value given by the PARi [0-1]
    """
    if(pari < 5 ):
        return(1)
    else:
        return(max(1-alphapar*(pari - 5),0))

def fWaterStress(waterReserve, waterHoldingCapacity, pet):
    """
    f of water stess to compute ENV
    \f[
    f(W)=
    \begin:cases
    \begin:cases
    4 * W           & \text:if        W \leq 0.2 \\
    0.75 * W + 0.65 & \text:if  0.2 < W \leq 0.4 \\
    0.25 * W + 0.85 & \text:if  0.4 < W \leq 0.6 \\
    1                    & \text:if  0.6 < W
    \end:cases
    &\text:if  PET \leq 3.8
    \\
    \begin:cases
    2 * W         & \text:if        W \leq 0.2 \\
    1.5 * W + 0.1 & \text:if  0.2 < W \leq 0.4 \\
    W + 0.3            & \text:if  0.4 < W \leq 0.6 \\
    0.5 * W + 0.6 & \text:if  0.6 < W \leq 0.8 \\
    1                  & \text:if  0.8 < W
    \end:cases
    & \text:if  3.8 < PET \leq 6.5 \\
    W & \text:if  6.5 < PET
    \end:cases
    \f]
    @param waterReserve reserve of water in the soil
    @param waterHoldingCapacity capacity of the soil to hold a certain volume of water
    @param pet potential evapotranspiration
    @return the value given by the waterstress f
    """
    waterStress = min(waterReserve/waterHoldingCapacity, 1)
    if(pet <= 3.8):
        if(waterStress<=0.2):
            return 4 * waterStress
        elif (waterStress <= 0.4):
            return 0.75 * waterStress + 0.65
        elif (waterStress <= 0.6 ):
            return 0.25 * waterStress + 0.85
        else:
            return 1

    elif(pet <= 6.5):
        if(waterStress<=0.2):
            return 2 * waterStress
        elif (waterStress <= 0.4):
            return 1.5 * waterStress + 0.1
        elif (waterStress <= 0.6 ):
            return waterStress + 0.3
        elif (waterStress <= 0.8 ):
            return 0.5 * waterStress + 0.6
        else:
            return 1

    else:
        return waterStress

def rep(ni):
    """
    #Replace the value of NI (Nutrition Index (Belanger et al., 1992))

    rep = 0.25+\frac:0.75*(NI-0.35):0.65

    @param ni The Nutrition Index (Belanger et al., 1992)
    @return the value of the rep f
    """
    return(0.25+((0.75*(ni-0.35)) / 0.65))

def pgro(pari, ruemax, pctlam, sla, gv_biomass, lai):
    """
    Compute and return potential growth

    PGRO = PAR_i * RUE_:max * (1-\exp(-0.6 * LAI) ) * 10

    @param pari the incident PAR
    @param ruemax the maximum Radiation Use Efficiency
    @param pctlam % leaf of laminae in Green Vegetation
    @param sla the specific leaf area (m2 g-1)
    @param gv_biomass the Green Vegetation biomass
    @param lai the LAI from remote sensing (if available)
    @return the calculated pGRO (kg DM ha-1)
    """
    #print("pgro**************************")
    #print("pgro: pariIn = %.2f" % (pari))
    #print("pgro: ruemaxIn = %.2f" % (ruemax))
    #print("pgro: pctlamIn = %.2f" % (pctlam))
    #print("pgro: SLAIn = %.2f" % (sla))
    #print("pgro: gv_biomassIn = %.2f" % (gv_biomass))
    if(int(lai) == 0):
        try:
            lai = sla * pctlam * (gv_biomass/10)
        except:
            # In case of input malfunction
            lai = sla * pctlam * 1.0

    lightInterceptionByPlant = (1-np.exp(-0.6*lai))
    #print("pgro: LightInter.byPlant = %.2f" % (lightInterceptionByPlant))
    pgro = (pari*ruemax*lightInterceptionByPlant*10)
    #print("pgro: pgro = %.2f" % (pgro))
    return(pgro)

def fclai(pctlam, sla, gv_biomass):
    """
    Compute and return the leaf area index
    \f[
    LAI(t) = SLA * \%LAM * \frac:biomass_:GV(t):10
    \f]
    @param pctlam % leaf of laminae in Green Vegetation
    @param sla the specific leaf area (m2 g-1)
    @param gv_biomass the Green Vegetation biomass
    @return the calculated lai
    """
    return(sla * (gv_biomass/10) * pctlam)

def aet(pet, pctlam, sla, gv_biomass, waterReserve, waterHoldingCapacity, lai):
    """
    Return the actual evapotranspiration (AET)
    \f[
    AET(t) = \min(PET(t), PET(t) * \frac:LAI(t):3)
    \f]
    @param pet the daily potential evapotranspiration (PET)
    @param pctlam % leaf of laminae in Green Vegetation
    @param sla the specific leaf area (m2 g-1)
    @param gv_biomass the Green Vegetation biomass
    @param waterReserve reserve of water in the soil
    @param waterHoldingCapacity capacity of the soil to hold a certain volume of water
    @return the actual evapotranspiration (AET)
    """
    if(int(lai) == 0):
        lai = sla * pctlam * (gv_biomass/10)
        #print("aet mk LAI: LAI = %.2f" %(lai))

    lightInterceptionByPlant = (1-np.exp(-0.6*lai))
    pt = pet * lightInterceptionByPlant
    pe = pet - pt
    ta = pt * fWaterStress(waterReserve, waterHoldingCapacity, pet)
    ea = pe * min(waterReserve/waterHoldingCapacity, 1)
    return(ta+ea)

def updateSumTemperature(temperature, t0, sumT, tbase):
    """
    Add the daily temperature to the sum temperature if the daily one is positive
    @param temperature
    @param t0 minimum temperature for growth
    @param sumT actual sum of temperature
    @param tbase base temperature (substracted each day for the calculation of the ST)
    @param currentDay the current doy
    """
    #TODO return DOY in doc, but return sumT in code O_O ?????
    if(temperature >= t0):
        sumT += np.max(temperature - tbase, 0)
    return(sumT)

def getAvailableBiomassForCut(gv_biomass, dv_biomass, gr_biomass, dr_biomass, cutHeight, rhogv, rhodv, rhogr, rhodr):
    """
    Return the amount of biomass av for cut
    @param gv_biomass biomass of Green Vegetation
    @param dv_biomass biomass of Dry Vegetation
    @param gr_biomass biomass of Green Reproduction
    @param dr_biomass biomass of Dry Reproduction
    @param cutHeight height of the cut
    @param rhogv Volume VV (g m-3)
    @param rhodv Volume DV (g m-3)
    @param rhogr Volume GR (g m-3)
    @param rhodr Volume DR (g m-3)
    @return the amount of biomass av for cut
    """
    avDefoliationBiomassGV = avDefoliationBiomass(gv_biomass, cutHeight, rhogv)
    avDefoliationBiomassDV = avDefoliationBiomass(dv_biomass, cutHeight, rhodv)
    avDefoliationBiomassGR = avDefoliationBiomass(gr_biomass, cutHeight, rhogr)
    avDefoliationBiomassDR = avDefoliationBiomass(dr_biomass, cutHeight, rhodr)
    return(avDefoliationBiomassGV + avDefoliationBiomassDV + avDefoliationBiomassGR + avDefoliationBiomassDR)

def defoliation(gv_biomass, dv_biomass, gr_biomass, dr_biomass, cutHeight, rhogv, rhodv, rhogr, rhodr, maxAmountToIngest):
    """
    Defoliation method
    @param gv_biomass biomass of Green Vegetation
    @param dv_biomass biomass of Dry Vegetation
    @param gr_biomass biomass of Green Reproduction
    @param dr_biomass biomass of Dry Reproduction
    @param cutHeight height of the cut
    @param rhogv Volume VV (g m-3)
    @param rhodv Volume DV (g m-3)
    @param rhogr Volume GR (g m-3)
    @param rhodr Volume DR (g m-3)
    @param maxAmountToIngest The maximum amount of ingest
    @return the sum of ingested biomass
    @return isGrazed = True
    """
    avDefoliationBiomassGV = avDefoliationBiomass(gv_biomass, cutHeight, rhogv)
    avDefoliationBiomassDV = avDefoliationBiomass(dv_biomass, cutHeight, rhodv)
    avDefoliationBiomassGR = avDefoliationBiomass(gr_biomass, cutHeight, rhogr)
    avDefoliationBiomassDR = avDefoliationBiomass(dr_biomass, cutHeight, rhodr)

    sumAvailable = avDefoliationBiomassGV + avDefoliationBiomassDV + avDefoliationBiomassGR + avDefoliationBiomassDR
    sumBiomassIngested = 0
    if(sumAvailable > 0):
        if(sumAvailable <= maxAmountToIngest):
            sumBiomassIngested = exeDefoliationByBiomass(avDefoliationBiomassGV, maxAmountToIngest) + exeDefoliationByBiomass(avDefoliationBiomassDV, maxAmountToIngest) + exeDefoliationByBiomass(avDefoliationBiomassGR, maxAmountToIngest) + exeDefoliationByBiomass(avDefoliationBiomassDR, maxAmountToIngest)
        else:
            sumBiomassIngested = exeDefoliationByBiomass(maxAmountToIngest * avDefoliationBiomassGV/sumAvailable, maxAmountToIngest) + exeDefoliationByBiomass(maxAmountToIngest * avDefoliationBiomassDV/sumAvailable, maxAmountToIngest) + exeDefoliationByBiomass(maxAmountToIngest * avDefoliationBiomassGR/sumAvailable, maxAmountToIngest) + exeDefoliationByBiomass(maxAmountToIngest * avDefoliationBiomassDR/sumAvailable, maxAmountToIngest)

    return(sumBiomassIngested)

def greenLimbsMass(gv_gamma, gv_biomass):
    """
    Calculation of mass of green limbs for the cell
    (old name: mlv)
    @param gv_biomass biomass of Green Vegetation
    @param gv_biomass
    @return mass of green limbs
    """
    return (gv_gamma * gv_biomass)

def getOMDgv(gv_min_omd, gv_max_omd, gv_avg_age, lls):
    """
    Compute the Green Vegetation actual Organic Matter Digestibility
    @param gv_min_omd The minimum Green Vegetation Org. Mat. Digestibility
    @param gv_max_omd The maximum Green Vegetation Org. Mat. Digestibility
    @param gv_avg_age The average age of the Green Vegetation
    @param lls the leaf lifespan (degree Celsius per day-1)
    @return the Green Vegetation Organic Matter Digestibility
    """
    return max(gv_min_omd, gv_max_omd - gv_avg_age * (gv_max_omd - gv_min_omd) / lls)

def getOMDgr(gr_min_omd, gr_max_omd, gr_avg_age, st1, st2):
    """
    Compute the Green Reproduction actual Organic Matter Digestibility
    @param gr_min_omd The minimum Green Reproduction Org. Mat. Digestibility
    @param gr_max_omd The maximum Green Reproduction Org. Mat. Digestibility
    @param gr_avg_age The average age of the Green Reproduction
    @param st1 sum of temperature to begin vegeative activity
    @param st2 sum of temperature to end vegetative activity
    @return the Green Vegetation Organic Matter Digestibility
    """
    return max(gr_min_omd, gr_max_omd - gr_avg_age * (gr_max_omd - gr_min_omd) / (st2 - st1))

def getSumTemperature(weather, doy, t0):
    """
    Return the sum temperature corresponding to the DOY
    @param weather the weather array
    @param doy the day of year wanted [1-366]
    @param t0 minimum temperature for growth
    @return the sum temperature above t0 corresponding to the DOY
    """
    sumTemperature = 0
    for i in range(doy):
        if(weather[i][1] > t0):
            sumTemperature += (weather[i][1] - t0)

    return(sumTemperature)

#TODO This set of functions are either not used or not useful

def addNI(ni, amountToIncrease):
    return(max(0, min(amountToIncrease+ni, 1.2)))

