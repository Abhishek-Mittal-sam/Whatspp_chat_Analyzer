import re
import pandas as pd

def preprocess(data):
    pattern = "\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2} [ap]m - "
    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)
    dates = [i.replace("\u202f", " ") for i in dates]  # create a new list with the replaced strings

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M %p - ")

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notifications')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df['month'] = df['message_date'].dt.month_name()
    df['month_num'] = df['message_date'].dt.month
    df['day'] = df['message_date'].dt.day
    df['year'] = df['message_date'].dt.year
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    df['only_date'] = df['message_date'].dt.date
    df['day_name'] = df['message_date'].dt.day_name()

    period = []
    for hour in df[['day_name','hour' ]]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" +str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period'] = period


    df.drop(columns = ['user_message','message_date'] ,inplace= True)

    return df




