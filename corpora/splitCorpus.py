#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fileinput

import xml.etree.ElementTree as ET
#from lxml import etree as ET
#from lxml import objectify

baseDir = '/home/cristinae/pln/CLUBS/corpora'
idsFile = 'final_evaluation_IDs.dat'
corpusFile = 'corpus.xml'
pathFile = os.path.join(baseDir,corpusFile)


def main():

    # Read the file with the IDs separated for testing
    print ("Reading test IDs...")
    with open(os.path.join(baseDir,idsFile), 'r') as f:
        ids = [line.rstrip('\n') for line in f]
        
    # It is difficult to deal with namespaces in python
    # I just remove them
    for line in fileinput.input(pathFile, inplace=True):
        print line.replace(" xmlns=\"http://ns.clubs-project.eu\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"Corpus.xsd\"", ""),
        
    #Read the full corpus into a tree structure
    print ("Reading corpus...")
    tree = ET.parse(pathFile)
    root = tree.getroot()
    #objectify.deannotate(root, cleanup_namespaces=True)

    rootTest = ET.Element('clir-pubpsych-records-test')
    treeTest = ET.ElementTree(rootTest)
    rootTrain = ET.Element('clir-pubpsych-records-training')
    treeTrain = ET.ElementTree(rootTrain)
    print("Splitting XML according to the ID...")
    for record in root:
        recordAtributs = record.attrib
        if recordAtributs['id'] in ids:
            rootTest.append(record)
        else:
            rootTrain.append(record)

    treeTest.write('corpusTest.xml', encoding='utf-8', xml_declaration=True)
    treeTrain.write('corpusTrain.xml', encoding='utf-8', xml_declaration=True)

    #    treeTest.write('corpusTest.xml', encoding='utf-8', xml_declaration=True, default_namespace='%s' % corpusXmlns)    #for idTest in ids:
    #    element = root.find("xmlns:record[@id='%s']" % idTest, namespaces={'xmlns': 'http://ns.clirproject.net'})
    #    if (element is not None):
    #        print "kk"
    #        rootTest.append(element)
        #else:
        #    rootTrain.append(element)

    
if __name__ == "__main__":
    main()
