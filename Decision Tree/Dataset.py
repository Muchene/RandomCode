'''
This file contains the definition of class Dataset to be used in decision tree learning and classification
'''
class Dataset:

    def __init__(self, indim, outdim):
        '''
        param indim: The input dimension
        param outdim: The output dimension
        '''
        self.indim = indim
        self.outdim = outdim
        self.inputs = []
        self.targets = []
        self.possibleOutputs = [] ##possibleOutputs[n-1] stores all the possible values for output feature n
        self.possibleValues = [] ##possibleValues[n-1] stores all the possible values for attribute n.
        for i in range(indim):
            self.possibleValues.append(set([]))
        for i in range(outdim):
            self.possibleOutputs.append(set([]))
        
        
    #Add a data vector to the dataset i.e. inp:[1,0,0,1,.....] target:[1,0...]
    def addSample(self, inp, target):
        if len(inp) == self.indim and len(target) == self.outdim:
            self.inputs.append(inp)
            self.targets.append(target)
    
            for i in range(self.indim):
                self.possibleValues[i].add(inp[i])
            for i in range(self.outdim):
                self.possibleOutputs[i].add(target[i])
        else:
            raise Exception("Error Dimensions don't match\nIndim: " + str(self.indim) + " Outdim: " + str(self.outdim))
    
    #Load dataset from comma seperated file
    def loadFromFile(self, filename,offset):
        f = open(filename)
        for line in f:
            line = line.replace('\n','')
            if line != '':
                splitLine = line.replace(' ', '').split(',') #remove space and split by commas
                
                #collect the input 
                inp = []
                for i in range(offset,self.indim+offset):
                    val = splitLine[i]
                    inp.append(val)
                
                #collect the target
                target = []
                for i in range(self.indim+offset, self.indim+self.outdim+offset):
                    
                    target.append(splitLine[i])
                self.addSample(inp,target)
        f.close()

    ##return a Dataset containing samples which input[attr] = value or target[attr]
    def getSamples(self, attr, value):
        rDs = Dataset(self.indim,self.outdim)
        index = 0 
        for inp in self.inputs:
            if inp[attr] == value:
                rDs.addSample(inp, self.targets[index])
            index += 1
        return rDs

    ##Update all possible values
    def  updatePossibleValues(self):
        '''
        Set the possible value which attributes can take on
        '''
        self.possibleValues = [set([]) for i in range(self.indim)] ##reset the possible values
        for inp in self.inputs:
            for i in range(self.indim):
                self.possibleValues[i].add(inp[i])

    def getSamplesT(self, tbit, value):
        '''
        Return a dataset containing samples whose targets[tbit] is equal to the given 
        value
        '''
        rDs = Dataset(self.indim,self.outdim)
        index = 0 
        for targ in self.targets:
            if targ[tbit] == value:
                rDs.addSample(self.inputs[index], targ)
            index += 1
        return rDs
