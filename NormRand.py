import random
import math
import threading
import time
import multiprocessing
from multiprocessing import Process, Pool

NEURON_NUM = 86
DT = 0.025

def createNormRand(STIM_TIME = 5000.0,NC = 86,FileCounter = 0): 
    STM_TIME_TERM = STIM_TIME / DT
    print "== START_CREATE_NORM_RAND =="
    normRandList = []
    StimEventsList = []
    
    for timeCount in range(0,int(STM_TIME_TERM)):
        StimEventsList = []
        for neuronCount in range(0,NC):
            StimEventsList.append(random.normalvariate(0,1))
        
        normRandList.append(StimEventsList)
    
    writeStimEvent("EtaList"+str(FileCounter)+".txt",normRandList)
    
    print "== END_CREATE_NORM_RAND =="


def writeStimEvent(StimEventsFileName = "EtaList.csv",SELList = [[]]):
    SEF = open(StimEventsFileName, "w")
    for stimEventsList in SELList:
        for stimEvents in stimEventsList:
            SEF.write(str(float(stimEvents))+"\t")
        
        SEF.write("\n")
    
    SEF.close()
    return 1

def startCNR(SeedNumber = 2014):
    random.seed(SeedNumber)
    for counter in range(1,101):
        print "fileCounter = %s",counter
        createNormRand(250,86,counter)
    

