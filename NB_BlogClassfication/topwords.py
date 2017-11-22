import sys
from nbLib import *
N=20
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
#printStats(termDictionaryLib,termDictionaryCon,vocabulary)
top20=termDictionaryLib.top(N)
for word,score in top20:
	print word+" "+'{:0.4f}'.format(score)
print ""
top20=termDictionaryCon.top(N)
for word,score in top20:
	print word+" "+'{:0.4f}'.format(score)

