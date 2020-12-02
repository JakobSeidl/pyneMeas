import pyneMeas.Instruments as I
import pyneMeas.utility as U

T = I.TimeMeas(0.001)
T.setOptions({"name": "timeMachine"})

T2 = I.TimeMeas(0.001)
T2.setOptions({"name": "timeMachine2"})

#Setting up the essential inputs. We use a dictionary for this. The keys need to stay exactly the same!
Dct = {}
Dct['basePath'] = "Data/"
# on Windows Dct['basePath'] = "../Data/"
Dct['fileName'] = 'fileName'

Dct['inputHeaders'] = ['timePoint']
Dct['sweepArray'] = U.targetArray([0,-0.2,0.1,0],stepsize=0.05)
Dct['inputSetters'] = [T]

Dct['outputHeaders'] = ['measTime', 'measTime2']
Dct['outputReaders'] = [T, T2]


########### Do the actual sweep ##########
df = U.sweepAndSave(
    Dct,
    delay = 0.0,
    plotParams = ['timePoint','measTime','measTime2','timePoint'],
    comments = "Just a dummy measurement",
    plotString= ['o']
)


#df.plot.scatter(x = 'Time',y ='measTime')