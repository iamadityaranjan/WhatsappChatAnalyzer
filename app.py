import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import random
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    
    st.title("🔍 Your Messages:")
    st.dataframe(df)
    
    # unique Users
    users_list = list(df['user'].unique())
    users_list.remove('Group_Notification')  # Removing group_notification from list
    users_list.sort() # sorting the list in ascending form
    users_list.insert(0,"Overall")   # Inserting overall for overall analysis
    selected_user = st.sidebar.selectbox("Show Analysis WRT:",users_list)
    
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media,links = helper.fetch_stats(selected_user,df)
        
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages:")
            st.subheader(num_messages)
            
        with col2:
            st.header("Total Words:")
            st.subheader(words)
            
        with col3:
            st.header("Total Media:")
            st.subheader(num_media)
            
        with col4:
            st.header("Total Links:")
            st.subheader(links)
            
        # Finding busiest users
        if selected_user == "Overall":
            st.title("Most Busy Users:")
            x,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            
            col1,col2 = st.columns(2)
            
            with col1:
                # Generate random colors for each bar
                random_colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(x))]
                ax.bar(x.index,x.values,color=random_colors)
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)
                
            with col2:
                st.dataframe(new_df)
        
        
        # wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        #most common words
        st.title("Most Common Words:")
        most_common_df = helper.most_common_words(selected_user,df)
        st.dataframe(most_common_df)
        
        #emoji stats
        st.title("Emoji Analysis:")
        emoji_df = helper.emoji_stats(selected_user,df)
        st.dataframe(emoji_df)
        
        
        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
