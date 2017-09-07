import pprint
import re

class TomatoEnricher(object):

    def print( self, tomato ):
        pp = pprint.PrettyPrinter()
        pp.pprint( tomato )
        
    def addTags( self, tomato ):
        tags = re.findall( '\w*tomate' , tomato['description'] )
        tags = list( set( tags ) )
        if tags:
            tomato['tags'] = tags
        return tomato
        