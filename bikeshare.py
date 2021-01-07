import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
'new york city': 'new_york_city.csv',
'washington': 'washington.csv' }

def get_filters(city, month, day):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nPlease select a city to view data for: Chicago, New York City or Washington!\n").lower()
        if city in CITY_DATA:
            break
        else:
            print("\n your input is not correct. please enter a valid city\n")

    while True:
        time = input("\nDo you want to filter by month, day, all or none?\n").lower()
        if time == 'month':
            month = ['january', 'february', 'march', 'april', 'may', 'june']
            month = input("\nWhich month? January, Feburary, March, April, May or June?\n").lower()
            if month.lower() in month:
                day = 'all'
                break
            else:
                print ('Oops! it seems your entry is not valid, please try again')

        elif time == 'day':
            day = ('sunday','monday','tuesday','wednesday','thursday','friday','saturday','all')
            day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n").lower()
            if day.lower() in day:
                month = 'all'
                break
            else:
                print('Oops! It seems your entry is not valid, please try again')

        elif time == 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = input("\nWhich month? January, Feburary, March, April, May or June?\n").lower()
            if month not in months:
                print('Sorry, that\'s not valid. please try again')
                continue
            else:
                days = ('sunday','monday','tuesday','wednesday','thursday','friday','saturday','all')
                day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday\n").lower()
                if day not in days:
                    print ('Oops! It seems your entry is not valid, please try again')
                    continue
                else:
                    break
        elif time == 'none':
            month ='all'
            day ='all'
            break
        else:
            print('Oops! seems you wrote the wrong word!\n')
            continue

    print('\nShowing data for {}, month: {}, day: {}\n'.format ((city), (month), (day)))

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

# display the most common month
    common_month = df['month'].mode()[0]
    common_month = calendar.month_name[common_month]
    print('The most popular month for trips is {}'.format(common_month))

# display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most popular day of the week is {}'.format(common_day_of_week))


# display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most popular hour is {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

# display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}'.format(common_start))

# display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most commonly used end station is {}'.format(common_end))

# display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print('The most frequent combination of start and end station trip is {}'.format(common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

# display total travel time
    total_travel = df['Trip Duration'].sum()
    print('The total travel time is {}'.format(total_travel))

# display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('The average travel time is {}'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

# Display counts of user types
    print('\nThe breakdown of users is as follows:\n')
    user_types = df['User Type'].value_counts()
    print('User type\n{0}: {1}\n{2}: {3}'.format(user_types.index[0],user_types.iloc[0],user_types.index[1],user_types.iloc[1]))

# Display counts of gender
    print('\nThe breakdown of gender is as follows:\n')
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('\nMale:{0}\nFemale:{1}. '.format(gender.loc['Male'],gender.loc['Female']))
    else:
        print("There is no gender information for this city.")


# Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        print('\nThe earlist year of birth is {}'.format(earliest))
        recent = df['Birth Year'].max()
        print('The most recent year of birth is {}'.format(recent))
        common_year = df['Birth Year'].mode()[0]
        print('The most common year of birth is {}'.format(common_year))
    else:
        print("There is no birth year information for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
"""Asking 5 lines of the raw data and more, if they want"""
def display_raw_data(df):
    """
    Questions the user on if they would like to see raw data or not.

    Returns:
            5 rows of raw data at a time if input == yes
    """
    raw_data = 0
    while True:
        respond = input("Would you like to see the raw data? Yes or No\n").lower()
        if respond not in ['yes', 'no']:
            print("\nSeems you entered the wrong word. Please try again.\n")
            continue
        elif respond == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])
        repeat = input("would you like to see some more raw data? Yes or No\n").lower()
        if repeat == 'no':
            break
        elif respond == 'no':
            return
def main():
    city = ""
    month = ""
    day = ""
    while True:
        city, month, day = get_filters(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
