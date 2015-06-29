#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Wed Jun 24 21:48:52 2015
#
#@author: vijeth
#"""


import rospy
import message_filters


from geometry_msgs.msg import TransformStamped
from tango_msgs.msg import TangoPoseDataMsg

def callback(tango_pose):
    rospy.loginfo("callback");
    rospy.loginfo(tango_pose.header.stamp);


    print('pose_time = '+str(tango_pose.timestamp)+ ','+ str(tango_pose.translation)+ ','+str(tango_pose.orientation)+'\n') 

def vicon_callback(vicon_pose):
    rospy.loginfo("vicon_callback");
    rospy.loginfo(vicon_pose.header.stamp);


   # print('pose_time = '+str(tango_pose.timestamp)+ ','+ str(tango_pose.translation)+ ','+str(tango_pose.orientation)+'\n') 

    
def sync_callback( tango_pose_start_device,  vicon_pose):
     rospy.loginfo("synced");

     print("tango: " +str(tango_pose_start_device.header.stamp)  )
     print("vicon: " + str(vicon_pose.header.stamp))
     f=open('tango_vicon_pose','a')

     f.write('pose_time = '+str(tango_pose_start_device.header.stamp)+ ','+ str(tango_pose_start_device.translation)+ ','+str(tango_pose_start_device.orientation)+'\n') 	 
     f.write('vicon_time = '+str(vicon_pose.header.stamp)+ ','+ str(vicon_pose.transform.translation)+ ','+str(vicon_pose.transform.rotation)+'\n')      
	
     f.close();
     
    
def listener():

    rospy.init_node('listener', anonymous=True)

    #rospy.Subscriber('/tango_pose_start_device', TangoPoseDataMsg, callback)
    #rospy.Subscriber('/vicon/tangoJune29/mainBody', TransformStamped, vicon_callback)
    rospy.loginfo("listening");

    tango_sub= message_filters.Subscriber('/tango_pose_start_device', TangoPoseDataMsg) #Start of service to device

    vicon_sub= message_filters.Subscriber('/vicon/tangoJune29/mainBody',TransformStamped )  # Vicon pose est 
    
    ts = message_filters.ApproximateTimeSynchronizer([tango_sub,vicon_sub], 10,5)
    
    ts.registerCallback(sync_callback)
    
    
    rospy.spin()

if __name__ == '__main__':
    listener()
