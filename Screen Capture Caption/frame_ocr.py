from cv2 import cv
import tesseract
from utils import *

def FrameOcr(img):
    '''
    Use the tesseract api to OCR the given frame.
    '''
	api = tesseract.TessBaseAPI()
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetPageSegMode(tesseract.PSM_AUTO)
	text = ""	

	##img = cv.LoadImage(SENS_FRAME_DIR + str(frameNum) +'.png')
	#####Preprocess each frame to improve ocr###############
	threshold=140
	colour=255
	#binarize the image
	cv.Threshold(img,img, threshold,colour,cv.CV_THRESH_BINARY) 
	#scale the image up
	imgProcessed = cv.CreateImage((img.width * 4,img.height *4), img.depth, img.nChannels)
	cv.Resize(img, imgProcessed)
	tesseract.SetCvImage(imgProcessed,api)
	
	text = api.GetUTF8Text() 
	conf=api.MeanTextConf()
	return text
