# -*- coding: utf-8 -*-

import re


def splitter(language, text):
    ''' Function to load the language-specific information
    '''

    # Note: These are note exactly moses files: lowercase letters have to be removed
    filePrefixes = './nonbreaking_prefixes/nonbreaking_prefix.' + language

    prefixes = ''
    prefixList = []
    with open(filePrefixes, "r") as f:
         for line in f:
             if not line.startswith("#"):         # This eliminates line comments
                 line = line.strip()
                 line = line.split('#', 1)[0]     # This eliminates inline comments
                 if line is not '':
                     line = line.replace(".","\.")
                     prefixList.append(line)
         prefixes = '|'.join(prefixList)

    return split_into_sentences(prefixes, text)


def split_into_sentences(prefixes, text):
    ''' Sentence splitter version from:
    http://stackoverflow.com/questions/4576077/python-split-text-on-sentences
    '''

    caps = "([A-Z])"

    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|de|es|fr|uk|eu)"
    
    #prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    prefixes = '('+prefixes+')[.]'
    # @TODO: make it language independent as the prefixes
    # (probably not relevant for the CLuBS project)
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"

    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(". ",".<stop>")
    text = text.replace("? ","?<stop>")
    text = text.replace("! ","!<stop>")
    text = text.replace("<prd>",".")

    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]

    return sentences
