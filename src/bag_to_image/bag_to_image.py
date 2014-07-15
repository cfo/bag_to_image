#!/usr/bin/python

import rosbag
import argparse
import cv
from cv_bridge import CvBridge, CvBridgeError

def extract(bagfile, pose_topic, out_filename):
    n = 0
    f = open(out_filename, 'w')
    f.write('# timestamp image_name')
    cv_bridge = CvBridge()
    with rosbag.Bag(bagfile, 'r') as bag:
        for (topic, msg, ts) in bag.read_messages(topics=str(pose_topic)):
            try:
                img = cv_bridge.imgmsg_to_cv(msg, "bgr8")
            except CvBridgeError, e:
                print e
            ts = msg.header.stamp.to_sec()
            image_name = 'image_'+str(n)+'.png'
            f.write('%.12f %s \n' % (ts, image_name))
            cv.SaveImage(image_name, img)
            n += 1
            
    print('wrote ' + str(n) + ' images messages to the file: ' + out_filename)
          
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Extracts Images messages from bagfile.
    ''')
    parser.add_argument('bag', help='Bagfile')
    parser.add_argument('topic', help='Topic')
    args = parser.parse_args()
    print('Extract images from bag '+args.bag+' in topic ' + args.topic)
    extract(args.bag, args.topic, 'images.txt')