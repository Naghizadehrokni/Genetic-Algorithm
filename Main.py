import MyGenetic
import random
import math
import statistics
import pickle

from plxscripting.easy import *

f1 = open("points.txt", "r")
if f1.mode == "r":
    xloc = list(map(float, f1.read().split()))
else:
    print("can't read 'points.txt' file")
f1.close()

f2 = open("VelocityZ.txt", "r")
if f2.mode == "r":
    Vz = list(map(float, f2.read().split()))
else:
    print("can't read 'Velocity.txt' file")
f2.close()
doLoad = False 
if doLoad:
    with open('GaData.pkl', 'rb') as f:
        pop, f_iter = pickle.load(f)

Npoints = len(xloc)

# var name: wx, width, depth, length
Min = [2, 0.25, 2, 5, 50]
Max = [8, 1, 6, 15, 50]
popSize = 30
maxIter = 50
pm = 0.008 # probability of mutate
pc = 0.8 # probability of crossover

input_port_i = '10000'
input_port_o = '10001'
input_password = 'gkiePHMehran7075'# PUT YOUR PLAXIS 3D INPUT PASSWORD HERE
save_path = 'C:\Program Files (x86)\Plaxis\PLAXIS 3D' # r'C:\Plaxis\Data' # PUT THE FOLDER TO SAVE THE PLAXIS FILES HERE

def fitness(gene):
    s_i, g_i = new_server('localhost', input_port_i, password=input_password)
    s_i.new()
    material1 = g_i.soilmat()
    material1.setproperties(
        "MaterialName", "Soil",
        "Colour", 15262369,
        "SoilModel", 1,
        "gammaUnsat", 20,
        "gammaSat", 20,
        "Gref", 96150,
        "nu", 0.3,
        "cref", 0,
        "phi", 0,
        "RayleighBeta", 0.0003183)
    material2 = g_i.soilmat()
    material2.setproperties(
        "MaterialName", "Geofoam",
        "Colour", 9079434,
        "SoilModel", 1,
        "gammaUnsat", 0.61,
        "gammaSat", 0.61,
        "Gref", 6807,
        "nu", 0.01,
        "cref", 0,
        "phi", 0)
    g_i.Soilcontour.initializerectangular(0,0,40,20)
    borehole = g_i.borehole(0,0)
    g_i.soillayer(20)
    g_i.setmaterial(g_i.Soil_1, material1)
    g_i.gotostructures()
    g_i.plate((0, 0, 0), (0.36, 0, 0), (0.36, 0.36, 0), (0, 0.36, 0))
    material3 = g_i.platemat()
    material3.setproperties(
        "MaterialName", "Plate",
        "Colour", 16711680,
        "IsIsotropic", True,
        "E1", 30000000,
        "E2", 30000000,
        "d", 0.1,
        "G12", 15000000,
        "G13", 15000000,
        "G23", 15000000)
    g_i.setmaterial(g_i.plate_1, material3)

    # var name: wx, width, depth, length
    wx = gene[0]
    width = gene[1]
    depth = gene[2]
    length = gene[3]

    g_i.surface(wx-width/2, 0, 0, wx+width/2, 0, 0, wx+width/2, length, 0, wx-width/2, length, 0, wx-width/2, 0, 0)
    g_i.extrude((g_i.Polygon_2), 0, 0, 0-depth)
    g_i.delete(g_i.Polygon_2)
    g_i.setmaterial(g_i.Soil_2, material2)

    g_i.surfload(0, 0, 0, 0.36, 0, 0, 0.36, 0.36, 0, 0, 0.36, 0)
    g_i.surface(0, 0, 0, 35, 0, 0, 35, 20, 0, 0, 20, 0, 0, 0, 0)
    g_i.surface(0, 0, 0, 35, 0, 0, 35, 0, -15, 0, 0, -15, 0, 0, 0)

    g_i.gotomesh()

    g_i.Polygon_1_Polygon_2_Polygon_3_1.CoarsenessFactor = 0.1
    g_i.Polygon_3_1.CoarsenessFactor = 0.15
    g_i.Polygon_3_2.CoarsenessFactor = 0.2
    g_i.Polygon_4_1.CoarsenessFactor = 0.15
    g_i.Polygon_4_2.CoarsenessFactor = 0.3
    g_i.BoreholeVolume_1_1.CoarsenessFactor = 0.7

    g_i.mesh(0.15, 256)
    g_i.gotostages()

    phase1 = g_i.phase(g_i.phases[0])
    g_i.Polygon_1_Polygon_2_Polygon_3_1.activate(g_i.phase_1)

    phase2 = g_i.phase(g_i.phases[1])
    g_i.BoreholeVolume_1_Volume_1_1.deactivate(g_i.phase_2)

    phase3 = g_i.phase(g_i.phases[2])
    g_i.Soil_1_Soil_2_1.Material[g_i.Phase_3] = material2

    phase4 = g_i.phase(g_i.phases[3])
    g_i.Volume_1.activate(g_i.phase_4)

    f = round(gene[4])
    phase5 = g_i.phase(g_i.phases[4])
    g_i.set(g_i.phase_5.DeformCalcType,"Dynamic")
    g_i.set(g_i.Phase_5.Deform.TimeIntervalSeconds, 0.5)
    g_i.set(g_i.Phase_5.Deform.ResetDisplacementsToZero, True)
    g_i.DynSurfaceLoad_1_1.activate(g_i.phase_5)
    g_i.set(g_i.phase_5.DeformCalcType,"Dynamic")
    g_i.DynSurfaceLoad_1_1.sigz[g_i.Phase_5] = -26
    g_i.loadmultiplier()
    g_i.set(g_i.LoadMultiplier_1.Signal, "Harmonic")
    g_i.set(g_i.LoadMultiplier_1.Amplitude, 1)
    g_i.set(g_i.LoadMultiplier_1.Frequency, f)
    g_i.DynSurfaceLoad_1_1.Multiplierz[g_i.Phase_5] = g_i.LoadMultiplier_1
    g_i.Dynamics.BoundaryXMin[g_i.Phase_5] = "None"
    g_i.Dynamics.BoundaryYMin[g_i.Phase_5] = "None"
    g_i.Dynamics.BoundaryZMin[g_i.Phase_5] = "Viscous"

    phase6 = g_i.phase(g_i.phases[5])
    g_i.set(g_i.phase_6.DeformCalcType,"Dynamic")
    g_i.set(g_i.Phase_6.Deform.TimeIntervalSeconds, 0.5)
    g_i.DynSurfaceLoad_1_1.activate(g_i.phase_6)
    g_i.set(g_i.LoadMultiplier_1.Signal, "Harmonic")
    g_i.set(g_i.LoadMultiplier_1.Amplitude, 1)
    g_i.set(g_i.LoadMultiplier_1.Frequency, f)
    g_i.DynSurfaceLoad_1_1.Multiplierz[g_i.Phase_6] = g_i.LoadMultiplier_1
    g_i.Dynamics.BoundaryXMin[g_i.Phase_6] = "None"
    g_i.Dynamics.BoundaryYMin[g_i.Phase_6] = "None"
    g_i.Dynamics.BoundaryZMin[g_i.Phase_6] = "Viscous"

    g_i.calculate()

    outpu_port = g_i.view(phase6)
    s_o, g_o = new_server('localhost', input_port_o, password=input_password)

    thresh = wx+width/2
    value = []
    for k in range(0, Npoints):
        if (xloc[k]>thresh) and (xloc[k]<(thresh+25)):
            vz = abs(float(g_o.getsingleresult(g_o.Phase_6, g_o.ResultTypes.Soil.Vz, (xloc[k], 0, 0))))
            value.append(vz/Vz[k])

    g_o.close()
    AR = 1-statistics.mean(value)
    D_AR = 0.75
    alpha = 0.995
    beta  = 0.005
    Cost = alpha*abs(AR-D_AR) + beta*depth
    return Cost


if __name__ == '__main__':

    if not doLoad:
        pop = MyGenetic.createPop(popSize, Min, Max)
        for i in range(0, popSize):
            pop[i].Fitness = fitness(pop[i].Genes)
        (bestFit, idx) = MyGenetic.minFit(pop)
        print("In iteration 0\t best fitness value is {0:12.9f}".format(
            bestFit
        ))
        f_iter = 0
    iter0 = f_iter
    for itr in range(iter0, maxIter):
        NewPop = []

        # crossover
        idr = random.sample(range(0,popSize),popSize)
        for i in range(0, int(popSize/2)):
            id1 = idr[i*2]
            id2 = idr[i*2+1]
            if random.random()<pc:
                (newChrom1, newChrom2) = MyGenetic.crossover(pop[id1], pop[id2])

                newChrom1.Fitness = fitness(newChrom1.Genes)
                newChrom2.Fitness = fitness(newChrom2.Genes)

                if newChrom1.Fitness<pop[id1].Fitness:
                    NewPop.append(newChrom1)
                else:
                    NewPop.append(pop[id1])

                if newChrom2.Fitness<pop[id2].Fitness:
                    NewPop.append(newChrom2)
                else:
                    NewPop.append(pop[id2])
            else:
                NewPop.append(pop[id1])
                NewPop.append(pop[id2])

        # Mutate
        pop = []
        for i in range(0, popSize):
            if random.random()<pm:
                newChrom = MyGenetic.mutate(NewPop[i], Min, Max)
                newChrom.Fitness = fitness(newChrom.Genes)
                if newChrom.Fitness<NewPop[i].Fitness:
                    pop.append(newChrom)
                else:
                    pop.append(NewPop[i])
            else:
                pop.append(NewPop[i])

        (bestFit, idx) = MyGenetic.minFit(pop)
        print("In iteration {0}\t best fitness value is {1:12.9f}".format(
            (itr+1),
            bestFit
        ))
        f_iter = itr
        with open('GaData.pkl', 'wb') as f:
            pickle.dump([pop, f_iter], f)

    # var name: wx, width, depth, length
    wx = pop[idx].Genes[0]
    width = pop[idx].Genes[1]
    depth = pop[idx].Genes[2]
    length = pop[idx].Genes[3]
    f = round(pop[idx].Genes[4])
    print("best value obtained with wx = {0:3.2f}, width = {1:3.2f}, depth = {2:3.2f}, length = {3:3.2f} and Frequency = {4}.".format(
        wx, width, depth, length, f
    ))
    print("best fittness value is: {0:12.9f} .".format(bestFit))
