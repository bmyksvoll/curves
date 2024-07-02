import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.holiday import AbstractHolidayCalendar, DateOffset, Holiday, next_monday, next_monday_or_tuesday, GoodFriday, EasterMonday, nearest_workday, MO

# Define a custom UK business day calendar that accounts for UK public holidays
class UKBusinessCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Year’s Day', month=1, day=1, observance=nearest_workday),
        GoodFriday,
        EasterMonday,
        Holiday('Early May Bank Holiday', month=5, day=1, offset=DateOffset(weekday=MO(1))),
        Holiday('Spring Bank Holiday', month=5, day=31, offset=DateOffset(weekday=MO(-1))),
        Holiday('Summer Bank Holiday', month=8, day=31, offset=DateOffset(weekday=MO(-1))),
        Holiday('Christmas Day', month=12, day=25, observance=next_monday),
        Holiday('Boxing Day', month=12, day=26, observance=next_monday_or_tuesday)
    ]
# Create a custom business day offset using the UK business calendar
uk_bd = CustomBusinessDay(calendar=UKBusinessCalendar())

# Function to calculate the first trading day which is one UK business days before the first of next month
# Last trading day is two UK business days before the first of next month
def is_first_trading_day(trade_date):
    first_day_next_month = pd.Timestamp(trade_date.year + int(trade_date.month == 12), trade_date.month % 12 + 1, 1)
    first_trading_day = first_day_next_month - 1 * uk_bd
    if first_trading_day == trade_date:
        return True
    else:
        return False
    