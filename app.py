import streamlit as st
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt


import helper
import preprocessor


st.sidebar.title("WHatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    user_list = df['user'].unique().tolist()
    user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0,"overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt " ,user_list)

    if st.sidebar.button("Show Analysis"):
        num_message, words , num_Media_msg, num_links= helper.fetch_user(selected_user,df)

        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_Media_msg)
        with col4:
            st.header("Total Links Sent")
            st.title(num_links)

        if selected_user == 'overall':
            st.title('Most Busy Users')
            x  ,new_df = helper.most_busy_users(df)
            fig ,ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig ,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

# most common words

        most_common_df = helper.most_used_words(selected_user,df)
        fig , ax=plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1] , color ='orange')
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

# emoji analysis

        emoji_df = helper.emoji_analysis(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2  = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig ,ax = plt.subplots()
            ax.pie(emoji_df[1], labels = emoji_df[0],autopct = "%0.2f")
            st.pyplot(fig)

# timeline analysis
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig ,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'] , color = 'cyan')

        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig ,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'] , color = 'brown')

        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

    #activity map

        st.title("Most active days of week")
        col1,col2 = st.columns(2)

        with col1:
            busy_day = helper.daywise_activity(selected_user,df)
            fig ,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color = 'purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            busy_month = helper.month_activity(selected_user,df)
            fig ,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # weekly activity

        weekly_heatmap = helper.weekly_activity(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(weekly_heatmap)
        st.pyplot(fig)






































