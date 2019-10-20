

import QuantLib.QuantLib as ql


day_count = ql.Thirty360()
d1=ql.Date(5,7,2019)
d2=ql.Date(6,7,2019)

print(day_count.name())
print(day_count.BondBasis)
print(day_count.yearFraction(d1,d2))

