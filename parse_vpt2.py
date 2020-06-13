import os
import csv
import sys
import pandas as pd
from csv import writer
import matplotlib.pyplot as plt

# -------------------------------------------------
# PART 1: THE DAWN OF FREQUENCIES AND INTENSITIES
# -------------------------------------------------

# Copying data from the raw output file into a dummy file temp1.txt
# https://stackoverflow.com/questions/35758444/copy-section-of-text-in-file-python
name = sys.argv[1]
with open('{0}'.format(name),'r') as inp1, open('temp1.txt','w') as temp1:
    copy = False
    for lines in inp1:
        if (lines.strip() == 'Fundamentals' or lines.strip() == 'Overtones' or lines.strip() == 'Combination bands'):
            copy = True
        elif lines.strip() == 'CPU-Time for VPT2 calculation:          0.0 sec.':
            copy = False
        elif copy:
            temp1.write(lines)

inp1.close()
temp1.close()

# A new dummy file (temp2.txt) is created without blank lines
# https://www.8bitavenue.com/remove-blank-lines-from-file-in-python/
# os.remove() removes the first dummy file
with open('temp1.txt','r') as inp2, open('temp2.txt','w') as temp2:
    for lines in inp2:
        if lines.strip():
            temp2.write(lines)

inp2.close()
temp2.close()
os.remove('temp1.txt')

# Duplicated lines are deleted and a new dummy .txt file is created (temp3.txt)
# https://stackoverflow.com/questions/1215208/how-might-i-remove-duplicate-lines-from-a-file
lines_seen = set()
with open('temp2.txt','r') as inp3, open('temp3.txt','w') as temp3:
    for lines in inp3:
        if lines not in lines_seen:
            temp3.write(lines)
            lines_seen.add(lines)
            
inp3.close()
temp3.close()
os.remove('temp2.txt')

# The file temp3.txt is converted into a new file temp4.txt in csv format
# temp3.txt is then removed
txt_csv = pd.read_fwf('temp3.txt')
txt_csv.to_csv('temp4.txt', index=False)
os.remove('temp3.txt')

# The relevant columns from temp4.txt are placed into a final csv file called freq_int_vpt2.txt
temp4 = pd.read_csv('temp4.txt')
freq_int = ['Anharmonic','Intensity']
results_vpt2 = temp4[freq_int]
results_vpt2.to_csv('freq_int_vpt2.txt', index=False)
os.remove('temp4.txt')

# ---------------------------------------------------------------------
# PART 2: ON THE SEARCH OF ZERO POINT ENERGIES AND COMPUTATIONAL TIMES
# ---------------------------------------------------------------------

# This sections allows to obatin the vibrational zero point energies at the VPT2 and Harmonic levels
# As well as the computational time taken to perform the VPT2 calculation
# The output of this section is the results_vpt2.txt file in csv format.
# The columns in the file are placed as follows: File Name (name), VPT2 Zero Point Energy (ZPE), VPT2 Comp. Time (tvpt2), Harmonic
# Zero Point Energy (HZPE)

with open('{0}'.format(name),'r') as x, open('results_vpt2.txt','a') as y:
    f = x.readline()
    while f:
        if f.startswith(' Anharmonic:'):
            g = f.split()
            ZPE = g[1]
            #print(ZPE)
        if f.startswith(' CPU-Time for VPT2 calculation:'):
            g = f.split()
            tvpt2 = g[4]
            #print(tvpt2)
        if f.startswith(' Harmonic:'):
            g = f.split()
            HZPE = g[1]
            #print(HZPE)
        f = x.readline()    
    processed = '{0},{1},{2},{3} \n'.format(name,ZPE,tvpt2,HZPE)
    y.write(processed)
x.close()
