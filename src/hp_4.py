# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        new_date_str = date_obj.strftime('%d %b %Y--%d %b %Y')
        new_dates.append(new_date_str)
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_list = date_range(start_date, len(values))
    return list(zip(date_list, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile, 'r') as f:
        reader = DictReader(f)
        # Create a defaultdict to store the fee totals for each patron id
        patron_fees = defaultdict(float)
        # Iterate over each row in the input file
        for row in reader:
            # Get the due date and return date for the book
            due_date_str = row['due_date']
            return_date_str = row['return_date']
            # Reformat the dates to the required format
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d')
            due_date_str = due_date.strftime('%d %b %Y--%d %b %Y')
            return_date_str = return_date.strftime('%d %b %Y--%d %b %Y')
            # Calculate the number of days late
            days_late = (return_date - due_date).days
            if days_late > 0:
                # Calculate the fee for this book
                fee_per_day = float(row['fee_per_day'])
                fee = fee_per_day * days_late
                # Add the fee to the total for this patron id
                patron_id = row['patron_id']
                patron_fees[patron_id] += fee
    # Write the output file
    with open(outfile, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=['patron_id', 'total_fees'])
        writer.writeheader()
        for patron_id, total_fees in patron_fees.items():
            writer.writerow({'patron_id': patron_id, 'total_fees': total_fees})


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

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
