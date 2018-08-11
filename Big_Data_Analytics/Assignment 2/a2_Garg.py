
# coding: utf-8


from pyspark import SparkContext
from pyspark import SparkConf
import io
from tifffile import TiffFile 
import numpy as np
import zipfile
from PIL import Image 
import hashlib
from scipy import linalg 


conf = SparkConf().setAppName("SatelliteProject").setMaster("local")
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")


# ### Part - 1


rdd = sc.binaryFiles('hdfs:/data/large_sample')
fileNameList = rdd.map(lambda key: key[0].split("/")).flatMap(lambda key: key).filter(lambda key: str(key).__contains__(".zip")).collect()
zipName_broadcast = sc.broadcast(set(fileNameList))


def getOrthoTif(zfBytes):
#given a zipfile as bytes (i.e. from reading from a binary file),
# return a np array of rgbx values for each pixel
    bytesio = io.BytesIO(zfBytes)
    zfiles = zipfile.ZipFile(bytesio, "r")
    #find tif:
    for fn in zfiles.namelist():
        if fn[-4:] == '.tif':#found it, turn into array:
            tif = TiffFile(io.BytesIO(zfiles.open(fn).read()))
    return tif.asarray()


def divideImages(key):
    fileName = key[0].split("/")
    name = str()
    for file in fileName:
        if file in zipName_broadcast.value:
            name = file
            break
    imageArray = key[1]
    tupList = list()
    tupList.clear()
    imageArray = np.array(imageArray)
    row = imageArray.shape[0]
    col = imageArray.shape[1]
    for i in range(0,row,500):
        for j in range(0,col,500):
            tempArr = imageArray[i:i + 500, j:j + 500]
            tupList.append(np.array(tempArr))
    nameImageList = list()
    for i in range(len(tupList)):
        nameImageList.append((name+"-"+str(i),tupList[i]))
    return nameImageList



ques1_lis = ['3677454_2025195.zip-0', '3677454_2025195.zip-1', '3677454_2025195.zip-18', '3677454_2025195.zip-19']

# Here we are applying transformations to just divide the image in smaller parts and then collecting the images after filtering out what
# is required for showing output

rdd_1 = sc.binaryFiles('hdfs:/data/large_sample')
imageRDD = rdd_1.map(lambda key: (key[0],getOrthoTif(key[1]))).map(lambda key: divideImages(key)).            flatMap(lambda key: key)
filesList = imageRDD.filter(lambda key: key[0] in ques1_lis).collect()


# ### Result - Part -1

print("Part 1 Output")
lis = ['3677454_2025195.zip-0', '3677454_2025195.zip-1', '3677454_2025195.zip-18', '3677454_2025195.zip-19']
for tup in filesList:
    if tup[0] in lis:
        print(tup[0],tup[1][0][0])

print("\n")

# ### Part - 2


def calculateIntensity(matrix):
    matrix = np.array(matrix)
    matrix = ((np.mean(matrix[:,:,:3],axis=2))*(matrix[:,:,3]/100))
    matrix = matrix.astype(int)
    return matrix

def getIntensityFromRGBI(pixel):
    r = int(pixel[0])
    g = int(pixel[1])
    b = int(pixel[2])
    I = int(pixel[3])
    rgb_mean = (r+g+b)/3
    intensity = int(rgb_mean * (I/100))
    return intensity

def reductionResolution(matrix,factor):
    matrix = np.array(matrix)
    temp = 500
    k = 500//factor
    matrix = np.array(np.split(matrix,indices_or_sections=k,axis=1))
    matrix = np.array(np.split(matrix,indices_or_sections=k,axis=1))
    matrix = np.mean(matrix,axis=(2,3))
    return matrix

# This function get the mean value so as to do reduction of resolution
def getMeanOverFactor(matrix):
    return np.mean(matrix)

# This function performs row diff
def row_diff(matrix):
    matrix = np.array(matrix)
    matrix = np.diff(matrix,axis=1)
    matrix = np.where(np.logical_or(matrix < -1, matrix > 1), matrix, 0)
    matrix = np.clip(matrix, -1, 1)
    return matrix

# This function performs col diff
def col_diff(matrix):
    matrix = np.array(matrix)
    matrix = np.diff(matrix,axis=0)
    matrix = np.where(np.logical_or(matrix < -1, matrix > 1), matrix, 0)
    matrix = np.clip(matrix, -1, 1)
    return matrix

# This function flatten the row diff and col diff matrix
def getFeature(row_diff,col_diff):
    row_diff = np.array(row_diff)
    col_diff = np.array(col_diff)
    return np.append(row_diff.flatten(),col_diff.flatten())

# Below are the transformations for second part where we are doing reduction in resolution and then performing row and then col diff
# and then flattened the array and after we are filtering first before collecting.

imageRdd_1 = imageRDD.map(lambda key: (key[0],calculateIntensity(key[1])))
imageRdd_1.persist()


imageRdd_2 = imageRdd_1.map(lambda key: (key[0],reductionResolution(key[1],10)))

imageRdd_3 = imageRdd_2.map(lambda key: (key[0],row_diff(key[1]),key[1])).map(lambda key: (key[0], key[1] , col_diff(key[2]))).map(lambda key: (key[0],getFeature(key[1],key[2])))



ques_2lis = ["3677454_2025195.zip-1", "3677454_2025195.zip-18"]


ques_2lis_broadcast = sc.broadcast(set(ques_2lis))


featuresList = imageRdd_3.filter(lambda key: key[0] in ques_2lis_broadcast.value).collect()

# ### Result - Part - 2


print("Part 2 Output")
lis = ["3677454_2025195.zip-1", "3677454_2025195.zip-18"]
for tup in featuresList:
    if tup[0] in lis:
        print(tup[0],np.array(tup[1]))
print("\n")
lengthBroadCast = sc.broadcast(len(featuresList[0][1]))


# ### Part - 3

# We are calculating 128 bit md5 by using np.array split and then taking the middle bit after converitng the hashed
# value into binary
def getMD5HashForFeatures(feature,factor):
    feature = np.array(feature)
    hashcode = str()
    increment = len(feature)//factor
    for arr in np.array_split(np.array(feature), 128):
        hexdigest = hashlib.md5(arr).hexdigest()
        binstr = bin(int(hexdigest,16))
        bit = binstr[len(binstr)//2]
        hashcode += bit
    return hashcode

# Here we are getting the buckets mapped by passing bands and no of buckets in function to make it abstract.
# I am returning (band No, bucket no) so that later I can make it a key and find the images mapped to same bucket in
# same band.

def getBucketsMapped(signatureVector,bands,prime):
    #bands = 8
    rowsPBand = len(signatureVector)//bands
    #prime = 419
    bucketList = list()
    count = 0
    for i in range(0,len(signatureVector),rowsPBand):
        bucketNo = hash(signatureVector[i : i + rowsPBand]) % prime
        bucketList.append((count,bucketNo))
        count += 1
        if count == bands:
            break
    return bucketList

# Here we making list like (name, candidate list), this is called in rdd.
questionList = ['3677454_2025195.zip-0', '3677454_2025195.zip-1', '3677454_2025195.zip-18', '3677454_2025195.zip-19']
def appendMatcheddNames(commonlist):
    temp = list()
    for name in questionList:
        if name in commonlist:
            for each in commonlist:
                if name != each:
                    temp.append((name,each))

    return temp  

# Here we are first getting the 128 md5 hash and then getting buckets mapped according to the function explained and then doing
# flat map so as to associate (band no, bucket no) with each file name and doing group by key so as get all images mapped to
# same bucket in same band together and then calling appendMatcheddNames() so as to get candidate list for image asked in question

lshRdd = imageRdd_3.map(lambda key: (key[0],key[1],getMD5HashForFeatures(key[1],128)))



lshRdd_1 = lshRdd.map(lambda key: (key[0],key[1],getBucketsMapped(key[2],8,1283)))


templshRdd_1 = lshRdd_1.map(lambda key: (key[0],key[2])).flatMapValues(lambda key: key).\
                map(lambda key: (key[1],key[0]))

templshRdd_2 = templshRdd_1.groupByKey().map(lambda key: (key[1]))

templshRdd_3 = templshRdd_2.map(lambda key: appendMatcheddNames(key)).flatMap(lambda key: key)

candidatesListCheck = templshRdd_3.groupByKey().map(lambda x: (x[0],set(x[1]))).\
        map(lambda x:(x[0],list(x[1]))).collect()


print("Output Part - 3b")
questionList3B = ['3677454_2025195.zip-1', '3677454_2025195.zip-18']
for i in range(len(candidatesListCheck)):
    if candidatesListCheck[i][0] in questionList3B:
        print(candidatesListCheck[i][0],"==== Candidate List =====",candidatesListCheck[i][1])

print("\n")

# This is for part 3c so that later we can apply filter and get reduced feature vectors only for images required in question.
vectorsToBeTakenList = list()
for i in range(len(candidatesListCheck)):
    if candidatesListCheck[i][0] in questionList3B:
        vectorsToBeTakenList.extend(candidatesListCheck[i][1])
vectorsToBeTakenList.extend(questionList3B)
vectorsToBeTakenList = set(vectorsToBeTakenList)
vectorsToBeTakenList = list(vectorsToBeTakenList)


# ### SVD


def makePair(nameSVD):
    name, vector = nameSVD
    temp = []
    i = 0
    for ele in name:
        temp.append((ele,vector[i]))
        i += 1
    return temp


def getNameVector(namevector1,namevector2,featureLength):
    name1 , vector1 = namevector1
    name2 , vector2 = namevector2
    a = np.array(vector1)
    b = np.array(vector2)
    return np.append(name1,name2),np.reshape(np.append(a,b),(-1,featureLength))


def getTag(st):
    a = st.split("-")[0]
    return a

# Here we perform svd and return Vh so that we can use it later.
def SVD(image,dimensions):
    mean = np.mean(image, axis=0)
    stDev = np.std(image, axis=0)
    stDev[stDev == 0] = 1
    
    img_zscore = (image - mean) / stDev

    U, s, Vh = linalg.svd(img_zscore, full_matrices=1)

    
    return Vh[:,0:dimensions]

# Here are using the above V so as to get the projections on other matrices and then get the same feature vectors.
def SVDFromCommonV(image,vBroadCast):
    mean = np.mean(image, axis=0)
    stDev = np.std(image, axis=0)

    stDev[stDev == 0] = 1
    
    img_zscore = (image - mean) / stDev
    img_zscore = np.array(img_zscore)
    img_zscore_lowdim = np.matmul(img_zscore , vBroadCast.value)
    
    return img_zscore_lowdim

# Here we are doing take 1 so as to get V that can be later used to get reducecd feature vectors for other images.
lshRdd_3 = lshRdd_1.map(lambda key:(getTag(key[0]),(key[0],key[1]))).reduceByKey(lambda a,b: getNameVector(a,b,lengthBroadCast.value))
lshRdd_4 = lshRdd_3.map(lambda key:(key[1][0],SVD(key[1][1], 10)))
vCollect = lshRdd_4.take(1)

vBroadCast = sc.broadcast(vCollect[0][1])

# These transformations are to get the reduced feature fectors for images asked in question and their candidate list which is a type
# of optimization. However svd is perfomed for all feature vectors.

lshRdd_3 = lshRdd_1.map(lambda key:(getTag(key[0]),(key[0],key[1]))).reduceByKey(lambda a,b: getNameVector(a,b,lengthBroadCast.value))
lshRdd_4 = lshRdd_3.map(lambda key:(key[1][0],SVDFromCommonV(key[1][1],vBroadCast))).map(lambda key : makePair(key)).flatMap(lambda x:x)
svdList = lshRdd_4.filter(lambda x: x[0] in vectorsToBeTakenList).collect()


def getVectors(name,svdList):
    for i in range(len(svdList)):
        if svdList[i][0] == name:
            return svdList[i][1]


# In[ ]:

print("Part 3c Output")
ques_3C_List = ['3677454_2025195.zip-1', '3677454_2025195.zip-18']
for i in range(len(candidatesListCheck)):
    if candidatesListCheck[i][0] in ques_3C_List:
        parentName = candidatesListCheck[i][0]
        vectorParent = getVectors(parentName,svdList)
        print("Distance Between " + str(parentName) + " and its candidate pairs sorted from least to highest:")
        print()
        temp = list()
        for candidateName in candidatesListCheck[i][1]:
            candidateVector = getVectors(candidateName,svdList)
            temp.append(((candidateName) , \
                         float(np.linalg.norm(np.array(vectorParent)-np.array(candidateVector)))))
        lis = sorted(temp,key=lambda x:x[1])
        for x in lis:
            print(x[0],"       ",x[1])
        print("\n")

print("Extra Credit Part")
# Extra Credit


def extraCreditDifferentFactor(factor,bandsTotal,bucketsize):
    imageRdd_2 = imageRdd_1.map(lambda key: (key[0],reductionResolution(key[1],factor)))
    imageRdd_3 = imageRdd_2.map(lambda key: (key[0],row_diff(key[1]),col_diff(key[1]))).\
                    map(lambda key: (key[0],getFeature(key[1],key[2])))
        
    ques_2lis = ["3677454_2025195.zip-1", "3677454_2025195.zip-18"]
    ques_2lis_broadcast = sc.broadcast(set(ques_2lis))
    featuresList = imageRdd_3.filter(lambda key: key[0] in ques_2lis_broadcast.value).collect()
    
    lis = ["3677454_2025195.zip-1", "3677454_2025195.zip-18"]

    lengthBroadCast = sc.broadcast(len(featuresList[0][1]))
    

    lshRdd = imageRdd_3.map(lambda key: (key[0],key[1],getMD5HashForFeatures(key[1],128)))
    lshRdd_1 = lshRdd.map(lambda key: (key[0],key[1],getBucketsMapped(key[2],bandsTotal,bucketsize)))

    questionList = ['3677454_2025195.zip-0', '3677454_2025195.zip-1', '3677454_2025195.zip-18', '3677454_2025195.zip-19']


    templshRdd_1 = lshRdd_1.map(lambda key: (key[0],key[2])).flatMapValues(lambda key: key).\
                    map(lambda key: (key[1],key[0]))

    templshRdd_2 = templshRdd_1.groupByKey().map(lambda key: (key[1]))

    templshRdd_3 = templshRdd_2.map(lambda key: appendMatcheddNames(key)).flatMap(lambda key: key)

    candidatesListCheck = templshRdd_3.groupByKey().map(lambda x: (x[0],set(x[1]))).\
            map(lambda x:(x[0],list(x[1]))).collect()


    print("\n")
    print("Output Part - 3b")
    questionList3B = ['3677454_2025195.zip-1', '3677454_2025195.zip-18']
    for i in range(len(candidatesListCheck)):
        if candidatesListCheck[i][0] in questionList3B:
            print(candidatesListCheck[i][0],"==== Candidate List =====",candidatesListCheck[i][1])

    print("\n")

    vectorsToBeTakenList = list()
    for i in range(len(candidatesListCheck)):
        if candidatesListCheck[i][0] in questionList3B:
            vectorsToBeTakenList.extend(candidatesListCheck[i][1])
    vectorsToBeTakenList.extend(questionList3B)
    vectorsToBeTakenList = set(vectorsToBeTakenList)
    vectorsToBeTakenList = list(vectorsToBeTakenList)


    lshRdd_3 = lshRdd_1.map(lambda key:(getTag(key[0]),(key[0],key[1]))).reduceByKey(lambda a,b: getNameVector(a,b,lengthBroadCast.value))
    lshRdd_4 = lshRdd_3.map(lambda key:(key[1][0],SVD(key[1][1], 10)))
    vCollect = lshRdd_4.take(1)

    vBroadCast = sc.broadcast(vCollect[0][1])
    lshRdd_3 = lshRdd_1.map(lambda key:(getTag(key[0]),(key[0],key[1]))).reduceByKey(lambda a,b: getNameVector(a,b,lengthBroadCast.value))
    lshRdd_4 = lshRdd_3.map(lambda key:(key[1][0],SVDFromCommonV(key[1][1],vBroadCast))).map(lambda key : makePair(key)).flatMap(lambda x:x)
    svdList = lshRdd_4.filter(lambda x: x[0] in vectorsToBeTakenList).collect()

    print("\n")
    print("Part 3D Output")
    ques_3C_List = ['3677454_2025195.zip-1', '3677454_2025195.zip-18']
    for i in range(len(candidatesListCheck)):
        if candidatesListCheck[i][0] in ques_3C_List:
            parentName = candidatesListCheck[i][0]
            vectorParent = getVectors(parentName,svdList)
            print("Distance Between " + str(parentName) + " and its candidate pairs sorted from least to highest:")
            print()
            temp = list()
            for candidateName in candidatesListCheck[i][1]:
                candidateVector = getVectors(candidateName,svdList)
                temp.append(((candidateName) , \
                             float(np.linalg.norm(np.array(vectorParent)-np.array(candidateVector)))))
            lis = sorted(temp,key=lambda x:x[1])
            for x in lis:
                print(x[0],"       ",x[1])
            print("\n")


# This is for 3d. Here we passing factor as 5, no of bands as 8 and no of buckets as 491.I have made a fucntion for this were we can
# pass factor, bands and buckets as parameters and it will as required.
extraCreditDifferentFactor(5,8,1297)
