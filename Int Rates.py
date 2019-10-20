# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 21:27:11 2018

@author: patemi
"""

#http://gouthamanbalaraman.com/blog/quantlib-basics.html


import QuantLib.QuantLib as ql

annualRate=0.05
dayCount=ql.ActualActual()
compoundType = ql.Compounded
frequency = ql.Annual

interestRate = ql.InterestRate(annualRate, dayCount, compoundType, frequency)

#the compoundFactor method gives you how much your investment will be worth after t years
print(interestRate.compoundFactor(2))

print((1.0 + annualRate)*(1.0 + annualRate))  # Check the above calculation

#The discountFactor method returns the reciprocal of the compoundFactor method.

print(interestRate.discountFactor(2.0))

print(1.0 / interestRate.compoundFactor(2.0))

