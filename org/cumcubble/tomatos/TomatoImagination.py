import json
import urllib.request
from pathlib import Path
from org.cumcubble.tomatos.TomatosFromURL import TomatosFromURL
from copy import deepcopy

class TomatoImagination(object):
    """
    Class to add images to tomatos in tomato file
    """
    
    def __init__( self, io ):
        """
        Constructor
        """
        self.io = io
    
    def getTomatoImages( self, inFile, outFolder ):
        """
        Fetch the images from their path per tomato
        """
        ## init
        with open( inFile, mode='r', encoding='utf-8' ) as tomato_file:
            tomato_list = json.load( tomato_file )
        prefix = 'http://www.birgit-kempe-tomaten.de/images/stories/tomaten/'
        
        ## get all urls
        urls = []
        for tomato in tomato_list:
            try:
                tomato_image = tomato['image']
                tomato_image = tomato_image.replace( 'images/', '' )
                urls.append( prefix + tomato_image )
            except:
                pass
            
        ## download images
        for url in urls:
            file_name = url.replace( 'http://www.birgit-kempe-tomaten.de/images/stories/tomaten', outFolder )
            try:
                urllib.request.urlretrieve( url, file_name )
            except:
                print( 'Failed to download ' + url + '.' )
                
    def remove_missing_image_path( self, inFile, outFile ):
        """
        Remove paths to missing images
        """
        ## initialize
        self.io.setFile( inFile )
        tomatoList = self.io.fromFileToList()
        ## loop
        tomatoList2 = []
        for tomato in tomatoList:
            try:
                image_file = Path( tomato['image'] )
                if not image_file.is_file():
                    print( 'Deleting ' + tomato['image'] )
                    del tomato['image']
            except KeyError:
                pass
            tomatoList2.append( tomato )
        ## write out
        self.io.setFile( outFile )
        self.io.fromListToFile( tomatoList2 )
        
    def add_missing_tomato_images( self, inFile, outFile ):
        """
        Add missing tomato images
        """
        ## get images urls
        tfu = TomatosFromURL()
        image_urls = tfu.generate_list_of_image_urls( 'http://www.birgit-kempe-tomaten.de/index.php/de/tomaten-galerie' )
        ## get tomatos without image
        tomatos_without_image = self.find_tomatos_without_image( inFile )
        ## match tomatos
        tomato_matches = {}
        for tomato in tomatos_without_image:
            tomato_match = self.match_tomato_images( tomato, image_urls )
            tomato_matches.update( tomato_match )
        ## fetch and update
        new_tomato_list = self.fetch_images_update_tomtatos( inFile, tomato_matches )
        ## save new tomato list
        self.io.setFile( outFile )
        self.io.fromListToFile( new_tomato_list )
        
    def find_tomatos_without_image( self, inFile ):
        """
        Find such tomatos that do not have an image
        """
        ## initialize
        self.io.setFile( inFile )
        tomatoList = self.io.fromFileToList()
        ## loop
        tomatos_without_image = []
        for tomato in tomatoList:
            if not 'image' in tomato:
                tomatos_without_image.append( tomato )
        ## return result
        return tomatos_without_image
 
    def match_tomato_images( self, tomato, image_urls ):
        """
        Try to find an image url for this particular tomato
        """
        ## init
        tomato_name = tomato['name']
        tomato_match = { tomato_name: '' }
        ## make tomato name matchable
        tomato_name_matchable = tomato_name.lower() \
            .replace( 'ä', 'ae' ) \
            .replace( 'ö', 'oe' ) \
            .replace( 'ü', 'ue' ) \
            .replace( '´', '' ) \
            .replace( 'ß', 'ss' ) \
            .replace( '-', ' ' ) \
            .replace( 'aus sibirien', '' ) \
            .replace( 'kelloggs breakfast', 'kelloggs breakfest' ) \
            .replace( 'kubanische', 'kubanisch' )
        
        ## loop image urls
        for image_url_list in image_urls:
            ## init
            is_matching = True
            image_url = image_url_list[0]
            ## split name into single words
            tomato_name_words = tomato_name_matchable.split(" ")            
            ## loop single words
            for tomato_name_word in tomato_name_words:
                is_matching = is_matching and ( tomato_name_word in image_url.lower() )
            if is_matching:
                tomato_match[ tomato_name ] = image_url
        ## return result
        return tomato_match
    
    def fetch_images_update_tomtatos( self, inFile, tomato_matches ):
        """
        Fetch one image of one tomato, update this one
        """
        ## initialize
        self.io.setFile( inFile )
        old_tomato_list = self.io.fromFileToList()
        new_tomato_list = deepcopy( old_tomato_list )
        ## iterate
        for tomato_name, image_url in tomato_matches.items():
            if image_url:
                ## find old tomato
                old_tomato = next( tomato for tomato in old_tomato_list if tomato['name'] == tomato_name )
                ## do work
                file_name = image_url.replace( 'http://www.birgit-kempe-tomaten.de/images/stories/tomaten', 'images' )
                try:
                    ## fetch image
                    urllib.request.urlretrieve( image_url.replace( ' ', '%20' ), file_name )
                    ## create new tomato
                    new_tomato = deepcopy( old_tomato )
                    new_tomato['image'] = file_name
                    ## remove old tomato from list
                    new_tomato_list = [ tomato for tomato in new_tomato_list if tomato != old_tomato ]
                    ## add new tomato to list
                    new_tomato_list.append( new_tomato )
                except Exception as e:
                        print( 'Failed to download ' + image_url + '.' )
                        print( e )
        ## return result
        return new_tomato_list
    