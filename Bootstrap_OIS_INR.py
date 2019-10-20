# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 21:27:11 2018

@author: patemi
"""


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

calc_date = ql.Date(17, 5, 2017)
ql.Settings.instance().evaluationDate = calc_date





#swap_tenors = [ql.Period(x, ql.Years) for x in [2,3,4]]
swap_tenors = [ql.Period(x, ql.Years) for x in [2,3,4,5,6,7,8,9,10,12,15,20,25,30]]
swap_rates=[-0.0023800,-0.00145,-0.0003800,0.0007600,0.0020000,0.0032700,0.0045400,0.0057700,0.0069300,0.0079800,0.0089200,0.0110700,
             0.0129400,0.0136800,0.0140400,0.0142000,0.0138200]
swap_dcc=[ql.Thirty360() for code in swap_tenors]

 
calendar = ql.TARGET()
bussiness_convention = ql.Unadjusted
day_count = ql.Thirty360()
end_of_month = False
settlement_days = 0
#face_amount = 100
coupon_frequency = ql.Period(ql.Semiannual)
settlement_days = 0



# Deposit rates
depo_tenors = [ql.Period(3,ql.Months)]
depo_rates = [-0.331]

# create deposit rate helpers from depo_rates
depo_helpers = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(r/100.0)),
                                     m,
                                     settlement_days,
                                     calendar,
                                     bussiness_convention,
                                     end_of_month,
                                     day_count )
                for r, m in zip(depo_rates, depo_tenors)]




swFixedLegFrequency = ql.Annual
swFixedLegConvention = ql.ModifiedFollowing
swFixedLegDayCounter = ql.Thirty360()
swFloatingLegIndex = ql.Euribor3M()
forwardStart = ql.Period(0, ql.Days)

# Swap rate helpers
swap_helpers=[ql.SwapRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate)),
        tenor,
        calendar,
        swFixedLegFrequency,
        swFixedLegConvention,
        swFixedLegDayCounter,
        swFloatingLegIndex,
        ql.QuoteHandle(ql.SimpleQuote(0)),
        forwardStart) 
    for rate, tenor in zip(swap_rates, swap_tenors)]






##The yield curve is constructed by putting the two helpers together.

rate_helpers = depo_helpers + futures_helpers + swap_helpers
yieldcurve = ql.PiecewiseLogCubicDiscount(calc_date,
                             rate_helpers,
                             day_count)


print(day_count.name())


# get spot rates
spots = []
tenors = []
for d in yieldcurve.dates():
    yrs = day_count.yearFraction(calc_date, d)
    
    compounding = ql.Compounded
    freq = ql.Semiannual
    zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
    tenors.append(yrs)
    eq_rate = zero_rate.equivalentRate(day_count,
                                       compounding,
                                       freq,
                                       calc_date,
                                       d).rate()
    #z_rate= zero_rate.
    
    spots.append(100*eq_rate)



print_curve(tenors, spots)