CLuBS CORPORA EXTRACTION SCRIPTS
--------------------------------

Scripts to extract parallel and monolingual corpora from an xml dump of the
PubPshyc database


### Contents

- README 
- splitCorpus.py 
- extractParallelCorpus.py
- extractMonolingualCorpus.py 
- sentenceAligner.py
- sentenceSplitter.py
- splitAbstractSentences.py
- final_evaluation_corpus_950.dat
- final_testcorpus_MT.dat
- final_testIDs.dat


### Pipeline

1. Split the original xml file into training and test according to a list of
   IDs for testing (final_testIDs.dat)

   python splitCorpus.py


2. Extract the parallel corpora for the three language pairs for the desired partition

   python extractParallelCorpus.py test950
   python extractParallelCorpus.py train


3. Extract the monolingual corpora for the four languages

   python extractMonolingualCorpus.py train



