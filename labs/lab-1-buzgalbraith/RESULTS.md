# Lab 1 results

Your name: Woodward (Buz) Galbraith 

## Part 1
Paste the results of your queries for each question given in the README below:

Question 1:
(22344, 'Outburst')
(66084, 'Got My Modem Working')
(66096, 'Mistress Song')
---
Question 2:
[(None,), ('Radio-Safe',), ('Radio-Unsafe',), ('Adults-Only',)]
---
Question 3:
(62460, 'Siesta')
---
Question 4:
453
---
Question 5:
[('de', 4), ('ru', 4)]
---
Question 6:
34
---
Question 7:
('Ars Sonor', 19)
('junior85', 15)
('The Fucked Up Beat', 11)
Question 8:
(76008, 'JessicaBD', 'Cody Goss')
---


## Part 2

- Execution Before optimization:
    Mean time: 1.325 [seconds/query]
    Best time: 0.251 [seconds/query]
- Execution time after optimization:
    Mean time: 0.889 [seconds/query]
    Best time: 0.176 [seconds/query]


- Briefly describe how you optimized for this query: I made a cluserd index for the joining table tracks, as well as clusterd index for id, albums acsending

- Did you try anything other approaches?  How did they compare to your final answer?: 
    1.  my first idea was just to try to index everything like this. 
        - index_1_querry="CREATE INDEX ARTIST_INDEX ON track (ARTIST_ID, ALBUM_ID)"
        - index_2_querry="CREATE INDEX ARTIST_INDEX_2 ON album (ID, ALBUM_LISTENS)"
        - index_3_querry="CREATE INDEX ARTIST_INDEX_3 ON artist (ID, artist_name)"
        - this did not work at all, and my mean time actually went up.
    2. my second idea was just using indexing the joining table track to make the joins more efficnet.
    so i tried these
        -  index_1_querry="CREATE INDEX track_INDEX ON track (ALBUM_ID,ARTIST_ID)"
        - index_1_querry="CREATE INDEX track_INDEX ON track (ARTIST_ID,ALBUM_ID)"
        - I was shocked by how much faster the first one was. 

    3. my thid idea was to index Album by listines in a ascending way.
    so i tried this 
        - index_2_querry="CREATE INDEX Album_Index ON album (id, ALBUM_LISTENS asc )"
        - so this will sort each album in an ascending way, which will make it easier for th emin funciton hopefully.
    4. i thought about adding an index for artist coloumn but artist id is the primary coloumn and artist name is the only other thing from that table we use which is obviously asociated with artist index anyway so it was not nesscary. 
