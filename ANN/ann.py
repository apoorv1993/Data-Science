import csv,sys
import numpy as np
import timeit,random
#import matplotlib.pyplot as plt
encodingValues={"Yes":1,"yes":1,"No":0,"no":0}
decodingValues={1:"Yes",0:"No",1.0:"Yes",0.0:"No"}
def loadCSV(sFile,skipHeader=True):
    with open(sFile,'r') as dest_f:
        data_iter = csv.reader(dest_f, delimiter = ",")
        data = [data for data in data_iter]
        if skipHeader:
            data=data[1:]
    data_array = np.asarray(data,dtype=None)
    return data_array
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def dsigmoid(y):
    return y * (1.0 - y)
def addBias(input_val):
    input = np.ones((len(input_val),len(input_val[0])+1))
    input[:,1:]=input_val
    return input
def predict(input,weighti_h,weighth_o,addBiasNeuron=False,printValues=False,decimals=2):
    input_layer=input
    if addBiasNeuron:
        input_layer=addBias(input_layer)
    hidden_layer=sigmoid(np.dot(input_layer,weighti_h))
    if addBiasNeuron:
        hidden_layer=addBias(hidden_layer)
    output_layer=sigmoid(np.dot(hidden_layer,weighth_o))
    return output_layer
def calculateError(output,predicted_out,printValues=False,decimals=2):
    if printValues:
        for p,a in zip(np.around(predicted_out,decimals=decimals),np.around(output,decimals=decimals)):
            print str(a)+"=>"+str(p)
    output_error=(np.around(output,decimals=decimals)-np.around(predicted_out,decimals=decimals)) #This is output error
    return 0.5*(np.sum(np.square(output_error))),output_error
def getRandomWeight(seed,thresshold,x,y):
    np.random.seed(seed)
    return np.random.uniform(low=-thresshold,high=thresshold,size=(x,y))
def train(input_count,hidden_count,output_count,step_value,input,output,validation_input,validation_label,epoch,thresshold=0.10,addBiasNeuron=False,maxRunTime=None,
    decimals=2,weighti_h=None,weighth_o=None):
    start=timeit.default_timer()
    bias=0
    if addBiasNeuron:
        bias=1
        input=addBias(input)
    sif weighti_h is None:
        weighti_h=getRandomWeight(1,0.1,input_count+bias,hidden_count)
        weighth_o=getRandomWeight(2,0.1,hidden_count+bias,output_count)
    ##parameters to store bestset of weights
    minError=sys.maxint
    minweighti_h=weighti_h
    minweighth_o=weighth_o
    p_errors_graph=[]
    o_errors_graph=[]
    prev=sys.maxint
    for i in xrange(epoch):
        if maxRunTime:
            runTime=timeit.default_timer()-start
            if runTime>maxRunTime:
                break
        predicted_out=predict(validation_input,weighti_h,weighth_o,addBiasNeuron,False,decimals)
        p_error,_=calculateError(validation_label,predicted_out,False,decimals)
        if p_error<minError:
            minError=p_error
            minweighti_h=weighti_h
            minweighth_o=weighth_o
        if p_error-minError > thresshold*minError:
            #THreshhold found, where curve will increasing, stop training
            break
        #Feed forward
        input_layer=input
        hidden_layer=sigmoid(np.dot(input_layer,weighti_h))
        if addBiasNeuron:
            hidden_layer=addBias(hidden_layer)
        output_layer=sigmoid(np.dot(hidden_layer,weighth_o))
        ###Back propagate
        output_error=(output-output_layer) #This is output error
        mse=0.5*(np.sum(np.square(output_error)))
        if mse>prev:
            pass
            print str(mse)
        prev=mse
        delta_output=dsigmoid(output_layer)*output_error
        hidden_error=np.dot(delta_output,weighth_o.T)
        delta_hidden=dsigmoid(hidden_layer)*hidden_error
        weighth_o+=(step_value*np.dot(hidden_layer.T,delta_output))
        #calculate input to hidden error
        if addBiasNeuron:
            weighti_h+=(step_value*np.dot(input_layer.T,delta_hidden[:,1:]))
        else:
            weighti_h+=(step_value*np.dot(input_layer.T,delta_hidden))
    return minweighti_h,minweighth_o,minError
def encode(A):
    ret=[]
    for d in A:
        if d in encodingValues:
            ret.append(encodingValues[d])
        else:
            ret.append(0.0)
    return ret
def oneHotEncoding(data):
    encoded=[]
    for d in data.T:
        try:
            float(d[0])
            encoded.append(d.tolist())
        except:
            encoded.append(encode(d))
    data_array = np.asarray(encoded,dtype=float).T
    return data_array
def scaleData(data,mins=None,maxs=None):
    data=oneHotEncoding(data)
    high = 1.0
    low = 0.0
    if mins is None:
        mins = np.min(data, axis=0)
        maxs = np.max(data, axis=0)
    rng = maxs - mins
    data = high - (((high - low) * (maxs - data)) / rng)
    return mins,maxs,data
def scaleData100(data,mins=None,maxs=None):
    data=oneHotEncoding(data)
    data/=100
    return None,None,data
if __name__ == "__main__":
    inCSV=loadCSV(sys.argv[1])
    output=loadCSV(sys.argv[2],False)
    p=len(inCSV.T)
    n=len(inCSV)
    mins,maxs,inCSV=scaleData(inCSV)
    minso,maxso,output=scaleData(output)
    inDEVCSV=loadCSV(sys.argv[3])
    outputDEV=loadCSV(sys.argv[4],False)
    _,_,inDEVCSV=scaleData(inDEVCSV,mins,maxs)
    _,_,outputDEV=scaleData(outputDEV,minso,maxso)
    minError=sys.maxint
    minweighti_h=None
    minweighth_o=None
    #10 Fold cross validation
    for i in range(0,10):
        rate=int(0.1*len(inCSV))
        fold=int(rate*i)
        split=np.split(inCSV, [fold, fold+rate])
        split1=np.split(output, [fold, fold+rate])
        validation_input=split[1]
        validation_label=split1[1]
        if len(split[0]) >0 :
            if len(split[2])>0:
                input=np.concatenate((split[0],split[2]),axis=0)
                out=np.concatenate((split1[0],split1[2]),axis=0)
            else:
                input=split[0]
                out=split1[0]
        else:
            input=split[2]
            out=split1[2]
        weighti_h,weighth_o,estimatedMinError=train(p,p+4,1,0.02,input,out,validation_input,validation_label,epoch=10000,thresshold=0.1,addBiasNeuron=False,maxRunTime=2000,decimals=0)
        #This used the best one. It can be modified to keeo all 10 models and use voting or averatge later
        if estimatedMinError<minError:
            minError=estimatedMinError
            minweighti_h=weighti_h
            minweighth_o=weighth_o
    print "TRAINING COMPLETED! NOW PREDICTING."
    p_error,error=predict(inDEVCSV,minweighti_h,minweighth_o,outputDEV,False,True,decimals=0)
    print "Minsquare error for prediction is :"+str(p_error)+", however expected error was "+str(minError)
    print "Average Error is:"+str(np.average(np.abs(error)))
