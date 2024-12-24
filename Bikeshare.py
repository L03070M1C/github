import time
from traceback import print_list
import pandas as pd # type: ignore
import numpy as np # type: ignore

# Constants
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_filter_city():
    """
    Asks user to specify a city.
    Returns:
        (str) city - name of the city to analyze
    """
    cities_list = list(CITY_DATA.keys())
    num_cities = len(cities_list)
    for i, city in enumerate(cities_list, start=1):
        print(f'        {i}. {city.title()}')

    while True:
        try:
            city_num = int(input(f"\n    Enter a number for the city (1 - {num_cities}): "))
            if 1 <= city_num <= num_cities:
                return cities_list[city_num - 1]
        except ValueError:
            continue

def get_filter_month():
    """
    Asks user to specify a month to filter on, or choose all.
    Returns:
        (str) month - name of the month to filter by, or "all" for no filter
    """
    while True:
        month = input("Enter the month with January=1, June=6 or 'a' for all: ").strip().lower()
        if month == 'a':
            return 'all'
        elif month.isdigit() and 1 <= int(month) <= 6:
            return MONTHS[int(month) - 1]
        else:
            print("        ---->>  Valid input:  1 - 6, a")

def get_filter_day():
    """
    Asks user to specify a day to filter on, or choose all.
    Returns:
        (str) day - day of the week to filter by, or "all" for no filter
    """
    while True:
        day = input("Enter the day with Monday=1, Sunday=7 or 'a' for all: ").strip().lower()
        if day == 'a':
            return 'all'
        elif day.isdigit() and 1 <= int(day) <= 7:
            return WEEKDAYS[int(day) - 1]
        else:
            print("        ---->>  Valid input:  1 - 7, a")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('=' * 40)
    print('\n  Hello! Let\'s explore some US bikeshare data!\n')
    city = get_filter_city()
    month = get_filter_month()
    day = get_filter_day()
    return city, month, day

def filter_summary(city, month, day, init_total_rides, df):
    """
    Displays selected city, filters chosen, and simple stats on dataset.
    """
    filtered_rides = len(df)
    num_stations_start = len(df['Start Station'].unique())
    num_stations_end = len(df['End Station'].unique())

    print('    Gathering statistics for:', city)
    print('    Filters (month, day):', month, ',', day)
    print('    Total rides in dataset:', init_total_rides)
    print('    Rides in filtered set:', filtered_rides)
    print('    Number of start stations:', num_stations_start)
    print('    Number of end stations:', num_stations_end)

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    if month != 'all':
        month_i = MONTHS.index(month) + 1
        df = df[df['month'] == month_i]
    
    if day != 'all':
        day_i = WEEKDAYS.index(day)
        df = df[df['day_of_week'] == day_i]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    popular_month = MONTHS[df['month'].mode()[0] - 1].title()
    print('Most Common Month:', popular_month)

    popular_day = WEEKDAYS[df['day_of_week'].mode()[0]].title()
    print('Most Common Day:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_station = df['Start Station'].mode()[0]
    end_station = df['End Station'].mode()[0]
    combo_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    
    print('Most Commonly Used Start Station:', start_station)
    print('Most Commonly Used End Station:', end_station)
    print('Most Commonly Used Combination of Start and End Station Trip:', combo_station)
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    print('Total Travel Time:', total_travel_time / 86400, "Days")
    print('Mean Travel Time:', mean_travel_time / 60, "Minutes")
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    except KeyError:
        print('\nGender Types:\nNo data available for this month.')

    try:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('\nEarliest Year:', earliest_year)
        print('Most Recent Year:', most_recent_year)
        print('Most Common Year:', most_common_year)
    except KeyError:
        print('\nBirth Year Data:\nNo data available for this month.')
    print('-' * 40)

def display_raw_data(df):
    """
    Asks if the user would like to see some lines of data from the filtered dataset.
    Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Continues asking until they say stop.
    """
    show_rows = 5
    rows_start = 0
    rows_end = show_rows - 1

    print('\n    Would you like to see some raw data from the current dataset?')
    while True:
        raw_data = input('      (y or n):  ')
        if raw_data.lower() == 'y':
            print('\n    Displaying rows {} to {}:'.format(rows_start + 1, rows_end + 1))

            print('\n', df.iloc[rows_start : rows_end + 1])
            rows_start += show_rows
            rows_end += show_rows

            print_list('.')
            print('\n    Would you like to see the next {} rows?'.format(show_rows))
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        init_total_rides = len(df)
        filter_summary(city, month, day, init_total_rides, df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()