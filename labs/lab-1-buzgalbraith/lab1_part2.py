#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# USAGE:
#   python lab1_part2.py music_small.db

import sys
import sqlite3
import timeit


# The database file should be given as the first argument on the command line
# Please do not hard code the database file!
db_file = sys.argv[1]

  
# The query to be optimized is given here
# It finds all the artists (ids and names) for which all of their albums received at least 50K listens
MY_QUERY = """SELECT artist.id, artist.artist_name, MIN(album.album_listens) as listens
	      FROM artist
	      INNER JOIN track ON track.artist_id = artist.id
	      INNER JOIN album ON track.album_id = album.id
	      GROUP BY artist.id
	      HAVING listens >= 50000"""

NUM_ITERATIONS = 100
# NUM_ITERATIONS = 10 


def run_my_query(conn):
    for row in conn.execute(MY_QUERY):
        pass
    


# We connect to the database using
with sqlite3.connect(db_file) as conn:
    # We use a "cursor" to mark our place in the database.
    cursor = conn.cursor()
    # We could use multiple cursors to keep track of multiple
    # queries simultaneously.
    try:
        q_1="DROP INDEX track_INDEX;"
        cursor.execute(q_1)
    except:
        0
    try:
        q_1="DROP INDEX Album_Index;"
        cursor.execute(q_1)
    except:
        0
    try:
        q_1="DROP INDEX artist_index;"
        cursor.execute(q_1)
    except:
        0
    
    orig_time = timeit.repeat('run_my_query(conn)', globals=globals(), number=NUM_ITERATIONS)
    print("Before optimization:")

    print(f'Mean time: {sum(orig_time)/NUM_ITERATIONS:.3f} [seconds/query]')
    print(f'Best time: {min(orig_time)/NUM_ITERATIONS:.3f} [seconds/query]')

    #MAKE YOUR MODIFICATIONS TO THE DATABASE HERE
    
    ## try catch statements to keep things simple for adding and removing index

    index_1_querry="CREATE INDEX track_INDEX ON track (ALBUM_ID,ARTIST_ID)"
    index_2_querry="CREATE INDEX Album_Index ON album (ALBUM_LISTENS asc,id )"
    print(index_2_querry)
   # index_3_querry="CREATE INDEX artist_index ON artist (id, artist_name)"
    try:
        cursor.execute(index_1_querry)
    except:
        0
    try:
        cursor.execute(index_2_querry)
    except:
        0
    try:
        cursor.execute(index_3_querry)
    except:
        0

    new_time = timeit.repeat('run_my_query(conn)', globals=globals(), number=NUM_ITERATIONS)
    print("After optimization:")

    print(f'Mean time: {sum(new_time)/NUM_ITERATIONS:.3f} [seconds/query]')
    print(f'Best time   : {min(new_time)/NUM_ITERATIONS:.3f} [seconds/query]')
