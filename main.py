from datetime import datetime
from decimal import Decimal, ROUND_DOWN
import argparse
import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import calendar

def main():
    def trading_days(start_date, end_date):
        us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
        dt_range = pd.date_range(start=start_date, end=end_date, freq=us_bd)
        dt_range = dt_range[dt_range.dayofweek < 5]
        return len(dt_range)

    parser = argparse.ArgumentParser(description="Display a calendar of US stock market trading days and summary.")
    parser.add_argument("--start_date", help="Start date in 'YYYY-MM-DD' format", default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument("end_date", help="End date in 'YYYY-MM-DD' format")
    parser.add_argument("amount", type=str, help="Amount to be divided by the number of trading days")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    amount_decimal = Decimal(args.amount)

    num_days = trading_days(start_date, end_date)
    if num_days > 0:
        divided_amount_per_day = (amount_decimal / Decimal(num_days)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        total_divided = divided_amount_per_day * num_days
        difference = amount_decimal - total_divided
        distributed_additional_amount = (divided_amount_per_day + difference / Decimal(num_days)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    else:
        distributed_additional_amount = Decimal('0.00')

    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    dt_range = pd.date_range(start=start_date, end=end_date, freq=us_bd)
    dt_range = dt_range[dt_range.dayofweek < 5]

    print("\nTrading Days Calendar with Equally Divided Amount (Decimal):")
    for dt in dt_range:
        print(f"{dt.strftime('%Y-%m-%d')} ({calendar.day_name[dt.weekday()]}): {distributed_additional_amount}")

    total_invested = distributed_additional_amount * num_days

    print("\nSummary:")
    print(f"Total number of trading days: {num_days}")
    print(f"Total amount invested: {total_invested}")

if __name__ == "__main__":
    main()