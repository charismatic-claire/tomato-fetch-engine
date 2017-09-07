from org.cumcubble.tomatos.TomatosFromURL import TomatosFromURL
import json

class TomatoJSON(object):

    def __init__( self, file ):
        self.file = file
        
    def setFile(self, file ):
        self.file = file
        
    def fromWebToFile( self ):
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
        
        ## export to json file
        with open( self.file, mode='w', encoding='utf-8' ) as tomatoFile:
            json.dump( tomatoList, tomatoFile, indent=2 )

    def fromFileToList( self ):
        with open( self.file, mode='r', encoding='utf-8' ) as tomatoFile:
            tomatoList = json.load( tomatoFile )
        return tomatoList

    def fromListToFile( self, tomatoList ):
        with open( self.file, mode='w', encoding='utf-8' ) as tomatoFile:
            json.dump( tomatoList, tomatoFile, indent=2 )