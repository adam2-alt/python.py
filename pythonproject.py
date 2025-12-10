import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_valid_input(
        'Name of the city to analyze (chicago, new york city, washington): ',
        CITY_DATA.keys()
    )

    month = get_valid_input(
        'Enter month (january, february, march, april, may, june, all): ',
        ['january','february','march','april','may','june','all']
    )

    day = get_valid_input(
        'Enter day (monday, tuesday, wednesday, thursday, friday, saturday, sunday, all): ',
        ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    )

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
    df = pd.read_csv(CITY_DATA[city])
    df = add_time_columns(df)

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
         months = ['january', 'february', 'march', 'april', 'may', 'june']
         month_num = months.index(month.lower()) + 1
         df = df[df['month'] == month_num]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]
      
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('the most common month',df['month'].mode()[0])

    # TO DO: display the most common day of week
    print('the most common day of week',df['day'].mode()[0])

    # TO DO: display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    print("the most common start hour",df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
       
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station=df['Start Station'].value_counts().idxmax()
    print('most commonly used start station',start_station)

    # TO DO: display most commonly used end station
    end_station=df['End Station'].value_counts().idxmax()
    print('most commonly used end station',end_station)
    # TO DO: display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('most frequent combination of start station and end station trip:',most_common_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time']=pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time= df['Travel Time'].sum()
    print('total travel time is ',total_travel_time)
    # TO DO: display mean travel time
    print('Total travel time (seconds):', total_travel_time.total_seconds())
    print('Total travel time (hours):', total_travel_time.total_seconds()/3600)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)


    # TO DO: Display counts of gender
    # Display counts of gender (if available)
    if 'Gender' in df.columns:
        print('\nGender counts:')
        print(df['Gender'].value_counts())
    else:
        print('\nNo Gender data available for this city.')

    # Display birth year stats (if available)
    if 'Birth Year' in df.columns:
        birth_years = df['Birth Year'].dropna()
        print('Earliest year:', int(birth_years.min()))
        print('Most recent year:', int(birth_years.max()))
        print('Most common year:', int(birth_years.mode()[0]))
    else:
        print('No Birth Year data available for this city.')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw = input('Would you like to see 5 rows of raw data? Enter yes or no: ').lower()
        start = 0
        while raw == 'yes':
         print(df.iloc[start:start+5])
         start += 5
         raw = input('Would you like to see more 5 rows of data? Enter yes or no: ').lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
