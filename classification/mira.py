# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util
import math
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def newTao(self, incWeight, correctWeight, feature ):
        deltaWeight = incWeight-correctWeight
        newDeltaWeight = deltaWeight*feature +1.0
        divisor = math.sqrt(feature*feature)*2.0
        return newDeltaWeight/divisor

    def multCounter(self, num, count):
        newCounter = count.copy()
        for  i in count.keys():
            newCounter[i] = count[i] *num
        return newCounter

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        evals = 0
        bestWeight = {}
        bestValidation = -1
        print(list(Cgrid))
        newWeights = self.weights.copy()
        for c in Cgrid:
            self.weights = newWeights.copy()
            #self.initializeWeightsToZero()
            #errors = []
            for iteration in range(self.max_iterations):
                for i in range(len(trainingData)):
                    maxLabel = -1
                    maxValue = float("-inf")
                    for label in self.legalLabels:
                        #Score (activacion) de la clase
                        value = trainingData[i]*self.weights[label]
                        if value > maxValue:
                            maxValue = value
                            #Quedarse con el maximo
                            maxLabel = label
                    if maxLabel != trainingLabels[i]:
                        tao = self.newTao(self.weights[maxLabel], self.weights[trainingLabels[i]],trainingData[i])
                        print("tao="+str(tao))
                        nTao = min(tao,c)
                        print(nTao)
                        self.weights[maxLabel] -= self.multCounter(nTao,trainingData[i])
                        self.weights[trainingLabels[i]] += self.multCounter(nTao,trainingData[i])

            guesses = self.classify(validationData)
            countguess=0
            print(c)
            print(len(guesses))
            for i in range(len(guesses)):
                if guesses[i] == validationLabels[i]:
                    countguess +=1
            print("bestVal ="+str(bestValidation))
            print("count = "+str(countguess))
            if bestValidation<countguess:
                bestValidation = countguess
                bestWeight = self.weights
        self.weights = bestWeight


    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses
