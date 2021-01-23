# pyneMeas documentation 

A package for simple electrical measurements using the National Instruments (NI) VISA standard.
Developed by Jakob Seidl and coworkers at the Nanoelectronics group at the University of New South Wales, Sydney.
It was originally written in Python 2.7 and later adapted for modern Python 3.

The package is divided into two sub-units: Instruments and utility functions that help carry out a electronic measurement.
It allows you to connect to various electronic measurement equipment in few lines of code.

Currently implemented instruments include:

1. Keithley 2400 series source measure units (SMUs)
2. Keithley 2000 series digital multimeters
3. Keithley 6517 'Electrometer'
4. Stanford Instruments SRS830 Lock-in amplifier
5. National Instruments USB6216 data acquisition card (NiDAQ)
6. Yokogawa GS200 source measure unit

It is easy to write you own instrument classes by just following a pre-made template. See [XX].

In addition, this software features code to control Oxford Instruments superconducting magnet power supplies and
read-out code to monitor the status of Oxford instruments Heliox cryostats. 
## A: Quickstart guide
### A.1 Installing pyneMeas:
Case A: from the online repository PyPi:

`$ pip install pyneMeas` 

Case B: from a local pyneMeas folder on your PC:

`$ pip install -e local/Path/pyneMeas/.`   the -e flag allows to make changes to the original files in the folder,
useful if you want to tweak the code while working.
You can download the sourcecode (.zip) from github under
https://github.com/JakobSeidl/pyneMeas

Install the package in a virtual environment (venv) or in your global Python 3 installation, whatever works best for your use-case.

Check if the installation was successful:\
`$ pip list` should return a list that contains of packages that should contain
```$ pip  20.3
pyneMeas           0.0.2    
```
if you installed it from the internet (Case A) or 
```$ pip  20.3
pyneMeas           /Path/To/Local/SourceDirectory    
```
if you installed pyneMeas from a local folder, e.g., after downloading the source code from gitHub (Case B). Enclose you path like this if it contains whitespace: "local Path/with whitespace/SourceDirectory" \
You can then try loading the package as described in the following section.

### A.2 Non-python drivers and hardware you'll need

IMPORTANT: In order to use commercial GPIB-controlled instruments such as Keithely source-measure units,
you need to install the proprietary National Instruments VISA/USB-H bundle driver 
(https://www.ni.com/en-au/support/downloads/drivers/download.ni-488-2.html#306147). Possibly, this could be
replaced by a fully open-source
library such as pyvisa-py that supplies the back-end (https://pyvisa-py.readthedocs.io/en/latest/).
For using the National Instruments Data Acquisition cards (NIDaQ), you need the corresponding driver
 (https://www.ni.com/en-au/support/downloads/drivers/download.ni-daqmx.html#288239). 
 
 For both we recommend not chossing the latest version but simpler, earlier versions.


### A.3 Loading and testing pyneMeas:
In your python console type:
```python:
>>> import pyneMeas.Instruments as I
>>> import pyneMeas.utility as U
```
If this works, you can run a test measurement using 'virtual' instruments to check weather 
plotting and data storage works fine:
```
>>> U.runTest()
```
should open a plot window with simulated linear and sinusoidal noise signals measured over time. 
A progress bar should indicated the status of the measurement.
In the console, you should see a notification that a folder has been created where the data will be stored.
```
Out: Created data storage directory: TempDat/
/>>>>>> Finished measurement A1 | Duration: 9.4 seconds = 0.2 min  <<<<<<<
```

Setting up any basic measurement requires three steps: 
1. Setting up all required instruments and configuring them
2. Defining the sweep-array and designating which instrument should sweep a variable and which instrument(s) should just read/measure.
3. Call the sweep function 'sweep()' from pyneMeas.utility using the Instrument parameters defined in 2.

### A.4 Initializing instruments:
We reccommend using an IDE such as PyCharm that supports code completion. E.g., type 'I.' 
(or any other alias you imported pyneMeas.Instruments as) and all implemented Instruments will appear in a drop-down list. Use TAB-completion when typing in the console. Let's use a Keithley 2401 source-measure unit:
```
>>> myKeithley = I.Keithley2401(10)  #  Initializes a Keithely2401 instrument at GPIB port 10
KEITHLEY INSTRUMENTS INC., MODEL nnnn, xxxxxxx, yyyyy/zzzzz /a/d  #  Parameters on the right depend on exact model/firmware
```
The `'KEITHLEY INSTRUMENTS INC.'` message is the instrument's response to the typical '*IDN?' query and indicates that the instrument has been successfully initiated.
Most instruments have internal options that can be set before the measurement. E.g., the Keithley source-measure
unit can be set to source voltage (and measure its output current) or to source a current instead. Every instrument has a set() and  setOptions() method:
E.g. 
```
myKeithley.set('name','myKeithleyInstrumentName) # Every instrument can have a unique 'name'
myKeithley.setOptions({'sourceMode':'voltage, # sourcing voltage
                      'sourceRange':20})      # Using high source range of up to 20 Volts
```
For a list of all instrument options and possible values, see [XX].
### A.5 Using the sweep() function 


In this example we define a simple current vs. voltage sweep with a single Keithley instrument. 
We define a empty dictionary that holds all relevant data. After defining `'basePath'` and `'fileName'`
under which the data will be stored, we define the `'setter'` and `'getters'` fields. They determine,
which instrument actively set (outputs) a value, e.g. a gate voltage, and which instruments measure the
resulting variables, e.g., input voltages, currents. Here we use the same Keithley instrument to do both.
The values we want to sweep over, in this case source-drain voltages, are defined in the `'sweepArray` field.
Here we use the `targetArray()` function, but standard lists or numpy.arrays can be used as well. 
In the last step, we call the `sweep()` function with the required `Dct` parameter and two optional parameters, `delay` and `plotVars`. 
Note that the name `Dct` of the dictionary may be changed but the keywords such as `'setter'` and `'sweepArray'` need to be exactly used as displayed here.
```
Dct = {} # Define empty dictionary as container
Dct['basePath'] = "Data/" # Relative to your current working directory
Dct['fileName'] = 'SampleA' # Sets the file name under which data will be save and logged.

Dct['setters'] = {myKeithley:    'V_SD'} # Set the variable called 'V_SD' with our 'myKeithley' object
Dct['readers'] = {myKeithley:    'I_SD'} # Measure the variable called 'I_SD' with our 'myKeithley' object

Dct['sweepArray'] = U.targetArray([0,1,0],stepsize=0.1) # Define values from 0V -> 1V -> 0V in 0.1V steps
                                                        # targetArray is a utility function provided

df = U.sweep(Dct,                          # call sweep function and provide the Dct dictionary defined
             delay=0.2,                    # seconds wait time in between points
             plotVars = [('V_SD','I_SD')]) # plot 'I_SD' (y-axis) over 'V_SD (x-axis)'      
                                                                   
```
This should open a live-plot that shows `'I_SD'` vs. `'V_SD'`. The data is saved under "Data/"
 (folder is created if it doesn't exist, see console output). Per measurement, four files are saved:
  The data is saved in .tsv format (blank text), in .mat matlab data format. In addition, a log.tsv file is created that logs 
  important information of the measurement run, such as instruments used etc. When plotting is enabled, the plot is also saved as .png.
  Note that each measurement has unique measurement ID consisting of a letter prefix and a running number. 
  This is e.g., displayed in the plot title and each saved data file is preceded by it. This also prevents data 
  from being overwritten even when the user uses the same `fileName` repeatedly. The `sweep()` function 
  returns a `pandas.DataFrame`, here assigned to `df`, that holds the acquired data with column labels corresponding to the variable names provided.
  This can be useful if the user wants to use the acquired data immediately during the measurement routine.

## B   Example scripts/ Tutorials
### B.1 Two variables: A gate-sweep measurement
```
[...]
df = U.sweep(Dct,                          # call sweep function and provide the Dct dictionary defined
             delay=0.2,                    # seconds wait time in between points
             plotVars = [('V_SD','I_SD')]) # plot 'I_SD' (y-axis) over 'V_SD (x-axis)'      
                                                                   
```
### B.2 Measure instruments over time
```
[...]
df = U.sweep(Dct,                          # call sweep function and provide the Dct dictionary defined
             delay=0.2,                    # seconds wait time in between points
             plotVars = [('V_SD','I_SD')]) # plot 'I_SD' (y-axis) over 'V_SD (x-axis)'      
                                                                   
```
### B.3 Simple measurements with the NIDaq
```
[...]
df = U.sweep(Dct,                          # call sweep function and provide the Dct dictionary defined
             delay=0.2,                    # seconds wait time in between points
             plotVars = [('V_SD','I_SD')]) # plot 'I_SD' (y-axis) over 'V_SD (x-axis)'      
                                                                   
```
### B.4 Example using lock-in amplifiers
```
[...]
df = U.sweep(Dct,                          # call sweep function and provide the Dct dictionary defined
             delay=0.2,                    # seconds wait time in between points
             plotVars = [('V_SD','I_SD')]) # plot 'I_SD' (y-axis) over 'V_SD (x-axis)'      
                                                                   
```
### B.5 Abruptly changing signals - sourcing step functions with SMU's
```
[...]
df = U.sweep(Dct,                          # call sweep function and provide the Dct dictionary defined
             delay=0.2,                    # seconds wait time in between points
             plotVars = [('V_SD','I_SD')]) # plot 'I_SD' (y-axis) over 'V_SD (x-axis)'      
                                                                   
```

## C   In-depth documentation on instruments and utility functions

#### C.1 Optional parameters of the sweep() function

`delay` Float, wait time in seconds after a value has been set and before instruments are read out. Default=0.0

`comments` String, Comments on experiment, sample etc. Is stored in the .log file together with
 the saved data. Useful for data not measured by instruments. Example: `"SampleA, I-V, T= 77K"`

`plotVars` list of `(xVar,yVar)` tuples to be plotted. Example: `[ ('V_SD', 'I_SD') ]` from above.

`plotParams` list of `('plotString','XAxisScale-YAxisScale')` tuples. `'plotString'` contains color, line and marker info. 
See https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.plot.html under Notes. 
'XAxisScale-YAxisScale' can be e.g. `'linear-linear'` or `'linear-log'` or any combination.
 Example: `[ ('go-', 'linear-linear') ]`
 
`plotAlpha` Float, Transparency of markers: 1= no transparencey, 0 = fully transparent. Default = 0.8

`plotCounter` Integer, After how many datapoints do you want to update the plot.  plotCounter > 1 helps speed up plotting. Default = 1

`plotSize` Tuple of two floats `(xSize,ySize)`, size of plot window in cm. Default = (10,10)

`saveCounter` Integer, After how many datapoints do you want to save data to disc. 
Can help speed up the measurement slightly. Default = 10

`breakCondition` Tuple, `('Variable','comparisonOperator',Value)`. Allows to stop a measurement when a certain condition is met.
 `'Variable'` is compared against `Value` using `'comparisonOperator'`. 
`'comparisonOperator'` can be `'<'` or `'>'` at the moment. Example: `'I_SD','>',1E-6)` will end the
 measurement when `'I_SD'` reaches a value above 1 microampere.
 
`extraInstruments` List of instrument objects, used to keep track of instruments that are not directly used as setter or reader but you still want to see logged in the .log file.

`saveEnable` Boolean, Defines wheather saving the data is desired. Default = True


### Beyond the sweep() function: Using instruments in a custom for-loop
