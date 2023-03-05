import crop
import labeling
import remove_bg
import scraping
import similar_images
import sys
sys.path.insert(1, '../')
import Utils.utils

def menu():
    opts = ['Scraping', 'Deleting copies', 'Comparing similar',
            'Crop', 'Remove Background', 'Labeling', 'Quit' ]
    x = Utils.utils.options(opts)
    if x>=1 and x<=6:
        enter = True
    else:
        enter = False
    return enter, x

# This is a menu like main
enter, x = menu()
while(enter):
    if x == 1:
        scraping.Scraping()
    elif x == 2:
        similar_images.SimilarImages(True)
    elif x == 3:
        similar_images.SimilarImages(True)
    elif x == 4:
        y = int(input('Would you like to use the cursor? (default is manually) (0/1)\n'))
        crop.Crop(y)
    elif x == 5:
        y = int(input('Automated mode (0/1) (takes as input all the image\n' + 
        ' when you want to use the grab cut algorithm): '))
        remove_bg.RemoveBackGround(y)
    elif x == 6:
        labeling.Labeling()
    else:
        enter = False
        continue

    print('Would you like to do anything else?')
    enter, x = menu() 