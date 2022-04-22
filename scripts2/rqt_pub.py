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

def publisher():
	
	pub = rospy.Publisher('image_test', UAVForge, queue_size=10)
	
	return pub
	
def main():

	rospy.init_node('sender', anonymous=True)	
	
	pub = publisher()
	
	path = '/home/ryan/catkin_ws/src/rqt_mypkg/Images/'
	
	jpegs = ['im0.jpg', 'im1.jpg', 'im2.jpg', 'im3.jpg'] 
	
	ID = ['alley', 'umbrella', 'van', 'belt']
	
	images = [' ', ' ', ' ', ' ']
	
	colors = [ 'black', 'blue', 'blue green', 'blue violet', 'brown', 'carnation pink', 'green', 'orange', 'red', 'red orange', 'red violet', 'violet', 'white', 'yellow', 'yellow green', 'yellow orange']
	
	alphanum = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
	
	shapes = ['Triangle', 'Square', 'Circle', 'Semi-Circle', 'Oval', 'Pentagon', 'Hexagon']
	
	orien = ['Upside Down', 'Sideways', 'Diagonal', 'Right Side Up']

	
	for i in range(0, len(jpegs)):
	
	    img = cv.imread(path + jpegs[i])
	
	    bridge = CvBridge()
	
	    images[i] = bridge.cv2_to_imgmsg(img, encoding="rgb8")
	    
	    
	
	msg = UAVForge()
	
	rate = rospy.Rate(1) 
	
	counter = 0
	
	while not rospy.is_shutdown():
            
            file = random.randint(0, len(images) - 1)
	    
            msg.image = images[file]
            
            msg.file_name = jpegs[file]
            
            msg.image_ID = ID[file]
            
            msg.shape = shapes[random.randint(0, len(shapes) - 1)]
            
            msg.shape_color = colors[random.randint(0, len(colors) - 1)]
            
            msg.alphanum = alphanum[random.randint(0, len(alphanum) - 1)]
            
            msg.alphanum_color = colors[random.randint(0, len(colors) - 1)]
            
            msg.alphanum_ori = orien[random.randint(0, len(orien) - 1)]
                
            msg.geo_loc[0] = random.uniform(0, 100)
            
            msg.geo_loc[1] = random.uniform(0, 100)
            
            msg.num = counter
            
            pub.publish(msg)
            
            rospy.loginfo(str(msg.num)+" Sent "+str(msg.file_name)+". It is a " + msg.shape_color +" " + msg.shape + " with a " + msg.alphanum_ori + " " + msg.alphanum_color + " " + msg.alphanum + " on it located at " +str(msg.geo_loc) + " with ID "+str(msg.image_ID)+"." )
                
            counter = counter + 1
            
            rate.sleep()

if __name__ == '__main__':
	try:
		main()
		
	except rospy.ROSInterruptException:
	
		pass
       
        
	
	
	
