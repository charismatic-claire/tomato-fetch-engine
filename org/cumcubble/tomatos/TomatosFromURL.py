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
