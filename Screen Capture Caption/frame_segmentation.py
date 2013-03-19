'''
This file contains code to 'caption' the a video. Captioning a 
video means grabbing any text contained within the video. For example
if you have a screen capture video, this program will write the text in that 
screen capture video to a text file. Videos could be thousands of frames, most of
which may be redundant. As such, this program does some basic scene detection (i.e. tries
to detect moments of drastic change in the video) to reduce the total number of frames. A frame is considered as
a transition if the change is between the frame and the previous frame is higher than a factor of 
the standard deviation. OCR is accomplished using tesseract ocr engine.
'''

from cv2 import cv
import numpy 
from scipy.ndimage import *
import tesseract
import sys
from threading import Thread
import thread
from pylab import *
import os
from copy import copy
from random import randint
from math import ceil
import time
from frame_ocr import FrameOcr



def CaptionVideo(videofile):
    '''
    This method takes a video and tries to capture any text contained in the video using tesseract OCR engine.
    In order to avoid OCRing redundant frames, we will try to detect scene changes, or frames in which significant 
    changes happen an only run those frames through OCR. 
    
    
    type videofile: string
    paraam videofile: location of the video file to be captioned
    '''
	
    sceneFrames = [] #frames from current scene
    changeVector = numpy.array([0]) #numerical changes between successive frames 
    cap = cv.CaptureFromFile(videofile)
    success = 1
    prevFrame = 0
    frameNum = 1
	
    while success:
	    success = cv.GrabFrame(cap) #grab a frame at a time
	    if not success:
		    break
	
	    currFrame = cv.RetrieveFrame(cap)

	    #we will represent a frameInfo as {the image, the frame number, the time the frame was recorded}
	    #frameInfo = {'img' : currFrame, 'frameNum': frameNum, 'frameTime': GetFrameTime(frameNum,startTime,fps)}
	    sceneFrames.append(currFrame)	

	    #convert from IIpimage to matrix of pixels so that the difference between frames can be calculated
	    mat = cv.CreateMat(currFrame.height, currFrame.width, cv.CV_32FC3)
	    cv.Convert(currFrame, mat)
	    currFrameArr = numpy.array(mat)

	    ###################Scene Detection#########################################
	    if frameNum > 1:
		    change = CompareImages(prevFrame,currFrameArr) 
		    changeVector = numpy.append(changeVector, change)
		
		    changeMean = mean(changeVector[-200:]) #calculate the mean of the last 200 changes
		    changeStdDev = standard_deviation(changeVector[-200:]) 
		    upperLimit = changeMean + 3*changeStdDev
		    lowerLimit = changeMean - 3*changeStdDev
		
		    #when a scene is detected
		    if change > upperLimit:
			    #send one percent of the frames from current scene to ocr
			    ocrThread = Thread(target = ocr, args = [GetRandomSubset(sceneFrames,.01)])
			    ocrThread.setDaemon(True)
			    ocrThread.start()
			    ocrThread.join()
			    sceneFrames = []
	    ###########################End Scene Detection##########################################
	    frameNum += 1
	    prevFrame = currFrameArr	
    return sceneFrames

def CompareImages(image1, image2):
    '''
    Return a numerical difference betweeen the two given
    images
    '''
	maxchangeframe = 1
	diff = abs(rgb2gray(image1) - rgb2gray(image2))
	if diff.sum() != 0:
		change = diff.sum()/(diff.size * maxchangeframe)
	else:
		change = 0
	return change

def GetRandomSubset(alist,prop):
    '''
    Returns a random subset of alist
    '''
	length = len(alist)
	subset = []
	for i in range(int(ceil(length*prop))):
		randIndex = randint(0,length-1)
		while alist[randIndex]  in  subset:
			randIndex = randint(0, length-1)
		subset.append(alist[randIndex])
	return subset



global ocrLock #lock to allow multiple access to file where text is written
ocrLock = thread.allocate_lock()

def ocr(frames):
    '''
    This Method runs the given frames through OCR and writes the resulting
    text in a result file.

    type frames: list
    param frames: A list of frames which to run through the OCR space
    '''
    ocrLock.acquire()
    f = open('Ocr Results.txt','a')
    frameNum = 0 
    for img in frames:
        text += 'OCR of Frame %d'%frameNum
        frameNum += 1
        text = FrameOcr(img) + '\n' ##get the ocr
        f.write(text)
    f.close()
    ocrLock.release()

if __name__ == '__main__':
    if sys.argc != 2:
        print 'Usage frame_segmentation [video filename]'
    else:
        CaptionVideo(sys.argv[1])
	
	

