#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math
import xml.etree.ElementTree as ET
from BeautifulSoup import BeautifulStoneSoup

import sentenceAligner as SA
import sentenceSplitter as SS
#from cStringIO import StringIO

baseDir = '/home/cristinae/pln/CLUBS/corpora'
minlen = 5 # minimum length for a sentence in the abstract to be considered

def generateFiles(setName, prefixT, prefixA):
    ''' Generates the names of the output files for the three language pairs
    '''
    
    #output files for titles
    titlesEsEnEn = prefixT + 'en-es.en'
    titlesEsEnEs = prefixT + 'en-es.es'
    titlesDeEnEn = prefixT + 'en-de.en'
    titlesDeEnDe = prefixT + 'en-de.de'
    titlesFrEnEn = prefixT + 'en-fr.en'
    titlesFrEnFr = prefixT + 'en-fr.fr'
    titlesFiles = [titlesEsEnEn, titlesEsEnEs, titlesDeEnEn,
                   titlesDeEnDe, titlesFrEnEn, titlesFrEnFr]

    #output files for abstracts
    abstractsEsEnEn = prefixA + 'en-es.en'
    abstractsEsEnEs = prefixA + 'en-es.es'
    abstractsDeEnEn = prefixA + 'en-de.en'
    abstractsDeEnDe = prefixA + 'en-de.de'
    abstractsFrEnEn = prefixA + 'en-fr.en'
    abstractsFrEnFr = prefixA + 'en-fr.fr'
    abstractsFiles = [abstractsEsEnEn, abstractsEsEnEs, abstractsDeEnEn,
                      abstractsDeEnDe, abstractsFrEnEn, abstractsFrEnFr]

    return (titlesFiles, abstractsFiles)


def sentencify(fragment):
    ''' Cleans a string extracted from the xml file
    '''

    fragment = unicode(fragment)
    fragment = unicode(BeautifulStoneSoup(fragment, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))

    cleanFrag = fragment.encode("utf-8").replace(']','').replace('[','')
    if (cleanFrag.isupper()):
	return cleanFrag.lower()

    return cleanFrag

#    return fragment.encode("utf-8").strip('[]')+'\n'



def getGaussian(srcLan, tgtLan):
    ''' Mean and sigma values that characterise a normal distribution describing the different length
        among languages. Values for the distribution have been estimated from MT parallel corpora. 
    '''
    
    gaussian = { 'deen': (0.961, 0.463),
                 'ende': (1.176, 0.926),
                 'esen': (0.926, 0.441),
                 'enes': (1.133, 0.415),
                 'fren': (0.914, 0.313),
                 'enfr': (1.158, 0.411)
    }

    return gaussian[srcLan+tgtLan]


def lengthFactor(srcLen, trgLen, mu, sigma):
    ''' Length factor estimation. It assumes that the variation of the length ratio between two different
        languages approximately follows a normal distribution.
        "Automatic Identification of Document Translations in Large Multilingual Document Collections"
        Bruno Pouliquen, Ralf Steinberger & Camelia Ignat 
    '''

    base = ((float(trgLen)/float(srcLen)) - mu) / sigma;
    pot = -0.5 * math.pow(base, 2);

    return math.exp(pot);



def alignTitles(tit, sub, titEn, subEn, mu, sigma):
    ''' Function to align titles that might (or might not) be composed of a field Title and a field Subtitle.
        We assume that the ratio of the length of sentences (length factor) in two different languages follows 
        a normal distribution with mean 'mu' and sigma 'sigma'. The closest the length factor of a new sentence 
        pair to the mean is, the more probable it belongs to the distribution.
    '''
    tit = sentencify(tit.text)
    titEn = sentencify(titEn.text)
    lan = False
    lanEn = False

    # We know that the two titles exist, let's see if subtitles exist
    #if sub is not None:
    if sub is not None:       
       sub = sentencify(sub.text)
       lan = True
    if subEn is not None:
       subEn = sentencify(subEn.text)
       lanEn = True

    # Heuristic for the aligment: given a Gaussian distribution of the ratio of sentence length between two languages,
    # the sentence pair with a ratio closer to the mean is the most probable one
    fragment = ''
    fragmentEn = ''
    # We distinguish 4 cases:
    if not lan and not lanEn:     # None of the languages has subtitle
       fragment = tit
       fragmentEn = titEn
    elif lan and not lanEn:       # Only L1 has subtitle
       titSub = tit + ' ' + sub
       fragmentEn = titEn
       lfTitSub = lengthFactor(len(titSub), len(titEn), mu, sigma)
       lfTit = lengthFactor(len(tit), len(titEn), mu, sigma)
       if math.fabs(lfTitSub-1) <=  math.fabs(lfTit-1):  # The best option is the closest to 1
          fragment = titSub
       else:
          fragment = tit
    elif lanEn and not lan:       # Only L2 (en) has subtitle
       titSubEn = titEn + ' ' + subEn
       fragment = tit
       lfTitSub = lengthFactor(len(tit), len(titSubEn), mu, sigma)
       lfTit = lengthFactor(len(tit), len(titEn), mu, sigma)
       if math.fabs(lfTitSub-1) <=  math.fabs(lfTit-1):  # The best option is the closest to 1
          fragmentEn = titSubEn
       else:
          fragmentEn = titEn
    elif lan and lanEn:   # Both languages have subtitle. No guesses here
       fragment = tit + ' ' + sub
       fragmentEn = titEn + ' ' + subEn
        

    return (fragment, fragmentEn)


 
def main(setName):

    corpusIn = 'corpus'+setName.capitalize()+'.xml'
    prefixT = 'pubPsych.titles.'+setName+'.'
    prefixA = 'pubPsych.abstracts.'+setName+'.'
    (titlesFiles, abstractsFiles) = generateFiles(setName, prefixT, prefixA)

    # Read the full corpus into a tree structure
    print ("Reading corpus...")
    tree = ET.parse(os.path.join(baseDir,corpusIn))
    root = tree.getroot()

    # Open the output files
    handlers = {}
    for fileName in titlesFiles + abstractsFiles:
        f = open(fileName, "w")
        handlers[fileName] = f
    
    print("Exploring the tree...")
    # We asume that English is always one side of the parallel corpus
    # (and discard the cases where it is not)
    i = 0
    for record in root:
        #ET.dump(record)
        titles = record.find('titles')
        if titles is not None and len(titles) > 1:
            langs = []
            for title in titles:
                if title.attrib['lang'] != 'en' and title.tag == 'title':
                    langs.append(title.attrib['lang'])
            for lang in langs:
                filename = "%sen-%s.%s" % (prefixT, lang, lang)
                filenameEn = "%sen-%s.en" % (prefixT, lang)
                tit = titles.find("title[@lang='%s']" % lang)
                titEn = titles.find("title[@lang='en']")
                if titEn is not None:
                #if titEn:
                    sub = titles.find("subtitle[@lang='%s']" % lang)
                    subEn = titles.find("subtitle[@lang='en']")
                    (mu, sigma) = getGaussian(lang, 'en')
                    (fragmentLan, fragmentEn) = alignTitles(tit, sub, titEn, subEn, mu, sigma)
                    handlers[filename].write(fragmentLan+'\n')
                    handlers[filenameEn].write(fragmentEn+'\n')

        abstracts = record.find('abstracts')
        if abstracts is not None and len(abstracts) > 1:
            langs = []
            for abstract in abstracts:
                if abstract.attrib['lang'] != 'en':
                    langs.append(abstract.attrib['lang'])
                    #print abstract.text
            for lang in langs:
                filename = "%sen-%s.%s" % (prefixA, lang, lang)
                filenameEn = "%sen-%s.en" % (prefixA, lang)
                s = abstracts.find("abstract[@lang='%s']" % lang)
                sEn = abstracts.find("abstract[@lang='en']")
                if sEn is not None:  
                #if sEn:
                    sourceList = SS.splitter(lang, sentencify(s.text))
                    targetList = SS.splitter('en', sentencify(sEn.text))
                    aligned = SA.alignLists(sourceList, targetList)
                    for alignedSentence in aligned:
                        sentence = alignedSentence.split('\t')
			if (sentence[0] and sentence[1]):
                             if (len(sentence[0])>minlen and len(sentence[1])>minlen):
  	                         handlers[filename].write(sentence[0]+'\n')
         	                 handlers[filenameEn].write(sentence[1]+'\n')
 

    # Close the output files
    for fileName in titlesFiles + abstractsFiles:
        handlers[fileName].close

    
if __name__ == "__main__":
    
    if len(sys.argv) is not 2:
        sys.stderr.write('Usage: python %s train|test \n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1])
