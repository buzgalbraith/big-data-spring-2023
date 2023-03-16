#! /usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
import itertools

class MRBasket(MRJob):
    """
    A class to count item co-occurrence in shopping baskets
    """

    def mapper_get_session_items(self, _, line):
        """

        Parameters:
            -: None
                A value parsed from input and by default it is None because the input is just raw text.
                We do not need to use this parameter.
            line: str
                each single line a file with newline stripped

            Yields:
                (key, value) pairs
        """

        user,date,item=line.split(',')
        key=(user,date)
        value=item     
        yield (key,value) ## should be linear 
        
    def reducer_get_session_items(self, key, values ):
        shopping_list=set() ## creates a set so that a single item can not be added multiple times 
        for value in values: ## itterate through the valeus
            shopping_list.add(value)
        yield  (key, list(shopping_list))


    def map_pair(self,user, user_shopping_list):
        
        for item in list(itertools.permutations(user_shopping_list, 2)): 
            
            yield(item[0],item[1])

    def reducer_items(self, key,values):
        
        d=dict() ## here we create a dictionary 

        for value in values: ## there are (n-1)*d other possible combinations
            if(value not in d.keys()):
                d[value]=1
            else:
                d[value]+=1
        yield(key,[max(d, key=d.get), d[max(d, key=d.get)]])



    def steps(self):
        return [
            MRStep(
            
                mapper=self.mapper_get_session_items,
                reducer=self.reducer_get_session_items
                
            )
        ,MRStep(
           
            mapper=self.map_pair,
            reducer=self.reducer_items

               ) 
        ]

# this '__name__' == '__main__' clause is required: without it, `mrjob` will
# fail. The reason for this is because `mrjob` imports this exact same file
# several times to run the map-reduce job, and if we didn't have this
# if-clause, we'd be recursively requesting new map-reduce jobs.
if __name__ == "__main__":
    # this is how we call a Map-Reduce job in `mrjob`:
    MRBasket.run()
