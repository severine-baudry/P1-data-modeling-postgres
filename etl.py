import os
import glob
import psycopg2
import pandas as pd
import getpass
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process the .json song file <filepath> using postgresql cursor <cur>.
    If relevant, add entries into the song table and artist table.
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    selected_song_info = df[["song_id", "title", "artist_id", "year", "duration"] ]
    for song in selected_song_info.itertuples(index = False):
        song_data = song._asdict()
        cur.execute(song_table_insert, song_data)
    
    # insert artist record
    selected_artist_info = df[["artist_id", "artist_name", "artist_location", "artist_longitude", "artist_latitude"] ]
    for artist in selected_artist_info.itertuples(index = False):
        artist_data = artist._asdict()
        cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Process the .json log file <filepath>
    If relevant, add entries to the time table, user table, and songplay table
    """
    # open log file
    df = pd.read_json(filepath, lines = True)
    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = df["ts"].apply(lambda x : pd.Timestamp(x/1000, unit = "s"))
    
    # insert time data records
    time_df = pd.DataFrame()
    time_df["timestamp"] = df["ts"]
    time_df["year"]= t.dt.year
    time_df["month"]= t.dt.month
    time_df["day"]= t.dt.day
    time_df["dayofweek"] = t.dt.dayofweek
    time_df["weekofyear"] = t.dt.weekofyear
    time_df["hour"] = t.dt.hour
    time_df["minute"] = t.dt.minute
    time_df["second"] = t.dt.second

    for row in time_df.itertuples(index = False):
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for row in user_df.itertuples(index = False):
       drow = row._asdict()
       cur.execute(user_table_insert, drow)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        #print(row.song, row.artist, row.length)
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        #print(songid, artistid)
        # insert songplay record
        if songid and artistid :
            # songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
            songplay_data = {
            'start_time' : row.ts, 
             'user_id' : row.userId,
             'level' : row.level, 
             'song_id' : songid, 
             'artist_id' : artistid, 
             'session_id' : row.sessionId, 
             'location' : row.location, 
             'useragent' : row.userAgent
            }
            print(filepath)
            print(songplay_data)
            print(len(songplay_data))
            cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Find every .json file in directory <filepath>
    Apply function <func> with sql connection <conn> on each found .json file.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    udacity_credential = "host=127.0.0.1 dbname=sparkifydb user=student password=student"
    conn = psycopg2.connect( udacity_credential)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()