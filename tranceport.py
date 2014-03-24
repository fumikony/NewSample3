import csv

def fireCount(inputPath = 'VR_1_34_5.csv',outputPath = 'result_1_34_5.csv',TSTOP = 5000.0):
        file=[]
        filetemp =open(inputPath,'r')
        file1 = open(outputPath,'w')
        
        for row in csv.reader(filetemp, delimiter=','):
                file.append(row)
        
        tstart = int(500.0/0.025)+1
	tsize =int((TSTOP/0.025)/2.0)
        numBin = (TSTOP/250.0)/2.0-2
        
	for i in range(1,87):
                FireFlg = 0
                fireCounter = 0
                for t in range(tstart,tsize):
                        temp = float(file[t][i])
                        if temp >= -20 and FireFlg ==0:
                                fireCounter = fireCounter + 1
                                FireFlg = 1
                        elif temp < -20:
                                FireFlg = 0
                
                file1.write(str(fireCounter/numBin)+",")
                
                fireCounter = 0
                FireFlg = 0
                
                for t in range(tsize+tstart,2*tsize):
                        temp = float(file[t][i])
                        if temp >= -20 and FireFlg == 0:
                                fireCounter = fireCounter + 1
                                FireFlg = 1
                        elif temp < -20:
                                FireFlg = 0
                
                file1.write(str(fireCounter/numBin)+"\n")
        
	filetemp.close()
        file1.close()

