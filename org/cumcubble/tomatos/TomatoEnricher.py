import pprint
import re

class TomatoEnricher(object):

    def print( self, tomato ):
        pp = pprint.PrettyPrinter()
        pp.pprint( tomato )
        
    def addTypes( self, tomato ):
        types = re.findall( '\w*tomate' , tomato['description'] )
        types = list( set( types ) )
        if types:
            tomato['types'] = types
        return tomato
    
    def addColors( self, tomato ):
        query_colors = [ 'rot', 'gelb', 'orange', 'rosa', 'grün', 'lila', 'violett', 'weiß', 'braun' ]
        found_colors = []
        for color in query_colors:
            if re.search( '\w*' + color + '\w*' , ( str( tomato['name'] ) + ' ' + str( tomato['description'] ) ).lower() ):
                found_colors.append( color )
        if found_colors:
            tomato['colors'] = found_colors
        return tomato
        