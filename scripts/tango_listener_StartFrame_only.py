#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Wed 15 th Nov 2016
#
#@author: vijeth
#"""


import rospy
import message_filters
import os, datetime, sys

from geometry_msgs.msg import TransformStamped
from tango_msgs.msg import TangoPoseDataMsg

mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
subjectName=[]
tango_counter=0;

mustAnnotate = True;


def sync_start_callback(tango_pose_start_device):
     
         global tango_counter;
         global mydir;
    
     
         tango_start_file=open(os.path.join(mydir,'tango_pose_start'),'a')        
        

         tango_start_file.write(str(tango_pose_start_device.status_code.status)+','+ str(tango_pose_start_device.header.stamp.secs)+ ','+str(tango_pose_start_device.header.stamp.nsecs)+ ','
            +str(tango_pose_start_device.translation[0])+ ','+ str(tango_pose_start_device.translation[1])+ ','+ str(tango_pose_start_device.translation[2])+ ','
            +str(tango_pose_start_device.orientation[0])+','+str(tango_pose_start_device.orientation[1])+','+str(tango_pose_start_device.orientation[2])+','+str(tango_pose_start_device.orientation[3])+','
            +str(tango_counter)+'\n') 

        

         tango_counter +=1;
     
         tango_start_file.close();

         if int(tango_pose_start_device.status_code.status) == 1:
           print ' Relocalized...synced and saving start -- Subject Name',subjectName;
         else :
           rospy.loginfo("error status...");   
           

def listener():
    global mydir;
    global subjectName;

    print "Start of Service Only"

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

   
    rospy.Subscriber('/tango_pose_start_device', TangoPoseDataMsg, sync_start_callback)

    rospy.loginfo("listening to Start of Service only")
    rospy.spin()
    
    
if __name__ == '__main__':
    listener()
