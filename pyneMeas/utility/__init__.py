from pyneMeas.utility.GlobalMeasID import readCurrentSetup
from pyneMeas.utility.GlobalMeasID import readCurrentID
from pyneMeas.utility.GlobalMeasID import initID
from pyneMeas.utility.GlobalMeasID import listIDs
from pyneMeas.utility.GlobalMeasID import setCurrentSetup
from pyneMeas.utility.GlobalMeasID import addPrefix

from pyneMeas.utility.SweepFunction import sweepAndSave as sweep

from pyneMeas.utility.utils import targetArray
from pyneMeas.utility.utils import runTest
"""
Utility package with helper functions for using the measurement instruments from the pyneMeas.Instruments package.
Includes methods:

utility.sweep(...) # Performs a measurement sweep

utility.targetArray([start, target1, target2,...],stepSize) # Creates a linearly spaced array ranging from start -> target1 -> target2 in steps of stepSize

utility.runTest() # Runs a test 'measurement' run. Uses two virtual instruments that create noisy linear and sinusoidal signals.

Functions specific to the 'measurement ID' prefix:

utility.listIDs()

"""