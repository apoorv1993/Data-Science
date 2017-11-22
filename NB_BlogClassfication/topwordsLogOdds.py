import sys
from nbLib import *
termDictionaryLib=TermDictionary()
termDictionaryCon=TermDictionary()
with open(sys.argv[1],"r") as fin:
	blogs=fin.read()
	for blog in blogs.split("\n"):
		if blog.find("con")!=-1:
			termDictionaryCon.process_blog(blog)
		elif blog.find("lib")!=-1:
			termDictionaryLib.process_blog(blog)
vocabulary=generateVocab(termDictionaryLib,termDictionaryCon)
termDictionaryLib.processMLE(len(vocabulary))
termDictionaryCon.processMLE(len(vocabulary))
logVocabLib={}
logVocabCon={}
for word,_ in vocabulary.iteritems():
	wclib=termDictionaryLib.getMLE(word,len(vocabulary))
	wccon=termDictionaryCon.getMLE(word,len(vocabulary))
	logVocabLib[word]=math.log(wclib)-math.log(wccon)
	logVocabCon[word]=math.log(wccon)-math.log(wclib)
for word,score in findTop(logVocabLib,20):
	print word+" "+'{:0.4f}'.format(score)
print ""
for word,score in findTop(logVocabCon,20):
	print word+" "+'{:0.4f}'.format(score)