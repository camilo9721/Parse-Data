import os
import csv
import sys
import pandas as pd
from csv import writer
import matplotlib.pyplot as plt

# -------------------------------------------------
# PART 1: THE DAWN OF FREQUENCIES AND INTENSITIES
# -------------------------------------------------

# Copying the relevant information from the output file into a new temporal file called temp2.txt.
#https://stackoverflow.com/questions/35758444/copy-section-of-text-in-file-python
name = sys.argv[1]
with open('{0}'.format(name), 'r') as inp1, open('temp1.txt','w') as temp1:
    copy = False
    for lines in inp1:
        if lines.strip() == 'Results of VCI calculation:':
            copy = True
        elif lines.strip() == 'VCI/ZPVE vibrationally averaged geometry (Bohr)':
            copy = False
        elif copy:
            temp1.write(lines)

inp1.close()
temp1.close()

# This section is new as the VCI calculation relays on a previously performed VSCF calculation.
# Getting rid of the lines that are not relevant in the temp1.txt file.
#https://stackoverflow.com/questions/4710067/using-python-for-deleting-a-specific-line-in-a-file
with open('temp1.txt','r') as inp2, open('temp2.txt','w') as temp2:
    for lines in inp2:
        if (lines.strip() != 'Fundamentals' and lines.strip() != 'Overtones'):
            temp2.write(lines)

inp2.close()
temp2.close()
os.remove('temp1.txt')

# Deliting blank lines from the temp1.txt file and creating a new one temp2.txt
# os.remove removes the first temporal file temp1.txt.
#https://www.8bitavenue.com/remove-blank-lines-from-file-in-python/
with open('temp2.txt','r+') as inp3, open('temp3.txt','w') as temp3:  
    for lines in inp3:
        if lines.rstrip():
            temp3.write(lines)
            
inp3.close()
temp3.close()
os.remove('temp2.txt')

# Removing duplicated lines and creating a new file called temp4.txt.
# https://stackoverflow.com/questions/1215208/how-might-i-remove-duplicate-lines-from-a-file
lines_seen = set()
with open('temp3.txt','r') as inp4, open('temp4.txt','w') as temp4:          
    for lines in inp4:
        if lines not in lines_seen:
            temp4.write(lines)
            lines_seen.add(lines)

inp4.close()
temp4.close()
os.remove('temp3.txt')

# Transforms the temp4.txt file into temp5.txt file with a csv format.
# temp4.txt is then removed.
txt_csv = pd.read_fwf('temp4.txt')
txt_csv.to_csv('temp5.txt', index=False)
os.remove('temp4.txt')

# Only the relevant columns present in temp5.txt are placed into the final file freq_int_vci.txt.
# The line new_temp5 = temp5.fillna(0) makes sure that whenever there's a blank space, it is filled with zero.
# https://kite.com/python/answers/how-to-replace-nan-values-with-zeros-in-a-column-of-a-pandas-dataframe-in-python
# The file has the columns: VCI Frequencies, Intensities
# temp5.txt is then removed.
temp5 = pd.read_csv('temp5.txt')
new_temp5 = temp5.fillna(0)
freq_int = ['VCISDTQ','Intens']
results_vci = new_temp5[freq_int]
results_vci.to_csv('freq_int_vci.txt', index=False)
os.remove('temp5.txt')

# ---------------------------------------------------------------------
# PART 2: ON THE SEARCH OF ZERO POINT ENERGIES AND COMPUTATIONAL TIMES
# ---------------------------------------------------------------------

# This sections allows to obatin the vibrational zero point energies at the VCI (which I think is the same as VSCF) and Harmonic levels
# As well as the computational time taken to perform the VCI calculation
# The output of this section is the results_vci.txt file in csv format.
# The columns in the file are placed as follows: VSCF Zero Point Energy (VZPE), VCI Comp. Time (vscf_t), Harmonic
# Zero Point Energy (HZPE)

with open('{0}'.format(name),'r') as x, open ('results_vci.txt','a') as y:
    f = x.readline()
    while f:
        if (f.startswith(' VSCF') and len(f.split()) == 3 and not f.startswith(' VSCF/')):
            g = f.split()
            VZPE = g[1]
            #print(VZPE)
        if f.startswith(' CPU-Time for VCI calculation:'):
            g = f.split()
            tvci = g[4]
            #print(vscf_t)
        if f.startswith(' Harm.'):
            g = f.split()
            HZPE = g[1]
            #print(HZPE)
        f=x.readline()
    processed = '{0},{1},{2},{3} \n'.format(name,VZPE,tvci,HZPE)
    #print(processed)
    y.write(processed)
x.close()
