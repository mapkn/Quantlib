# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 21:27:11 2018

@author: patemi
"""

#http://gouthamanbalaraman.com/blog/quantlib-basics.html


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

# Deposit rates
depo_maturities = [ql.Period(6,ql.Months), ql.Period(12, ql.Months)]
depo_rates = [5.25, 5.5]

# Bond rates
bond_maturities = [ql.Period(6*i, ql.Months) for i in range(3,21)]
bond_rates = [5.75, 6.0, 6.25, 6.5, 6.75, 6.80, 7.00, 7.1, 7.15,
              7.2, 7.3, 7.35, 7.4, 7.5, 7.6, 7.6, 7.7, 7.8]

print_curve(depo_maturities+bond_maturities, depo_rates+bond_rates)


# some constants and conventions
# here we just assume for the sake of example
# that some of the constants are the same for
# depo rates and bond rates

calc_date = ql.Date(15, 1, 2015)
ql.Settings.instance().evaluationDate = calc_date

calendar = ql.UnitedStates()
bussiness_convention = ql.Unadjusted
day_count = ql.Thirty360()
end_of_month = True
settlement_days = 0
face_amount = 100
coupon_frequency = ql.Period(ql.Semiannual)
settlement_days = 0



# create deposit rate helpers from depo_rates
depo_helpers = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(r/100.0)),
                                     m,
                                     settlement_days,
                                     calendar,
                                     bussiness_convention,
                                     end_of_month,
                                     day_count )
                for r, m in zip(depo_rates, depo_maturities)]



# create fixed rate bond helpers from fixed rate bonds
bond_helpers = []
for r, m in zip(bond_rates, bond_maturities):
    termination_date = calc_date + m
    schedule = ql.Schedule(calc_date,
                   termination_date,
                   coupon_frequency,
                   calendar,
                   bussiness_convention,
                   bussiness_convention,
                   ql.DateGeneration.Backward,
                   end_of_month)

    helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(face_amount)),
                                        settlement_days,
                                        face_amount,
                                        schedule,
                                        [r/100.0],
                                        day_count,
                                        bussiness_convention,
                                        )
    bond_helpers.append(helper)


##The yield curve is constructed by putting the two helpers together.

rate_helpers = depo_helpers + bond_helpers
yieldcurve = ql.PiecewiseLogCubicDiscount(calc_date,
                             rate_helpers,
                             day_count)



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
    spots.append(100*eq_rate)


print_curve(tenors, spots)