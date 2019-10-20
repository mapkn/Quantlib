# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:54:32 2019

@author: patemi
"""

import QuantLib.QuantLib as ql


########### CONSTRUCT FIXED AND FLOAT LEG SCHEDULES ###################

settlement_offset=2  #in days
swap_term=5 # in years

calculation_date = ql.Date(28, 5, 2019)

calendar=ql.UnitedStates()

settle_date=calendar.advance(calculation_date,settlement_offset,ql.Days)
maturity_date=calendar.advance(settle_date,swap_term,ql.Years)

fixed_leg_tenor=ql.Period(3, ql.Months)
fixed_leg_date_gen=ql.DateGeneration.Forward

float_leg_tenor=ql.Period(3, ql.Months)
float_leg_date_gen=ql.DateGeneration.Forward


fixed_leg_schedule=ql.Schedule(settle_date, 
                             maturity_date, 
                             fixed_leg_tenor, 
                             calendar,
                             ql.ModifiedFollowing, 
                             ql.ModifiedFollowing,
                             fixed_leg_date_gen, False)

float_leg_schedule=ql.Schedule(settle_date, 
                             maturity_date, 
                             float_leg_tenor, 
                             calendar,
                             ql.ModifiedFollowing, 
                             ql.ModifiedFollowing,
                             float_leg_date_gen, False)
####################################################################



########### CONSTRUCT DISCOUNT AND LIBOR CURVES ###################

risk_free_rate=0.01

libor_rate = 0.02
day_count = ql.Actual365Fixed()

discount_curve = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))

libor_curve = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, libor_rate, day_count))

#libor3M_index = ql.Euribor3M(libor_curve)  
libor3M_index = ql.USDLibor(ql.Period(3, ql.Months), libor_curve)



###################################################################



#################### CONSTRUCT THE VANILLA SWAP ####################

notional = 10000000
fixed_rate = 0.025
fixed_leg_daycount = ql.Actual360()
float_spread = 0.005224509209907545
float_leg_daycount = ql.Actual360()



ir_swap = ql.VanillaSwap(ql.VanillaSwap.Payer, notional, fixed_leg_schedule, 
               fixed_rate, fixed_leg_daycount, float_leg_schedule,
               libor3M_index, float_spread, float_leg_daycount )


####################################################################


#################  EVALUATE THE SWAP ##############################

swap_engine = ql.DiscountingSwapEngine(discount_curve)
ir_swap.setPricingEngine(swap_engine)


#####################################################################


print(calculation_date, settle_date,maturity_date)

print(ir_swap.NPV())
print(ir_swap.fairSpread())
print(ir_swap.fixedLegBPS())
print(ir_swap.floatingLegBPS())

#calendar.

