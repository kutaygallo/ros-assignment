#!/usr/bin/env python
import rospy
import string

from std_msgs.msg import String

class Processor:
	def __init__(self):
		self.result = '' #result variable to keep string data
		rospy.init_node('listener')
		
		self.pub_16 = rospy.Publisher('/position/drive', String, queue_size = 10) #publisher to /position/drive
		self.pub_24 = rospy.Publisher('/position/robotic_arm', String, queue_size = 10) #publsiher to /position/robotic_arm
		
		rospy.Subscriber('/serial/drive', String, self.callback_16) #subscriber to /serial/drive
		rospy.Subscriber('/serial/robotic_arm', String, self.callback_24) #subscriber to /serial/robotic_arm

		self.publish_data() #class method to publish result at the end

	def callback_16(self, data):
		if data.data[0] == 'A' and data.data[-1] == 'B': #format checker (A...B)
			ab_removed = data.data[1:-1] #first & last character removal
			slices = [ab_removed[i: i + 4] for i in range(0, 16, 4)] #slice string into 4 then assign into a list.
			for i in range(4):
				if int(slices[i][1:]) > 255: #range checker (<255)
					slices[i] = slices[i].replace(slices[i][1:],"255",1) #replace outlier with 255
				if slices[i][0] == '1': #sign checker (1:negative, 0:positive)
					slices[i] = slices[i].replace(slices[i][0],"-",1) #replace 1 with "-"
				else:
					slices[i] = slices[i].replace(slices[i][0],"+",1) #replace 0 with "+"
			self.result = " ".join(slices) #merge slices with space between each slice then assign to the self.result
		else:
			self.result = 'data in false format' #error identifier for the format
		rospy.loginfo(self.result)

	def callback_24(self, data):		
		if data.data[0] == 'A' and data.data[-1] == 'B': #format checker (A...B)
			ab_removed = data.data[1:-1] #first & last character removal
			slices = [ab_removed[i: i + 4] for i in range(0, 24, 4)] #slice string into 6 then assign into a list.
			for i in range(6):
				if int(slices[i][1:]) > 255: #range checker (<255)
					slices[i] = slices[i].replace(slices[i][1:],"255",1) #replace outlier with 255
				if slices[i][0] == '1': #sign checker (1:negative, 0:positive)
					slices[i] = slices[i].replace(slices[i][0],"-",1) #replace 1 with "-"
				else:
					slices[i] = slices[i].replace(slices[i][0],"+",1) #replace 0 with "+"
			self.result = " ".join(slices) #merge slices with space between each slice then assign to the self.result
		else:
			self.result = 'data in false format' #error identifier for the format
		rospy.loginfo(self.result)

	def publish_data(self):
		rate = rospy.Rate(1) #1 hz
		while not rospy.is_shutdown():
			if len(self.result) == 16: #length checker to call the specific publisher
				self.pub_16.publish(self.result)
			else:
				self.pub_24.publish(self.result)
			rate.sleep()
		rospy.spin()

if __name__ == '__main__':
	p = Processor()
