#!/usr/bin/python

# a daily summary of the activity of a tsm server. (pipe to a mail user agent)
verbose = True
debug = 1
queries = ['drive',
          'volume devclass=disk',
          'libvolume',
          'db',
          'log',
          'volhistory type=dbbackup',
          'actlog search=ANR????E',
          ]

import csv
import optparse
import sys
import tempfile
try:
  sys.path.index('/root/pydsm/')
except ValueError:
  sys.path.append('/root/pydsm/')

import pydsm2

def listqueries(option,opt,value,parser):  # optarse always passes four values
  """list the queries to be made of tivoli storage manager."""
  print "queries are:"
  for i in queries:
    print str(queries.index(i) ) + " query " + i
  parser.values.querieslisted = True

def explainqueries(option,opt,value,parser): 
  """accept an int, return the tivoli help text for the option selected."""
  print value
  try:
    helptext=pydsm2.runcommand("help query " + str(queries[value]))
  except IndexError:
    print """Error looking up the index number you entered.
Try using the -l switch to find a valid index number.
          """
  for i in helptext:
    print i,
  parser.values.explainqueries = True

parser = optparse.OptionParser()
parser.add_option("-l","--list-queries", action="callback",
                                          callback=listqueries)
parser.add_option("-e","--explain-queries", action="callback",
                  callback=explainqueries, type="int", dest="queryindex")
(options, args) = parser.parse_args()

if len(sys.argv) == 1 :
  alerts = []
  data = {}
  for i in queries:
    print "query " + i
    data[i] = []
    rowsofcsv = csv.reader(pydsm2.runcommand("query " + i))
    for row in rowsofcsv:
      print row
      data[i].append(row)
  print "DATA"
  print data['drive']
  print "Number of Drives: " + str(len(data['drive']))
  for j in data['drive']:
    print repr(j[3])

if debug >= 2:
  print "options supplied:"
  print options
  print "\n"
  print "arguments supplied:"
  print args
  print "\n"


