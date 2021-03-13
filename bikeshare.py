#Code developed by David Singh Arjona, for the purpose of the Project #2: Explore US Bikeshare Data,
#during the Data Analytics Fundamentals Nanodegree Program by Udacity.

#Compilation time calculations were suppressed to make the code a little more efficient, since it's not
#really necessary. Time and numpy importations were suppressed too.


import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    
    '''
    This section requires the name of the city, the month and the week day to analyze, 
    then converts it to lowercase and validates if they are well written. Otherwise, 
    it returns a string that asks for a new input. Finally, it returns the variables
    city, month and day. Addicionally, the 'valid_stat' boolean statement allows the
    code to exit the loop when the variable names are permitted.
    '''
   
    print('Hello! Let\'s explore some US bikeshare data!')
    valid_names = ["new york city", "chicago", "washington"]
    valid_stat = False
    while not valid_stat:
        city = input("Please enter a valid city name (New York City, Chicago or Washington): ")
        city = city.lower()
        if city in valid_names:
            print("Valid name!")
            valid_stat = True
            break
        else:
            print("Unvalid name, please try again")
        
    valid_months = ["all", "january", "february", "march", "april", "may", "june"]
    valid_stat = False
    while not valid_stat:
        month = input("Please enter a valid month (January, February, March, April, May, June or All): ")
        month = month.lower()
        if month in valid_months:
            print("Valid month!")
            valid_stat = True
            break
        else:
            print("Unvalid month, please try again")
    
    valid_days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    valid_stat = False
    while not valid_stat:
        day = input("Please enter a valid day (Monday, Tuesday, Wednesday, Thurday, Friday, Saturday, Sunday or All): ")
        day = day.lower()
        if day in valid_days:
            print("Valid day!")
            valid_stat = True
            break
        else:
            print("Unvalid day, please try again")

    print('-'*100)
    return city, month, day

def load_data(city, month, day):
    '''
    This section filters the data, depending on the month and day requested (if
    used requested of all months and/or all days).
    '''

    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
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
    '''
    This section calculates the most frequent month, day and hour of travel. The 
    purpose of [0] is to display the data as a single number (without the index).
    The first part filters the most common month if the user asks for a specific 
    month.
    '''

    print('\nCalculating The Most Frequent Hours, Days and Months of travel...\n')

    if df['month'].unique().shape[0] > 1:
        
        common_month = df['month'].mode()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        print('Most Common Month:', months[common_month[0] -1].title())
    
    common_dow = df['day_of_week'].mode()
    print('Most Common Day of Week:', common_dow[0])

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)
    
    print('-'*100)

def station_stats(df):
    '''
    This section calculates the most popular stations (Start & End) and trip. The 
    purpose of [0] is to display the data as a single number (without the index).
    in the 'Most Frequent Combination' line, the purpose of '&' is to stylize the output.
    '''

    print('\nCalculating The Most Popular Stations and Trip...\n')
    
    common_start_station= df['Start Station'].mode()
    print('Most Common Start Station:', common_start_station[0])

    common_end_station= df['End Station'].mode()
    print('Most Common End Station:', common_end_station[0])

    most_frequent_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print ('Most Frequent Combination of Start and End Station Trip: ', '"', most_frequent_combination[0],'"', '&','"', most_frequent_combination[1],'"')
    
    print('-'*100)

def trip_duration_stats(df):
    '''
    This section calculates the total travel time and mean travel time. The first one
    is calculated as hours, and the second one is calculated as minutes.
    '''

    print('\nCalculating Trip Duration...\n')

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', int(total_travel_time/3600), ' hours')

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', int(mean_travel_time/60), ' minutes')

    print('-'*100)

def user_stats(df):
    
    '''
    This section calculates the number of users by type (Subscriber, Customer or Dependent),
    and by gender (Male or Female). It also returns the earliest, most recent and most common
    birth year, converting them into integers. Gender and birth year sections incorporate 
    exceptions, since the Washington csv file doesn't have gender and birth year columns.
    '''

    print('\nCalculating User Stats...\n')

    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)
    
    while True:
        try:
            counts_gender = df['Gender'].value_counts()
            print('Counts of Gender:\n', counts_gender)
            break
        except KeyError:
            break
    while True:
        try:
            birth_year = df['Birth Year']
            print('Earliest year of birth: ', int(birth_year.min()))
            print('Most recent year of birth: ', int(birth_year.max()))
            print('Most common year of birth: ', int(birth_year.mode()))
            break
        except KeyError:
            break

    print('-'*100)

def data_view(df):
    '''
    This section interacts with the user, by asking if they would like to view 5 or 
    more rows of individual trip data.
    '''
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Please enter yes or no: \n')
    view_data = view_data.lower()
    start_loc = 0
    valid_stat = False
    if view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        while not valid_stat:
            view_display = input("Would you like to view the next 5 rows? Please enter yes or no: ")
            view_display = view_display.lower()
            if view_display == 'yes':
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
            else:
                valid_stat = True     

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_view(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()