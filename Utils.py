from Webscraper import *

class Utils(object):
    TF_Corpus = {}
    TF_Reversed_Corpus = {}
    term_IDFs = {}

    '''
        Function to initiate pre-processing on data for clustering
    '''
    def process_data_for_clustering(self):
        self.buildCorpus()
        self.buildReversedCorpus()
        self.compute_TF_documents()
        self.compute_TF_IDFs()

        for job in Webscraper.jobs_fetched:
            print "ID:"+str(job.id)
            print "TF document"+str(job.TFvector)
            print "TF*IDF document"+str(job.TF_IDF)

    '''
        Function to build Corpus of terms and their frequencies in each document
    '''
    def buildCorpus(self):
        Corpus = {}

        for i in range(len(Webscraper.jobs_fetched)):
            job = Webscraper.jobs_fetched[i]
            job.set_id(i)
            for word in job.summary:
                if word not in Corpus.keys():
                    frequencies = []
                    for i in range(0, len(Webscraper.jobs_fetched)):
                        frequencies.append(0)
                    Corpus[word] = frequencies
                Corpus[word][i] += 1
        self.TF_Corpus = Corpus

    '''
        Function to reverse the corpus as job ids vs. corresponding term frequency document
    '''
    def buildReversedCorpus(self):
        ReversedCorpus = {}

        terms = self.TF_Corpus.keys()

        for i in range(0, len(Webscraper.jobs_fetched)):
            array_termFrequency = []
            for k in range(0, len(terms)):
                array_termFrequency.append(0)
            ReversedCorpus[i] = array_termFrequency

        jobIDs = ReversedCorpus.keys()

        for jobIdkey in jobIDs:
            for j in range(0, len(terms)):
                word = terms[j]
                ReversedCorpus[jobIdkey][j] = self.TF_Corpus[word][jobIdkey]

        self.TF_Reversed_Corpus = ReversedCorpus

    '''
        Function to compute term frequency vector for all fetched jobs
    '''
    def compute_TF_documents(self):

        for job in Webscraper.jobs_fetched:
            termFreq = self.TF_Reversed_Corpus[job.id]
            # finding TF for each job document
            for k in range(0, len(termFreq)):
                var1 = termFreq[k]
                var2 = sum(self.TF_Reversed_Corpus[job.id])
                job.TFvector.append(float(var1 / var2))

    '''
        Function to compute tf*idf vector for all fetched jobs
    '''
    def compute_TF_IDFs(self):

        terms = self.TF_Corpus.keys()
        jobIDs = self.TF_Reversed_Corpus.keys()

        idf_terms = {}
        for term in terms:
            termVector = self.TF_Corpus[term]
            occurance = 0
            for k in range(0,len(termVector)):
                if termVector[k] != 0:
                    occurance += 1
            idf_terms[term] = math.log(float(len(jobIDs) / occurance))

        #computing TF*IDF for every job document
        for job in Webscraper.jobs_fetched:
            for i in range(0,len(terms)):
                val = float(idf_terms[terms[i]])
                val2 = float(job.TFvector[i])
                job.TF_IDF.append(float(val * val2))

        self.term_IDFs = idf_terms