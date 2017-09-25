from lxml import html
import requests
from org.cumcubble.tomatos.Tomato import Tomato

class TomatoGenerator(object):
    
    def getName( self, post ):
        name = post.xpath( 'div[@class="page-header"]/h2/text()' )
        if not name:
            name = post.xpath( 'h1/text()' )   
        return name    

    def getImage(self, post ):
        image = post.xpath( 'p/img/@src' )
        if not image:
            image = post.xpath( 'p/strong/img/@src' )
        return image

    def getDescription( self, post ):
        description = post.xpath( 'p/text()' )
        return description
    
    def enhanceDescription( self, link ):
        ## fetch stuff
        page = requests.get( 'http://www.birgit-kempe-tomaten.de/' + link )
        tree = html.fromstring( page.content )
        post = tree.xpath( '//div[@itemprop="articleBody"]' )
        ## get new description
        new_description = ""
        if post:
            descriptions = post[0].xpath( 'p/text()' )
            for description in descriptions:
                new_description = new_description + " " + description
        ## return result
        return [new_description.strip()]
    
    def getLink( self, post ):
        link = post.xpath( 'p[@class="readmore"]/a/@href' )
        return link
    
    def generateTomato( self, post ):
        ## get values
        name = self.getName( post )
        image = self.getImage( post )
        description = self.getDescription( post )
        link = self.getLink( post )
        if link:
            description = self.enhanceDescription( link[0] )
        
        ## create tomato
        tomato = Tomato( name[0].strip() )
        if description:
            tomato.setDescription( " ".join( description ) )
        if image:
            tomato.setImage( image[0].replace( '/images/stories/tomaten', 'images' ) )
        if link:
            tomato.setLink( link[0] )
            
        ## return tomato
        return tomato
