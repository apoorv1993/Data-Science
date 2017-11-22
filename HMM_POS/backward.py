import sys
from hmm import *
if len(sys.argv)!=5:
	print "Incorrect no of arguments"
	sys.exit(1)
dev,trans,emit,prior=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
transMatrix=processTransitionProbability(trans)
emissionMatrix=processEmissionProbability(emit)
priorMatrix=processPriorProbability(prior)
for prob in backwardMatrix(dev,transMatrix,emissionMatrix,priorMatrix):
	print prob