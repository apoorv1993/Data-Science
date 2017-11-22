import sys,collections,math
from logsum import *
def multiply(a,b):
	return math.log(a)+math.log(b)
def processTransitionProbability(inFile):
	transMatrix={}
	with open(inFile,"r") as input:
		lines=input.read().strip()
		for line in lines.split("\n"):
			items=line.split()
			state=items[0]
			transMatrix[state]={}
			for item in items[1:]:
				item=item.strip().split(":")
				tState,prob=item[0],float(item[1])
				transMatrix[state][tState]=prob
	return transMatrix
def processEmissionProbability(inFile):
	emissionMatrix={}
	with open(inFile,"r") as input:
		lines=input.read().strip()
		for line in lines.split("\n"):
			items=line.split()
			state=items[0]
			emissionMatrix[state]={}
			for item in items[1:]:
				item=item.strip().split(":")
				observable,prob=item[0],float(item[1])
				emissionMatrix[state][observable]=prob
	return emissionMatrix
def processPriorProbability(inFile):
	priorMatrix={}
	with open(inFile,"r") as input:
		lines=input.read().strip()
		for line in lines.split("\n"):
			items=line.split()
			state,prior=items[0].strip(),float(items[1].strip())
			priorMatrix[state]=prior
	return priorMatrix
def forwardMatrix(dev,transMatrix,emissionMatrix,priorMatrix):
	with open(dev,"r") as inFile:
		lines=inFile.read().strip()
		states=transMatrix.keys()
		for sentence in lines.split("\n"):
			observables=sentence.split()
			T=len(observables)-1
			alpha={}
			alpha[0]={ state:(multiply(priorMatrix[state],emissionMatrix[state][observables[0]])) for state in states}
			for t in range(T):
				alpha[t+1]={}
				for state in states:
					summation=alpha[t][states[0]]+math.log(transMatrix[states[0]][state])
					for prevState in states[1:]:
						summation=log_sum(summation,alpha[t][prevState]+math.log(transMatrix[prevState][state]))
					alpha[t+1][state]=math.log(emissionMatrix[state][observables[t+1]])+summation
			prob=alpha[T][states[0]]
			for state in states[1:]:
				prob=log_sum(prob,alpha[T][state])
			yield prob
def backwardMatrix(dev,transMatrix,emissionMatrix,priorMatrix):
	with open(dev,"r") as inFile:
		lines=inFile.read().strip()
		states=transMatrix.keys()
		for sentence in lines.split("\n"):
			observables=sentence.split()
			T=len(observables)-1
			beta={}
			beta[T]={state:math.log(1) for state in states}
			for t in range(T-1,-1,-1):
				beta[t]={}
				for state in states:
					summation=None
					for nextState in states:
						beta_t_plus_1=beta[t+1][nextState]
						a_ij=math.log(transMatrix[state][nextState])
						b_j_ot=math.log(emissionMatrix[nextState][observables[t+1]])
						if summation:
							summation=log_sum(summation,beta_t_plus_1+a_ij+b_j_ot)
						else:
							summation=beta_t_plus_1+a_ij+b_j_ot
					beta[t][state]=summation
			prob=None
			for state in states:
				prior=math.log(priorMatrix[state])
				bi=math.log(emissionMatrix[state][observables[0]])
				beta_1=beta[0][state]
				if prob:
					prob=log_sum(prob,prior+bi+beta_1)
				else:
					prob=prior+bi+beta_1
			yield prob
def viterbi(dev,transMatrix,emissionMatrix,priorMatrix):
	with open(dev,"r") as inFile:
		lines=inFile.read().strip()
		states=transMatrix.keys()
		for sentence in lines.split("\n"):
			observables=sentence.split()
			T=len(observables)-1
			VP={}
			Q_Star={}
			Q_Star[0]={state:[state] for state in states}
			VP[0]={state:(math.log(priorMatrix[state])+math.log(emissionMatrix[state][observables[0]])) for state in states}
			for t in range(T):
				VP[t+1]={}
				Q_Star[t+1]={}
				for state in states:
					maxValue=float('-inf')
					maxArg=None
					for j in states:
						val=VP[t][j]+math.log(transMatrix[j][state])+math.log(emissionMatrix[state][observables[t+1]])
						if val>maxValue:
							maxValue=val
							maxArg=j
					VP[t+1][state]=maxValue
					ar=[]
					ar.extend(Q_Star[t][maxArg])
					ar.append(state)
					Q_Star[t+1][state]=ar
			maxValue=float('-inf')
			maxArg=None
			for j in states:
				if VP[T][j]>maxValue:
					maxValue=VP[T][j]
					maxArg=j
			st=""
			for i,observable in enumerate(observables):
				st+=(observable)+"_"+Q_Star[T][maxArg][i]+" "
			yield st



