#!/usr/bin/env python3

# Python libs
import sys, time

# OpenCV
import cv2 as cv

# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import Image
from rqt_mypkg.msg import UAVForge
from rqt_mypkg.msg import UAVForge_bool

#CV bridge
from cv_bridge import CvBridge

import random

def callback(data):

	if data.correct:
	    check = 'correct'
	
	else:
	    check = 'incorrect'    
	
	rospy.loginfo(str(data.num)+" Image: " + str(data.image_ID) + " is " + check + "." )
	
	#put in queue
	
def main():

	rospy.init_node('printer', anonymous=True)	
	
	rospy.Subscriber('correct', UAVForge_bool, callback)

	rospy.spin()
	
if __name__ == '__main__':

	try:
		main()
		
	except rospy.ROSInterruptException:
	
		pass	
