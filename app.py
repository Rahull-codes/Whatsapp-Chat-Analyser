import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

from helper import most_common_words

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df =preprocessor.preprocess(data)

    # st.title("Overall Chat")
    # st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0 , "Overall")

    selected_user = st.sidebar.selectbox("show analysis wrt" , user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages , words ,media_count , num_links = helper.fetch_stats(selected_user , df)
        st.title('Top Statistics')
        col1 , col2 , col3 , col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.title(num_messages)
        with col2:
            st.subheader("Total no. of Words")
            st.title(words)
        with col3:
            st.subheader("Total Media files")
            st.title(media_count)
        with col4:
            st.subheader("Total no. of Links")
            st.title(num_links)

        # timeline
        st.title('Message Activity Over Time')
        st.subheader("Monthly timeline")
        col1, col2 = st.columns([4 , 1])
        with col1:
            timeline = helper.monthly_timeline(selected_user, df)
            fig , ax = plt.subplots(figsize=(10, 5))
            ax.plot(timeline['time'], timeline['message'], marker='o', linestyle='-', color='g', linewidth=2, markersize=6)
            plt.xticks(rotation=90)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.xlabel("TimeLine", fontsize=12)
            plt.ylabel("Message Count", fontsize=12)
            st.pyplot(fig)
        with col2:
            print()

        # daily timeline
        st.subheader("Daily timeline")
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='orange')
            plt.xticks(rotation=90)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.xlabel("TimeLine", fontsize=12)
            plt.ylabel("Message Count", fontsize=12)
            st.pyplot(fig)
        with col2:
            print()

        # activity map
        st.title("Activity Map")
        col1 , col2  = st.columns(2)

        with col1:
            st.subheader("Most busy day")
            busy_day = helper.week_activity_map(selected_user , df)
            fig , ax =plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='skyblue', edgecolor='black')
            ax.set_xlabel("Day of the Week", fontsize=12)
            ax.set_ylabel("Message Count", fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            st.pyplot(fig)

        with col2:
            st.subheader("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='seagreen', edgecolor='black')
            ax.set_xlabel("Month", fontsize=12)
            ax.set_ylabel("Message Count", fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            st.pyplot(fig)


        st.title("Weekly Activity map")
        col1, col2 = st.columns([.7 , .3])
        with col1:
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig , ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

        # finding the busiest users in the Group
        if selected_user == 'Overall':

            st.title("Most Active user")
            x , new_df = helper.most_busy_users(df)
            fig , ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                ax.set_title("Most Active Users", fontsize=14, fontweight="bold", color="darkblue")
                ax.set_xlabel("Users", fontsize=12)
                ax.set_ylabel("Number of Messages", fontsize=12)
                ax.grid(axis="x", linestyle="--", alpha=0.7)
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                new_df.index = new_df.index + 1
                st.dataframe(new_df, height=480)

        # WordCloud
        st.title("Most Common Words")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Word Cloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)

        with col2:
            st.subheader("Word Frequency")
            most_common_df = helper.most_common_words(selected_user, df)

            fig , ax= plt.subplots(figsize=(5, 5))

            # Add title & labels
            ax.set_title("Most used words", fontsize=14, fontweight="bold", color="darkblue")
            ax.set_xlabel("Number of times used", fontsize=12)
            ax.set_ylabel("Words", fontsize=12)

            ax.barh(most_common_df[0] , most_common_df[1])
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df , height=480)
        with col2:
            plt.rcParams['font.family'] = 'Segoe UI Emoji'

            fig, ax = plt.subplots(figsize=(3,3))
            ax.pie(emoji_df["Number of time used"].head(),
                   labels=emoji_df["Emojis"].head(),
                   autopct=lambda p: f'{p:.2f}%',
                   textprops={'fontsize': 8}
                   )

            st.pyplot(fig)





