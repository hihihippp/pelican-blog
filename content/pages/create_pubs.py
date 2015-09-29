#!/usr/bin/env python 


import bibtexparser
import re
import time

import pandas as pd

from nameparser import HumanName 

def parseLink(record):
    """
    creates a PDF link for paper
    """
    link = " [[PDF]](http://tillbergmann.com/papers/{})".format(record['pdf'])
    return link

def parseTitle(record, emph=False):
    """
    parses the author, year and title for a given record. Emphasises title if emph=True
    """
    authors = parseNames(record['author'])
    t = re.sub('\\\\\emph{(.+)}',r'*\1*', record['title'])
    if emph: t = '*{}*'.format(t)
    title = "{authors} ({year}). {title}.".format(
        authors = authors,
        year = record['year'],
        title = t)
    return title


# In[409]:

def parseNames(authors):
    """
    parses the author names, returning a formatted string
    """

    names = [HumanName(x) for x in authors.split('and')]
    out = []
    for name in names:
        name.first = name.first[0] + '.'
        name.string_format = "{last}, {first} {middle}, {suffix}"
        if str(name) == 'Bergmann, T.': 
            name = '**Bergmann, T.**'
        out.append(str(name))
    if len(out)>1:
        s = " & ".join([", ".join(out[:-1]),out[-1]])
    else:
        s = out[0]
    return s



def parseChapter(record):
    editors = parseNames(record['editor'])
    t = parseTitle(record)
    s = t + " In {ed} (Eds.), *{booktitle}*, {pages}. {location}: {publisher}.".format(
        ed = editors,
        booktitle = record['booktitle'],
        pages = record['pages'],
        location = record['address'],
        publisher = record['publisher'])
    return s


def parseArticle(record):
    authors = parseNames(record['author'])
    t = parseTitle(record)
    s = t +" *{journal}*".format(
        journal = record['journal'])
    if 'volume' in record.keys(): s += ', *{}*'.format(record['volume'])
    if 'issue' in record.keys(): s += '({})'.format(record['issue'])
    if 'pages' in record.keys(): s += ', {}'.format(re.sub('--', '-', record['pages']))
    
    return s + '.'


def parseTalks(record):
    authors = parseNames(record['author'])
    t = parseTitle(record, emph=True)
    s = t + " {loc}".format(
        loc = record['howpublished'])
    if s[-1] != '.': s += '.'
    return s


def parseRow(row):
    row = row[~row.isnull()].to_dict()
    if row['type'] == 'article':
        s = parseArticle(row)
    elif row['type'] in ['incollection', 'inproceedings']:
        s = parseChapter(row)
    else:
        s = parseTalks(row)
#     print(row.keys())
    if 'pdf' in row.keys(): s += parseLink(row)
    return '* ' + s + '\n'


with open("refs.bib") as fh:
    data = fh.read()

bib_database = bibtexparser.loads(data)

pubs = pd.DataFrame.from_records(bib_database.entries)

p_out = []
papers = pubs[pubs['type']!='misc'].sort('year', ascending=False)
for idx, row in papers.iterrows():
    p_out.append((parseRow(row)))
    
t_out = []
talks = pubs[pubs['type']=='misc'].sort('year', ascending=False)
for idx, row in talks.iterrows():
    t_out.append(parseRow(row))

output = """Title: CV

I'm currently updating my full CV. Please find a list of publications below:

# Publications

<small>*Last updated: {}*</small>

## Papers

{}

## Talks and Posters

{}
""".format(time.strftime("%m/%d/%Y"), "".join(p_out), "".join(t_out))



with open('cv.md', 'w') as fh:
    fh.write(output)