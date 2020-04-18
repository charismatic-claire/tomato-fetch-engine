class Tomato(object):

    def __init__( self, name ):
        self.name = name
        
    def setName( self, name ):
        self.name = name
        
    def setDescription( self, description ):
        self.description = description
        
    def setImage( self, image ):
        self.image = image
    
    def setLink( self, link ):
        self.link = link
        
    def toString(self):
        print( self.name )
        try:
            print( "  ", self.image )
        except:
            pass
        try:
            print( "  ", self.description )
        except:
            pass
        try:
            print( "  ", self.link )
        except:
            pass
        print( "" )
        
    def toDictionary(self):
        d = {}
        d['name'] = self.name
        d['description'] = self.description.replace( '\xa0', '' )
        try:
            d['image'] = self.image
        except:
            pass
        try:
            d['link'] = self.link
        except:
            pass
        return d
    