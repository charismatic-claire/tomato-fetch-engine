from lxml import html
import requests
from org.cumcubble.tomatos.TomatoGenerator import TomatoGenerator

class TomatosFromURL(object):

    def generateTomatos( self, url ):
        ## fetch stuff
        page = requests.get( url )
        tree = html.fromstring( page.content )
        posts = tree.xpath( '//div[@itemprop="blogPost"]' )

        ## create tomatos from posts
        tg = TomatoGenerator()
        tomatos = []
        for post in posts:
            tomato = tg.generateTomato( post )
            tomatos.append( tomato )
            
        ## return tomatos
        return tomatos
    
    def generate_list_of_image_urls( self, url ):
        ## fetch stuff
        page = requests.get( url )
        tree = html.fromstring( page.content )
        tomato_ul = tree.xpath( '//li[@class="sige_cont_0"]' )
        
        ## create image paths
        image_urls = []
        for list_item in tomato_ul:
            image_url = list_item.xpath( 'span/a/@href' )
            image_urls.append( image_url )
        
        ## return result
        return image_urls;
