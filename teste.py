import exifread
import os


for filename in os.listdir("C:\\Users\\ricks\\Downloads\\Python\\ImageMetaData"):
    if filename.endswith('.jpg'):
        with open("%s/%s" % ("C:\\Users\\ricks\\Downloads\\Python\\ImageMetaData", filename), 'rb') as image: # file path and name
            exif = exifread.process_file(image)
            dt = str(exif['EXIF DateTimeOriginal'])  # might be different
            # segment string dt into date and time
            day, dtime = dt.split(" ", 1)
            # segment time into hour, minute, second
            hour, minute, second = dtime.split(":", 2)
            print(dt)