from src.org.cumcubble.tomatos.TomatoJSON import TomatoJSON
from src.org.cumcubble.tomatos.TomatoPrinter import TomatoPrinter
from src.org.cumcubble.tomatos.TomatoEnricher import TomatoEnricher

from src.org.cumcubble.tomatos.TomatoImagination import TomatoImagination

## main variables
io = TomatoJSON()
tp = TomatoPrinter()
te = TomatoEnricher()
ti = TomatoImagination( io )

## main functions
def enrichTomatos( category, inFile, outFile ):
    if category == 'types':
        io.setFile( inFile )
        tomatoList = io.fromFileToList()
        tomatoListTypes = []
        for tomato in tomatoList:
            tomatoTypes = te.addTypes( tomato )
            tomatoListTypes.append( tomatoTypes )
        io.setFile( outFile )
        io.fromListToFile( tomatoListTypes )
    
    if category == 'colors':
        io.setFile( inFile )
        tomatoList = io.fromFileToList()
        tomatoListColors = []
        for tomato in tomatoList:
            tomatoColor = te.addColors( tomato )
            tomatoListColors.append( tomatoColor )
        io.setFile( outFile )
        io.fromListToFile( tomatoListColors )

def getNewTomatos( outFile ):
    io.setFile( outFile )
    io.fromWebToFile( True )
    

## main program
if __name__ == '__main__':
    
    ## initial fetch
    print( "Initial fetch of Tomatos..." )
    getNewTomatos( outFile='res/tomatos01.json' )
    print( "Done\n" )
    
    ## enrichment
    print( "Adding colors..." )
    enrichTomatos( category='colors' ,  inFile='res/tomatos01.json' , outFile='res/tomatos02.json' )
    print( "Done\n" )
    print( "Adding types..." )
    enrichTomatos( category='types' ,  inFile='res/tomatos02.json' , outFile='res/tomatos03.json' )
    print( "Done\n" )
    
    ## images
    print( "Fetching images..." )
    ti.get_tomato_images( inFile='res/tomatos03.json' , outFolder='res/images' )
    ti.remove_missing_image_path( inFile='res/tomatos03.json', outFile='res/tomatos04.json' )
    print( "Done\n" )
    print( "Adding missing images..." )
    ti.add_missing_tomato_images( inFile='res/tomatos04.json', outFile='res/tomatos05.json' )
    print( "Done\n" )
