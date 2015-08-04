#!/usr/bin/env python
# license removed for brevity
import rospy

from tango_msgs.msg import TangoPoseDataMsg

def talker():
    pub = rospy.Publisher('tango_pose', TangoPoseDataMsg, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(30) # 10hz
    while not rospy.is_shutdown():
        t= rospy.get_time()
        pose =TangoPoseDataMsg()
        pose.timestamp=t;
        
        rospy.loginfo(str(t))
        
        
        pub.publish(pose)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

