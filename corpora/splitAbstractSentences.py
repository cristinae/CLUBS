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


def sentencify(fragment):
    ''' Cleans a string extracted from the xml file
    '''

    fragment = unicode(fragment)
    # no need, it will be written as xml
    #fragment = unicode(BeautifulStoneSoup(fragment, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))

    return fragment.encode("utf-8").replace(']','').replace('[','')
#    return fragment.encode("utf-8").strip('[]')+'\n'

 
def main(setName):

    corpusIn = 'corpus'+setName.capitalize()+'.xml'
    corpusIn = 'corpus'+setName+'.xml'
    corpusOut = 'corpus'+setName.capitalize()+'.KKsnt.xml'

    # Read the full corpus into a tree structure
    print ("Reading corpus...")
    tree = ET.parse(os.path.join(baseDir,corpusIn))
    root = tree.getroot()

    # Open the output file
    #f = open(corpusOut, "w")

    print("Exploring the tree...")
    i = 0
    for record in root:
       
        abstracts = record.find('abstracts')
        sEn, sDe, sFr, sEs = None, None, None, None
        if abstracts is not None:
           sEn = abstracts.find("abstract[@lang='en']")
           sDe = abstracts.find("abstract[@lang='de']")
           sFr = abstracts.find("abstract[@lang='fr']")
           sEs = abstracts.find("abstract[@lang='es']")
        sabs = [sEn, sDe, sFr, sEs]
        langs = ['en', 'de', 'fr', 'es',]

        for lang in zip(langs, sabs):
            if lang[1] is not None:
	       #raw_input('ss')
               sentences = SS.splitter(lang[0], sentencify(lang[1].text))
	       abstractSentences = '\n'.join(sentences)
	       #sys.stderr.write(sentences[0])
	       lang[1].text = abstractSentences.decode('utf-8','strict')
	       #print(lang[1].text)

    # Close the output files
    tree.write(corpusOut, encoding='utf-8')
    #f.close

    
if __name__ == "__main__":
    
    if len(sys.argv) is not 2:
        sys.stderr.write('Usage: python %s test950 \n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1])
