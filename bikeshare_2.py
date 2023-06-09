import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }




def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    city = input ('Would you like to see data for Chicago, New York City, or Washington? ').lower()
    while city not in cities:
            print('Sorry I did not understad that. Please select Chicago, New York City, or Washington.')
            city = input ('Select city: ').lower()

    # get user to chose month or day filter
    filters = ['m', 'd', 'n']
    filter = input('Would you like to filter for month ("m"), day ("d"), or no filter at all ("n")? ').lower()
    while filter not in filters:
        print('Sorry I did not understad that. Please type "m", "d", or "n". ')
        filter = input().lower()
    
    if filter =='n':
        month = 'all'
        day = 'all'
    elif filter == 'm':
        # get user input for month (all, january, february, ... , june)
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input ('Would you like to filter for month, or see all data? (type January, February, ..., June, or "all") ').lower()
        day = 'all'
        while month not in months:
            print('Sorry I did not understad that. Please select January, February, ..., June, or "all". ')
            month = input ('Select month or type "all": ').lower()
    elif filter == 'd':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        day = input('For which day would you like to see data for? Type Monday, Tuesday, ..., Sunday, or "all"! ').lower()
        month = 'all'
        while day not in days:
            print('Sorry I did not understad that. Please try again.' )
            day = input('Selet day or type "all". ').lower()
    else:
        print('Please type "m", "d", or "n"! ')
    
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # create new column for trip (combination of start+end station)
    df['trip'] = df['Start Station'] + str(' - ') + df['End Station']


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    c_month = calendar.month_name[df['month'].mode()[0]]
    print('The most common month for your selection was: {}.'.format(c_month))

    # display the most common day of week
    c_day = df['day_of_week'].mode()[0]
    print('The most common day of week for your selection was: {}.'.format(c_day))

    # display the most common start hour
    c_hour = df['hour'].mode()[0]
    print('The most common start hour for your selection was: {}.'.format(c_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    c_start = df['Start Station'].mode()[0]
    print('The most common start station for your selection was: {}.'.format(c_start))

    # display most commonly used end station
    c_end = df['End Station'].mode()[0]
    print('The most common end station for your selection was: {}.'.format(c_end))

    # display most frequent combination of start station and end station trip
    c_trip = df['trip'].mode()[0]
    print('The most common trip for your selection was: {}.'.format(c_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttl_duration = df['Trip Duration'].sum()
    print('The total trip duration for your selection was: {} seconds.'.format(ttl_duration))

    # display mean travel time
    c_duration = df['Trip Duration'].mean()
    print('The most common trip duration for your selection was: {} seconds.'.format(c_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    u_type = df['User Type'].value_counts()
    print('User types for your selection: \n' + str(u_type))

    # Display counts of gender
    if city != 'washington':
        g_count = df['Gender'].value_counts()
        print('\nGenders for your selection: \n' + str(g_count))
    else:
        print('\nGender stats not available for Washington.')     

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        year_early = int(df['Birth Year'].min())
        year_recent = int(df['Birth Year'].max())
        year_common = int(df['Birth Year'].mode()[0])
        print('\nThe oldest user from your selection was born in {}, the youngest was born in {}. The most common birth year was {}.'.format(year_early, year_recent, year_common))
    else:
        print('\nYear of birth stats not available for Washington.')  


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data (df):
    """Displays raw data on bikeshare users."""  
    
    yes_no = ['yes', 'no']
    d = input('Would you like to see see 5 lines of raw data? Type yes/no: ') 
    c = 5
    while d == 'yes':
        print(df[c-5:c])
        d = input('Would you like to see 5 more rows of data? Type yes/no: ')
        c += 5
    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()