from streamlit import columns
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import emoji

extract = URLExtract()

def fetch_stats(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. fetch number od messages
    num_messages =  df.shape[0]

    # 2. number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # 3. Number of media count
    media_count = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4. numbers of link
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages , len(words) , media_count , len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()

    df = df['user'].value_counts(normalize=True).mul(100).round(2).reset_index()
    df.columns = ['name', 'percentage%']

    return x , df

def create_wordcloud(selected_user , df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].isin(["<Media omitted>\n", "This message was deleted\n" ])]

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user , df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].isin(["<Media omitted>\n", "This message was deleted\n" ])]

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df =  pd.DataFrame(Counter(words).most_common(20))


    return most_common_df

def emoji_helper(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.columns = ["Emojis" ,"Number of time used" ]
    emoji_df.index = emoji_df.index+1
    return emoji_df

def monthly_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', "month"]).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    dailyy_timeline = df.groupby('only_date').count()['message'].reset_index()

    return dailyy_timeline

def week_activity_map(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index = 'Day_name', columns='Period' , values = 'message' , aggfunc = 'count').fillna(0)

    return user_heatmap