import pandas as pd
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud


extract = URLExtract()


def fetch_stats(df, selected_user):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    tot_member = sorted(df['user'].unique().tolist())

    tot_msgs = df.shape[0]

    tot_words = []
    tot_links = []
    for msg in df['message']:
        tot_words.extend(msg.split())
        tot_links.extend(extract.find_urls(msg))

    tot_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    return len(tot_member), tot_msgs, len(tot_words), tot_media, len(tot_links)


def busiest_ppl(df):

    busyppl = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,
               2).reset_index().rename(columns={'index': 'name', 'user': 'percentage'})

    return busyppl, df


def wrdcld(df, selected_user):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # tmp = df[df['user'] != 'grp_notification']
    tmp = df[df['message'] != '<Media omitted>\n']

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='black')
    dfwc = wc.generate(tmp['message'].str.cat(sep=' '))

    return dfwc


def popwords(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # tmp = df[df['user'] != 'grp_notification']
    tmp = df[df['message'] != '<Media omitted>\n']

    popwords = []
    for msg in tmp['message']:
        for w in msg.lower().split():
            popwords.append(w)

    ndf = pd.DataFrame(Counter(popwords).most_common(15))

    wc = WordCloud(width=200, height=200, min_font_size=10,
                   background_color='black')
    ndfwc = wc.generate(str(ndf))

    return ndf, ndfwc


def timeline(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    mtimeline = df.groupby(['year', 'monthnum', 'month']).count()[
        'message'].reset_index()

    time = []
    for t in range(mtimeline.shape[0]):
        time.append(mtimeline['month'][t][:3] + ', ' +
                    str(mtimeline['year'][t])[2:])

    mtimeline['monyear'] = time

    dtimeline = df.groupby('_date_').count()['message'].reset_index()

    return mtimeline, dtimeline


def weeklyact(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    busyday = df['day'].value_counts()
    busymonth = df['month'].value_counts()

    return busyday, busymonth


def heatmap(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heatmap = df.pivot_table(index='day', columns='hour',
                             values='message', aggfunc='count').fillna(0)

    return heatmap
