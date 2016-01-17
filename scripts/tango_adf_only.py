#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Wed Jun 24 21:48:52 2015
#
#@author: vijeth
#"""


import rospy
import message_filters
import os, datetime, sys

from geometry_msgs.msg import TransformStamped
from tango_msgs.msg import TangoPoseDataMsg

mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
tango_counter=0;
mustAnnotate = True;
subjectName=[]
   
def adf_callback(tango_pose_adf_device):
    
     global tango_counter;
     global vicon_counter;
      
   
     if int(tango_pose_adf_device.status_code.status) == 1:
         rospy.loginfo("synced");
         tango__adf_file=open(os.path.join(mydir,'tango_pose_adf'),'a')

         tango__adf_file.write(str(tango_pose_adf_device.status_code.status)+','+ str(tango_pose_adf_device.header.stamp.secs)+ ','+str(tango_pose_adf_device.header.stamp.nsecs)+ ','
            +str(tango_pose_adf_device.translation[0])+ ','+ str(tango_pose_adf_device.translation[1])+ ','+ str(tango_pose_adf_device.translation[2])+ ','
            +str(tango_pose_adf_device.orientation[0])+','+str(tango_pose_adf_device.orientation[1])+','+str(tango_pose_adf_device.orientation[2])+','+str(tango_pose_adf_device.orientation[3])+','
            +str(tango_counter)+'\n') 

         tango_counter +=1;
         tango__adf_file.close();

     else  :
        rospy.loginfo("error status");   

    
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

    rospy.init_node('listener', anonymous=True)

    #rospy subscribers
    rospy.Subscriber('/tango_pose_adf_device', TangoPoseDataMsg, adf_callback)


    
    
    rospy.loginfo("listening");
    rospy.spin()
    
    
if __name__ == '__main__':
    listener()
