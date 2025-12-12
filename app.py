import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

from imojify import imojify
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

st.markdown(
    """
    <style>
    div[data-testid="stTextArea"] textarea {
        background-color: #0f172a0d;      /* subtle dark translucent bg */
        border-radius: 10px;              /* rounded corners */
        border: 1px solid #4b5563;        /* soft border */
        font-size: 1rem;               /* slightly smaller text */
        line-height: 1.4;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

    # 1. Initialize the state if it doesn't exist
    if "show_analysis" not in st.session_state:
        st.session_state["show_analysis"] = False


    # 2. Define a function to handle the click
    def enable_analysis():
        st.session_state["show_analysis"] = True


    # 3. Use the 'on_click' parameter (This is the key fix!)
    st.sidebar.button("Show Analysis", on_click=enable_analysis)

    # 4. Check the state
    if st.session_state["show_analysis"]:

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

        # ----------------- AI SUMMARY SECTION -----------------
        # st.markdown("---")
        st.title("AI Summary of this Chat")

        if st.button("Generate AI Summary"):
            with st.spinner("Analyzing conversation..."):
                # Call the helper function
                summary_text = helper.summarize_chat_from_df(selected_user, df)

                # PRINT TO TERMINAL FOR DEBUGGING (As you requested)
                print("\n" + "=" * 50)
                print("DEBUG: AI SUMMARY OUTPUT")
                print("=" * 50)
                print(summary_text)
                print("=" * 50 + "\n")

                st.write(summary_text)

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

        # ----------------- Emoji Analysis -----------------
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df, height=480)

        with col2:
            if not emoji_df.empty:
                # Use emoji‑capable font (Windows)
                # plt.rcParams["font.family"] = "Segoe UI Emoji"

                # Smaller figure for desktop + mobile
                fig, ax = plt.subplots(figsize=(3, 3))

                # Use column names instead of numeric indices
                sizes = emoji_df["Number of time used"].head()
                emojis = emoji_df["Emojis"].head()

                # Base pie (reduced radius so it doesn't touch edges)
                wedges, texts, autotexts = ax.pie(
                    sizes,
                    labels=[""] * len(emojis),
                    autopct="%0.2f%%",
                    startangle=90,
                    radius=0.8,  # <‑ smaller pie inside the figure
                    textprops={"fontsize": 7},
                )

                # Add emoji images (or fallback to text)
                for i, (emoji_char, count) in enumerate(zip(emojis, sizes)):
                    try:
                        img_path = imojify.get_img_path(emoji_char)
                        if img_path:
                            img = plt.imread(img_path)

                            angle = wedges[i].theta1 + (wedges[i].theta2 - wedges[i].theta1) / 2
                            x = 0.85 * np.cos(np.radians(angle))  # closer to center
                            y = 0.85 * np.sin(np.radians(angle))

                            im = OffsetImage(img, zoom=0.025)  # smaller emoji icons
                            ab = AnnotationBbox(im, (x, y), frameon=False, pad=1)
                            ax.add_artist(ab)
                        else:
                            angle = wedges[i].theta1 + (wedges[i].theta2 - wedges[i].theta1) / 2
                            x = 0.9 * np.cos(np.radians(angle))
                            y = 0.9 * np.sin(np.radians(angle))
                            ax.text(x, y, emoji_char, ha="center", va="center", fontsize=14)
                    except Exception:
                        angle = wedges[i].theta1 + (wedges[i].theta2 - wedges[i].theta1) / 2
                        x = 0.9 * np.cos(np.radians(angle))
                        y = 0.9 * np.sin(np.radians(angle))
                        ax.text(x, y, emoji_char, ha="center", va="center", fontsize=14)

                ax.set_title("Most Used Emojis", fontsize=6, pad=10)
                ax.axis("equal")
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.write("No emojis found in the selected conversation.")
