#! /usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
import itertools

class MRBasket(MRJob):
    """
    A class to count item co-occurrence in shopping baskets
    """

    def mapper_user_follows(self, _, line):
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
        user,follow=line.split(',')   
        yield (user.strip() ,follow.strip() ) 
        yield (follow.strip() , user.strip() ) 
    def reducer_follows(self, key,values):
        out=[]
        for value in values:
            out.append(value)
        yield (key, out)
    def map_inverse(self, key,values):
        it1, it2 = itertools.tee(values, 2)
        for value1 in it1:
            out=[]
            it1, it2 = itertools.tee(values, 2)
            for value2 in it2:
                if value1!=value2:
                    out.append(value2)
            output_key=[key,value1]
            output_key = sorted(output_key)
            yield (output_key, (key,out))
    #def reduce_inverse(self, key,values):

    def mapper_semi(self,key,values):
        for value in values:
            



    def steps(self):
        return [

            MRStep(mapper=self.mapper_user_follows
                ,reducer=self.reducer_follows
                
            ),
            MRStep(mapper=self.map_inverse,
            #    reducer=self.reducer_follows
                
           #)
        #,MRStep(
        #    mapper=self.map_pair,
        #    reducer=self.reducer_items
                
               ) 
        ]
#["1003", "27-02-2014"]  ["rolls/buns"]

# this '__name__' == '__main__' clause is required: without it, `mrjob` will
# fail. The reason for this is because `mrjob` imports this exact same file
# several times to run the map-reduce job, and if we didn't have this
# if-clause, we'd be recursively requesting new map-reduce jobs.
if __name__ == "__main__":
    # this is how we call a Map-Reduce job in `mrjob`:
    MRBasket.run()
