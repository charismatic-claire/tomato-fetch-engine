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
        query_colors = [ 'rot', 'gelb', 'orange', 'rosa', 'grün', 'lila', 'creme'
            'violett', 'weiß', 'braun', 'blau', 'schwarz', 'purpur', 'gold', 'bronze' ]
        found_colors = []
        for color in query_colors:
            if re.search( '.*' + color + '.*' , ( str( tomato['name'] ) + ' ' + str( tomato['description'] ) ).lower() ):
                found_colors.append( color )
        if re.search( '.*ocker*.', ( str( tomato['name'] ) + ' ' + str( tomato['description'] ) ).lower() ):
            if not re.search( '.*locker*.', ( str( tomato['name'] ) + ' ' + str( tomato['description'] ) ).lower() ):
                found_colors.append( 'ocker' )
        if found_colors:
            tomato['colors'] = found_colors
        return tomato
        