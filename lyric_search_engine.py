
# coding: utf-8

# ### Get Top100 songs

# In[1]:


def get_top100_list():
    output_list = list()
    url = "https://www.billboard.com/charts/hot-100"

    import requests
    from bs4 import BeautifulSoup
    
    try:
        response = requests.get(url)   
        if not response.status_code == 200:
            print("HTTP error",response.status_code)
        else:
            try:
                soup = BeautifulSoup(response.content,'lxml')
            except:
                print('something went wrong')
    except:
        print("Something went wrong with request.get")
    
    top1_name = soup.find('div',class_='chart-number-one__title').get_text()
    top1_artist = soup.find('div',class_='chart-number-one__artist').get_text()
    output_list.append((top1_name,top1_artist))
    
    all_songs = soup.find_all('div',class_='chart-list-item__text')
    
    for song in all_songs:
        song_name = song.find('span',class_='chart-list-item__title-text').get_text()
        artist = song.find('div',class_='chart-list-item__artist').get_text()
        output_list.append((song_name,artist))
    
    return output_list


# In[2]:


def get_all_info(list_of_songs):
    import requests
    import re
    from bs4 import BeautifulSoup
    all_song_info = []
    for song in list_of_songs:
        name = song[0].strip()
        pattern = r'[^()]+'
        match = re.search(pattern,name)
        name = match.group().strip()
        artist = song[1].strip()
        search_artist = artist.lower().replace(' x ',' & ')
        if ' featuring' in search_artist:
            pattern_artist = r' featuring'
            search_artist = search_artist.lower()[:re.search(pattern_artist,search_artist.lower()).span()[0]]
        token = 'agZ_VYrkzow8Wo80yQSUpgi0V9J9szWwtLF4cY9inzE-jIoOe3xrs43F9yYB28Xg'
        base_url = 'https://api.genius.com'
        headers = {'Authorization': 'Bearer ' + token}
        search_url = base_url + '/search'
        data = {'q': name + ' ' + search_artist}
        
        try:
            response = requests.get(search_url, data=data, headers=headers)
            if not response.status_code == 200:
                print("HTTP error",response.status_code)
            else:
                try:
                    lyric_path = 'http://genius.com'+response.json()['response']['hits'][0]['result']['path']
                except:
                    print('Error while searching for the song.')
                    continue
        except:
            print("Something went wrong with request.get")
            continue

        try:
            response2 = requests.get(lyric_path)
            if not response2.status_code == 200:
                print("HTTP error",response2.status_code)
            else:
                try:
                    response2_page = BeautifulSoup(response2.content,'lxml')
                except:
                    print('Error happens while searching for lyrics.')
                    continue
        except:
            print("Something went wrong with request.get")
            continue
#         list_=response2_page.find('div',class_='lyrics').find_all('a',class_='referent')
#         lyrics = ''
#         for item in list_:
#             line = item.get_text()
#             lyrics += line + ' '
#         lyrics = lyrics.replace('\n', ' ')
#         print(lyric_path)
        try:
            lyrics = response2_page.find('div',class_='lyrics').get_text().replace('\n',' ').strip()
        except:
            continue
        all_song_info.append((name,artist,lyrics))
    return all_song_info


# ### Get albums information

# In[3]:


def album_info(artist):
    import requests
    import re
    from bs4 import BeautifulSoup
    result = dict()
    token = 'agZ_VYrkzow8Wo80yQSUpgi0V9J9szWwtLF4cY9inzE-jIoOe3xrs43F9yYB28Xg'
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + token}
    search_url = base_url + '/search'
    data = {'q':artist}
    
    try:
        response = requests.get(search_url, data=data, headers=headers)
        if not response.status_code == 200:
            print("HTTP error",response.status_code)
        else:
            try:
                url_artist = response.json()['response']['hits'][0]['result']['primary_artist']['url']
            except:
                print('Error happens. Cannot find albums information of %s.'%artist)
                return []
    except:
        print('Something went wrong with request.get')
        return []
    try:
        response2 = requests.get(url_artist)
        if not response2.status_code == 200:
            print("HTTP error",response2.status_code)
        else:
            try:
                response2_page = BeautifulSoup(response2.content,'lxml')
            except:
                print('Error happens. Cannot find albums information of %s.'%artist)
                return []
    except:
        print('Something went wrong with request.get')
        return []
    string1 = str(response2_page)
    pattern1 = r'https://genius.com/albums/[0-9A-Za-z-/]*'
    urls_album = re.findall(pattern1,string1)
    urls_album = set(urls_album)
    if len(urls_album) == 0:
        print('Cannot find albums information of %s.'%artist)
        return []
    for url_a in urls_album:
        try:
            response3 = requests.get(url_a)
            if not response3.status_code == 200:
                print("HTTP error",response3.status_code)
            else:
                try:
                    response3_page = BeautifulSoup(response3.content,'lxml')
                except:
                    print('Error happens.')
                    continue
        except:
            print("Something went wrong with request.get")
            continue
        try:
            name = response3_page.find('h1').get_text()
        except:
            print('Error happens in finding the album name.')
            name = 'unknown'
            continue
        if response3_page.find_all('div',class_='metadata_unit') != []:
            date = response3_page.find_all('div',class_='metadata_unit')[0].get_text()[9:]
        else:
            date = 'NA'
        songs = list()
        list_of_songs = response3_page.find_all('h3',class_='chart_row-content-title')
        for song in list_of_songs:
            pattern2 = r'[^\n]+'
            string2 = song.get_text().strip()
            song_name = re.search(pattern2,string2).group()
            song_name = song_name[re.search(r'[^\w]*',song_name).span()[1]:]
            songs.append(song_name.replace('\xa0',' '))
        album_info = (date,songs)
        result[name] = album_info
    return result


# ### search songs

# In[4]:


def get_song_lyrics(top100_list):  # top100_list contain (song_name,artist,lyrics)
    i=0
    song_lyrics_dict = dict()
    while i < len(top100_list):
        song_name = top100_list[i][0].strip()
        lyrics = top100_list[i][2].strip()
        song_lyrics_dict[song_name]= lyrics
        i = i+1
    return song_lyrics_dict # (song_name,lyrics)


# In[5]:


def find_song(song_lyrics_dict,search_list):  # song_lyrics_dict
    
    import re
    from nltk import word_tokenize
    
    song_name= []
    result_dict=dict()
    for key in song_lyrics_dict.keys():
        result_dict[key] = 1
    
    for sword in search_list:
        sword = sword.lower()
        for key,value in song_lyrics_dict.items():
            lyrics=value.replace(',','').lower()
            lyrics_list = word_tokenize(lyrics)
            if sword not in lyrics_list:
                result_dict[key]= 0
    
    for key, value in result_dict.items():
        if value:
            song_name.append(key)
    return song_name


# ### song recommendation(similarity analysis)

# In[6]:


def similar_song(song_name,lyric_list,lyric_dict):
    from gensim import corpora
    from gensim.parsing.preprocessing import STOPWORDS
    from gensim.similarities.docsim import Similarity
    from gensim import corpora, models, similarities

    # texts = [[word for word in doc.lower().split()
    #         if word not in STOPWORDS and word.isalnum()]
    #         for doc in reference_docs]

    all_song_info = lyric_list
    
    texts = [[word for word in song[2].lower().split()
            if word not in STOPWORDS and word.isalnum()]
            for song in all_song_info]

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=5)
    lyrics = lyric_dict[song_name]
    vec_bow = dictionary.doc2bow(lyrics.lower().split())
    vec_lsi = lsi[vec_bow]
    lsi_index = similarities.MatrixSimilarity(lsi[corpus])
    sims = lsi_index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    most_similar_song_num = sims[1][0]
    most_similar_song = all_song_info[most_similar_song_num]
    return most_similar_song


# ### sentiment analysis

# In[7]:


def get_nrc_data():
    nrc = "NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
    count=0
    emotion_dict=dict()
    with open(nrc,'r') as f:
        all_lines = list()
        for line in f:
            if count < 46:
                count+=1
                continue
            line = line.strip().split('\t')
            if int(line[2]) == 1:
                if emotion_dict.get(line[0]):
                    emotion_dict[line[0]].append(line[1])
                else:
                    emotion_dict[line[0]] = [line[1]]
    return emotion_dict


# In[8]:


def emotion_analyzer(text,emotion_dict):
    #Set up the result dictionary
    emotions = {x for y in emotion_dict.values() for x in y}  
    emotion_count = dict()  
    for emotion in emotions:
        emotion_count[emotion] = 0

    #Analyze the text and normalize by total number of words
    total_words = len(text.split())
    for word in text.split():
        if emotion_dict.get(word):  
            for emotion in emotion_dict.get(word):
                emotion_count[emotion] += 1/len(text.split())
    return emotion_count


# In[9]:


def emotion_analyzer_and_recommend(song_name,text,dict_,lyric_list,lyric_dict):
    
    for key,value in lyric_dict.items():
        if key == song_name:
            text = value 
            result = emotion_analyzer(text,dict_)
            emotions = {'fear': result['fear'], 'joy': result['joy'], 'anticipation': result['anticipation'],'sadness': result['sadness']}
            emotion = 'This is a song of '+ sorted(emotions,key=lambda x:emotions[x])[-1]
            similar =  'A similar song we recommend: ' + similar_song(song_name,lyric_list,lyric_dict)[0]
            print(emotion,'\n',similar)
    return None


# ## Song Info

# #### Find the mv or a relevent trending video

# In[10]:


def get_mv(song_name, singer):
    from bs4 import BeautifulSoup as bs
    import requests
    base = "https://www.youtube.com/results?search_query="

    try:
        response = requests.get(base+song_name+singer)
        if not response.status_code == 200:
            print("HTTP error",response.status_code)
        else:
            page = response.text
            soup = bs(page,'html.parser')
    except:
        print('Cannot parse using BeautifulSoup.')
        return None
    vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
    if len(vids) != 0:
        mv = vids[0]
        if 'http' in mv['href']:
            mv = vids[1]
        mv_link = 'https://www.youtube.com' + mv['href']

    else:
        mv_link = 'NO MV FOUND'
        print(my_link)
    if mv_link != 'NO MV FOUND':
        while True:
            whether = str(input('Do you want to watch its MV or the trending relevent video on Youtube right now? [y/n] '))
            if whether.lower() == 'y' or whether.lower() == 'n':
                break
            else:
                print('Wrong input! Try again.')
        if whether.lower() == 'y':
            import webbrowser
            webbrowser.open(mv_link, new=0, autoraise=True)
        else:
            print()
            print('Here is the link to the mv for you to enjoy later: ' + mv_link)
            print()
    return None

    


# #### Concert info

# In[11]:


def get_concert(singer,city = None):
    try:
        import requests
        from bs4 import BeautifulSoup as bs 
        base = "https://www.songkick.com/search?utf8=✓&type=initial&query="
        qstring = singer
        try:
            r = requests.get(base+qstring)
            if not r.status_code == 200:
                print("HTTP error",r.status_code)
            else:
                page = r.text
                soup = bs(page,'lxml')
        except:
            print('Cannot parse using BeautifulSoup.')
            return None
        vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
        events = soup.findAll('li',attrs={'class':'artist'})
        artist = events[0].findAll('a')[1]
        artist_link = "https://www.songkick.com" + artist['href']
        r = requests.get(artist_link)
        page = r.text
        soup=bs(page,'lxml')
        tour = soup.findAll('li',attrs={'class':'ontour'})
        on_tour = tour[0].get_text()
        if on_tour[-2:] == 'no':
            print('Sorry, %s is not on tour.' % singer)
            return None
        else:
            upcoming = soup.findAll('p', class_ = 'see-all')
            upcoming_link = "https://www.songkick.com" + upcoming[0].find('a')['href']
        try:
            r = requests.get(upcoming_link)
            if not r.status_code == 200:
                print("HTTP error",r.status_code)
            else:
                page = r.text
                soup = bs(page,'html.parser')
        except:
            print('Cannot parse using BeautifulSoup.')
            return None
        events = soup.find('ul',class_="event-listings artist-focus")
        concert_list = list()
        concert_list = get_venue_and_time(events)
        if len(concert_list) == 0:
            print('Sorry, %s is not on tour.' % singer)
            return None
        print()
        whether = str(input('Do you want to see info for all concerts? [y/n] '))
        if whether.lower() == 'y':
            print()
            for concert in concert_list:
                print(concert[:(concert.find('; Link to ticket'))])
            print()
        if city is None:
            return None
        print()
        whether_city = str(input('Do you want to check if a concert will be held in the city you want? [y/n] '))
        if whether_city.lower() == 'y':
            found = check_city(city, concert_list)
            if found is not None:
                print()
                whether_ticket = str(input('Do you want to buy the tickets? [y/n] '))
            if whether_ticket and whether_ticket.lower() == 'y':
                try:
                    ticket_link(found,singer)
                except:
                    pass
        return None
    except:
        print('No concert info available on songkick.com.')
        print()
        return None
    


# In[12]:


def get_venue_and_time(events):
    concert_list = list()
    results = events.find_all('li')
    for i in range(len(results)):
        if results[i].attrs.get('class') == ['with-date']:
            when = results[i].get_text().replace('\n','')
            locations = results[i+1].find('p',class_ = 'location')
            try:
                ticket = 'https://www.songkick.com' + results[i+1].find('span',class_="button buy-tickets").parent.get('href')
            except:
                ticket = 'Sorry, ticket is not on sale yet.'
            venue = locations.find_all('span')[0]
            city = locations.find_all('span')[1]
            where = " ".join(venue.get_text().replace('\n','').split()) + ', '+ " ".join(city.get_text().replace('\n','').split())
            concert_list.append('Time: %s; Location: %s; Link to ticket: %s' % (when, where, ticket))
    return concert_list


# In[13]:


def check_city(city, list_):
    import re
    found = list()
    for i in range(len(list_)):
        if city.lower() in list_[i].lower():
            found.append(list_[i])
    if len(found) > 0:
        print()
        print('Great new, concerts will be held in the city you want!')
        print()
        for concert in found:
            print(concert[:(concert.find('; Link to ticket'))])
        print()
        return found
    else:
        print()
        print('Sorry, no concert will be held in the city you want. Stay tuned!')
        print()
        return None
            
            
    


# In[14]:


def ticket_link(found_list,singer):
    ticket_list = list()
    contains_http = False
    for concert in found_list:
        info = concert[:(concert.find('; Link to ticket'))]
        ticket = concert[(concert.find('; Link to ticket'))+1:]
        if 'http' in ticket:
            contains_http = True
        print()
        print(info)
        print()
        print(ticket)
        print()
        ticket_list.append((info,ticket))
        
    if contains_http == True:
        done = False
        while True:
            selection = input('Do you want me to send you a reminder email? [y/n] ')
            if selection.lower() == 'y' or selection.lower() == 'n':
                break
            else:
                print('Wrong input! Try again.')
        if selection.lower() == 'y':
            account = str(input("Please enter your email account as a string(e.g. 'instance@example.com'): "))
        elif selection.lower() == 'n':
            print()
            print('See ya!')
            print()
        else:
            print('Wrong input!')
            print()
    if account:
        try:
            import smtplib 
  
            fromMy = 'antonio_ye@yahoo.com' 
            to  = str(account)
            subj='Gotta buy those tickets!'
            date='11/29/2018'
            for info in ticket_list:
                text = info[0] + '\n' + info[1] + '\n\n'
            message_text='Here is the ticket info for the concerts of %s in your city:\n\n' % str(singer) + text + 'Your Tools for Analytics Students'

            msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )
            username = str('antonio_ye@yahoo.com')  
            password = str('NRBDkTqMPvN4Aqg') 

            server = smtplib.SMTP("smtp.mail.yahoo.com",587)
            server.ehlo() 
            server.starttls()
            server.login(username,password)
            server.sendmail(fromMy, to,msg)
            server.quit()    
            print('Sent! Enjoy the show. Note that the email may take several minutes to arrive...')
            print()
        except:
            print('Oops! An error occurred.')
            print()
            
    return None


# ## main functions

# #### name seperater (if multiple singers)

# In[15]:


def seperate_name(singer):
    singer = singer.replace(' x ',' & ').replace(' X ',' & ').replace(' Featuring ',' & ').replace(', ',' & ')
    singer = singer.split(' & ')
    if len(singer) == 1:
        return singer[0]
    else:
        for i in range(len(singer)):
            print('%s.%s' % (str(i+1),singer[i]))
        print()
        which_singer = int(input('More than one singer in this song! Please select who you want to know about: '))
        singer = singer[which_singer-1]
        return singer
        

        


# #### song search main function

# In[16]:


def find_song_based_on_search(list_of_songs,songs_with_lyrics,song_lyrics_dict,search_string=None,first_time=None):
    if not first_time:
        search_string = str(input('Please enter a lyric string: '))
        print('Searching, please be patient...')
        print()
    song_name = find_song(song_lyrics_dict,search_string.split())
    
    if len(song_name) == 1:
        the_one_name = song_name[0]
        print(the_one_name)
        for trio in songs_with_lyrics:
            if trio[0] == the_one_name:
                corresponding_artist = trio[1]
                lyric = trio[2]
                return the_one_name,corresponding_artist,lyric
    if len(song_name) > 1:
        for i in range(len(song_name)):
            print('%s.%s' % (str(i+1),song_name[i]))
        print()
        which_song = int(input('More than one song found! Hear them out and select which one you like the most (enter its number): '))
        the_one_name = song_name[which_song-1]
        for trio in songs_with_lyrics:
            if trio[0] == the_one_name:
                corresponding_artist = trio[1]
                lyric = trio[2]
                return the_one_name,corresponding_artist,lyric
    elif len(song_name) == 0:
        print('Sorry, based on our search, your search does not match any records of the recent trending songs...')
        print()
        return None,None,None


# #### main menu

# In[17]:


def get_info_main_menu(song,name,lyric,lyric_list,lyric_dict):
    done = False
    while done is not True:
        print('--------------------------------------------')
        print('1.Watch its MV or a trending relevent video')
        print('2.Check concert info')
        print('3.See albums of this singer')
        print('4.Find a similar song')
        print('5.Quit')
        print()
        selection = str(input('Please make a choice: ')).replace('.','')
        if selection == '1':
            get_mv(song, name)
            while True:
                main_menu = str(input('Would you like to go back to main menu? [y/n] '))
                if main_menu.lower() == 'y' or main_menu.lower() == 'n':
                    break
                else:
                    print('Wrong input! Try again.')
            if main_menu.lower() == 'n':
                done = True
        elif selection == '2':
            singer = seperate_name(name)
            whether_city = str(input('Do you want to find out about a specific city? [y/n] '))
            if whether_city == 'y':
                city_name = str(input('Please enter a city name: '))
                get_concert(singer,city = city_name)
            else:
                get_concert(singer,city = None)
            while True:
                main_menu = str(input('Would you like to go back to main menu? [y/n] '))
                if main_menu.lower() == 'y' or main_menu.lower() == 'n':
                    break
                else:
                    print('Wrong input! Try again.')
            if main_menu.lower() == 'n':
                done = True
        elif selection == '3':
            singer = seperate_name(name)
            albums = album_info(singer) 
            if len(albums) > 0:
                print()
                print('Previous album(s) of this singer (album name : release date, [songs in this album]): ')
                print(albums)
                print()
            else:
                print('Somehow this singer does not have any album...')
                print()
            while True:
                main_menu = str(input('Would you like to go back to main menu? [y/n] '))
                if main_menu.lower() == 'y' or main_menu.lower() == 'n':
                    break
                else:
                    print('Wrong input! Try again.')
            if main_menu.lower() == 'n':
                done = True
        elif selection == '4':
            emotion_dict = get_nrc_data()
            emotion_analyzer_and_recommend(song,lyric,emotion_dict,lyric_list,lyric_dict)
            while True:
                main_menu = str(input('Would you like to go back to main menu? [y/n] '))
                if main_menu.lower() == 'y' or main_menu.lower() == 'n':
                    break
                else:
                    print('Wrong input! Try again.')
            if main_menu.lower() == 'n':
                done = True
        elif selection == '5':
            done = True
        else:
            print('Wrong number. Try again.')
            print()
    print()   
    return None


# #### run them all

# In[18]:


def run_all():
    # for the first time searching
    while True:
        try:
            search_string = str(input('Please enter a lyric string: '))
            print('Searching for the first time. May take around 1 minute, please be patient...')
            print()
            list_of_songs = get_top100_list()
            songs_with_lyrics = get_all_info(list_of_songs)
            song_lyrics_dict = get_song_lyrics(songs_with_lyrics)
            song, singer, lyric = find_song_based_on_search(list_of_songs, songs_with_lyrics, song_lyrics_dict,
                                                            search_string, first_time=True)
            if song:
                get_info_main_menu(song, singer, lyric, songs_with_lyrics, song_lyrics_dict)
            while True:
                answer = str(input('Do you want to search for another lyric string? [y/n] '))
                if answer.lower() == 'y' or answer.lower() == 'n':
                    break
                else:
                    print('Wrong input! Try again.')
                    print()
            if answer == 'n':
                print()
                print('Bye-bye.')
                print()
                return None
            break
        except:
            print('Please try again.')
            print()

    # for searching after the first
    while True:
        try:
            while True:
                song, singer, lyric = find_song_based_on_search(list_of_songs, songs_with_lyrics, song_lyrics_dict)
                if song:
                    get_info_main_menu(song, singer, lyric, songs_with_lyrics, song_lyrics_dict)
                while True:
                    answer = str(input('Do you want to search for another lyric string? [y/n] '))
                    if answer.lower() == 'y' or answer.lower() == 'n':
                        break
                    else:
                        print('Wrong input! Try again.')
                        print()
                if answer == 'n':
                    print()
                    print('Bye-bye.')
                    print()
                    return None
        except:
            print('Please try again.')
            print()
    return None


# In[19]:


run_all()

