# hp_4.py
#
import csv
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    formatted_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date_str = datetime.strftime(date_obj, '%d %b %Y')
        formatted_dates.append(formatted_date_str)
    return formatted_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError('start should be a str type.')
    if not isinstance(n, int):
        raise TypeError('n should be an int type.')

    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    if not isinstance(start_date, str):
        raise TypeError("start_date must be a string")
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    start = datetime.strptime(start_date, "%Y-%m-%d")
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    # read input file
    with open(infile, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    # calculate late fees on a patron_id basis
    fees = {}
    for row in data:
        patron_id = row['patron_id']
        date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
        date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')
        if date_returned > date_due:
            days_late = (date_returned - date_due).days
            fee = days_late * 0.25  # $0.25 per day late fee
            fees[patron_id] = fees.get(patron_id, 0) + fee

    # write summary report to outfile
    with open(outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['patron_id', 'late_fees'])
        for patron_id, fee in fees.items():
            writer.writerow([patron_id, '{:.2f}'.format(fee)])


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    #BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
