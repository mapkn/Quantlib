# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:47:18 2019

@author: patemi
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 21:27:11 2018

@author: patemi
"""

#http://gouthamanbalaraman.com/blog/quantlib-basics.html
#http://khandrikacm.blogspot.com/2014/03/usd-yield-curve-building-using-python.html
#http://mikejuniperhill.blogspot.com/2018/11/quantlib-python-builder-for-piecewise.html


# Let's consider a hypothetical bond with a par value of 100, that pays 6% coupon semi-annually issued on January 15th, 2015 and set to mature on January 15th, 2016. 
# The bond will pay a coupon on July 15th, 2015 and January 15th, 2016. The par amount of 100 will also be paid on the January 15th, 2016.

# To make things simpler, lets assume that we know the spot rates of the treasury as of January 15th, 2015. The annualized spot rates are 0.5% for 6 months and 
# 0.7% for 1 year point. Lets calculate the fair value of this bond.


import QuantLib.QuantLib as ql


def print_curve(xlist, ylist, precision=3):
    """
    Method to print curve in a nice format
    """
    print ("----------------------")
    print ("Maturities\tCurve")
    print ("----------------------")
    for x,y in zip(xlist, ylist):
        print (x,"\t\t", round(y, precision))
    print ("----------------------")

calc_date = ql.Date(15, 1, 2015)

ql.Settings.instance().evaluationDate = calc_date

# Deposit rates
depo_maturities = [ql.Period(3,ql.Months)]
depo_rates = [-0.331]


# Futures
future_dates=['M7','U7','Z7','H8','M8','U8','Z8','H9']
future_prices=[100.335,100.325,100.3,100.265,100.22,100.17,100.12,100.07]



swap_tenors=['2Y','3Y']
swap_maturities=[ql.Period(2,ql.Years),ql.Period(3,ql.Years)]
swap_rates=[-0.00145,-0.00145]

# Bond rates
#bond_maturities = [ql.Period(6*i, ql.Months) for i in range(3,21)]
#bond_rates = [5.75, 6.0, 6.25, 6.5, 6.75, 6.80, 7.00, 7.1, 7.15,
 #             7.2, 7.3, 7.35, 7.4, 7.5, 7.6, 7.6, 7.7, 7.8]

print_curve(depo_maturities+swap_tenors, depo_rates+swap_rates)


# some constants and conventions
# here we just assume for the sake of example
# that some of the constants are the same for
# depo rates and bond rates



calendar = ql.UnitedStates()
bussiness_convention = ql.Unadjusted
day_count = ql.Thirty360()
end_of_month = True
settlement_days = 0
face_amount = 100
coupon_frequency = ql.Period(ql.Semiannual)
settlement_days = 0



swapIndex=ql.USDLibor(ql.Period(3,ql.Months))

#future_helper1=ql.FuturesRateHelper(100.335,ql.IMM.nextDate(calc_date+ql.Period(3,ql.Months)), swapIndex)

future_helper1=ql.FuturesRateHelper(100.335,'Z7', swapIndex)

future_helper2=ql.FuturesRateHelper(99,ql.IMM.nextDate(calc_date+ql.Period(3,ql.Months)), swapIndex)

#future_helper3=ql.FuturesRateHelper(ql.QuoteHandle(99), months, calendar, bussiness_convention, end_of_month, day_count, ql.QuoteHandle(0))
 #               for p, t in zip(future_prices, future_dates)

#ql.IMM_date(

imm = ql.IMM.nextDate(calc_date)

print(ql.IMM.nextDate(imm+1))

r=ql.IMM.isIMMcode('Y9')
d=ql.IMM.isIMMdate(ql.Date(10,10,2020))

#ql.IMM_code()


v=ql.IMM.code(ql.Date(10,10,2020))



#futures_helpers = [ql.FuturesRateHelper(ql.QuoteHandle(p),
#                                     months,
#                                     calendar,
#                                     bussiness_convention,
#                                     end_of_month,
#                                     day_count,
#                                     ql.QuoteHandle(0))
#                for p, t in zip(future_prices, future_dates)]
#
#
#print(ql.IMM.nextCode)
#



#print_curve(tenors, spots)