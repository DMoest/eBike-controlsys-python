#!/usr/bin/python

import threading
import time

exitFlag = 0

class CustomerThread (threading.Thread):
   def __init__(self, customer):
      threading.Thread.__init__(self)
      self.customer = customer

   def run(self):
      print("Starting " + str(self.customer._id))
      self.customer.run()
      print ("Exiting " + str(self.customer._id))