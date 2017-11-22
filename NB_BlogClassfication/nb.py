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
printStats(termDictionaryLib,termDictionaryCon,vocabulary,True)
correct=0
count=0
with open(sys.argv[2],"r") as fin:
	blogs=fin.read()
	pvlib=math.log(float(termDictionaryLib.blogCount)/float(termDictionaryLib.blogCount+termDictionaryCon.blogCount),2)
	pvcon=math.log(float(termDictionaryCon.blogCount)/float(termDictionaryLib.blogCount+termDictionaryCon.blogCount),2)
	for blog in blogs.split("\n"):
		if blog.find("con")==-1 and blog.find("lib")==-1:
			continue
		if(blog.find("con"))!=-1:
			expected=CONSERVATIVE
		else:
			expected=LIBERAL
		#printStats(termDictionaryLib,termDictionaryCon,vocabulary,False)
		mleLibScore=getTotalMLEScore(termDictionaryLib,blog,vocabulary)
		mleConScore=getTotalMLEScore(termDictionaryCon,blog,vocabulary)
		libScore=mleLibScore+pvlib
		conScore=mleConScore+pvcon
		if(libScore>conScore):
			actual=LIBERAL
			print "L"
		elif(libScore<=conScore):
			actual=CONSERVATIVE
			print "C"
		if(actual==expected):
			correct+=1
		count+=1
print "Accuracy: "+'{:0.4f}'.format(float(correct)/float(count))