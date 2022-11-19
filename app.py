import streamlit as st
import prepro
import support
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from PIL import Image

img = Image.open('whatsapp.png')
st.set_page_config(page_title='WhatsApp chat Analyzer', page_icon=img)


sns.set()

col1, col2 = st.columns(2)
with col1:
    st.sidebar.header("WhatsApp Chat Analyzer")
with col2:
    st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/479px-WhatsApp.svg.png', width=90)

st.sidebar.markdown("Instruction")
st.sidebar.caption(
    'This application lets you analyze Whatsapp conversations in a very comprehensive manner, with charts, metrics, '
    'and other forms of analysis. '
    '(scroll here)')
with st.expander('See!!.. How it works?'):
    st.subheader('Steps to Analyze:')
    st.markdown(
        '1. Export your WhatsApp chat (Steps to export: Open your WhatsApp in phone>Open Chat> Click on three dots>More>Export '
        'Chat> Without Media>Save anywhere or save on Google Drive.)')
    st.markdown('2. Browse your chat file or drag and drop(if you are using phone then click \' > \' left side, if sidebar not visible)')
    st.markdown('3. Select User: default All, means data will be analyzed for all users/groups')
    st.markdown('4. Click on Show Analysis button')
    st.markdown(
        '5. Turn on Wide mode for better viewing exprience from settings, If you are using phone then close the sidebar for better view')
    st.markdown(
        '6. If you want analyze for single user, just select the name from the dropdown and click on \'Show '
        'Analysis\' button')




uploaded_file = st.sidebar.file_uploader("Select a file to Analyze:")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    # printing file name/chat name
    a = str(uploaded_file)[44:]
    b = a.split('.txt')
    st.title('WhatsApp Chat Analysis with {}'.format(b[0]))
    # st.title()

    # View data on webpage
    # st.text(data)

    df = prepro.preprocess(data)

    # display DF on webpage
    # st.dataframe(df)

    # unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'Overall')

    if 'grp_notification' in user_list:
        user_list.remove('grp_notification')
        df = df[df['user'] != 'grp_notification']

    selected_user = st.sidebar.selectbox('Select User', user_list)

    if st.sidebar.button('Analyse'):
        # stats
        st.title('Chat Stats:')
        tot_member, tot_msgs, tot_words, tot_media, tot_links = support.fetch_stats(
            df, selected_user)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header('Total messages')
            st.header(tot_msgs)

        with col2:
            st.header('Total words')
            st.header(tot_words)

        with col3:
            st.header('Shared media')
            st.header(tot_media)

        with col4:
            st.header('Shared Links')
            st.header(tot_links)

        with col5:
            st.header('Total member')
            st.header(tot_member)

        # Timelines
        mtimeline, dtimeline = support.timeline(df, selected_user)
        busyday, busymonth = support.weeklyact(df, selected_user)

        col1, col2 = st.columns(2)

        with col1:
            st.title('Monthly Timeline:')
            fig, ax = plt.subplots()
            ax.plot(mtimeline['monyear'], mtimeline['message'], 'g-')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            fig, ax = plt.subplots()
            ax.bar(busymonth.index, busymonth.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.title('Daily Timeline:')
            fig, ax = plt.subplots()
            ax.plot(dtimeline['_date_'], dtimeline['message'], 'green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            fig, ax = plt.subplots()
            ax.bar(busyday.index, busyday.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # busiest user in group chat
        if selected_user == 'Overall' and len(df['user'].unique()) > 2:

            st.title('Chattiest Users:')

            # pie chart of user activity percentage
            user_count = df['user'].value_counts().reset_index()
            user_count.columns = ['member', 'message']
            fig = px.pie(user_count, names='member', values='message', hole=0.5)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(title_text='Users Activity in Percentage', title_x=0.5,
                              font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            st.plotly_chart(fig, use_container_width=True)

        # top user chats 5
        col1, col2, col3 = st.columns([1.5, 0.2, 1.5])
        top5 = df['user'].value_counts().sort_values(ascending=False).reset_index().iloc[0:5]
        top5.columns = ['Member', 'Message']
        with col1:
            st.markdown('Most Active Members')
            st.dataframe(top5)

        last5 = df['user'].value_counts().sort_values().reset_index().iloc[0:5]
        last5.columns = ['Member', 'Message']
        with col3:
            st.markdown('Less Active Members')
            st.dataframe(last5)

        # wordcloud
        st.title('Word Cloud:')
        dfwc = support.wrdcld(df, selected_user)
        fig, ax = plt.subplots()
        ax.imshow(dfwc)
        plt.axis('off')
        st.pyplot(fig)

        # Mostly used words
        st.title('Mostly Used Words:')

        col1, col2 = st.columns(2)

        popwords, dfwc = support.popwords(df, selected_user)
        with col1:
            fig, ax = plt.subplots()
            ax.imshow(dfwc)
            plt.axis('off')
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.barh(popwords[0], popwords[1])
            plt.gca().invert_yaxis()
            st.pyplot(fig)

        # heatmap
        st.title('Activity Heatmap:')
        heatmap = support.heatmap(df, selected_user)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap)
        st.pyplot(fig)

        df['message_chars'] = df['message'].apply(lambda z: len(z))
        longest_msg = df.sort_values(by='message_chars', ascending=False)[
            ['date', 'hour', 'minute', 'user', 'message', 'message_chars']].head(5).reset_index(drop=True)
        longest_msg['date'] = longest_msg['date'].apply(lambda x: str(x)[:10])
        longest_msg['time'] = longest_msg['hour'].apply(lambda x: str(x)) + ":" + longest_msg['minute'].apply(
            lambda x: str(x))
        st.markdown(f"Top 5 longest Message of {selected_user}")
        st.table(longest_msg[['date', 'time', 'user', 'message', 'message_chars']])

        a = df.groupby(by='date')
        top = a.size().sort_values(ascending=False).index[0]
        top5_msg = a.get_group(top).sort_values(by='message_chars', ascending=False)[
            ['date', 'user', 'message']].head(5).reset_index(drop=True)
        top5_msg['date'] = top5_msg['date'].apply(lambda x: str(x)[:10])
        st.markdown(f'5 Longest message of highest chat happened on a single day by {selected_user}')
        st.table(top5_msg)

footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;'>TYSBCIT-B-47/48</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
