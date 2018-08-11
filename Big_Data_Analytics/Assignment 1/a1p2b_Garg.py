from pyspark import SparkContext
from pyspark import SparkConf
import string

def main():

    rdd = sc.wholeTextFiles("/Users/jatingarg/Desktop/BdaA1/blogs/")

    rdd_1 = rdd.map(lambda key: key[0].split(".")).map(lambda x:[x[3],1]).reduceByKey(lambda a,b:a+b).keys().collect()

    indusName_broadcast = sc.broadcast(set(rdd_1))

    rdd_2 = rdd.map(lambda key: key[1].split("</post>")).map(lambda x: func(x, indusName_broadcast)).filter(
        lambda x: x.__len__() >= 1)

    rdd_3 = rdd_2.flatMap(lambda x: x).map(lambda x: ((x[0],x[1][0]),x[1][1])).reduceByKey(lambda a,b:a+b).sortByKey()

    rdd_4 = rdd_3.map(lambda x: (x[0][0],(x[0][1],x[1]))).groupByKey()

    print(rdd_4.mapValues(list).collect())


def func(x,indusName_broadcast):
    lst = []
    tup = []
    for item in x:
        post = str(item)
        start,end = "",""
        tup.clear()
        if(post.__contains__("<date>")):
            start = post.index("<date>")
            end = post.index("</date>")
        if(start != "" and end != ""):
            date = post[start:end]
            splitlst = date.split(",")
            tup.append(str(splitlst[2])+"-"+str(splitlst[1]))

        exclude_punc = list(string.punctuation)
        exclude_punc.remove('-')
        table = str.maketrans(dict.fromkeys(exclude_punc," "))
        post = post.translate(table)
        for element in indusName_broadcast.value:
            industry = str(element).lower()
            count = post.lower().split().count(industry)
            if count>=1 and tup[0]:
                lst.append(tuple(list([industry,tuple(list([tup[0],count]))])))
    return lst

if __name__ == "__main__":
    conf = SparkConf().setAppName("Blogger").setMaster("local")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")
    main()