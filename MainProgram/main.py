import crop
import labeling
import remove_bg
import scraping
import similar_images

def menu():
    x = input('1) Scraping\n2) Deleting copies of images\n' +
    '3) Comparing and deleting similar images\n4) Crop Images\n5) '+ 
    'Remove Background \n6) Labeling \n7) Quit (default):\n ' )
    try:
        x = int(x)
    except:
        x = 6
    if x>=1 and x<=6:
        enter = True
    else:
        enter = False
    return enter, x

# This is a menu like main
print('Hi, what would you like to do?')
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