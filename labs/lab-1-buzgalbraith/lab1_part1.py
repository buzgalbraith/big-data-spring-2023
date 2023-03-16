#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# USAGE:
#   python lab1_part1.py music_small.db

import sys
import sqlite3


# The database file should be given as the first argument on the command line
# Please do not hard code the database file!
db_file = sys.argv[1]

# We connect to the database using 
with sqlite3.connect(db_file) as conn:
    # This query counts the number of artists who became active in 1990
    sql_query = """SELECT name FROM sqlite_master
    WHERE type='table';"""
 
    # Creating cursor object using connection object
    cursor = conn.cursor()
     
    # executing our sql query
    cursor.execute(sql_query)
    #print("List of tables\n")
    #print(cursor.fetchall()) ## wack no tables are being read in 
    year = (1990,)
    for row in conn.execute('SELECT count(*) FROM artist WHERE artist_active_year_begin=?', year):
        # Since there is no grouping here, the aggregation is over all rows
        # and there will only be one output row from the query, which we can
        # print as follows:
        #print('Tracks from {}: {}'.format(year[0], row[0]))
        0
        # The [0] bits here tell us to pull the first column out of the 'year' tuple
        # and query results, respectively.

    # ADD YOUR CODE STARTING HERE
    
    # Question 1
    print('Question 1:')
    #1. Which tracks (ids and names) have a lyricist whose name begins with "W"?
    q_1="SELECT id, track_title  FROM track WHERE track_lyricist LIKE 'w%'" ## i am going to assume they just mena first name?
    # implement your solution to q1
    for row in conn.execute(q_1):
        print(row)
        
    print('---')
    
    # Question 2. What are the values that can be taken by the `track.track_explicit` field?
    print('Question 2:')
    q_2='SELECT DISTINCT track_explicit FROM track'
    # implement your solution to q2
    r_2=conn.execute(q_2).fetchall()
    print(r_2)
    print('---')
    
    # Question 3. Which track (id and title) has the most listens?
    print('Question 3:')
    # implement your solution to q3
    q_3="SELECT id, track_title  FROM track ORDER BY track_listens DESC"
    a=conn.execute(q_3) #(62460, 'Siesta', 356588)
    print(a.fetchone()) 
    print('---')
    
    
    # Question 4. How many artists have "related projects"?
    print('Question 4:')
    q_4="SELECT COUNT(artist_related_projects) from artist where artist_related_projects IS NOT NULL"
    # implement your solution to q4
    a=conn.execute(q_4) 
    print(a.fetchone()[0]) 
    print('---')
    
    # Question 5. Which non-null language codes have exactly 4 tracks?
    # implement your solution to q5
    print('Question 5:')
    q_5='SELECT track_language_code,count(track_language_code) from track group by track_language_code having  count(track_language_code)=4'
    a=conn.execute(q_5) 
    print(a.fetchall()) 
    print('---')


    
    # Question 6
    print('Question 6:')
   # 6. How many tracks are by artists known to be active only within the 1990s?
    # implement your solution to q6
    ## do a left join of artist<-track
    q_6='SELECT count(track_title) \
        FROM artist LEFT JOIN track ON artist.id = track.artist_id where\
        artist_active_year_begin>=1990 and artist_active_year_begin<=1999 and artist_active_year_end<=1999 and artist_active_year_end>=1990;'
    # for row in conn.execute(q_6):
    #     print(row)
    a=conn.execute(q_6) 
    print(a.fetchone()[0])     
    print('---')
    
    # Question 7. Which three artists have worked with the largest number of distinct album producers?
    print('Question 7:')
    
    # implement your solution to q7
    q_7='SELECT artist_name,COUNT(album_producer) \
        FROM artist LEFT JOIN track ON artist.id = track.artist_id \
        left join album on album_id=album.id \
        GROUP BY artist_name, album_producer \
        HAVING album_producer IS NOT NULL\
        ORDER BY COUNT(album_producer) DESC\
        LIMIT 3;'
    for row in conn.execute(q_7):
        print(row)
        
    # Question 8 Which track (include id, title, and artist name) has the largest difference between the number of `album listens` and `track listens`?
    print('Question 8:')
    q_8='SELECT track.id, track_title, artist_name \
        FROM track LEFT JOIN artist ON  track.artist_id=artist.id  \
        left join album on album_id=album.id \
        ORDER BY ABS(album_listens-track_listens)  DESC\
        limit 1;'
    # implement your solution to q8
    for row in conn.execute(q_8):
        print(row)
    print('---')
