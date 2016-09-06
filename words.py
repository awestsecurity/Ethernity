import os
import sys

class WordList():

	#file = "words.txt"
	openFile = None
	maxSize = 0
	wordList = []
	listlength = 0
	
	def __init__(self,length=""):
		filename = "words"+str(length)+".txt"
		self.__open_file(filename)
		self.load_list()
	
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
		#print("list loaded.")
	
	def count_words_by_length(self, length):
		number = 0
		for word in self.openFile:
			word = word.strip()
			
	def find_longest_words(self):
		largest = 0
		i = 0
		for word in self.openFile:
			length = len(word.strip())
			if length > self.maxSize:
				self.maxSize = length
				self.largestwords = []
				self.largestwords.append( word )
			elif length == self.maxSize:
				self.largestwords.append( word )
			i += 1
		print("Longest words: ",self.maxSize,self.largestwords)
		
	def find_words_by_length(self, wordlength):
		words = []
		for word in self.wordList:
			length = len(word)
			if length == wordlength: words.append(word)
		return words

	def write_wordlist(self, list, filename = "untitled.txt", lowfilter = 0, highfilter = 9999):
		file = open(filename, 'w')
		for line in list:
			if len(line) >= lowfilter and len(line) <= highfilter : file.write(line + "\n")
		file.close()
		print("list written with low filter: %r and upperlimit: %r" % (lowfilter, highfilter) )
		
#l = WordList()
#l.write_wordlist(l.wordList,"words16.txt",16,16)