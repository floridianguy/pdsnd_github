import time
import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
	"""
	This section asks the user to input a city, month and day of the week.  There
    is an option to use 'all' for the months and days in order to analyze the 
    complete data set.  Also note that months run from January to June.
	Returns:
		(str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
	"""
	print('Hello! Let\'s explore some US bikeshare data!\n')

	city = input('Please choose a city to analyze\n')
	city = city.lower()
	while city != 'chicago' and city != 'washington' and city != 'new york city':
		city = input('Please choose a valid city: either chicago, washington or new york city\n')
		city = city.lower()
	else:
		print('Okay great! We\'re going to look at stats for', city.capitalize(), '\n')

	# next input month by name and we'll do the indexing in the load_data section

	month = input('Please enter a month from January to June to analyze, or type "all" to view all months.\n')
	list_of_valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
	month = month.lower()
	while month not in list_of_valid_months:
		month = input('Please choose a valid month, January though June, or \'all\'\n')
		month = month.lower()
		if month == 'all':
			print('Great, you\'ve selected all months\n')
		elif month in list_of_valid_months:
			print('Great, you\'ve selected', month.capitalize())
			break
	else:
		print('Great, you\'ve selected', month.capitalize())

	day = input('Please choose a day of the week to analyze or type "all"\n')
	list_of_valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
	day = day.lower()
	while day not in list_of_valid_days:
		day = input('Please choose a valid day of the week or type \'all\'\n')
		day = day.lower()
		if day == 'all':
			print('Great you have selected all days of the week')
		elif day in list_of_valid_days:
			print('Great, you\'ve selected', day.capitalize())
	else:
		print('\n')
		print('Great, you\'ve selected', day.capitalize())

	print('-'*40)
	return city, month, day


def load_data(city, month, day):
	"""
	Next we will load the data for the specified city and filters for month and day, if applicable.
	Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

	df = pd.read_csv(CITY_DATA[city])
	df['Start Time'] = pd.to_datetime(df['Start Time'])
	df['End Time'] = pd.to_datetime(df['End Time'])
	df['month'] = df['Start Time'].dt.month
	df['day_of_week'] = df['Start Time'].dt.weekday_name

	if month != 'all':
		months = ['january', 'february', 'march', 'april', 'may', 'june']
		month = months.index(month) + 1

		df = df[df['month'] == month]

	if day != 'all':
		df = df[df['day_of_week'] == day.title()]

	return df

def time_stats(df):
	"""This next section provides stats on the most frequent times of travel."""

	print('\nCalculating the most frequent times of travel...\n')
	start_time = time.time()

	# display the most common month
	popular_month = df['month'].mode()[0]
	print('The most popular month, expressed as an integer is: ', popular_month)

    # display the most common day of week
	popular_day = df['day_of_week'].mode()[0]
	print('The most popular day of the week for a ride is: ', popular_day)

    # display the most common start hour
	df['hour'] = df['Start Time'].dt.hour
	popular_hour = df['hour'].mode()[0]
	print('The most popular time to start is: ', popular_hour, "o'clock")

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def station_stats(df):
	"""This section provides data on the most popular stations and round trip."""

	print('\nCalculating the most popular stations and trip...\n')
	start_time = time.time()

	# display most commonly used start station
	popular_start_station = df['Start Station'].mode()[0]
	print('The most popular starting point is: ', popular_start_station)

    # display most commonly used end station
	popular_end_station = df['End Station'].mode()[0]
	print('The most popular ending point is: ', popular_end_station)

    # display most frequent combination of start station and end station trip
	df['combination'] = df['Start Station'] + ' and ' + df['End Station']
	popular_combination = df['combination'].mode()[0]
	print(popular_combination)


def trip_duration_stats(df):
	"""This section provides stats on the total and average trip duration."""

	print('\nCalculating trip durations...\n')
	start_time = time.time()

	# display total travel time
	df['start_time'] = df['Start Time']
	df['end_time'] = df['End Time']
	trip_duration = (df['end_time'].subtract(df['start_time'])).sum()
	print('Total duration of all trips: ', trip_duration)

    # display mean travel time

	mean_trip_duration = (df['end_time'].subtract(df['start_time'])).mean()
	print('Average trip duration: ', mean_trip_duration)


def user_stats(df):
	"""This section provides information on the bikeshare users.  Note that
    age and gender data is not available for Washington."""

	print('\nCalculating user stats...\n')
	start_time = time.time()
	city = input('Please type the city name again.\n')

	# Display counts of user types
	user_types = df['User Type'].value_counts()
	print(user_types)

    # Display counts of gender

	city = city.lower()
	if city == 'washington':
		print('No gender data is available for washington.\n')
	else:
		gender_counts = df['Gender'].value_counts()
		gender_not_specified = df['Gender'].isna().sum()
		print(gender_counts, '\nand ', gender_not_specified, 'users have no gender specified')

    # Display earliest, most recent, and most common year of birth

	city = city.lower()
	if city == 'washington':
		print('No year of birth data is available for washington.')
	else:
		min_birth_year = df['Birth Year'].min()
		max_birth_year = df['Birth Year'].max()
		min_age = pd.datetime.now().year - max_birth_year
		common_birth_year = df['Birth Year'].mode()[0]
		percentile_fifty_year = df['Birth Year'].quantile(.5)
		median_age = pd.datetime.now().year - percentile_fifty_year

		print('The minimum year of birth is: ', min_birth_year)
		print('The maximum year of birth is: ', max_birth_year)
		print('The most common year of birth is: ', common_birth_year)
		print('\nHalf of the riders are at least', median_age, 'years old.' )

		if max_birth_year > 2010:
			print('Wow! Someone only', min_age, ' years old rented a bike!')
		else:
			print('Cool!  Those are some interesting stats!')


def show_data(df):
	"""This section provides the option to view some of the raw data."""
	view_data = input('Would you like to see the first 5 rows?\n')
	view_data = view_data.lower()
	while view_data not in ['yes', 'no']:
		view_data = input('Please input "yes" or "no"')
		view_data = view_data.lower()
	while view_data == 'yes':
		print(df.head())
		initial_row = 0
		fifth_row = 5
		view_data = input('Would you like to see another 5 rows of data?\n')
		view_data = view_data.lower()
		while view_data == 'yes':
			initial_row += 5
			fifth_row += 5
			print(df.iloc[initial_row:fifth_row])
			view_data = input('Would you like to see another 5 rows of data?\n')
			view_data = view_data.lower()
		else:
			print('\n')


def main():
	while True:
		city, month, day = get_filters()
		df = load_data(city, month, day)

		time_stats(df)
		station_stats(df)
		trip_duration_stats(df)
		user_stats(df)
		show_data(df)

		restart = input('\nWould you like to restart? Enter yes or no.\n')
		if restart.lower() != 'yes':
			break

if __name__ == "__main__":
	main()
