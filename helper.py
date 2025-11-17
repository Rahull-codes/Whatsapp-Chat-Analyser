from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import emoji
import  os
import streamlit as st
import traceback

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

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
    temp = df[df['user'] != 'group_notification']  # Remove group notifications

    # Remove both "<Media omitted>" and "This message was deleted"
    temp = temp[~temp['message'].isin(["<Media omitted>\n", "This message was deleted\n"])]

    x = temp['user'].value_counts().head()

    df = temp['user'].value_counts(normalize=True).mul(100).round(2).reset_index()


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

    user_heatmap = df.pivot_table(index = 'day_name', columns='period' , values = 'message' , aggfunc = 'count').fillna(0)

    return user_heatmap

def summarize_chat_from_df(selected_user,df ):

    # Filter based on selected user (for 'Overall' use entire df)
    if selected_user != "Overall":
        df_to_use = df[df["user"] == selected_user]
    else:
        df_to_use = df

    # If no messages, avoid empty prompt
    if df_to_use.empty:
        return "No messages available to summarize."

    # Join messages into one long text (limit to last N to keep prompt small)
    messages = df_to_use["message"].astype(str).tolist()
    MAX_MSG = 500   # you can tune this
    chat_text = "\n".join(messages[-MAX_MSG:])

    user_prompt = (
        "You are analyzing a WhatsApp chat export.\n\n"
        "Task: In ONE short paragraph, summarize this chat.\n"
        "- Say if it looks like a group chat or personal chat.\n"
        "- Describe who is talking (for example: college students, friends, family).\n"
        "- Mention the main topics (for example: CT exam, classes, projects, casual talk).\n"
        "- Mention the overall mood (for example: serious, casual, fun).\n\n"
        "Do not list individual messages or names, just high‑level summary.\n\n"
        "Chat messages:\n"
        f"{chat_text}"
    )

    try:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",  # or the model you actually use
            messages=[
                {
                    "role": "system",
                    "content": "You summarize WhatsApp chats for an analytics dashboard."
                },
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=200,
        )
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        # Show error in the app instead of blank page
        st.error(f"Error while generating summary: {e}")
        # Log full traceback in terminal for debugging
        traceback.print_exc()
        return "Could not generate summary due to an error."


