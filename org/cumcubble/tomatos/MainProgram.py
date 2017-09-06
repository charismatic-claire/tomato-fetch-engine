from org.cumcubble.tomatos.TomatosFromURL import TomatosFromURL
import json
import pprint

def fetchFromWeb():
    ## generate list of tomatos
    tfu = TomatosFromURL()
    tomatos = tfu.generateTomatos( 'http://www.birgit-kempe-tomaten.de/index.php/de/tomatensorten-a-d' )
    tomatos.extend( tfu.generateTomatos( 'http://www.birgit-kempe-tomaten.de/index.php/de/tomatensorten-e-h' ) )
    tomatos.extend( tfu.generateTomatos( 'http://www.birgit-kempe-tomaten.de/index.php/de/tomatensorten-i-l' ) )
    tomatos.extend( tfu.generateTomatos( 'http://www.birgit-kempe-tomaten.de/index.php/de/tomatensorten-m-p' ) )
    tomatos.extend( tfu.generateTomatos( 'http://www.birgit-kempe-tomaten.de/index.php/de/tomatensorten-q-u' ) )
    tomatos.extend( tfu.generateTomatos( 'http://www.birgit-kempe-tomaten.de/index.php/de/tomatensorten-v-z' ) )

    ## list to dict
    tomatoList = []
    for tomato in tomatos:
        tomatoList.append( tomato.toDictionary() )
    tomatoDict = {}
    tomatoDict['tomatos'] = tomatoList

    ## export to json file
    with open( 'tomatos.json', mode='w', encoding='utf-8' ) as tomatoFile:
        json.dump( tomatoDict, tomatoFile, indent=2 )

def loadFromFile():
    with open( 'tomatos.json', mode='r', encoding='utf-8' ) as tomatoFile:
        tomatoDict = json.load( tomatoFile )
    return tomatoDict


## main program
if __name__ == '__main__':
    ## fetch from web
    #fetchFromWeb()

    ## load and print
    tomatoDict = loadFromFile()
    pp= pprint.PrettyPrinter( indent=1, compact=True )
    pp.pprint( tomatoDict )