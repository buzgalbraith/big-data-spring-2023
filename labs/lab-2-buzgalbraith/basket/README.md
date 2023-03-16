# Part 5: Item co-occurrence

## Explain each step of your solution

- the first step has a mapper and reduceer: 
    - the mapper takes in the raw lines and creates a key value mapping of the form {(user_id, date), item_bought}
    - the reducer takes aggreagates the items that users bought into a set (to avoid duplicates) then returns a list of the from {(user_id,date), [item_1...item_n]}
- the seond step also has a mapper and reducer function:
    - the mapper is slightly more complex it loops thrugh the permutations of length 2 combinations of items (using itertools.permutations) and returns (item_1, item_2)
    - the reducer takes a key and it's asociated valeus. for each key it creates an empty dictionary, it then loops through all values and adds the value to the dictionary if it is not already present and otherwise increments the dictionary value by 1. it then finally returns the dictionary item with the max value, the key to that dictionary and the orginal item. so that is it outputs of the form {item_1, (item_j, d[item_j])} where d is a dictionary counting the number of times the key of item 1 was asociatd with item_i and item_j is argmax(d[item_i]) for i in [1...n] 

...

## What problems, if any, did you encounter?
- I learned a lot implementing this, I think i am more fmailar with map reduce than i was at the start, despite this it was a hard problem taht took me quite a bit of time to debug. 

...

## How does your solution scale?

Analyze the time and space used by each stage of your solution, including the number of (intermediate) output values.
- let there be M (user_id,date) combinations, and D total items, let L be the number of lines
- my first mapper is constant in time and space at each call, but is called a total of L times 
- the first reducer at each stage creates a set and itterates through all items so it is O(D) at each call then it is called for all keys (user, session) so in total it should be O(MD)
- the second mapper uses (itertools.permutations(user_shopping_list, 2)) so it is looping through (d-1)(d) so the space should be O(d^2) items, i think space will be constant   O(1) since we are using an itterator
- the final reducer within each call can loop at most for all users and d-1 items, and creates a dictionary at each call so it would be O(MD) in time, and O(D) in space (Since the dictionary can have at most d-1 ellements). then it is called once for each ellement and thus D times so teh total time is $O(MD^2)$ and O(D) space
- I mean the first mapper and reducer scale reasonably well as they are linearly, but the second step mapper and reducer both have quadratic time complexity so they will scale poorly. 
...
