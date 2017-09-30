from org.cumcubble.tomatos.TomatoJSON import TomatoJSON
from elasticsearch.client import Elasticsearch
from org.cumcubble.tomatos.TomatoPrinter import TomatoPrinter
from org.cumcubble.tomatos.TomatoEnricher import TomatoEnricher

from org.cumcubble.tomatos.TomatoImagination import TomatoImagination

## main variables
io = TomatoJSON()
es = Elasticsearch()
tp = TomatoPrinter()
te = TomatoEnricher()
ti = TomatoImagination( io )

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

def enrichTomatos( category, inFile, outFile ):
    if category == 'types':
        io.setFile( inFile )
        tomatoList = io.fromFileToList()
        tomatoListTypes = []
        for tomato in tomatoList:
            tomatoTypes = te.addTypes( tomato )
            tomatoListTypes.append( tomatoTypes )
        io.setFile( outFile )
        io.fromListToFile( tomatoListTypes )
    
    if category == 'colors':
        io.setFile( inFile )
        tomatoList = io.fromFileToList()
        tomatoListColors = []
        for tomato in tomatoList:
            tomatoColor = te.addColors( tomato )
            tomatoListColors.append( tomatoColor )
        io.setFile( outFile )
        io.fromListToFile( tomatoListColors )

def getNewTomatos( outFile ):
    io.setFile( outFile )
    io.fromWebToFile( True )
    

## main program
if __name__ == '__main__':
    
    ## initial fetch
    print( "Initial fetch of Tomatos..." )
    getNewTomatos( outFile='tomatos01.json' )
    print( "Done\n" )
    
    ## enrichment
    print( "Adding colors..." )
    enrichTomatos( category='colors' ,  inFile='tomatos01.json' , outFile='tomatos02.json' )
    print( "Done\n" )
    print( "Adding types..." )
    enrichTomatos( category='types' ,  inFile='tomatos02.json' , outFile='tomatos03.json' )
    print( "Done\n" )
    
    ## images
    print( "Fetching images..." )
    ti.getTomatoImages( inFile='tomatos03.json' , outFolder='images' )
    ti.remove_missing_image_path( inFile='tomatos03.json', outFile='tomatos04.json' )
    print( "Done\n" )
    print( "Adding missing images..." )
    ti.add_missing_tomato_images( inFile='tomatos04.json', outFile='tomatos05.json' )
    print( "Done\n" )
    
    ## misc shit
    #importToElasticSearch( 'tomatos_types_colors.json' )
    #queryElasticSearch( 'types' )
    #queryElasticSearch( 'colors' )
    