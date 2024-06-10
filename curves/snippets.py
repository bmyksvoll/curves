from datetime import datetime, timedelta

data = {
    'Include': [True, True, True, True, True, True, True, True, True, True],
    'Contract': ["JUL-21", "AUG-21", "SEP-21", "OCT-21", "NOV-21", "DEC-21", "Q1-22", "Q2-22", "Q3-22", "Q4-22"],
    'From': ["2021-07-01", "2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01", "2022-01-01", "2022-04-01", "2022-07-01", "2022-10-01"],
    'To': ["2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01", "2022-01-01", "2022-04-01", "2022-07-01", "2022-10-01", "2022-12-31"],
    'Price': [32.55, 32.5, 32.5, 32.08, 36.88, 39.8, 39.4, 25.2, 21.15, 29.5],
}

# List to hold lists of daily dates for each row
list_of_daily_dates = []

# Loop through each row and create a list of dates for that row
for from_date, to_date in zip(data['From'], data['To']):
    # Convert the 'From' and 'To' dates to datetime objects
    start_date = datetime.strptime(from_date, '%Y-%m-%d')
    end_date = datetime.strptime(to_date, '%Y-%m-%d')
    
    # Generate the list of dates for the current row
    current_row_dates = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d') 
                         for x in range((end_date - start_date).days)]
    
    # Append the list of dates for the current row to the main list
    list_of_daily_dates.append(current_row_dates)

# Now 'list_of_daily_dates' contains a list of lists with daily dates for each row
list_of_daily_dates