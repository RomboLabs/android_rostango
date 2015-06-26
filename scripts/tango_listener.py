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
    f=open('tango_pose','a')
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
     
   # grab_vicon_pose = rospy.ServiceProxy('grab_vicon_pose', PoseStamped);
    #try:
    #   avg_vicon_pose = grab_vicon_pose(n)
    #except rospy.ServiceException as exc:
    #    print("Service did not process request: " + str(exc))
  
    f.write('pose_time = '+str(tango_pose.timestamp)+ ','+ str(tango_pose.translation)+ ','+str(tango_pose.orientation)+'\n') 
    #f.write('vicon_time = '+str(avg_vicon_pose.timestamp)+'\n')   
    
     
    f.close();
    
def sync_callback(tango_pose_adf_device, tango_pose_start_device, tango_pose__adf_start, vicon_pose):
    
     f=open('tango_pose','a')

     f.close();
     
    
def listener():

    rospy.init_node('listener', anonymous=True)

   # rospy.Subscriber("tango_pose", TangoPoseDataMsg, callback)
   # rospy.loginfo("listening");

    tango_sub_1= message_filters.Subscriber('tango_pose_adf_device', TangoPoseDataMsg) #adf to device
    tango_sub_2= message_filters.Subscriber('tango_pose_start_device', TangoPoseDataMsg) #Start of service to device
    tango_sub_3= message_filters.Subscriber('tango_pose__adf_start', TangoPoseDataMsg)  #Area description to start of service

    vicon_sub= message_filters.Subscriber('vicon/<subject_name>/<segment_name>',TransformStamped )  # Vicon pose est 
    
    ts = message_filters.TimeSynchronizer([tango_sub_1, tango_sub_2,tango_sub_3,vicon_sub], 10)
    
    ts.registerCallback(sync_callback)
    
    
    rospy.spin()

if __name__ == '__main__':
    listener()