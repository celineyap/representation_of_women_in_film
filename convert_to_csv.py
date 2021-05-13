import requests
import csv
import time

bechdel_headers = ['imdbid','id','title','rating','year']
imdbws_headers = ['tconst','titleType','primaryTitle','originalTitle','isAdult','startYear','endYear','runtimeMinutes','genres']
tmdb_headers = ['original_title', 'popularity', 'release_date', 'vote_count', 'vote_average', 'revenue', 'status', 'production_companies_name', 'budget'] 
tmdb_ep_headers = ['executive_producer_name', 'executive_producer_gender', 'executive_producer_popularity', 'executive_producer_department', 'executive_producer_job'] 
tmdb_director_headers = ['director_name', 'director_gender', 'director_popularity', 'director_department', 'director_job'] 
tmdb_casting_headers = ['casting_name', 'casting_gender', 'casting_popularity', 'casting_department', 'casting_job'] 
tmdb_sp_headers = ['screen_play_name', 'screen_play_gender', 'screen_play_popularity', 'screen_play_department', 'screen_play_job'] 

all_headers = bechdel_headers + imdbws_headers + tmdb_headers + tmdb_ep_headers + tmdb_director_headers + tmdb_casting_headers + tmdb_sp_headers

title_basis = open("title.basics.tsv")

# extract title.basics.tsv and add them into all_data_set
imdbws={}
tsv_reader = csv.reader(title_basis, delimiter="\t")
header=next(tsv_reader, None)
for row in tsv_reader:
    row_data = {}
    for idx in range(len(header)):
        if idx >= len(row):
            continue
        row_data[header[idx]] = row[idx]
    key =row_data['tconst']
    imdbws[row_data['tconst']] = row_data

print('title.basics.tsv loaded')
idx = 1

with open('./all_movie.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',') 
    writer.writerow(all_headers)
    # extract bechdeltest and add them into all_data_set
    bechdeltest = requests.get('http://bechdeltest.com/api/v1/getAllMovies')
    for bechdel_row in bechdeltest.json():

        imdb_id = 'tt'+bechdel_row['imdbid']
        tmdb_raw = requests.get('https://api.themoviedb.org/3/find/' + imdb_id + '?api_key=a346dee1a428bd5053fcffa998c1ab32&language=en-US&external_source=imdb_id').json()

        if len(tmdb_raw['movie_results']) > 0 and 'id' in tmdb_raw['movie_results'][0]:
            tmdb_movie_raw = requests.get('https://api.themoviedb.org/3/movie/' + str(tmdb_raw['movie_results'][0]['id']) + '?api_key=a346dee1a428bd5053fcffa998c1ab32&language=en-US').json()
            if 'production_companies' in tmdb_movie_raw and len(tmdb_movie_raw['production_companies']) > 0 and 'name' in tmdb_movie_raw['production_companies'][0]:
                tmdb_movie_raw['production_companies_name'] = tmdb_movie_raw['production_companies'][0]['name']

            tmdb_credits_raw = requests.get('https://api.themoviedb.org/3/movie/' + str(tmdb_raw['movie_results'][0]['id']) + '/credits?api_key=a346dee1a428bd5053fcffa998c1ab32&language=en-US').json() 
            if tmdb_credits_raw is not None:
                for crew in tmdb_credits_raw['crew']:
                    if crew['job'] == 'Executive Producer':
                        bechdel_row['executive_producer_name'] = crew['name'] if crew['name'] is not None else ''
                        bechdel_row['executive_producer_gender'] = crew['gender'] if crew['gender'] is not None else ''
                        bechdel_row['executive_producer_popularity'] = crew['popularity'] if crew['popularity'] is not None else ''
                        bechdel_row['executive_producer_department'] = crew['department'] if crew['department'] is not None else ''
                        bechdel_row['executive_producer_job'] = crew['job'] if crew['job'] is not None else ''
                    if crew['job'] == 'Casting':
                        bechdel_row['casting_name'] = crew['name'] if crew['name'] is not None else ''
                        bechdel_row['casting_gender'] = crew['gender'] if crew['gender'] is not None else ''
                        bechdel_row['casting_popularity'] = crew['popularity'] if crew['popularity'] is not None else ''
                        bechdel_row['casting_department'] = crew['department'] if crew['department'] is not None else ''
                        bechdel_row['casting_job'] = crew['job'] if crew['job'] is not None else ''
                    if crew['job'] == 'Director':
                        bechdel_row['director_name'] = crew['name'] if crew['name'] is not None else ''
                        bechdel_row['director_gender'] = crew['gender'] if crew['gender'] is not None else ''
                        bechdel_row['director_popularity'] = crew['popularity'] if crew['popularity'] is not None else ''
                        bechdel_row['director_department'] = crew['department'] if crew['department'] is not None else ''
                        bechdel_row['director_job'] = crew['job'] if crew['job'] is not None else ''
                    if crew['job'] == 'Screenplay':
                        bechdel_row['screen_play_name'] = crew['name'] if crew['name'] is not None else ''
                        bechdel_row['screen_play_gender'] = crew['gender'] if crew['gender'] is not None else ''
                        bechdel_row['screen_play_popularity'] = crew['popularity'] if crew['popularity'] is not None else ''
                        bechdel_row['screen_play_department'] = crew['department'] if crew['department'] is not None else ''
                        bechdel_row['screen_play_job'] = crew['job'] if crew['job'] is not None else ''


        else:
            tmdb_movie_raw = None

        if imdb_id in imdbws:
            imdbws_row = imdbws[imdb_id]
        else:
            imdbws_row={}
            for h in imdbws_headers:
                imdbws_row[h]=None

        # flattening tmdb rows
        tmdb_row = {}
        if len(tmdb_raw['movie_results']) > 0:
            tmdb_row.update(tmdb_raw['movie_results'][0])
        if len(tmdb_raw['person_results']) > 0:
            tmdb_row.update(tmdb_raw['person_results'][0])
        if len(tmdb_raw['tv_results']) > 0:
            tmdb_row.update(tmdb_raw['tv_results'][0])
        if len(tmdb_raw['tv_episode_results']) > 0:
            tmdb_row.update(tmdb_raw['tv_episode_results'][0])
        if len(tmdb_raw['tv_season_results']) > 0:
            tmdb_row.update(tmdb_raw['tv_season_results'][0])
        if tmdb_movie_raw is not None:
            tmdb_row.update(tmdb_movie_raw)
        
        print ('data for imdb id: ' + imdb_id)
        print ('bechdel')
        print (bechdel_row)
        print ('tmdb')
        print (tmdb_row)
        print ('imdbws')
        print (imdbws_row)

#['imdbid','bechdel_id','bechdel_title','bechdel_rating','bechdel_year', 'imdbws_genre', 'tmdb_original_title', 'tmdb_popularity', 'tmdb_release_date', 'tmdb_vote_count', 'tmdb_vote_average', 'imdbws_runtimeMinutes']
        row_data=[]
        for header in bechdel_headers:
            if header in bechdel_row:
                row_data.append(bechdel_row[header])
            else:
                row_data.append(None)

        for header in imdbws_headers:
            if header in imdbws_row:
                row_data.append(imdbws_row[header])
            else:
                row_data.append(None)

        for header in tmdb_headers:
            if header in tmdb_row:
                row_data.append(tmdb_row[header])
            else:
                row_data.append(None)

# tmdb_ep_headers + tmdb_director_headers + tmdb_casting_headers + tmdb_sp_headers
        for header in tmdb_ep_headers:
            if header in bechdel_row:
                row_data.append(bechdel_row[header])
            else:
                row_data.append(None)
        for header in tmdb_director_headers:
            if header in bechdel_row:
                row_data.append(bechdel_row[header])
            else:
                row_data.append(None)
        for header in tmdb_casting_headers:
            if header in bechdel_row:
                row_data.append(bechdel_row[header])
            else:
                row_data.append(None)
        for header in tmdb_sp_headers:
            if header in bechdel_row:
                row_data.append(bechdel_row[header])
            else:
                row_data.append(None)

        print('writing row: ' + str(row_data) + ' ' + str(len(row_data)))
        print ('===================')
        writer.writerow(row_data)

        #row_data = [imdb_id, bechdel_row['id'], bechdel_row['title'], bechdel_row['rating'], bechdel_row['year'], imdbws_row['genres'], tmdb_row['movie_results']['original_title'], tmdb_row['movie_results']['popularity'], tmdb_row['movie_results']['release_date'], tmdb_row['movie_results']['vote_count'], tmdb_row['movie_results']['vote_average'], imdbws_row['runtimeMinutes']]
        #print(row_data)

        # wait 1 second every call to avoid getting banned
        time.sleep(1)

'''




    for id in all_data_set.keys():

        print('imdb id : ' + id)

        # use writer.writerow() to write data to csv
        #writer.writerow()
        row_data = []
        row_data.append(id)
        if 'tmdb' in all_data_set[id]:
            print('tmdb data: ' + str(all_data_set[id]['tmdb']))
            row_data.append(str(all_data_set[id]['tmdb']))
        else:
            row_data.append('')

        if 'bechdeltest' in all_data_set[id]:
            print('bechdeltest data: ' + str(all_data_set[id]['bechdeltest']))
            row_data.append(str(all_data_set[id]['bechdeltest']))
        else:
            row_data.append('')

        if 'imdbws' in all_data_set[id]:
            print('imdbws data: ' + str(all_data_set[id]['imdbws']))
            row_data.append(str(all_data_set[id]['imdbws']))
        else:
            row_data.append('')

        # write row
        writer.writerow(row_data)
'''