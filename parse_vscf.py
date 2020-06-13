# -----------------------------------------------------------------------
# PARSING ANHARMONIC-REALTED INFORMATION FROM A MOLRPO_VSCF OUTPUT FILE
# -----------------------------------------------------------------------

# LAST VERSION 13/06/2020

# This code allows to parse information from a VSCF calculation run in Molpro.
# The code is divided into two sections and produces two final csv file: freq_int_vscf.txt and results.txt
# In order to better undersatnd the script, I do recommend to go into each section within the two parts and see what the dummy files look like. Hopefully, this will provide a better picture of the script's workflow.


# Code Preamble 

import os
import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# PART 1: THE DAWN OF FREQUENCIES AND INTENSITIES
# -------------------------------------------------

# This section extracts the VSCF anharmonic frequencies and intensities from the raw Molpro output file.
# Four dummy .txt files (temp1.txt, ..., temp4.txt) are created and deleted during the execution of the code.
# The final output is the freq_int_vscf.txt file containing both frequencies and intensities in a csv format.


# Section to take the anharmonic vibrational analysis out from the raw output file.
# The information is placed into a dummy file names as temp1.txt.
# https://stackoverflow.com/questions/35758444/copy-section-of-text-in-file-python
name = sys.argv[1]
with open('{0}'.format(name),'r') as inp1, open('temp1.txt','a') as temp1:
    copy = False
    for line in inp1:
        if (line.strip() == 'Fundamentals' or line.strip() == 'Overtones' or line.strip() == 'Combination bands'):
            copy = True
        elif line.strip() == 'Zero point vibrational energy (cm-1)':
            copy = False
        elif copy:
            temp1.write(line)

inp1.close()
temp1.close()

# The file temp1.txt has some blank lines that are not needed.
# This section deletes those blank lines from the temp1.txt file and creates a new dummy file named as temp2.txt.
# os.remove removes the first dummy file temp1.txt.
# https://www.8bitavenue.com/remove-blank-lines-from-file-in-python/
with open('temp1.txt','r') as inp2, open('temp2.txt','w') as temp2:
      for line in inp2:
             if line.strip():
                    temp2.write(line)

inp2.close()
temp2.close()
os.remove('temp1.txt')

# A new file temp3.txt is created without the duplicated lines present in the temp2.txt file.
# The temp2.txt file is then removed.
# https://stackoverflow.com/questions/1215208/how-might-i-remove-duplicate-lines-from-a-file
lines_seen = set()
with open('temp2.txt','r') as inp3, open('temp3.txt','w') as temp3:          
    for line in inp3:
        if line not in lines_seen:
            temp3.write(line)
            lines_seen.add(line)

inp3.close()
temp3.close()
os.remove('temp2.txt')

# The dummy file temp3.txt is converted into a new file with the csv format (temp4.txt).
# temp3.txt is then removed.
txt_csv = pd.read_fwf('temp3.txt')
txt_csv.to_csv('temp4.txt', index=False)
os.remove('temp3.txt')

# Only the relevant columns present in temp4.txt are placed into the final file freq_int_vscf.txt
# The file has the columns: VSCF Frequencies, Intensities
temp4 = pd.read_csv('temp4.txt')
freq_int = ['VSCF','IR Intens']
results_vscf = temp4[freq_int]
results_vscf.to_csv('freq_int_vscf.txt', index=False)
os.remove('temp4.txt')

# ---------------------------------------------------------------------
# PART 2: ON THE SEARCH OF ZERO POINT ENERGIES AND COMPUTATIONAL TIMES
# ---------------------------------------------------------------------

# This sections allows to obatin the vibrational zero point energies at the VSCF and Harmonic levels
# As well as the computational time taken to perform the VSCF calculation
# The output of this section is the results.txt file in csv format.
# The columns in the file are placed as follows: File Name (name), VSCF Zero Point Energy (VZPE), VSCF Comp. Time (vscf_t), Harmonic
# Zero Point Energy (HZPE)

with open('{0}'.format(name),'r') as x, open ('results.txt','a') as y:
    f = x.readline()
    while f:
        if (f.startswith(' VSCF') and len(f.split()) == 3 and not f.startswith(' VSCF/')):
            g = f.split()
            VZPE = g[1]
            #print(VZPE)
        if f.startswith(' CPU-Time for VSCF calculation:'):
            g = f.split()
            vscf_t = g[4]
            #print(vscf_t)
        if f.startswith(' Harm.'):
            g = f.split()
            HZPE = g[1]
            #print(HZPE)
        f=x.readline()
    processed = '{0},{1},{2},{3} \n'.format(name,VZPE,vscf_t,HZPE)
    #print(processed)
    y.write(processed)
x.close()
