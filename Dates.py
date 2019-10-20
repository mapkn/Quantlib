# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 11:11:59 2018

@author: patemi
"""

import QuantLib.QuantLib as ql


y=ql.Date(10,1,2018)

#QL.ZeroIn

print(y)

print(y.month())
print(y.year())
#print(y.weekday())


z = y+1
print(z)

x = y-1
print(x)

y_=ql.Period(2,ql.Months)
print(y_)



#The Schedule object can be used to construct a list of dates such as coupon payments.


date1=ql.Date(1,1,2015)
date2=ql.Date(1,1,2016)

tenor=ql.Period(ql.Monthly)
calendar=ql.UnitedStates()
schedule=ql.Schedule(date1,date2,tenor,calendar,ql.Following,ql.Following, ql.DateGeneration.Forward, False)

print(list(schedule))

#print(calendar.FederalReserve)