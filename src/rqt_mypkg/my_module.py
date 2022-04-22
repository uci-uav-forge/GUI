#!/usr/bin/env python3

import os
import rospy
import rospkg

# Ros Messages
from sensor_msgs.msg import Image
from rqt_mypkg.msg import UAVForge
from rqt_mypkg.msg import UAVForge_bool

#CV bridge
from cv_bridge import CvBridge

# OpenCV
import cv2 as cv


from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget
from python_qt_binding.QtGui import QPixmap, QFont

class MyPlugin(Plugin):

    def __init__(self, context):
        super(MyPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('MyPlugin')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print('arguments: ', args)
            print ('unknowns: ', unknowns)

        # Create QWidget
        self._widget = QWidget()
        
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rospkg.RosPack().get_path('rqt_mypkg'), 'resource', 'MyPlugin.ui')
        
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        
        # Give QObjects reasonable names
        self._widget.setObjectName('MyPluginUi')
        
        self.image = self._widget.Image
        self.yes = self._widget.Yes
        self.no = self._widget.No
        self.c = self._widget.Counter
        self.t = self._widget.Tracker
        self.classify = self._widget.Classify
        self.geo_loc = self._widget.Geo_Location
        self.path = '/home/ryan/catkin_ws/src/rqt_mypkg/Queue/'
        
        self.c.setFont(QFont('Arial', 20))
        self.t.setFont(QFont('Arial', 20))
        self.classify.setFont(QFont('Arial', 20))
        self.geo_loc.setFont(QFont('Arial', 20))
        
        self.queue = []
        
        self.yes.clicked.connect(self.buttonY)
        
        self.no.clicked.connect(self.buttonN)
        
        # Show _widget.windowTitle on left-top of each plugin (when 
        # it's set in _widget). This is useful when you open multiple 
        # plugins at once. Also if you open multiple instance0s of your 
        # plugin at once, these lines add number to make it easy to 
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
            
        # Add widget to the user interface
        context.add_widget(self._widget)
        
        self.counter = 0
        
        self.tracker = -1
        
        self.c.setText('Just received: ')
        
        self.t.setText('Now showing: ')
        
        self.classify.setText('Classification: ')
        
        self.geo_loc.setText('Location: ')
        
        rospy.Subscriber("image_test", UAVForge, self.callback)
        
        self.pub = rospy.Publisher('correct', UAVForge_bool, queue_size=10)
        

	
    def callback(self, data):
    
        rospy.loginfo("I got image "+str(self.counter) + ' ' + str(data.file_name))
        
        bridge = CvBridge()
        
        cv_image = bridge.imgmsg_to_cv2(data.image, desired_encoding='rgb8')
        
        cv.imwrite(self.path+str(self.counter)+'.jpg', cv_image)
        
        self.c.setText('Just received: ' + str(data.file_name) + "    " +str(self.counter))
        
        self.queue.append(data)
        
        self.counter = self.counter + 1
	
        	
    def buttonY(self):
    	
    	if self.tracker > -1:
    	
    	    self.new_Message(True)
    	
    	self.tracker = self.tracker + 1
    	
    	self.gui_display()
    	

    def buttonN(self):
    
        if self.tracker > -1:
        
            self.new_Message(False)	
        
        self.tracker = self.tracker + 1
        
        self.gui_display()
        
    	
    def gui_display(self):
    
        self.pixmap = QPixmap(self.path+str(self.tracker)+'.jpg')
        
        self.pixmap =  self.pixmap.scaled(self.image.size())
    	
        self.image.setPixmap(self.pixmap)
    	
        if os.path.exists(self.path+str(self.tracker)+'.jpg'):
    	
            os.remove(self.path+str(self.tracker)+'.jpg')
    	    
        else:
    	
            print(str(self.tracker)+'.jpg is missing')
    	
        rospy.loginfo("Looking at image "+str(self.tracker))
    	
        self.t.setText('Now showing: ' + self.queue[self.tracker].image_ID + "    " +str(self.tracker))
    	
        self.classify.setText('Classification: ' +self.queue[self.tracker].shape + ', ' + self.queue[self.tracker].shape_color + ', ' + self.queue[self.tracker].alphanum + ', ' + self.queue[self.tracker].alphanum_color + ', ' + self.queue[self.tracker].alphanum_ori)
    	
        self.geo_loc.setText('Location: ' + str(self.queue[self.tracker].geo_loc))
    
    
    def new_Message(self, correct):
    
        msg = UAVForge_bool()
        
        msg.image_ID = self.queue[self.tracker].image_ID
        
        msg.num = self.queue[self.tracker].num
	
        msg.correct = correct
	
        self.pub.publish(msg)
    

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog
        

                
    
    
    
