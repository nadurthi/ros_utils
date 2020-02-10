#!/usr/bin/env python
# license removed for brevity
import rospy
from rosutils.msg import roverpwmcontrol
from geometry_msgs.msg import Twist
import argparse
from std_msgs.msg import String


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--control_lrdd", nargs='+', help="lrdd")
    parser.add_argument("--vx", help="control x velocity")
    parser.add_argument("--wz", help="control z ang-velocity")
    parser.add_argument("-r","--repeat", help="repeat command these many times")

    pubroverctr_lrdd = rospy.Publisher('/roverbot/lrdd', roverpwmcontrol, queue_size=10)
    pub = rospy.Publisher('chatter', String, queue_size=10)
    pubroverctr_keyvel = rospy.Publisher('/roverbot/key_vel', Twist, queue_size=10)

    rospy.init_node('customcommander', anonymous=True)
    
    rate = rospy.Rate(1) # 10hz
    rate.sleep()
    rate = rospy.Rate(10) # 10hz

    args = parser.parse_args()
    print(args)

    try:
        # talker()
        
        if args.control_lrdd:
            for i in range(int(args.repeat)):
                lrdd = roverpwmcontrol()
                lrdd.Lpwm = int(args.control_lrdd[0])
                lrdd.Rpwm = int(args.control_lrdd[1])
                lrdd.dirn = int(args.control_lrdd[2])
                lrdd.durn = int(args.control_lrdd[3])
                pubroverctr_lrdd.publish(lrdd)
                print "sent ",args.control_lrdd
                print lrdd
                rate.sleep()

        if args.vx: 
            for i in range(int(args.repeat)):    
                tw = Twist()
                tw.linear.x = int(args.vx)
                pubroverctr_keyvel.publish(tw)
                rate.sleep()


        if args.wz:
            for i in range(int(args.repeat)): 
                tw = Twist()
                tw.angular.z = int(args.wz)
                pubroverctr_keyvel.publish(tw)
                rate.sleep()

        

        # rate = rospy.Rate(10) # 10hz
        # while not rospy.is_shutdown():
        #     hello_str = "hello world %s" % rospy.get_time()
        #     rospy.loginfo(hello_str)
        #     pub.publish(hello_str)
        #     rate.sleep()

    except rospy.ROSInterruptException:
        pass