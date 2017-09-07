from org.cumcubble.tomatos.TomatoJSON import TomatoJSON
from elasticsearch.client import Elasticsearch
from org.cumcubble.tomatos.TomatoPrinter import TomatoPrinter

if __name__ == '__main__':

    ## init
    io = TomatoJSON( 'tomatos_enriched.json' )
    es = Elasticsearch()
    tp = TomatoPrinter()
         
    ## load data
    tomatoList = io.fromFileToList()
    
    ## import to elasticsearch
    #es.indices.delete( index='tomatos' )
    #tomatoId = 1
    #for tomato in tomatoList:
    #    result = es.index( index='tomatos' , doc_type='profiles', id=tomatoId, body=tomato )
    #    tomatoId += 1
    #    print( result )
    
    ## find all tags
    tags = set()
    for tomato in tomatoList:
        try:
            for tag in tomato['tags']:
                tags.add( tag )
        except:
            pass
         
    ## query elasticsearch
    for tag in tags:
        query = '{ "query":  { "match": { "tags": "' + tag + '" } } }'
        response = es.search( index='tomatos', doc_type='profiles', body=query, size=5 )
        result = response['hits']
        print( '-------- ' + tag + ' --------')
        tp.print( result )
         