- this lab has two tasks 
    - writing basic queries in sql
    - indexing 
- take away is don't index on literally everything
- so we were working with the following query 
- MY_QUERY = """SELECT artist.id, artist.artist_name, MIN(album.album_listens) as listens
	      FROM artist
	      INNER JOIN track ON track.artist_id = artist.id
	      INNER JOIN album ON track.album_id = album.id
	      GROUP BY artist.id
	      HAVING listens >= 50000"""
-  i found these indices helled     index_1_querry="CREATE INDEX track_INDEX ON track (ALBUM_ID,ARTIST_ID)"
    index_2_querry="CREATE INDEX Album_Index ON album (ALBUM_LISTENS asc,id )"
- so that is only index the track col which can be searched for the join, the the album listens call which helps our having statement.
