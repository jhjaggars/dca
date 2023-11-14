from datetime import datetime
import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import argparse

def trading_days(start_date, end_date):
    """
    Calculate the number of US stock market trading days between two dates.

    Args:
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
    int: Number of trading days.
    """
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # Define US business day calendar
    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())

    # Generate date range for business days
    dt_range = pd.date_range(start=start, end=end, freq=us_bd)

    # Remove weekends (Saturday and Sunday)
    dt_range = dt_range[dt_range.dayofweek < 5]

    return len(dt_range)

def modified_trading_days(start_date, end_date, amount):
    """
    Calculate the number of US stock market trading days between two dates and 
    divide a given amount by this number.

    Args:
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.
    amount (float): The amount to be divided.

    Returns:
    float: The amount divided by the number of trading days.
    """
    num_days = trading_days(start_date, end_date)
    return amount / num_days if num_days > 0 else 0

import calendar

def display_trading_days_calendar(start_date, end_date):
    """
    Display a calendar of US stock market trading days between two dates, 
    including the date and the day of the week.

    Args:
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.
    """
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # Define US business day calendar
    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())

    # Generate date range for business days
    dt_range = pd.date_range(start=start, end=end, freq=us_bd)

    # Remove weekends (Saturday and Sunday)
    dt_range = dt_range[dt_range.dayofweek < 5]

    # Displaying each date with its corresponding weekday
    for dt in dt_range:
        print(f"{dt.strftime('%Y-%m-%d')} ({calendar.day_name[dt.weekday()]})")

def display_trading_days_with_amount(start_date, end_date, amount):
    """
    Display a calendar of US stock market trading days between two dates, 
    including the date, day of the week, and the divided amount rounded down to two decimal places.

    Args:
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.
    amount (float): The amount to be divided.
    """
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # Define US business day calendar
    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())

    # Generate date range for business days
    dt_range = pd.date_range(start=start, end=end, freq=us_bd)

    # Remove weekends (Saturday and Sunday)
    dt_range = dt_range[dt_range.dayofweek < 5]

    # Calculate the divided amount per day, rounded down to two decimal places
    divided_amount_per_day = np.floor((amount / len(dt_range)) * 100) / 100

    # Displaying each date with its corresponding weekday and divided amount
    for dt in dt_range:
        print(f"{dt.strftime('%Y-%m-%d')} ({calendar.day_name[dt.weekday()]}): {divided_amount_per_day:.2f}")

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Display a calendar of US stock market trading days between two dates, each with a portion of a divided amount.")
    # Add arguments for start and end dates, and the amount
    parser.add_argument("--start_date", help="Start date in 'YYYY-MM-DD' format", default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument("end_date", help="End date in 'YYYY-MM-DD' format")
    parser.add_argument("amount", type=float, help="Amount to be divided by the number of trading days")

    # Parse the arguments
    args = parser.parse_args()

    # Display the trading days with divided amount
    print("\nTrading Days Calendar with Divided Amount:")
    display_trading_days_with_amount(args.start_date, args.end_date, args.amount)

if __name__ == "__main__":
    main()