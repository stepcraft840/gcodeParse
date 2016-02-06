import sys
import io



class UCCNCProfile():
	def __init__(self, profile) :
		self.__config = {}
		with open(profile, 'r') as f:
			line = f.readline()
			currentCategory = ''
			while line:
				if len(line) > 1:
					if line.startswith('['):
						currentCategory = line.strip('\n').strip('[').strip(']')
					else:
						nvPair = line.strip('\n').split('=')
						if nvPair < 2:
							print str(nvPair)
						name = nvPair[0]
						value = nvPair[1]
						if not currentCategory in self.__config:
							self.__config[currentCategory] = {}
						self.__config[currentCategory][name] = value 
				line = f.readline()
			f.closed

	def getConfig(self):
		return self.__config
		
	def getCategories(self):
		return self.__config.keys()
		
	def getProperties(self, category):
		res = []
		if category in self.__config:
			res = self.__config[category].keys()
		return res

	def getCategory(self, category):
		return self.__config[category]
			
	def getProperty(self, category, name):
		category = self.getCategory(category)
		return category[name]
	
	def printProperties(self, category):
		for c in self.getProperties(category):
			print c + '=' + self.getProperty(category, c)
		
#if not len(sys.argv) > 1:
#	raise "no input file provided"
#profile = sys.argv[1]
#pConfig = UCCNCProfile(profile)
#print str(pConfig.getConfig())
#print str(pConfig.getCategories())
#print str(pConfig.getProperties('axessettingscontrolY'))
#print str(pConfig.getCategory('axessettingscontrolY')['Softlimitnegative'])
#print str(pConfig.getCategory('axessettingscontrolY')['Softlimitpositive'])
