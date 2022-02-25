"""
=================================
Muse EEG Auditory Oddball Task
=================================

"""

"""
----------------------------------
Usage
----------------------------------

1. Seat subject comfortably. 

Subject should be fixating on a point (on a blank wall). 

Laptop computer should be located somewhere behind and nearby subject,
within easy reach of experimenter. 


2. Please muse EEG on subject's head.

(See separate muse usage notes for details)


3. Turn on muse EEG

It should be in pairing mode (flashing LED), and should NOT yet switch to paired mode (solid LED)


4. Launch experiment

Double click on this file or type `python run_aob_task.py` from conda terminal in the experiment folder. 

After a few seconds, two things will happen: 

1. Experiment instructions screen comes up

2. Muse connects to laptop. 

The experimenter should watch the muse device to confirm that the connection to laptop is successfully 
established at this point, as indicated by a change from flashing to solid white LED on the muse. 


When ready, and connection has been confirmed, press space to start experiment


5. Wait ~2.5 minutes for experiment to complete.

Experimenter should be in the room, stood behind the subject, quietly observing. 


6. Remove muse from subject and turn off. 


7. Check data has recorded ok

Data are saved as .csv files in the `MUSE-TMS\Data' folder

Each file has the recording start time stamp in its title. 

These can be renamed and associated specific subject and session numbers at a later point, 
e.g. end of the day. 


8. Analyze!

"""



"""
----------------------------------
Setup
----------------------------------
"""

# Importage
# ----------

import warnings
warnings.filterwarnings('ignore')

from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound


from numpy.random import seed,rand,binomial
from eegnb.experiments.auditory_oddball import auditory_erp_arrayin as expt
from eegnb.devices.eeg import EEG
from eegnb.analysis.utils import fix_musemissinglines
from datetime import datetime
import os
import time


# Options
# --------

# EEG device name (Muse 2, brainflow bluetooth native streaming option)
eeg_device = 'muse2_bfn'

# File paths and naming
pfx = 'mta' # Shorthand for 'Muse TMS AOB'
outdir = os.getcwd() + '\Data'

# Define auditory oddball parameters
n_trials = 50 
iti = 2.9 # inter-trial interval (same as ISI for this expt)
jitter = 0.05 # random variability adder to ITI
tone1_hz = '1024'
tone2_hz = '1920'

# Generate conditions list
seed(0) # use this to fix stim order for every subject, if desired
itis = iti + rand(n_trials) * jitter # ITIs list
conditions = binomial(1, 0.2, n_trials) # list of 1s (standard) and 2s (deviants)

do_fixation = True

# File and folder names
thistime = str(datetime.now()).replace(' ', '_').split('.')[0]
fname = os.path.join(outdir,pfx + '__' + str(thistime)  + '.csv')
fname = fname.replace(':', '-').replace('C-', 'C:')


"""
----------------------------------
Run experiment
----------------------------------
"""

if __name__ == '__main__':
 
    try:
        # Initiate data stream
        print('\n\n\nInitiating data stream...\n\n')
        eeg = EEG(device=eeg_device)

        # Run oddball task
        print('\n\n\nStarting auditory oddball task...\n\n')
        df = expt.present(eeg=eeg,
                          itis=itis,
                          stim_types=conditions,
                          tone1_hz=tone1_hz,
                          tone2_hz=tone2_hz,
                          save_fn=fname,
                          do_fixation=do_fixation)

        # End oddball task
        print('\n\n\nFinished AOB Experiment.\n\n')
   
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())

    finally:
        print("\n\n\nPress Enter to finish...")
        input()

