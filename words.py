import os
import sys

class WordList():

	file = "words.txt"
	openFile = None
	maxSize = 0
	largestwords = []
	wordList = []
	
	def __init__(self):
		self.__open_file()
		self.load_list()
	
	def __del__(self):
		self.__open_file()
	
	def __open_file(self):
		if self.openFile == None:
			self.openFile = open(self.file,"r")
		
	def __close_file(self):
		if not self.openFile.closed:
			self.openFile.close()
	
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
			if length == wordlength:
				words.append(word)
		print(words)

	def load_list(self):
		self.wordList = []
		for word in self.openFile:
			self.wordList.append(word.strip())
		print("list loaded.")
	
	def quicksort(self, args = None, left = 0, right = 0):
		if args == None:
			args = self.wordList
		if right == 0 :
			right = len(args)-1
		i = left
		j = right
		pivot = len(args[int((left+right) / 2)])
		print ("commencing sort", pivot)
		while ( i <= j ) :
			while (len(args[i]) < pivot) :
				i += 1
			while (len(args[j]) > pivot) :
				j -= 1
			if i <= j :
				#print("switching",args[i],args[j])
				tempword = args[i]
				args[i] = args[j]
				args[j] = tempword	
				i += 1
				j -= 1
		if i < right :
			print("prev")
			return self.quicksort(args, i, right)
		if left < j :
			print("next")
			return self.quicksort(args, left, j)
		print (i," is less than ",right)
		print ("shortest word: ",args[0])
		print ("longest word: ",args[-1])
		return args

os.chdir(os.path.dirname(sys.argv[0])) #change directory to local folder.
LIST = WordList()
LIST.find_words_by_length(16)
LIST.quicksort()
#LIST.find_longest_words()