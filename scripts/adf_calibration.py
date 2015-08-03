#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Wed Jun 24 21:48:52 2015
#
#@author: vijeth
#"""


import rospy
import message_filters
import os, datetime

from geometry_msgs.msg import TransformStamped
from tango_msgs.msg import TangoPoseDataMsg
tango_counter=0;
vicon_counter=0;
calib_file='vicon_adf_calibration';
vicon_pose_topic='vicon/TangoJuly24/mainBody';

mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))

def vicon_callback(vicon_pose):
    
    global vicon_counter;
    global calib_file;
    global mydir
    
    x_tolerance = 0.1;
    y_tolerance = 0.1;
    z_tolerance = 0.4;	
    
    vicon_adf_calibration_file=open(os.path.join(mydir,calib_file),'a')
              
    vicon_adf_calibration_file.write(str(vicon_pose.header.stamp.secs)+ ','+ str(vicon_pose.header.stamp.nsecs)+ ','
       +str(vicon_pose.transform.translation.x)+ ','+str(vicon_pose.transform.translation.y)+ ','+str(vicon_pose.transform.translation.z)+ ','
       +str(vicon_pose.transform.rotation.x)+ ','+str(vicon_pose.transform.rotation.y)+ ','+str(vicon_pose.transform.rotation.z)+ ','+str(vicon_pose.transform.rotation.w)+ ','
       +str(vicon_counter)+'\n') 

    vicon_counter +=1;    
     
    
    if (vicon_pose.transform.translation.x < x_tolerance and vicon_pose.transform.translation.y < y_tolerance and vicon_pose.transform.translation.z < z_tolerance):
     rospy.loginfo("Device within tolerance to vicon origin... start ADF learning ");
     
    vicon_adf_calibration_file.close();


    
def listener():

    global mydir;
   
    try:
        os.makedirs(mydir)
    except OSError, e:
        if e.errno != 17:
            raise 

    rospy.init_node('calibration', anonymous=True)

    #rospy.Subscriber('/tango_pose_start_device', TangoPoseDataMsg, callback)
    rospy.Subscriber(vicon_pose_topic, TransformStamped, vicon_callback)
    
    rospy.loginfo("reading vicon pose...start adf recording");

    rospy.spin()

if __name__ == '__main__':
    listener()
