"""
Load data from json file to ElasticSearch
Read an array of json objects, indexing each json object
"""

__author__ = 'saggu'

import json
from elasticsearch import Elasticsearch
from sys import stderr
import sys
import argparse

def loadDatainES(filename, index, doctype,dataFileType,hostname="localhost",port=9200,mappingFilePath=None,username="",password="",protocol="http"):
    try:
        print "Connecting to " + hostname + " at port:" + str(port) 
       # es = Elasticsearch([{'host': hostname, 'port': port}])

        if username is not None and password is not None:
            es = Elasticsearch([protocol + '://' + username + ':' + password + '@'+hostname + ":" + str(port)],show_ssl_warnings=False)
        else:
            es = Elasticsearch([protocol + '://'+hostname + ":" + str(port)],show_ssl_warnings=False)
        if mappingFilePath:
            with open(mappingFilePath) as m:
                mapping = m.read()
                #print "Mapping file:" + mapping
                es.indices.create(index=index,  body=mapping,ignore=400)
                
        if dataFileType=="1":
            with open(filename) as f:   
                d = json.load(f)
                for wp in d:
                  res = es.index(index=index,doc_type=doctype,body=wp,id=wp["uri"])
                  print "indexing id: " + res["_id"] + " for uri: " + wp["uri"]
        elif dataFileType == "0":
            with open(filename) as f:
                lines = f.readlines()

                for line in lines:
                    if line.strip() != "":
                        jsonurlobj = json.loads(line.strip())
                        objkey = jsonurlobj['uri']
                        print objkey
                        res = es.index(index=index,doc_type=doctype,body=line,id=objkey)
                        #print "indexing id: " + res["_id"] + " for uri: " + objkey
    except Exception, e:
        print e
        print >> stderr.write('ERROR: %s\n' % str(e))
        



if __name__ == '__main__':
    
    argp = argparse.ArgumentParser()
    argp.add_argument("-hostname",help="Elastic Search Server hostname, defaults to 'localhost'",default="localhost")
    argp.add_argument("-port",type=int, help="Elastic Search Server port,defaults to 9200",default=9200)
    argp.add_argument("-mappingFilePath", help="mapping/setting file for the index")
    argp.add_argument("-username", help="username for elasticsearch")
    argp.add_argument("-password", help="password for elasticsearch")
    argp.add_argument("-protocol", help="http or https")
    argp.add_argument("filepath",help="json file to be loaded in ElasticSearch")
    argp.add_argument("indexname",help="desired name of the index in ElasticSearch")
    argp.add_argument("doctype",help="type of the document to be indexed")
    argp.add_argument("dataFileType", help="Specify '0' if every line in the data file is different json object  or '1' otherwise")
    arguments = argp.parse_args()
    
    if arguments.hostname and arguments.port:
        loadDatainES(arguments.filepath, arguments.indexname, arguments.doctype,arguments.dataFileType,arguments.hostname, arguments.port,arguments.mappingFilePath,arguments.username,arguments.password,arguments.protocol)
    else:
        loadDatainES(arguments.filepath, arguments.indexname, arguments.doctype,arguments.dataFileType,arguments.mappingFilePath,arguments.username,arguments.password,arguments.protocol)
    
    print "Thats all folks!"
