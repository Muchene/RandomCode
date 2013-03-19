import math
import copy 
from Dataset import *

class Node:
    """Node for a tree structure"""
    def __init__(self, data,label, children):
        self.data = data
        self.children = list()
        self.label = label
        
      
def DTL(trainingds, attributes, default, fulltrn, verbose):
    '''
    This method creates a decision tree using the given training dataset. The nodes
    on which to split are decided using maximum information gain.
    
    param trainds: Dataset to use in building the decision tree
    param attributes: attribute names for the dataset
    param default: Default classification value
    param fulltrn: The full training dataset, this is needed because DTL is recursive
    param verbose: Flag to indicate whether there should be any output during the learning phase
    '''
    if len(trainingds.inputs)== 0 :
        ##no examples
        if verbose:
            print 'Leaf: ' + str(default)
        return Node(default,None,None)
    elif targetsEq(trainingds):
        ##all examples evaluate to same output
        if verbose:
            print 'Leaf: ' + str(trainingds.targets[0])
        return Node(trainingds.targets[0],None, None)
    elif len(attributes) == 0:
        ##no attributes to expand on
        mode = mostFrequent(trainingds.targets)
        if verbose:
            print 'Leaf: ' + str(mode)
        return Node(mode,None,None)
    else:
        best,gain = chooseAttribute(trainingds, attributes) #get the 'best' attribute one which to root this subtree
        attrcopy = copy.copy(attributes)
    
        attrcopy.remove(best)
        root = Node(best,None,None)

        if verbose:
            print "Expanding on atrribute: " + str(best+1) + " Information Gain: " + str(gain)
        for v in fulltrn.possibleValues[best]: 
            trainingwBest = trainingds.getSamples(best, v) ##training set with 'best' attribute = v
            child = DTL(trainingwBest,attrcopy, mostFrequent(trainingds.targets),fulltrn,verbose)
            child.label = v
            root.children.append(child)
        return root

##return the best attribute  to slit upon         
def chooseAttribute(dataset, attributes):
    '''
    Choose the best attribute on which to root the tree. 
    The metric used in deciding which attribute is Information gain
    or the maximum reduction in Entropy
    
    param dataset: training dataset
    param attributes: labels for the input of the training dataset
    '''
    maxGain = 0
    bestAttr = attributes[0]
    for attr in attributes:
        g = gain(dataset,attr)
        if g >= maxGain:
            maxGain = g
            bestAttr = attr
    return bestAttr,maxGain


def targetsEq(ds):
    '''
    Returns true if all targets in the 
    dataset are equal
    '''
    targets = ds.targets
    for i in range(len(targets)):
        if targets[i] != targets[0]: return False  
    return True

def entropy(dataset):
    '''
    Return Entropy value of the given dataset.
    '''
    freqMap = {}
    for t in dataset.targets:
        if t[0] in freqMap:
            freqMap[t[0]] += 1
        else:
            freqMap[t[0]] = 1
    e = 0
    datalen =len(dataset.targets)
    for freq in freqMap.values():
        p = float(freq)/float(datalen)
        e += -p*math.log(p,2)
    return e

def gain(dataset, attr):
    '''
    Calculate the entropy reduction caused by
    removing this attribute from the dataset
    '''
    freqMap = {}
    sub_entropy = 0
    for inp in dataset.inputs:
        if inp[attr] in freqMap:
            freqMap[inp[attr]] += 1
        else:
            freqMap[inp[attr]] = 1

    ##print freqMap.keys()
    for v in dataset.possibleValues[attr]:
        p = float(freqMap[v])/float(len(dataset.inputs))
        sub_entropy += p*entropy(dataset.getSamples(attr, v))
        
    return entropy(dataset) - sub_entropy
        

def mostFrequent(aList):
    '''
    Return the most frequent value in the given list
    '''
    maxim = 0
    mFreq = aList[0]
    for val in aList:
        c = aList.count(val)
        if  c > maxim:
            mFreq = val
            maxim = c
    return mFreq


##recall on a single input
def recall(tree, inp):
    '''
    Use the given tree to classify the given input. This is done by
    traversing the tree from root to a leaf node. The leaf node value
    is used as the class of the input
    
    type tree: Node
    param tree: The root of a decision tree
    
    type inp: list
    param inp: The input to be classified by the tree
    '''
    q = [tree] #maintain a queue and perform a BFS type traversal
    while len(q) > 0:
        current = q[0]
        del q[0]
        if len(current.children) == 0:
            return current.data
        if isinstance(current.data, int):
            value = inp[current.data]
            for c in current.children:
                if c.label == value:
                    q.append(c)
        else:
            return current.data
        


def recallOnDataset(tree,dataset):
    '''
    Classify every input in the given dataset using the given decision tree.
    
    type tree: Node
    param tree: Root of a decision tree
    
    type dataset: Dataset
    param dataset: Dataset to classify
    '''
    print '\n\nRECALL'
    
    inputs = dataset.inputs
    targets = dataset.targets
    index = 0
    numcorrect = 0 
    for inp in inputs:
        t = str(targets[index])
        o =  str(recall(tree,inp))
        if t == o:
            numcorrect += 1
        print "Actual" + t + "Output: " + o
        index += 1
    print '------------------------------------'
    print 'Percent Accurate: ' + str(float(numcorrect)*100/len(inputs))

def test():
    '''
    Test decision tree learning and classification
    '''
    ##Zoo Example
    zoo_attributes = ['hair','feathers','eggs', 'milk', 'airborne','aquatic', 'predator','toothed','backbone','breathes','venomous', 'fins', 'legs','tail', 'domestic','catsize']

    ds = Dataset(16,1) ##training Dataset
    ds.loadFromFile('zoo_train.data',1) ##load it from file
    tst = Dataset(16,1) ##testing Dataset
    tst.loadFromFile('zoo_test.data',1)
    attr = [i for i in range(16)] ##[0,1,2...,15]
    print "++++++++++++++++++++++++++++++++ZOO++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    tree = DTL(ds,attr,mostFrequent(ds.targets),ds,verbose = False) ##make decision tree
    recallOnDataset(tree,tst)
    print '+++++++++++++++++++++++++++++END ZOO +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

##res

if __name__ == '__main__':
    test()

