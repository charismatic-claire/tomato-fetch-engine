
class TomatoPrinter(object):

    def print(self, tomatoList ):
        print( 'total:', tomatoList['total'] )
        print()
        for tomato in tomatoList['hits']:
            print( '* name:\t\t', tomato['_source']['name'] )
            print( '  score:\t', tomato['_score'] )
            print( '  description:\t', str(tomato['_source']['description'])[:75], '...' )
            try:
                print( '  types:\t', tomato['_source']['types'] )
            except:
                pass
            try:
                print( '  colors:\t', tomato['_source']['colors'] )
            except:
                pass
            print()
        