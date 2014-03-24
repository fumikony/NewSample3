import csv

def fireCount(inputPath = 'VR_1_34_5.csv',outputPath = 'result_1_34_5.csv',TSTOP = 5000.0):
        file=[]
        filetemp =open(inputPath,'r')
        file1 = open(outputPath,'w')

	timeBin = 250*40
        
        for row in csv.reader(filetemp, delimiter=','):
                file.append(row)
        
        numBin = TSTOP/250.0
        print "numBin = %s\n",int(numBin)
	for i in range(1,87):
		print "NEURON%s\n",i
		for s in range(0,int(numBin)):
			FireFlg = 0
			fireCounter = 0
			for t in range(timeBin*s,(timeBin*s)+timeBin):
				temp = float(file[t][i])
				if temp >= -20 and FireFlg ==0:
					fireCounter = fireCounter + 1
					FireFlg = 1
				elif temp < -20:
					FireFlg = 0
                
			file1.write(str(fireCounter)+",")
		file1.write("\n")
                fireCounter = 0
                FireFlg = 0
	filetemp.close()
        file1.close()

