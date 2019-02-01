# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 14:33:13 2019

@author: kenny
"""

# dashboard names 

class dashboard_names():
    
    def __inti__(self):
        self.milk = None
        self.bread = None
        
        
        
        
    def initialize_name(self):
        self.bread = 'bread'
        self.milk = 'milk'

    class quantity():
        def __init__(self):
            self.milk_qty = None
            self.bread_qty = None
                
        def initialize_number(self):
            self.bread_qty = 0
            self.milk_qty = 0