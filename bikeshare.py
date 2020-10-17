import numpy as np
import pandas as pd
import time

# Setting up some needed data structures
cities_dict = {'Chicago': 'chicago.csv', 'New York': 'new_york_city.csv', 'Washington': 'washington.csv'}
days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

print('\n........Welcome to US bikeshare data analysis!..........\n')

def get_inputs():
    """ Returns inputs from the user in an interactive way """
    while True:
        where = input("Choose a city from (Chicago - New York - Washington) or 'quit' to exit: ").title()
        if where == 'Quit':
            quit()
        if where not in cities_dict:
            print('Not an available city! Please make sure you enter the correct city/name.')
            continue
        else: break

    while True:
        month_filter = input('Do you want to filter the data by month? (Yes/No) ').title()
        if month_filter == 'No':
            which_month = 'all'
            break
        elif month_filter == 'Yes':
            while True:
                try:
                    which_month = int(input('Choose a month filter from January to June (Please Enter it as an integer): '))
                except:
                    print('The month must be as an integer.')
                    continue
                if which_month in list(range(1,7)):
                    break
                else:
                    print('Not a valid month!')
                    continue
            break
        else:
            print('Not a valid input! you should Enter Yes or No.')
            continue


    while True:
        day_filter = input('Do you Want to filter the data by day? (Yes/No) ').title()
        if day_filter == 'No':
            which_day = 'all'
            break
        elif day_filter == 'Yes':
            while True:
                which_day = input('Choose a day filter (Please write the day full name): ').title()
                if which_day not in days:
                    print('Not a valid day! Please make sure you enter the right full name.')
                    continue
                else: break
            break
        else:
            print('Not a valid input! you should Enter Yes or No')
            continue
    return where, which_month, which_day


def load_data(city, month, day):
    """ Returns a dataframe of the city data file and filters it if requested """
    df = pd.read_csv(cities_dict[city])

    # Converting the Start Time to date time and extracting needed values to new cloumns
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']= df['Start Time'].dt.month
    df['day_of_date']= df['Start Time'].dt.day_name()
    df['hour']= df['Start Time'].dt.hour

    # Filtering by month if requested
    if month != 'all':
        df = df[df['month']==month]

    # Filtering by day if requested
    if day != 'all':
        df = df[df['day_of_date']==day]
    return df

# Date and time statistics
def time_stats():
    """ Calculates and prints date and time statistics """
    print('\nShowing data from City: ', where, ' Month filter: ', which_month,
                ' Day filter: ', which_day)
    time.sleep(1)
    print('\nCalculating date and time statistics...\n')
    time.sleep(1)
    common_hour = df['hour'].mode()[0]
    common_day = df['day_of_date'].mode()[0]
    common_month = df['month'].mode()[0]

    print('Most common hour: ', common_hour)
    if which_day == 'all':
        print('Most common day: ', common_day)
    if which_month == 'all' and which_day == 'all':
        print('Most common month: ', common_month)
    return None

# Popular stations and trip statistics
def stations_stats():
    """ Calculates and prints stations statistics """
    print('\nCalculating stations and trips statistics...\n')
    time.sleep(1)
    common_start = df['Start Station'].mode()[0]
    common_end = df['End Station'].mode()[0]

        # Concatenating Start Station and End Station columns in one new column
        # to get the most frequent trip
    df['Trip'] = 'Start Staion: ' + df['Start Station'] + ' End Station: ' + df['End Station']
    common_trip= df['Trip'].mode()[0]
    print('Most common start: ', common_start,
        '\nMost common end: ', common_end, '\nMost common trip: ', common_trip)
    return None

# Total and average travel time
def duration_stats():
    """ Calculates and prints duration statistics """
    print('\nCalculating total and average travel time...\n')
    time.sleep(1)
    total_time= df['Trip Duration'].sum()
    average_time= df['Trip Duration'].mean()

    print('Total travel time: ', total_time//60//60//24 ,
            ' days ',(total_time//60//60)%24, 'hours', (total_time//60)%60, 'minutes')
    print('Average travel time: ', average_time//60//60 ,
            ' hours ',(average_time//60)%60 ,' minutes')
    return None

# User Info statistics
def user_stats():
    """ Calculates and prints the users statistics """
    print('\nCalculating user info statistics...\n')
    time.sleep(1)
    user_type= df['User Type'].value_counts()
    print(user_type)
    try:
        user_gender= df['Gender'].value_counts()
        oldest_user= df['Birth Year'].min()
        youngest_user= df['Birth Year'].max()
        common_age= df['Birth Year'].mode()[0]
        print('\nUser gender:\n', user_gender, '\n\nEarliest year of birth: ', int(oldest_user),
                '\n\nMost recent year of birth: ', int(youngest_user),
                '\n\nMost comman year of birth: ', int(common_age))
    except: pass
    return None

# Asking the user if he wants to show some data:
def show_row_data():
    """ Prints the row data if the user want to show it """
    while True:
        show_data = input('\nDo you want to show first 5 rows of data? (Yes/No) ').title()
        if show_data == 'No':
            print('\nALL Done!\n')
            break
        elif show_data == 'Yes':
            i = 5
            while True:
                print(df.head(i))
                i+=5
                show_again = input('Do you want to show another 5 rows? (Yes/No) ').title()
                if show_again == 'Yes':
                    print('\n')
                    continue
                else:
                    print('\nALL Done!\n')
                break
            break
        else:
            print('Not a valid input!')
            continue

while True:
    where, which_month, which_day = get_inputs()
    df = load_data(where, which_month, which_day)
    time_stats()
    stations_stats()
    duration_stats()
    user_stats()
    show_row_data()
