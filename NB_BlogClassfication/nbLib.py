import sys,math
LIBERAL=1
CONSERVATIVE=0
GENERAL=-1
class Term:
	def __init__(self,term):
		self.term=term
		self.mle=0.0
		self.count=0.0
	def __str__(self):
		return "Term::"+self.term+" ["+str(self.count)+"]["+str(self.mle)+"]"
class TermDictionary:
	def __init__(self):
		self.terms={}
		self.wordCount=0
		self.blogCount=0
	def process_blog(self,file):
		with open(file,"r") as fin:
			data=fin.read()
			for word in data.split("\n"):
				word=word.lower()
				if len(word)==0 or word==" ":
					continue
				if word not in self.terms:
					self.terms[word]=Term(word)
				self.wordCount+=1
				self.terms[word].count+=1
			self.blogCount+=1
	def calculateMLE(self,nk,n,lenVocab,q=1.0):
		return float(nk+q)/float(n+q*lenVocab)
	def findMLE(self,word,vocabSize,q):
		word=word.lower()
		if word not in self.terms:
			nk=0
		else:
			nk=self.terms[word].count
		n=self.wordCount
		return self.calculateMLE(nk,n,vocabSize,q)
	def processMLE(self,vocabSize,q=1.0):
		for word,termObj in self.terms.iteritems():
			self.terms[word].mle=self.findMLE(word,vocabSize,q)
	def getMLE(self,word,vocabSize,q=1):
		if word not in self.terms:
			return self.findMLE(word,vocabSize,q)
		return self.terms[word].mle
	def top(self,n):
		ret=sorted([(value.mle,key) for key,value in self.terms.iteritems()],reverse=True)
		count=1
		for score,word in ret:
			if count<=n:
				yield (word,score)
			else:
				break
			count+=1
	def delTerm(self,word):
		if word in self.terms:
			self.wordCount-=self.terms[word].count
			del self.terms[word]
	def removeStopWords(self,n):
		topWords=self.top(n)
		for word,score in topWords:
			del self.terms[word]
	def combineVocab(self,dic):
		for word,termObj in self.terms.iteritems():
			if word not in dic:
				dic[word]=0
			dic[word]+=termObj.count
		return dic
	def printAll(self, terms=False):
		if terms:
			for term,obj in self.terms.iteritems():
				print obj
		print "Total distinct words:"+str(len(self.terms))
		print "Total words:"+str(self.wordCount)
def getTotalMLEScore(termDictionary,file,vocab,q=1):
	logScore=0
	count=0
	count1=0
	with open(file,"r") as fin:
		data=fin.read()
		for word in data.split("\n"):
			word=word.lower()
			if word in vocab:
				logScore+=math.log(termDictionary.getMLE(word,len(vocab),q))
	return logScore
def findTop(vocabulary,n):
	top=sorted([(value,key) for key,value in vocabulary.items()],reverse=True)
	count=1
	for score,word in top:
		if count<=n:
			yield (word,score)
		else:
			break
		count+=1
def generateVocab(A,B):
	dic={}
	dic=A.combineVocab(dic)
	dic=B.combineVocab(dic)
	return dic
def printStats(lib,con,vocab,terms=False):
	print "Liberal Stats"
	lib.printAll(terms)
	print "Conservative stats"
	con.printAll(terms)
	print "No of liberal blogs:"+str(lib.blogCount)
	print "No of conservative blogs:"+str(con.blogCount)
	print "Total vocabulary size:"+str(len(vocab))
