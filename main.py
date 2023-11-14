from datetime import datetime
from decimal import Decimal, ROUND_DOWN
import argparse
import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import calendar

def main():
    parser = argparse.ArgumentParser(description="Display a calendar of US stock market trading days and summary.")
    parser.add_argument("--start_date", help="Start date in 'YYYY-MM-DD' format", default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument("end_date", help="End date in 'YYYY-MM-DD' format")
    parser.add_argument("amount", type=str, help="Amount to be divided by the number of trading days")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    amount_decimal = Decimal(args.amount)

    # Inline trading days calculation
    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    dt_range = pd.date_range(start=start_date, end=end_date, freq=us_bd)
    dt_range = dt_range[dt_range.dayofweek < 5]
    num_days = len(dt_range)

    # Ensure entire amount is invested by spreading it as evenly as possible
    if num_days > 0:
        divided_amount_per_day = (amount_decimal / Decimal(num_days)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        total_divided = divided_amount_per_day * num_days
        remaining_amount = amount_decimal - total_divided

        # Distribute the remaining amount over the days
        adjusted_dates = {}
        for i in range(int(remaining_amount * 100)):  # Convert remaining_amount to cents
            day_index = i % num_days
            adjusted_dates[dt_range[day_index]] = adjusted_dates.get(dt_range[day_index], 0) + Decimal('0.01')

    print("\nTrading Days Calendar with Fully Invested Amount:")
    for dt in dt_range:
        amount_for_day = divided_amount_per_day + adjusted_dates.get(dt, Decimal('0.00'))
        print(f"{dt.strftime('%Y-%m-%d')} ({calendar.day_name[dt.weekday()]}): {amount_for_day}")

    total_invested = divided_amount_per_day * num_days + remaining_amount

    print("\nSummary:")
    print(f"Total number of trading days: {num_days}")
    print(f"Total amount invested: {total_invested}")

if __name__ == "__main__":
    main()