#!/usr/bin/python

import threading

exitFlag = 0

class CustomerThread (threading.Thread):
   def __init__(self, customer):
      threading.Thread.__init__(self)
      self.customer = customer

   def run(self):
      self.customer.run()