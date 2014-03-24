import random
import math
import threading
import time
import multiprocessing
from multiprocessing import Process, Pool

NEURON_NUM = 86
multiSEList = [[]]*NEURON_NUM

def createPoisson(RandomMax = 0.0,NC = 0,STM_TIME_TERM = 200000):
	StimEventsList = []
	print "Neuorn Number = %s,STM_TIME_TERM = %s" %(NC,STM_TIME_TERM)
	
	random.seed()
	for TimeCount in range(1, int(STM_TIME_TERM + 1)):
		if RandomMax > random.random():
			StimEventsList.append(TimeCount)
	
	return StimEventsList

def writeStimEvent(StimEventsFileName = "StimEvents.txt",SELList = [[]],MSEC_PAR_COUNT = 40.0):
	SEF = open(StimEventsFileName, "w")
	counter = 1
	for stimEventsList in SELList:
		SEF.write(str(counter) + "\t" + str(len(stimEventsList)))
		for stimEvents in stimEventsList:
			SEF.write("\t" + str(float(stimEvents)*MSEC_PAR_COUNT))
		
		counter = counter + 1
		SEF.write("\n")
	
	SEF.close()
	return 1

def writeStimCount(StimEventsFileName = "StimEvents.txt",SELList = [[]]):
	SEF = open(StimEventsFileName, "w")
	counter = 1
	for stimEventsList in SELList:
		SEF.write(str(counter) + "," + str(len(stimEventsList)) + "\n")
		counter = counter + 1
	
	SEF.close()
	return 1

def writeStimEvent2(StimEventsFileName = "StimEvents.txt",MSEC_PAR_COUNT = 40.0):
	SEF = open(StimEventsFileName, "w")
	counter = 1
	for stimEventsList in multiSEList:
		SEF.write(str(counter) + "\t" + str(len(stimEventsList)))
		for stimEvents in stimEventsList:
			SEF.write("\t" + str(float(stimEvents)*MSEC_PAR_COUNT))
		
		counter = counter + 1
		SEF.write("\n")
	
	SEF.close()
	return 1

def writeStimCount2(StimEventsFileName = "StimEvents.txt",SELList = [[]]):
	SEF = open("StimEvents.txt", "a")
	counter = 1
	for stimEventsList in SELList:
		SEF.write(str(counter) + "," + str(len(stimEventsList)))
		counter = counter + 1
	SEF.write("\n")
	SEF.close()
	return 1

def readStimVoltage(StimVoltageFileName = "StimVoltage.txt"):
	StimValueFile = open(StimVoltageFileName, "r")
	
	StimRamdaList = []
	for line in StimValueFile:
		StimRamda = float(line)
		StimRamdaList.append(StimRamda)
	
	StimValueFile.close()
	
	return StimRamdaList

def createStim(pathInputFile = "StimVoltage.txt",pathOutputFile = "StimEvents.txt",TimeStop = 5000.0,StimTimeTerm = 200000):
	PROB_STIM = TimeStop/(250.0 * StimTimeTerm)
	MSEC_PAR_COUNT = TimeStop/StimTimeTerm
	
	StimRamdaList = readStimVoltage(pathInputFile)
	
	print "= START_CREATE_STIM_EVENTS ="
	random.seed(2014) 
	selList = []
	
	for NeuronCount in range(1, int(NEURON_NUM + 1)):
		rndMax = PROB_STIM*StimRamdaList[NeuronCount-1]
		#print "%s,%s" %(PROB_STIM,rndMax)
		selList.append(createPoisson(rndMax,NeuronCount,StimTimeTerm))
	
	writeStimEvent(pathOutputFile,selList,MSEC_PAR_COUNT)
	
	print "= END_CREATE_STIM_EVENTS ="
	return 1

def multiTemp(NeuronCount,StimTimeTerm,StimRamdaList,PROB_STIM):
	rndMax = PROB_STIM*StimRamdaList[NeuronCount-1]
	print "%s,%s" %(NeuronCount,rndMax)
	multiSEList[NeuronCount-1] = createPoisson(rndMax,NeuronCount,StimTimeTerm)

def createStimMulti(pathInputFile = "StimVoltage.txt",pathOutputFile = "StimEvents.txt",TimeStop = 5000.0,StimTimeTerm = 200000):
	PROB_STIM = TimeStop/(250.0 * StimTimeTerm)
	
	StimRamdaList = readStimVoltage(pathInputFile)
	
	print "START_CREATE_STIM_EVENTS"
	
	threads = []
	for NeuronCount in range(1,int(NEURON_NUM+1)):
		t = threading.Thread(target=multiTemp,args=(NeuronCount,StimTimeTerm,StimRamdaList,PROB_STIM,))
		threads.append(t)
		t.start()
		time.sleep(0.001)
	
	for t in threads:
		t.join()
	
	writeStimCount(pathOutputFile)
	
	print "END_CREATE_STIM_EVENTS"

def createStims(pathInputFile = "StimVoltage.txt",pathOutputFile = "StimEvents.txt",TimeStop = 5000.0,StimTimeTerm = 200000,ThreadNum = 10):
	
	print "== START_CREATE_STIM_EVENTS =="
	
	threads = []
	for tc in range(1,int(ThreadNum+1)):
		tempFile = pathOutputFile.split(".")
		OutputFilePath = tempFile[0] + str(tc) + "." + tempFile[1]
		print "%s" %(OutputFilePath)
		t = threading.Thread(target=createStim,args=(pathInputFile,OutputFilePath,TimeStop,StimTimeTerm))
		threads.append(t)
		t.start()
	
	for t in threads:
		t.join()
	
	print "== END_CREATE_STIM_EVENTS =="

def argwrapper(args):
    return args[0](*args[1:])

def multiProcessingCS(pathInputFile = "StimVoltage.txt",pathOutputFile = "StimEvents.txt",TimeStop = 5000.0,StimTimeTerm = 200000,ThreadNum = 10):
	print "== START_CREATE_STIM_EVENTS =="	
	p = Pool(multiprocessing.cpu_count())
	func_args = []
	for tc in range(1,int(ThreadNum + 1)):
		tempFile = pathOutputFile.split(".")
		OutputFilePath = tempFile[0] + str(tc) + "." + tempFile[1]		
		func_args.append( (createStim, pathInputFile, OutputFilePath, TimeStop, StimTimeTerm) )
	p.map(argwrapper, func_args)
	p.terminate()
	print "== END_CREATE_STIM_EVENTS =="
