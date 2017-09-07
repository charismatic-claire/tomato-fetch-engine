
class TomatoPrinter(object):

    def print(self, tomatoList ):
        print( 'total:', tomatoList['total'] )
        print()
        for tomato in tomatoList['hits']:
            print( '* name:', tomato['_source']['name'] )
            print( '  score:', tomato['_score'] )
            print( '  description:', str(tomato['_source']['description'])[:75], '...' )
            if tomato['_source']['tags']:
                print( '  tags:', tomato['_source']['tags'] )
            print()
        