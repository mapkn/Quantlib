# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 10:35:58 2019

@author: patemi
"""

import QuantLib.QuantLib as ql
import pandas as pd


today=ql.Date(12,3, 2019)


calc_date = today
#calc_date = today()

ql.Settings.instance().evaluationDate = calc_date



# Use a flat yield curve
flat_rate = ql.SimpleQuote(0.0015)
rate_handle = ql.QuoteHandle(flat_rate)
day_count = ql.Actual360()
calendar = ql.UnitedStates()
ts_yield = ql.FlatForward(calc_date, rate_handle, day_count)
ts_handle = ql.YieldTermStructureHandle(ts_yield)

#flat_rate2=ql.


# Construct the bond itself


#### The Cashflow schedule ################

issue_date = today
maturity_date = ql.Date(28, 2, 2021)
tenor = ql.Period(ql.Semiannual)
#tenor = ql.Period(ql.Annual)
calendar = ql.UnitedStates()

# How to roll dates on non-business dates
bussiness_convention = ql.Following
bussiness_convention = ql.Following


# How to generate the dates, forwards, or backwards
date_generation = ql.DateGeneration.Backward
month_end = False


schedule = ql.Schedule (issue_date, maturity_date, 
                        tenor, calendar, 
                        bussiness_convention,
                        bussiness_convention, 
                        date_generation, 
                        month_end)

df=pd.DataFrame({'date': list(schedule)})

print(df)

settlement_days = 2
#day_count = ql.Thirty360()
day_count = ql.ActualActual()
coupon_rate = .025
coupons = [coupon_rate]


# Now lets construct the FixedRateBond
settlement_days = 1
face_value = 100

# fixed rate bond object
fixed_rate_bond = ql.FixedRateBond(
    settlement_days, 
    face_value, 
    schedule, 
    coupons, 
    day_count)


print([c.date() for c in fixed_rate_bond.cashflows()])
print([c.amount() for c in fixed_rate_bond.cashflows()])

# Discounting bond engine
bond_engine = ql.DiscountingBondEngine(ts_handle)


# Set the pricing engine for the fixed rate bond 
fixed_rate_bond.setPricingEngine(bond_engine)


print(fixed_rate_bond.NPV())


# Let us assume that the market prices this bond with a 50BP spread on top of the treasury yield curve. 
#Now we can, in this case, directly shock the flat_rate used in the yield term structure. Let us see what the value is:

flat_rate.setValue(0.0065)
print(fixed_rate_bond.NPV())

