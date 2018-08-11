from pyspark import SparkContext
from pyspark import SparkConf
import random
import string

class MapRed():
    conf = SparkConf().setAppName("Test").setMaster("local")
    sc = SparkContext(conf=conf)

    def __init__(self,data):
        self.data = data
        self.sc.setLogLevel("ERROR")
        self.rdd = self.sc.parallelize(self.data)

    def wordCount(self):

        exclude_punc = list(string.punctuation)
        table = str.maketrans(dict.fromkeys(exclude_punc, " "))
        rdd_1 = self.rdd.flatMap(lambda key: key[1].split()).map(lambda singleword : singleword.translate(table).lower()).\
            map(lambda x: (x,1)).reduceByKey(lambda a,b:  a+b).sortByKey().filter(lambda str: str[0]!=" ").groupByKey()

        print(rdd_1.mapValues(list).collect())

    def setDifference(self):
        rdd_1 = self.rdd.flatMapValues(lambda key: key).map(lambda key: (key[1],key[0])).reduceByKey(lambda a,b:a+b)
        rdd_2 = rdd_1.filter(lambda a:"R" in a).map(lambda key: ("R-S", key[0])).groupByKey()
        print(rdd_2.mapValues(list).collect())


if __name__ == "__main__":
    data = [(1, "The horse raced past the barn fell"),
            (2, "The complex houses married and single soldiers and their families"),
            (3, "There is nothing either good or bad, but thinking makes it so"),
            (4, "I burn, I pine, I perish"),
            (5, "Come what come may, time and the hour runs through the roughest day"),
            (6, "Be a yardstick of quality."),
            (7, "A horse is the projection of peoples' dreams about themselves - strong, powerful, beautiful"),
            (8,
             "I believe that at the end of the century the use of words and general educated opinion will have altered so much that one will be able to speak of machines thinking without expecting to be contradicted."),
            (9, "The car raced past the finish line just in time."),
            (10, "Car engines purred and the tires burned.")]

    mrObject = MapRed(data)
    mrObject.wordCount()

    data1 = [('R', ['apple', 'orange', 'pear', 'blueberry']),('S', ['pear', 'orange', 'strawberry', 'fig', 'tangerine'])]
    data2 = [('R', [x for x in range(50) if random.random() > 0.5]),('S', [x for x in range(50) if random.random() > 0.75])]

    mrObject1 = MapRed(data1)
    mrObject1.setDifference()

    data2 = [('R', [x for x in range(50) if random.random() > 0.5]),('S', [x for x in range(50) if random.random() > 0.75])]
    mrObject = MapRed(data2)
    mrObject.setDifference()