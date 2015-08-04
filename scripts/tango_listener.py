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

mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
tango_counter=0;
vicon_counter=0;
tango_ss_counter=0;
vicon_ss_counter=0

vicon_pose_topic='vicon/TangoJuly24/mainBody'

def callback(tango_pose_start_device):
    rospy.loginfo("tango callback");
    #global tango_counter;
    #tango_ss_file=open('tango_pose_start_device','a')

    #tango_ss_file.write(str(tango_pose_start_device.status_code)+','+ str(tango_pose_start_device.header.stamp.secs)+ ','+str(tango_pose_start_device.header.stamp.nsecs)+ ','
    #    + str(tango_pose_start_device.translation[0])+ ','+ str(tango_pose_start_device.translation[1])+ ','+ str(tango_pose_start_device.translation[2])+ ','
    #    +str(tango_pose_start_device.orientation[0])+','+str(tango_pose_start_device.orientation[1])+','+str(tango_pose_start_device.orientation[2])+','+str(tango_pose_start_device.orientation[3])++str(tango_counter)+'\n') 
    #print('pose_time = '+str(tango_pose_start_device.timestamp)+ ','+ str(tango_pose_start_device.translation)+ ','+str(tango_pose_start_device.orientation)+'\n') 
    
    tango_ss_file.close();


def vicon_callback(vicon_pose):
    rospy.loginfo("vicon_callback");
    rospy.loginfo(vicon_pose.header.stamp);


   # print('pose_time = '+str(tango_pose.timestamp)+ ','+ str(tango_pose.translation)+ ','+str(tango_pose.orientation)+'\n') 

    
def sync_callback( tango_pose_start_device,  tango_pose_adf_device,tango_pose_adf_start,vicon_pose):
     rospy.loginfo("synced");
     global tango_counter;
     global vicon_counter;
      

            
            
     tango__ss_file=open(os.path.join(mydir,'tango_pose_ss'),'w')    
     tango__adf_file=open(os.path.join(mydir,'tango_pose_adf'),'w')
     vicon_file =open(os.path.join(mydir,'vicon_pose'),'a')

     
     tango__ss_file.write(str(tango_pose_start_device.status_code)+','+ str(tango_pose_start_device.header.stamp.secs)+ ','+str(tango_pose_start_device.header.stamp.nsecs)+ ','
        +str(tango_pose_start_device.translation[0])+ ','+ str(tango_pose_start_device.translation[1])+ ','+ str(tango_pose_start_device.translation[2])+ ','
        +str(tango_pose_start_device.orientation[0])+','+str(tango_pose_start_device.orientation[1])+','+str(tango_pose_start_device.orientation[2])+','+str(tango_pose_start_device.orientation[3])+','
        +str(tango_counter)+'\n') 

     tango__adf_file.write(str(tango_pose_adf_device.status_code)+','+ str(tango_pose_adf_device.header.stamp.secs)+ ','+str(tango_pose_adf_device.header.stamp.nsecs)+ ','
        +str(tango_pose_adf_device.translation[0])+ ','+ str(tango_pose_adf_device.translation[1])+ ','+ str(tango_pose_adf_device.translation[2])+ ','
        +str(tango_pose_adf_device.orientation[0])+','+str(tango_pose_adf_device.orientation[1])+','+str(tango_pose_adf_device.orientation[2])+','+str(tango_pose_start_device.orientation[3])+','
        +str(tango_counter)+'\n') 

     tango__adf__ss_file.write(str(tango_pose_adf_start.status_code)+','+ str(tango_pose_adf_start.header.stamp.secs)+ ','+str(tango_pose_adf_start.header.stamp.nsecs)+ ','
        +str(tango_pose_adf_start.translation[0])+ ','+ str(tango_pose_adf_start.translation[1])+ ','+ str(tango_pose_adf_start.translation[2])+ ','
        +str(tango_pose_adf_start.orientation[0])+','+str(tango_pose_adf_start.orientation[1])+','+str(tango_pose_adf_start.orientation[2])+','+str(tango_pose_start_device.orientation[3])+','
        +str(tango_counter)+'\n')  

     #vicon_file.write(str(vicon_pose.header.stamp.secs)+ ','+ str(vicon_pose.header.stamp.nsecs)+ ','
     #   +str(vicon_pose.transform.translation.x)+ ','+str(vicon_pose.transform.translation.y)+ ','+str(vicon_pose.transform.translation.z)+ ','
     #   +str(vicon_pose.transform.rotation.x)+ ','+str(vicon_pose.transform.rotation.y)+ ','+str(vicon_pose.transform.rotation.z)+ ','+str(vicon_pose.transform.rotation.w)+ ','
     #   +str(vicon_counter)+'\n')  

     tango_counter +=1;
     vicon_counter +=1;    
	
     vicon_file.close();
     tango__ss_file.close();
     tango__adf_file.close();
     tango__adf__ss_file.close();

def sync_adf_only_callback(tango_pose_adf_device,vicon_pose):
     rospy.loginfo("synced");
     global tango_counter;
     global vicon_counter;
     global mydir;
    
             
     tango_adf_file=open(os.path.join(mydir,'tango_pose_adf'),'a')
     vicon_adf_file =open(os.path.join(mydir,'vicon_pose_adf'),'a')

     tango_adf_file.write(str(tango_pose_adf_device.status_code.status)+','+ str(tango_pose_adf_device.header.stamp.secs)+ ','+str(tango_pose_adf_device.header.stamp.nsecs)+ ','
        +str(tango_pose_adf_device.translation[0])+ ','+ str(tango_pose_adf_device.translation[1])+ ','+ str(tango_pose_adf_device.translation[2])+ ','
        +str(tango_pose_adf_device.orientation[0])+','+str(tango_pose_adf_device.orientation[1])+','+str(tango_pose_adf_device.orientation[2])+','+str(tango_pose_adf_device.orientation[3])+','
        +str(tango_counter)+'\n') 


     vicon_adf_file.write(str(vicon_pose.header.stamp.secs)+ ','+ str(vicon_pose.header.stamp.nsecs)+ ','
       +str(vicon_pose.transform.translation.x)+ ','+str(vicon_pose.transform.translation.y)+ ','+str(vicon_pose.transform.translation.z)+ ','
        +str(vicon_pose.transform.rotation.x)+ ','+str(vicon_pose.transform.rotation.y)+ ','+str(vicon_pose.transform.rotation.z)+ ','+str(vicon_pose.transform.rotation.w)+ ','
        +str(vicon_counter)+'\n')  

     tango_counter +=1;
     vicon_counter +=1;    
    
     vicon_adf_file.close();   
     tango_adf_file.close();
     
def sync_ss_only_callback(tango_pose_adf_device,vicon_pose):
     rospy.loginfo("synced");
     global tango_ss_counter;
     global vicon_ss_counter;
     global mydir;
    
             
     tango_ss_file=open(os.path.join(mydir,'tango_pose__ss'),'a')
     vicon_ss_file =open(os.path.join(mydir,'vicon_pose'),'a')

     tango_ss_file.write(str(tango_pose_adf_device.status_code.status)+','+ str(tango_pose_adf_device.header.stamp.secs)+ ','+str(tango_pose_adf_device.header.stamp.nsecs)+ ','
        +str(tango_pose_adf_device.translation[0])+ ','+ str(tango_pose_adf_device.translation[1])+ ','+ str(tango_pose_adf_device.translation[2])+ ','
        +str(tango_pose_adf_device.orientation[0])+','+str(tango_pose_adf_device.orientation[1])+','+str(tango_pose_adf_device.orientation[2])+','+str(tango_pose_adf_device.orientation[3])+','
        +str(tango_ss_counter)+'\n') 


     vicon_ss_file.write(str(vicon_pose.header.stamp.secs)+ ','+ str(vicon_pose.header.stamp.nsecs)+ ','
       +str(vicon_pose.transform.translation.x)+ ','+str(vicon_pose.transform.translation.y)+ ','+str(vicon_pose.transform.translation.z)+ ','
        +str(vicon_pose.transform.rotation.x)+ ','+str(vicon_pose.transform.rotation.y)+ ','+str(vicon_pose.transform.rotation.z)+ ','+str(vicon_pose.transform.rotation.w)+ ','
        +str(vicon_ss_counter)+'\n')  

     tango_ss_counter +=1;
     vicon_ss_counter +=1;    
    
     vicon_ss_file.close();     
     tango_ss_file.close();
    
def listener():
    global mydir;
   
    try:
        os.makedirs(mydir)
    except OSError, e:
        if e.errno != 17:
            raise 

    rospy.init_node('listener', anonymous=True)

    #rospy subscribers
    #rospy.Subscriber('/tango_pose_start_device', TangoPoseDataMsg, callback)
    #rospy.Subscriber('vicon/TangoJuly24/mainBody', TransformStamped, vicon_callback)
    
    

     # message filter subsribers 
    #tango_sub_ss= message_filters.Subscriber('/tango_pose_start_device', TangoPoseDataMsg) #Start of service to device
    tango_sub_adf= message_filters.Subscriber('/tango_pose_adf_device', TangoPoseDataMsg) #ADF to device
    #tango_sub_adf_ss= message_filters.Subscriber('/tango_pose_adf_start', TangoPoseDataMsg) #ADF to Start of service 
    vicon_sub= message_filters.Subscriber('vicon/TangoJuly24/mainBody',TransformStamped )  # Vicon pose est 

    #message filter sync params
    ts_adf = message_filters.ApproximateTimeSynchronizer([tango_sub_adf,vicon_sub], 10,40)
    #ts_ss = message_filters.ApproximateTimeSynchronizer([tango_sub_ss,vicon_sub], 10,40)

    #message filter callbacks 
    ts_adf.registerCallback(sync_adf_only_callback)
   # ts_ss.registerCallback(sync_ss_only_callback)
    
    
    rospy.loginfo("listening");
    rospy.spin()
    
    
if __name__ == '__main__':
    listener()
