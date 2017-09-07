from org.cumcubble.tomatos.TomatoJSON import TomatoJSON
from elasticsearch.client import Elasticsearch
from org.cumcubble.tomatos.TomatoPrinter import TomatoPrinter
from org.cumcubble.tomatos.TomatoEnricher import TomatoEnricher

## main variables
io = TomatoJSON( 'tomatos.json' )
es = Elasticsearch()
tp = TomatoPrinter()
te = TomatoEnricher()

## main functions
def importToElasticSearch( file ):
    io.setFile( file )
    tomatoList = io.fromFileToList()
    es.indices.delete( index='tomatos' )
    tomatoId = 1
    for tomato in tomatoList:
        result = es.index( index='tomatos' , doc_type='profiles', id=tomatoId, body=tomato )
        tomatoId += 1
        print( result )
    
def queryElasticSearch( category ):
    if category == 'types':
        ## find all types
        io.setFile( 'tomatos_types_colors.json' )
        tomatoList = io.fromFileToList()
        types = set()
        for tomato in tomatoList:
            try:
                for tomatoType in tomato['types']:
                    types.add( tomatoType )
            except:
                pass
        ## query all types
        for tomatoType in types:
            query = '{ "query":  { "match": { "types": "' + tomatoType + '" } } }'
            response = es.search( index='tomatos', doc_type='profiles', body=query, size=5 )
            result = response['hits']
            print( '-------- ' + tomatoType + ' --------')
            tp.print( result )
    
    if category == 'colors':
        colors = [ 'rot', 'gelb', 'orange', 'rosa', 'grün', 'lila', 'violett', 'weiß', 'braun' ]
        for color in colors:
            query = '{ "query":  { "match": { "colors": "' + color + '" } } }'
            response = es.search( index='tomatos', doc_type='profiles', body=query, size=5 )
            print( '-------- ' + color + ' --------')
            result = response['hits']
            tp.print( result )

def enrichTomatos( category ):
    if category == 'types':
        io.setFile( 'tomatos.json' )
        tomatoList = io.fromFileToList()
        tomatoListTypes = []
        for tomato in tomatoList:
            tomatoTypes = te.addTypes( tomato )
            tomatoListTypes.append( tomatoTypes )
        io.setFile( 'tomatos_types.json' )
        io.fromListToFile( tomatoListTypes )
    
    if category == 'colors':
        io.setFile( 'tomatos_types.json' )
        tomatoList = io.fromFileToList()
        tomatoListColors = []
        for tomato in tomatoList:
            tomatoColor = te.addColors( tomato )
            tomatoListColors.append( tomatoColor )
        io.setFile( 'tomatos_types_colors.json' )
        io.fromListToFile( tomatoListColors )

## main program
if __name__ == '__main__':
    #enrichTomatos( 'colors' )
    #importToElasticSearch( 'tomatos_types_colors.json' )
    queryElasticSearch( 'types' )
    queryElasticSearch( 'colors' )