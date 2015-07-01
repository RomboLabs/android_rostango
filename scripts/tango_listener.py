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
tango_counter=0;
vicon_counter=0;

def callback(tango_pose_start_device):
    #rospy.loginfo("callback");
    
    tango_file=open('tango_pose','a')

    tango_file.write(str(tango_pose_start_device.status_code)+','+ str(tango_pose_start_device.header.stamp.secs)+ ','+str(tango_pose_start_device.header.stamp.nsecs)+ ','
        + str(tango_pose_start_device.translation[0])+ ','+ str(tango_pose_start_device.translation[1])+ ','+ str(tango_pose_start_device.translation[2])+ ','
        +str(tango_pose_start_device.orientation[0])+','+str(tango_pose_start_device.orientation[1])+','+str(tango_pose_start_device.orientation[2])+','+str(tango_pose_start_device.orientation[3])+'\n') 
    print('pose_time = '+str(tango_pose_start_device.timestamp)+ ','+ str(tango_pose_start_device.translation)+ ','+str(tango_pose_start_device.orientation)+'\n') 
    
    tango_file.close();


def vicon_callback(vicon_pose):
    rospy.loginfo("vicon_callback");
    rospy.loginfo(vicon_pose.header.stamp);


   # print('pose_time = '+str(tango_pose.timestamp)+ ','+ str(tango_pose.translation)+ ','+str(tango_pose.orientation)+'\n') 

    
def sync_callback( tango_pose_start_device,  vicon_pose):
     rospy.loginfo("synced");
     global tango_counter;
     global vicon_counter;
     tango_file=open('tango_pose','a')
     vicon_file =open('vicon_pose','a')

     
     tango_file.write(str(tango_pose_start_device.status_code)+','+ str(tango_pose_start_device.header.stamp.secs)+ ','+str(tango_pose_start_device.header.stamp.nsecs)+ ','
        +str(tango_pose_start_device.translation[0])+ ','+ str(tango_pose_start_device.translation[1])+ ','+ str(tango_pose_start_device.translation[2])+ ','
        +str(tango_pose_start_device.orientation[0])+','+str(tango_pose_start_device.orientation[1])+','+str(tango_pose_start_device.orientation[2])+','+str(tango_pose_start_device.orientation[3])+','
        +str(tango_counter)+'\n') 

     vicon_file.write(str(vicon_pose.header.stamp.secs)+ ','+ str(vicon_pose.header.stamp.nsecs)+ ','
        +str(vicon_pose.transform.translation.x)+ ','+str(vicon_pose.transform.translation.y)+ ','+str(vicon_pose.transform.translation.z)+ ','
        +str(vicon_pose.transform.rotation.x)+ ','+str(vicon_pose.transform.rotation.y)+ ','+str(vicon_pose.transform.rotation.z)+ ','+str(vicon_pose.transform.rotation.w)+ ','
        +str(vicon_counter)+'\n')  

     tango_counter +=1;
     vicon_counter +=1;    
	
     vicon_file.close();
     tango_file.close();
     
    
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
