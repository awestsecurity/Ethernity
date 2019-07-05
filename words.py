import os
import sys

class WordList():

	file = "sortedwords.txt"
	openFile = None
	maxSize = 0
	wordList = []
	wordkeys = []
	listlength = 0
	
	instance = None
	
	def __init__(self):
		if type(self).instance == None:
			filename = type(self).file
			self.__open_file(filename)
			self.load_list()
			type(self).instance = self
			print("Word List Loaded")
	
	#def __del__(self):
	#	self.openFile.close()
	
	def __open_file(self, filename = ""):
		os.chdir(os.path.dirname(sys.argv[0])) #change directory to local folder.
		#if self.file == "" : self.file = type(self).file
		if self.openFile == None:
			try:
				self.openFile = open(filename,"r")
			except:
				print("Cannot open file: "+filename+". Check name.")
			
		
	def __close_file(self):
		if not self.openFile.closed:
			self.openFile.close()
	
	def load_list(self):
		self.wordList = []
		for word in self.openFile: self.wordList.append(word.strip())
		self.listlength = len(self.wordList)-1
		i = 0
		j = 1
		self.wordkeys.append(0)
		while i < self.listlength:
			if len(self.wordList[i]) > j:
				self.wordkeys.append(i)
				j += 1
			i += 1
		#print("list loaded.")
	
	def find_words_by_length(self, wordlength):
		words = []
		for n in range(self.wordkeys[wordlength-1],self.wordkeys[wordlength]):
			words.append(self.wordList[n])
		return words

	def write_wordlist(self, list, filename = "untitled.txt", lowfilter = 0, highfilter = 9999):
		file = open(filename, 'w')
		for line in list:
			if len(line) >= lowfilter and len(line) <= highfilter : file.write(line + "\n")
		file.close()
		print("list written with low filter: %r and upperlimit: %r" % (lowfilter, highfilter) )
		
#l = WordList()
#print(l.find_words_by_length(14))
#l.write_wordlist(l.wordList,"words16.txt",16,16)