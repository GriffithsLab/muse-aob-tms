
"""
=================================
Muse EEG Auditory Oddball Task
=================================

"""

"""
----------------------------------
Usage
----------------------------------

python run_oddball.py

"""



"""
----------------------------------
Setup
----------------------------------
"""

# Importage
# ----------

from numpy.random import seed,rand,binomial
from eegnb.experiments.auditory_oddball import auditory_erp_arrayin as expt
from eegnb.devices.eeg import EEG
from eegnb.analysis.utils import fix_musemissinglines
from datetime import datetime
import os
import time

# Options
# --------

# BlueMuse streaming options
install_bluemuse = False #True # False # True
start_bluemuse = False # True # False # True
stop_bluemuse = False # False

# EEG device names for BlueMuse streaming: 'muse2016', 'muse2', 'museS'
#  "    "     "    for brainflow streaming: 'muse2016_bfn', 'muse2_bfn', 'museS_bfn'
#eeg_device='muse2016'
#eeg_device = 'muse2'
eeg_device = 'muse2_bfn'

# File paths and naming
initials = 'TMS-AOB' # Could put per-subject initials in here if useful
run_num = '1' # Can add run labelling here if useful, but would require regular run script editing. 
#outdir = r"C:\Users\eeg_lab\Desktop\muse_aob_tms\recordings"
outdir = os.getcwd() + '..\\..\\data\\raw'


# Define auditory oddball parameters
n_trials = 10 #  50
iti = 2.9 # inter-trial interval (same as ISI for this expt)
jitter = 0.05 # random variability adder to ITI
tone1_hz = '1024'
tone2_hz = '1920'

# Generate conditions list
seed(0) # use this to fix stim order for every subject, if desired
itis = iti + rand(n_trials) * jitter # ITIs list
conditions = binomial(1, 0.2, n_trials) # list of 1s (standard) and 2s (deviants)


# Define some variables
# ----------------------

# BlueMuse streaming commands
install_bluemuse_cmd = r"""%windir%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'C:\Users\eeg_lab\Software\BlueMuse_2.3.0.0\BlueMuse_2.3.0.0\InstallBlueMuse.ps1'; exit " """
start_bluemuse_cmd = r"start bluemuse://start?addresses={00:55:da:b0:c2:f3} ;"
stop_bluemuse_cmd = r"start bluemuse://stop?stopall ;"

# File and folder names
thistime = str(datetime.now()).replace(' ', '_').split('.')[0]
fname = os.path.join(outdir,initials + '__' + str(thistime) + '__Run_' + str(run_num) + '.csv')
fname = fname.replace(':', '-')
fname = fname.replace('C-', 'C:')



"""
-----------------------------------------------
Define experimental functions
----------------------------------------------
"""


def start_stream():

  if install_bluemuse:
    print('\n Installing BlueMuse')
    print('\n\n\n' + install_bluemuse_cmd)
    os.system(install_bluemuse_cmd)

  if start_bluemuse:
    print('\n Starting BlueMuse')
    print('\n\n\n' +  start_bluemuse_cmd)
    os.system(start_bluemuse_cmd)

  if stop_bluemuse:
    print('\n Stopping BlueMuse')
    print('\n\n\n'  + stop_bluemuse_cmd)
    os.system(stop_bluemuse_cmd)


def run_task():

    eeg = EEG(device=eeg_device)

    df = expt.present(eeg=eeg,
                      itis=itis,
                      stim_types=conditions,
                      tone1_hz=tone1_hz,
                      tone2_hz=tone2_hz,
                      save_fn=fname)



"""
-----------------------------------------------
Do it. 
----------------------------------------------
"""

if __name__ == '__main__':

    # Optional: re-install bluemuse, start bluemuse, initiate stream
    # Flags for whether or not these steps are executed are at top of file. 
    start_stream()

    # Run oddball task
    print('\n\n\nStarting AOB Experiment...\n\n')
    
    """
    print('\n\n\n(make sure bluemuse stream started...)\n\n')
    time.sleep(15)
    """

    run_task()
    
    # Fix muselsl file writing bug (first few marker rows ommitted)
    """
    time.sleep(1)
    print('\n\nRunning muse file fix')
    fix_musemissinglines(fname)
    """

    print('\n\nFinished AOB Experiment :) \n')


