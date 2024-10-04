import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
import pytest

def generate_US_Federal_Holidays() -> []:
    """Generate the US Federal Holidays across the POC dates.
    
    There shouldn't be trading on Federal Holidays as the Federal Reserve isn't open.
    """
    
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start='2008-08-08', end='2016-07-01').to_pydatetime()

    # for day in holidays[:5]: # show dates if needed
    #     print(day.date())
    return holidays


# def is weekday
    # can use dt.weekday and choose the days

# def same timeframe
    # do the time frames of the different sources match