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

tango_counter=0;
vicon_counter=0;
calib_file='vicon_adf_calibration';
vicon_pose_topic='vicon/tango/mainBody';

mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
ideal_rotation=[-91,2,87];
rot_tolerance=5;
def vicon_callback(vicon_pose):
    
    global vicon_counter;
    global calib_file;
    global mydir
    

    
    vicon_adf_calibration_file=open(os.path.join(mydir,calib_file),'a')
              
    vicon_adf_calibration_file.write(str(vicon_pose.transform.translation.x)+ ','+str(vicon_pose.transform.translation.y)+ ','+str(vicon_pose.transform.translation.z)+ ','
       +str(vicon_pose.transform.rotation.x)+ ','+str(vicon_pose.transform.rotation.y)+ ','+str(vicon_pose.transform.rotation.z)+ ','+str(vicon_pose.transform.rotation.w)+ ','
       +str(vicon_counter)+'\n') 

    vicon_counter +=1;    
     
    #rospy.loginfo("Vicon trans: x:%f, y:%f, z:%f", vicon_pose.transform.translation.x,vicon_pose.transform.translation.y,vicon_pose.transform.translation.z);

    quaternion_current = (
    vicon_pose.transform.rotation.x,
    vicon_pose.transform.rotation.y,
    vicon_pose.transform.rotation.z,
    vicon_pose.transform.rotation.w);
    euler = tf.transformations.euler_from_quaternion(quaternion_current)
    roll_current = euler[0]
    pitch_current =euler[1]
    yaw_current = euler[2]

    #rospy.loginfo("Vicon Quat: x:%f,y: %f ,z:%f, w:%f",vicon_pose.transform.rotation.x,
    #  vicon_pose.transform.rotation.y,
    #  vicon_pose.transform.rotation.z,
    #  vicon_pose.transform.rotation.w)
    rospy.loginfo("Vicon: Roll:%f,pitch: %f ,yaw:%f",math.degrees(roll_current),math.degrees(pitch_current),math.degrees(yaw_current));
    
    if (isTranslationInBounds(vicon_pose.transform.translation) and isRotationInBounds(roll_current,pitch_current,yaw_current)):    
      rospy.loginfo("Device within tolerance to vicon origin... start ADF learning ");
     
    vicon_adf_calibration_file.close();


def isRotationInBounds(roll_current,pitch_current,yaw_current):
    global rot_tolerance;
    
    if ((abs(roll_current-ideal_rotation[0])<rot_tolerance) and (abs(pitch_current-ideal_rotation[1])<rot_tolerance) and (abs(yaw_current-ideal_rotation[2])<rot_tolerance)):
      return True;
    else:
     #  rospy.loginfo("Errors r:%f,p:%f,y:%f",abs(roll_current-ideal_rotation[0]),abs(pitch_current-ideal_rotation[1]),abs(yaw_current-ideal_rotation[2]));
       return False;   

def isTranslationInBounds(translation_current):
  
    x_tolerance = 0.05;
    y_tolerance = 0.05;
    z_tolerance = 0.4;	
    
    if (translation_current.x < x_tolerance and translation_current.y < y_tolerance and translation_current.z < z_tolerance):
        return True;

    else :
	#rospy.loginfo("translation error");
        return False;
        


def tango_callback(tango_pose_start_device):
    rospy.loginfo("tango callback");
    quaternion_tango = (
    tango_pose_start_device.orientation[0],
    tango_pose_start_device.orientation[1],
    tango_pose_start_device.orientation[2],
    tango_pose_start_device.orientation[3],);
    euler = tf.transformations.euler_from_quaternion(quaternion_tango)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]
    
    rospy.loginfo("Tango: Roll:%f,pitch: %f ,yaw:%f",roll,pitch,yaw);
    
    
def listener():

    global mydir;
    global filename;

  
    try:
        os.makedirs(mydir)
    except OSError, e:
        if e.errno != 17:
            raise 
     
    if len(sys.argv) == 1:
      print "No filename chosen... Using default"
    else:
      filename = sys.argv[1]
      
    
    rospy.init_node('calibration', anonymous=True)

    rospy.Subscriber('/tango_pose_start_device', TangoPoseDataMsg, tango_callback)
    rospy.Subscriber(vicon_pose_topic, TransformStamped, vicon_callback)
    
    rospy.loginfo("reading vicon pose..");

    rospy.spin()

if __name__ == '__main__':
    listener()

