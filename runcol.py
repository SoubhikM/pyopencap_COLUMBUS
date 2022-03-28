import os, sys
import numpy as np
from pathlib2 import Path
import glob

#Generate proper directories
pwd = os.getcwd()
path=os.getcwd()+'/WORK/'
path2=os.getcwd()+'/'+'CAP_INPS/'

if os.path.isdir(path) == False :
    print(r'WORK/ directory not found. We are done here!')
    exit
else:
    if os.path.isdir(path2) == False :
        os.system(r'mkdir CAP_INPS')
    if os.path.isfile('matrix_gen.py')==False :
        print(r'Need matrix_gen.py in WD')
        exit
    else:
        os.chdir(path)
        os.system('rm -rf *iwfmt 2> /dev/null')
        os.system('echo -e "aoints\n 1\n" |$COLUMBUS/iwfmt.x > aoints.iwfmt 2> err.ignore')

        files = glob.glob('cid1fl.*') + glob.glob( 'cid1trfl.*')
        for fname in files:
            if os.path.isfile(fname)==True :
                os.system('echo -e "%s\n 1\n" |$COLUMBUS/iwfmt.x > %s.iwfmt 2> err.ignore'%(fname, fname))
        os.chdir(pwd)

        #Move files in PWD
        os.system('cp WORK/*iwfmt .')
        os.system('cp MOLDEN/molden_mo_mc.sp .')

        #Create H0.dat
        H0=open('H0.dat', 'w')
        lines = [line for line in open('WORK/ciudgsm')]
        for line in lines:
            if 'convergence criteria not satisfied' in line:
                print ('Convergence of roots not achieved. We are done here!')
                break
            elif "eci     " in line:
               print(float(line.split()[2]), file=H0)

        H0.close()

        nstates = input(r"No of states/Roots:" "\n")

        os.system('python matrix_gen.py %s'%( nstates)) 
        os.system('rm -rf *iwfmt')
        os.system('mv sdm*.dat CAP_INPS/')
        os.system('mv tdm.s*TOs*.dat CAP_INPS/')
        os.system('mv mocoef-file.dat CAP_INPS/')
        os.system('mv H0.dat CAP_INPS/')
        os.system('echo Look into CAP_INPS/ folder. Done!')
        os.system(r'mv molden_mo_mc.sp CAP_INPS/')

