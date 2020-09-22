# Sparkify song usage database

This project creates a database of songs and of user activity on the Sparkify streaming app. The database can then be used to perform analytics, e.g. which users are the most active, or which songs are being played. It can be used to build more easily a recommendation system.


# Database structure

To simplify the database queries, we choose to follow a star design. The database thus contains a fact table, **songlays**, which contains information about each song played by users through Sparkify streaming app. The database also contains the following dimension tables :
- **users** : contains information about Sparkify users
- **songs** : contains song information
- **artists** : contains information about the songs' artists
- **time** : contains information about the playtime of songs through the app.

Sparkify analytics team is particularly interested in knowing what songs users are listening to. The **songplays** table is what is hence of interest to them, and is constantly updated as log data is retrieved from the streaming app. It is thus a fact table. The other tables gives more detail information about some elements of the fact table (i.e. users, songs, artist, and playtime). These are thus dimension tables.

# Installation

## Prerequisites

This project uses python3 and postgresql.
Python libraries to install :
- `psycopg2`
- `pandas`

## Data 
The data needed to fill the database should be located in ./data in the working directory
- `data/log_data` : contains log data from Sparkify streaming app.
- `data/song_data` : contains description of each song. 

## How to run the code

To create the sparkifydb database, open a terminal and run 

    python create_tables.py
    
To populate the database with data, run in the terminal :
    
    python etl.py
    
You can then perform queries on the database, for instance using postgresql client `psql` . First, launch `psql` and connect to the database with the credential for user "student": 

    psql -U student -W -h 127.0.0.1 sparkifydb
    
Enter `student` as the password. Then, enter your queries in postgresql format.

### Example queries
The star database design makes the database queries easy. For instance, if the analytics teams want to know what songs in the database have been played through the app, they can issue a simple sql query :

    SELECT sp.song_id, songs.title FROM songplays sp JOIN songs ON sp.song_id = songs.song_id; 

Output :

    song_id            |     title      
    --------------------+----------------
    SOZCTXZ12AB0182364 | Setanta matins
    (1 row)

To retrieve more detailed information, i.e. the song's artist and the playtime, use a `JOIN`query :

    SELECT s.title AS song, a.name AS artist, t.hour,t.minute, t.second,
    u.first_name AS "user first name", u.last_name AS "user last name"
    FROM songplays sp JOIN songs s ON sp.song_id = s.song_id  
    JOIN artists a on s.artist_id = a.artist_id
    JOIN time t ON t.timestamp = sp.start_time 
    JOIN users u on u.user_id = sp.user_id;

Output :

          song      | artist | hour | minute | second | user first name | user last name 
    ----------------+--------+------+--------+--------+-----------------+------------
    Setanta matins | Elena  |   21 |     56 |     47 | Lily            | Koch
    (1 row)    

To retrieve all the paying users in the database :

    SELECT * from users WHERE users.level = 'paid';
    
Output :

     user_id | first_name | last_name | gender | level 
    ---------+------------+-----------+--------+-------
        29 | Jacqueline | Lynch     | F      | paid
        58 | Emily      | Benson    | F      | paid
        97 | Kate       | Harrell   | F      | paid
        73 | Jacob      | Klein     | M      | paid
      ...

To list all songs in the database :

    SELECT s.title, a.name, s.year, s.duration
    FROM songs s JOIN artists a
    ON s.artist_id = a.artist_id;
    
Output :

                  title               |      name      | year | duration 
    ----------------------------------+----------------+------+----------
    Ten Tonne                        | Chase & Status | 2005 |  337.684
    Get Your Head Stuck On Your Neck | Soul Mekanik   |    0 |  45.6616
    Sonnerie lalaleulé hi houuu      | Blingtones     |    0 |   29.544
    ...



    