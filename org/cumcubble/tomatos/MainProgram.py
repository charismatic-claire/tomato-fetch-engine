from org.cumcubble.tomatos.TomatoJSON import TomatoJSON
from elasticsearch.client import Elasticsearch
from org.cumcubble.tomatos.TomatoPrinter import TomatoPrinter
from org.cumcubble.tomatos.TomatoEnricher import TomatoEnricher
from pathlib import Path
import json
import urllib.request

## main variables
io = TomatoJSON()
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
    
def getTomatoImages( inFile, outFolder ):
    ## init
    with open( inFile, mode='r', encoding='utf-8' ) as tomato_file:
        tomato_list = json.load( tomato_file )
    prefix = 'http://www.birgit-kempe-tomaten.de/images/stories/tomaten/'
    
    ## get all urls
    urls = []
    for tomato in tomato_list:
        try:
            tomato_image = tomato['image']
            tomato_image = tomato_image.replace( 'images/', '' )
            urls.append( prefix + tomato_image )
        except:
            pass
        
    ## download images
    for url in urls:
        file_name = url.replace( 'http://www.birgit-kempe-tomaten.de/images/stories/tomaten', outFolder )
        try:
            urllib.request.urlretrieve( url, file_name )
        except:
            print( 'Failed to download ' + url + '.' )
            
def remove_missing_image_path( inFile, imageFolder, outFile ):
    ## initialize
    io.setFile( inFile )
    tomatoList = io.fromFileToList()
    ## loop
    tomatoList2 = []
    for tomato in tomatoList:
        try:
            image_file = Path( tomato['image'] )
            if not image_file.is_file():
                print( 'Deleting ' + tomato['image'] )
                del tomato['image']
        except KeyError:
            pass
        tomatoList2.append( tomato )
    ## write out
    io.setFile( outFile )
    io.fromListToFile( tomatoList2 )

## main program
if __name__ == '__main__':
    
    ## initial fetch
    #getNewTomatos( outFile='tomatos3.json' )
    
    ## enrichment
    enrichTomatos( category='colors' ,  inFile='tomatos3.json' , outFile='tomatos3_enriched.json' )
    enrichTomatos( category='types' ,  inFile='tomatos3_enriched.json' , outFile='tomatos3_enriched.json' )
    
    ## fetch images
    #getTomatoImages( inFile='tomatos3.json' , outFolder='images' )
    
    ## remove missing images
    remove_missing_image_path( inFile='tomatos3_enriched.json', imageFolder='', outFile='tomatos3_enriched.json' )
    
    ## misc shit
    #importToElasticSearch( 'tomatos_types_colors.json' )
    #queryElasticSearch( 'types' )
    #queryElasticSearch( 'colors' )
    