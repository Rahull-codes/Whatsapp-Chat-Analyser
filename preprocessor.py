import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm)?\s-\s'

    messages = re.split(pattern, data)[1:]

    cleaned_dates = re.findall(pattern, data)
    dates = [re.sub(r'\s?[ap]m\s?-\s$', '', date.replace('\u202f', '')) for date in cleaned_dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        # Updated regex to capture full names and numbers
        # entry = re.split(r'(^[\w\s+\d-]+):\s', message)

        entry = re.split(r'(^[\w\s+\d\U0001F300-\U0001F6FF\U0001F900-\U0001F9FF\U0001F1E6-\U0001F1FF-]+):\s', message)

        if len(entry) > 2:  # If there's a user (name or number)
            users.append(entry[1].strip())  # Store full name or number
            messages.append(entry[2])  # Store message
        else:  # For group notifications
            users.append("group_notification")
            messages.append(entry[0])  # Store notification text

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 12:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df