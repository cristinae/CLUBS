#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math
import xml.etree.ElementTree as ET
from BeautifulSoup import BeautifulStoneSoup

import sentenceSplitter as SS
#from cStringIO import StringIO

baseDir = '/home/cristinae/pln/CLUBS/corpora'


def generateFiles(setName, prefixT, prefixA):
    ''' Generates the names of the output files for the four languages
    '''
    
    #output files for titles
    titlesEn = prefixT + 'en'
    titlesEs = prefixT + 'es'
    titlesDe = prefixT + 'de'
    titlesFr = prefixT + 'fr'
    titlesFiles = [titlesEn, titlesEs, titlesDe, titlesFr]

    #output files for abstracts
    abstractsEn = prefixA + 'en'
    abstractsEs = prefixA + 'es'
    abstractsDe = prefixA + 'de'
    abstractsFr = prefixA + 'fr'
    abstractsFiles = [abstractsEn, abstractsEs, abstractsDe, abstractsFr]

    return (titlesFiles, abstractsFiles)


def sentencify(fragment):
    ''' Cleans a string extracted from the xml file
    '''

    fragment = unicode(fragment)
    fragment = unicode(BeautifulStoneSoup(fragment, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))

    return fragment.encode("utf-8").replace(']','').replace('[','')
#    return fragment.encode("utf-8").strip('[]')+'\n'

 
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
    i = 0
    for record in root:
        titles = record.find('titles')
        titEn, titDe, titFr, titEs = None, None, None, None
	subEn, subDe, subFr, subEs = None, None, None, None
        if titles is not None:
           titEn = titles.find("title[@lang='en']")
           titDe = titles.find("title[@lang='de']")
           titFr = titles.find("title[@lang='fr']")
           titEs = titles.find("title[@lang='es']")
           subEn = titles.find("subtitle[@lang='en']")
           subDe = titles.find("subtitle[@lang='de']")
           subFr = titles.find("subtitle[@lang='fr']")
           subEs = titles.find("subtitle[@lang='es']")
        tits = [titEn, titDe, titFr, titEs]
        subs = [subEn, subDe, subFr, subEs]
        
        abstracts = record.find('abstracts')
        sEn, sDe, sFr, sEs = None, None, None, None
        if abstracts is not None:
           sEn = abstracts.find("abstract[@lang='en']")
           sDe = abstracts.find("abstract[@lang='de']")
           sFr = abstracts.find("abstract[@lang='fr']")
           sEs = abstracts.find("abstract[@lang='es']")
        sabs = [sEn, sDe, sFr, sEs]
        langs = ['en', 'de', 'fr', 'es',]

        for lang in zip(langs, tits, subs, sabs):
            if lang[1] is not None:
               handlers[prefixT+lang[0]].write(sentencify(lang[1].text)+'\n')
            if lang[2] is not None:
               handlers[prefixT+lang[0]].write(sentencify(lang[2].text)+'\n')
            if lang[3] is not None:
               sentences = SS.splitter(lang[0], sentencify(lang[3].text))
               for sentence in sentences:
                   handlers[prefixA+lang[0]].write(sentence+'\n')

    # Close the output files
    for fileName in titlesFiles + abstractsFiles:
        handlers[fileName].close

    
if __name__ == "__main__":
    
    if len(sys.argv) is not 2:
        sys.stderr.write('Usage: python %s train \n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1])
