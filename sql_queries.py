# DROP TABLES

def drop_table_query(table):
    """ drop table <table> if it exists
    """
    return "DROP TABLE IF EXISTS " + table + ";" 

#songplay_table_drop = "DROP TABLE IF EXIST songplay_table;"
songplay_table_drop = drop_table_query('songplays')
user_table_drop =  drop_table_query('users')
song_table_drop =  drop_table_query('songs')
artist_table_drop =  drop_table_query('artists')
time_table_drop =  drop_table_query('time')

# CREATE TABLES

# songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (songplay_id SERIAL,
    start_time bigint references time(timestamp),
    user_id int references users(user_id),
    level varchar,
    song_id varchar references songs(song_id),
    artist_id varchar references artists(artist_id),
    session_id int,
    location varchar(200),
    useragent varchar(200),
    PRIMARY KEY(user_id, song_id, start_time)
    );
""")
# user_id, first_name, last_name, gender, leve
user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    ( user_id int PRIMARY KEY,
    first_name varchar,
    last_name varchar,
    gender char,
    level varchar
    );
    

""")
# song_id, title, artist_id, year, duration
song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
    song_id varchar PRIMARY KEY,
    title varchar(200),
    artist_id varchar references artists(artist_id),
    year int,
    duration real
    );

""")
# artist_id, name, location, latitude, longitude
artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
    artist_id varchar PRIMARY KEY,
    name varchar,
    location varchar,
    latitude real,
    longitude real
    );
""")
# timestamps of records in songplays broken down into specific units
# start_time, hour, day, week, month, year, weekday
time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (
    timestamp bigint PRIMARY KEY,
    year int,
    month int,
    day int,
    dayofweek int,
    weekofyear int,
    hour int,
    minute int,
    second int
    );
""")

# INSERT RECORDS

# songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
songplay_table_insert = ("""
    INSERT INTO songplays
    ( start_time, user_id, level, song_id, artist_id, session_id, location, useragent)
    VALUES( %(start_time)s, %(user_id)s, %(level)s, %(song_id)s, %(artist_id)s, %(session_id)s, %(location)s, %(useragent)s ) 
    ON CONFLICT DO NOTHING;
""")

user_table_insert = ("""
        INSERT INTO users
        (user_id, first_name, last_name, gender, level)
        VALUES( %(userId)s, %(firstName)s, %(lastName)s, %(gender)s, %(level)s )
        ON CONFLICT (user_id) DO UPDATE SET level = %(level)s;
""")

song_table_insert = ("""
    INSERT INTO songs
    (song_id, title, artist_id, year, duration)
    VALUES( %(song_id)s, %(title)s, %(artist_id)s, %(year)s, %(duration)s )
    ON CONFLICT(song_id) DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists
    (artist_id, name, location, latitude, longitude)
    VALUES( %(artist_id)s, %(artist_name)s, %(artist_location)s, %(artist_longitude)s, %(artist_latitude)s )
    ON CONFLICT DO NOTHING;
""")


time_table_insert = ("""    
    INSERT INTO time
    ( timestamp, year, month, day, dayofweek, weekofyear, hour, minute, second)
     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
     ON CONFLICT DO NOTHING;
""")

# FIND SONGS
 # get songid and artistid from song and artist tables
song_select = ("""
    SELECT songs.song_id, songs.artist_id 
    FROM songs JOIN artists
    ON songs.artist_id = artists.artist_id
    AND songs.title = %s
    AND artists.name = %s
    AND abs(songs.duration - %s) <= 0.1
;    
""")

# QUERY LISTS

create_table_queries = [ user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]