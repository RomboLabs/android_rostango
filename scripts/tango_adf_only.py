#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Wed Jun 24 21:48:52 2015
#
#@author: vijeth
#"""


import rospy

import os, datetime
import sys
import math
import tf
filename= []

from geometry_msgs.msg import TransformStamped
from tf.transformations import euler_from_quaternion
from tango_msgs.msg import TangoPoseDataMsg

subjectName=[]
tango_counter=0;
vicon_counter=0;
mustAnnotate = True;

mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))


def tango_start_adf_callback(tango_pose_start_adf):
     rospy.loginfo("starts adf recording");
     global tango_counter;
    
     global mydir;

     tango_start_adf_file=open(os.path.join(mydir,'tango_pose_start_adf'),'a')

     tango_start_adf_file.write(str(tango_pose_start_adf.status_code.status)+','+ str(tango_pose_start_adf.header.stamp.secs)+ ','+str(tango_pose_start_adf.header.stamp.nsecs)+ ','
        +str(tango_pose_start_adf.translation[0])+ ','+ str(tango_pose_start_adf.translation[1])+ ','+ str(tango_pose_start_adf.translation[2])+ ','
        +str(tango_pose_start_adf.orientation[0])+','+str(tango_pose_start_adf.orientation[1])+','+str(tango_pose_start_adf.orientation[2])+','+str(tango_pose_start_adf.orientation[3])+','
        +str(tango_counter)+'\n') 
        
     tango_start_adf_file.close();  

    
    
def listener():

    global mydir;
    global subjectName;
    
    if len(sys.argv) == 1 and mustAnnotate == True:
     print "No Subject chosen... Enter subject below"
     subjectName = raw_input('Enter your Subject name: ')
    else:     
      subjectName = sys.argv[1]
      print 'Subject Name',subjectName;
      
    mydir=mydir+'-'+subjectName;


  
    try:
        os.makedirs(mydir)
    except OSError, e:
        if e.errno != 17:
            raise 
     
    if len(sys.argv) == 1:
      print "No filename chosen... Using default"
    else:
      filename = sys.argv[1]
      
    
    rospy.init_node('adf_only', anonymous=True)

    #rospy.Subscriber('/tango_pose_start_device', TangoPoseDataMsg, tango_callback)
    rospy.Subscriber('/tango_pose_adf_device', TangoPoseDataMsg, tango_start_adf_callback)	
    
    
    rospy.loginfo("reading adf pose..");

    rospy.spin()

if __name__ == '__main__':
    listener()
