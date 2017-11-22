from nbLib import *
q=float(sys.argv[3])
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
termDictionaryLib.processMLE(len(vocabulary),q)
termDictionaryCon.processMLE(len(vocabulary),q)
#printStats(termDictionaryLib,termDictionaryCon,vocabulary)
correct=0
count=0
with open(sys.argv[2],"r") as fin:
	blogs=fin.read()
	pvlib=math.log(float(termDictionaryLib.blogCount)/float(termDictionaryLib.blogCount+termDictionaryCon.blogCount))
	pvcon=math.log(float(termDictionaryCon.blogCount)/float(termDictionaryLib.blogCount+termDictionaryCon.blogCount))
	for blog in blogs.split("\n"):
		if blog.find("con")==-1 and blog.find("lib")==-1:
			continue
		if(blog.find("con"))!=-1:
			expected=CONSERVATIVE
		else:
			expected=LIBERAL
		mleLibScore=getTotalMLEScore(termDictionaryLib,blog,vocabulary,q)
		mleConScore=getTotalMLEScore(termDictionaryCon,blog,vocabulary,q)
		libScore=mleLibScore+pvlib
		conScore=mleConScore+pvcon
		if(libScore>conScore):
			actual=LIBERAL
			print "L"
		elif(libScore<=conScore):
			actual=CONSERVATIVE
			print "C"
		else:
			print "Some error should have occured"
		if(actual==expected):
			correct+=1
		count+=1
print "Accuracy: "+'{:0.4f}'.format(float(correct)/float(count))