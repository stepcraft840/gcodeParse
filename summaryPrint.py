import sys
import io
from profile import UCCNCProfile

if not len(sys.argv) > 1:
	raise "no gcode file provided"
gcodeFile = sys.argv[1]
print 'using gcode file: ' + gcodeFile
pFile = None
if len(sys.argv) > 2:
	pFile = sys.argv[2]
	print 'using profile: ' + pFile

commandsUsed = []
mins = {}
maxs = {}
axis = ['X', 'Y', 'Z', 'A', 'B', 'C', 'F']
filamentExtruded = 0
currentE = 0
#init
for a in axis:
	mins[a] = 999999999
	maxs[a] = -999999999

def updateMinMax(aName, value):
	if value.startswith(aName):
		numb = float(value.split(aName)[1])
		if numb > maxs[aName]:
			maxs[aName] = numb
		if numb < mins[aName]:
			mins[aName] = numb
			
with open(gcodeFile, 'r') as f:
	line = f.readline()
	while line:
		if (len(line) > 0):
			currentCmd = line
			if ';' in line:
				currentCmd = line.split(';')[0]
			if (len(currentCmd) > 0):
				cmdPart = currentCmd.split()
				if len(cmdPart) > 0:
					gcodeCmd = cmdPart[0]
					if not gcodeCmd in commandsUsed:
						commandsUsed.append(gcodeCmd)
					for i in range(1, len(cmdPart)):
						currentPart = cmdPart[i]
						for a in axis:
							updateMinMax(a, currentPart)
						if currentPart.startswith('E'):
							eValue = float(currentPart.split('E')[1])
							if eValue < currentE:
								filamentExtruded += currentE
							else:
								currentE = eValue
						
		line = f.readline()
	f.closed
print 'commands required: ' + str(sorted(commandsUsed))
for a in axis:
	if not mins[a] == 999999999:
		print 'range'+str(a) + '='+str(mins[a]) + ',' + str(maxs[a])
	else:
		print 'range'+str(a) + '=0,0'
print 'filament required: ' + str(filamentExtruded + currentE)
if pFile:
	pConfig = UCCNCProfile(pFile)
	homeOffset = pConfig.getCategory('Workoffset_G54')
	homeOffsetAxis = 0
	for a in axis:
		if 'axessettingscontrol' + a in pConfig.getCategories():
			if 'Workoffset' + a in homeOffset:
				homeOffsetAxis = float(homeOffset['Workoffset' + a])
			maxP = pConfig.getCategory('axessettingscontrol' + a)['Softlimitpositive']
			print 'profile soft limit positive for ' + a + ' is ' + maxP
			actualLimitMax = (maxs[a] + homeOffsetAxis)
			if pConfig.getCategory('axessettingscontrol' + a)['Homedirectionpositive'] == 'False':
				actualLimitMax = (maxs[a] - homeOffsetAxis)
			if actualLimitMax > float(maxP):
				print 'ERROR: axis ' + a + ' profile soft limit ' + str(maxP) + ' is too low for inputted gcode required max ' + str(actualLimitMax)
			else:
				print a + ' max limit ok at ' + str(maxs[a])
				
			minP = pConfig.getCategory('axessettingscontrol' + a)['Softlimitnegative']
			print 'profile soft limit negative for ' + a + ' is ' + minP
			actualLimitMin = (mins[a] + homeOffsetAxis)
			if pConfig.getCategory('axessettingscontrol' + a)['Homedirectionpositive'] == 'False':
				actualLimitMin = (mins[a] - homeOffsetAxis)
			if actualLimitMin > float(maxP):
				print 'ERROR: axis ' + a + ' profile soft limit ' + str(minP) + ' is too high for inputted gcode required min ' + str(actualLimitMin)
			else:
				print a + ' min limit ok at ' + str(mins[a])
			print pConfig.getCategory('axessettingscontrol' + a)['Homedirectionpositive']
			#pConfig.printProperties('axessettingscontrol' + a)