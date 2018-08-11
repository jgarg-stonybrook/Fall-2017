def main():
    '''
        Usage: q2_classifier.py -f1 <train_dataset> -f2 <test_dataset> -o <output_file>
            -f1     The csv formatted training dataset
            -f2     The csv formatted test data set
            -o      The path/name of the output file

        This function uses a niave Bayesian approach to identifying spam emails
    '''

    import sys
    import os

    featureList = list()
    featureDict = dict()

    # check if full emails are available
    fullAccess = os.path.exists("data\\")
    print(fullAccess)

    # parse training data into list of email data-object class
    trainingData = open(sys.argv[2], "r")
    trainingEmails = list()

    print("parsing into email data objects")
    for line in trainingData:
        newEmail = Email(line)
        trainingEmails.append(newEmail)

        # EXTRA CREDIT
        if fullAccess:
            domain = get_email_fromdomain(line[0:8])
            if domain is not None:
                if domain not in featureDict.keys():
                    featureDict[domain] = Feature(domain, [], False)

                if not newEmail.spam:
                    featureDict[domain].hamHits += 1
                elif newEmail.spam:
                    featureDict[domain].spamHits += 1

    # EXTRA CREDIT
    if fullAccess:
        featureList = list()

    # get total counts of spam/ham in test data
    spamCount = 0
    hamCount = 0
    for email in trainingEmails:
        if email.spam:
            spamCount += 1
        else:
            hamCount += 1
    print("hamcount:", hamCount, "spamcount:", spamCount)

    # calculate feature data
    print("calculating feature occurance rates")
    # search emails and pull out words to add to feature list
    for email in trainingEmails:
        for key in email.GetKeys():
            if key not in featureList:
                featureList.append(key)
    # create feature nodes containing a word and its spam/ham occurance counts
    for feature in featureList:
        featureDict[feature] = Feature(feature, trainingEmails)

    # classify test data using feature probabilities
    print("classifying test data")
    hamPredicted = 0
    spamPredicted = 0
    hamMiss = 0
    spamMiss = 0
    unkown = 0

    testData = open(sys.argv[4], "r")
    testData = testData.readlines()
    output = open(sys.argv[6], "w")

    for i in range(len(testData)):
        line = testData[i]
        emailX = Email(line)

        spamProb = spamCount / float(spamCount + hamCount)
        hamProb = (1 - spamProb)

        # multiply probabilities to estimate spam and ham probabilities
        for feature in emailX.data.keys():
            spamProb *= (float(featureDict[feature].SpamHits()) / float(spamCount))
            hamProb *= (float(featureDict[feature].HamHits()) / float(hamCount))

        # EXTRA CREDIT
        if fullAccess:
            domain = get_email_fromdomain(line[0:8])
            if domain is not None and domain in featureDict.keys():
                spamProb *= (float(featureDict[domain].SpamHits()) / float(spamCount))
                hamProb *= (float(featureDict[domain].HamHits()) / float(hamCount))

        # catalogue our prediction accuracy
        spamorham = "spam"
        if hamProb > spamProb:
            spamorham = "ham"
            hamPredicted += 1
            if emailX.spam:
                hamMiss += 1
        elif hamProb < spamProb:
            spamPredicted += 1
            if not emailX.spam:
                spamMiss += 1
        else:
            unkown += 1
        output.write(line[0:8] + " " + spamorham + "\n")

    # print results
    print("predicted:", hamPredicted, "ham", hamMiss, "wrong", (1.0 - float(hamMiss) / float(hamPredicted)),
          "accuracy rate")
    print("predicted:", spamPredicted, "spam", spamMiss, "wrong", (1.0 - float(spamMiss) / float(spamPredicted)),
          "accuracy rate")
    print("total accuracy rate", (1.0 - (float(hamMiss + spamMiss) / float(hamPredicted + spamPredicted))))
    print("unkown count", unkown)


class Email():
    def __init__(self, email):
        emailText = email.split()
        self.id = emailText[0]
        self.spam = True
        if "ham" in emailText[1]:
            self.spam = False

            # create word/occurance dictionary
        self.data = dict()
        wordCount = (len(emailText) / 2) - 2
        for i in range(1, int(wordCount)):
            self.data[emailText[i * 2]] = int(emailText[i * 2 + 1])

    def Count(self, word):
        return self.data[word]

    def GetKeys(self):
        return self.data.keys()


class Feature():
    def __init__(self, featureName, mailList, extracredit=False):
        self.name = featureName

        self.hamHits = 0
        self.spamHits = 0
        self.emailcount = len(mailList)
        if not extracredit:
            for mail in mailList:
                if featureName in mail.data and not mail.spam:
                    self.hamHits += mail.Count(featureName)
                if featureName in mail.data and mail.spam:
                    self.spamHits += mail.Count(featureName)

    def Name(self):
        return self.name

    def HamHits(self):
        return self.hamHits

    def SpamHits(self):
        return self.spamHits


def get_email_fromdomain(id):
    import os

    path = "data\\" + id
    if not os.path.exists(path):
        return None

    f = open(path, "r")
    fullemail = f.readlines()

    for line in fullemail:
        if "From" in line[0:4]:
            st = line.rfind('@') + 1
            ed = line.rfind('>')
            f.close()
            return line[st:ed]


if __name__ == "__main__":
    main()