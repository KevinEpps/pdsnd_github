import time
import pandas as pd
import numpy as np
import calendar


#Define global variables
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago' , 'new york city' , 'washington']

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'All']

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print("\nHello! Let's explore some US bikeshare data!\n")

    #Get user input to determine which city to analyze and make sure it's valid
    city = input('Select a city to analyze: Chicago, New York City, or Washington.\n').lower()
    while city not in CITIES:
        city = input('Select a valid city:  Chicago, New York City, or Washington.\n').lower()

    #Get user input to determine which month/s to analyze and make sure it's valid
    month = input('\nChoose month! January, February, March, April, May, June or All.\n').title()
    while month not in MONTHS:
        month = input('Enter a valid month.\n').title()

    #Get user input to determine which day/s to analyze and make sure it's valid
    day = input('\nChoose a day of the week: Sunday, Monday, Tuesday...or All\n').title()
    while day not in DAYS:
        day = input('Enter a valid day.\n').title()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

 # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

# convert Start Time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# create month and day colums from Start Time
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month

    # filter by month if applicable
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month =  months.index(month) + 1

        #create new dataframe based on month filter
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular_month: {}'.format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular_day: {}'.format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour (24hr): {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is: {}'.format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most commonly used end station is: {}'.format(popular_end))

    # display most frequent combination of start station and end station trip
    popular_combination = (df['Start Station'] + " " + df['End Station']).mode()[0]
    print('The most frequent combination is {}'.format(popular_combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is: {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('There are: {}'.format(gender_types))

    #Handles keyerror execption for washington data not having gender information
    except KeyError:
        print('\n There is no gender info for Washington')

    # Display earliest, most recent, and most common year of birth
    try:

        earliest = df['Birth Year'].min()
        latest = df['Birth Year'].max()
        mode = df['Birth Year'].mode()[0]
        print('The oldest users are born in {}.\nThe youngest users are born in {}.'
          '\nThe most popular birth year is {}.'.format(earliest, latest, mode))

    #Handles keyerror exception for washington data not having birth year data
    except KeyError:
        print('\n There is no birth year data for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Returns 5 rows of raw data based on user input
def display_raw(df):
    y = 0
    
    #checks to ensure the data is not outside bounds of the df
    while y < len(df.index):
        additional_data = input('Print 5 lines of raw data?  Yes or No.\n').title()

        #continues to add rows of data by intervals of five
        if additional_data == 'Yes':
            y += 5
            print(df.iloc[0:y])
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
