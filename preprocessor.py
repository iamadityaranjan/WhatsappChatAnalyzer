import re
import pandas as pd

def preprocess(data):
    regex_pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}[  ]?\w+\s-\s'
    all_messages = re.split(regex_pattern, data)[1:]
    all_dates = re.findall(regex_pattern, data)
    all_dates = [dt.replace('\u202f', '').rstrip(' -') for dt in all_dates]
    
    df = pd.DataFrame({'User_message':all_messages,'message_date':all_dates})

    #converting 'message_date' type 
    df['message_date'] = pd.to_datetime(df['message_date'],format='%d/%m/%y, %I:%M%p')
    df.rename(columns={'message_date':'date'},inplace=True)
    
    # Separating users and messages
    users = []
    messages = []

    for message in df['User_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:  # means user_name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group_Notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns = ['User_message'],inplace= True)
    
    df['year'] = df['date'].dt.year   # for year
    df['month_num'] = df['date'].dt.month # for month no 
    df['month'] = df['date'].dt.month_name()  # for month
    df['day'] = df['date'].dt.day  # for date
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour  # for hour
    df['minutes'] = df['date'].dt.minute  # for minutes
    
    # Add period column for heatmap
    periods = []
    for hour in df['hour']:
        if hour == 23:
            periods.append(f"{hour}-0")
        else:
            periods.append(f"{hour}-{hour+1}")
    df['period'] = periods

    return df