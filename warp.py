#!/usr/bin/python
import os
import glob

######################### Classes ##############################
class DrawableDensity:
    def __init__(self, name, path, scaleFactor):
        self.name = name
        self.path = path
        self.scaleFactor = scaleFactor

class HashedFile:
    def __init__(self, name, md5Hash):
        self.name = name
        self.md5Hash = md5Hash
################################################################

################# Directories configuration ####################
dirRoot = "./"
dirRaw = dirRoot + "raw/"
dirAssets = dirRoot + "drawables/"
dirHdpi = dirAssets + "drawable-hdpi/"
dirHdpiX = dirAssets + "drawable-xhdpi/"
dirHdpiXX = dirAssets + "drawable-xxhdpi/"
dirHdpiXXX = dirAssets + "drawable-xxxhdpi/"

allDirectories = [dirRaw, dirHdpi, dirHdpiX, dirHdpiXX, dirHdpiXXX]
drawablesDensities = [
DrawableDensity("HDPI", dirHdpi, 0.375),
DrawableDensity("X-HDPI", dirHdpiX, 0.5),
DrawableDensity("XX-HDPI", dirHdpiXX, 0.75),
DrawableDensity("XXX-HDPI", dirHdpiXXX, 1.0)
]
# ScaleFactor with origin in XXXHDPI density. Source: http://jennift.com/dpical.html
################################################################

def main():
    greet()
    makeDirectories()
    processPNGs()
    goodbye()

# Greet
def greet():
    print("WARP (Wolox Assets Rapid Processor)")

def makeDirectories():
    # Make required directories
    for directory in allDirectories:
        if not os.path.exists(directory):
            print("Making directory " + directory)
            os.makedirs(directory)

def processPNGs():
    # List PNG assets paths from the raw directory
    print("Analyzing raw PNGs assets...")
    pngAssetsPaths = glob.glob(dirRaw + "*.png")

    # Iterate over every PNG asset, then scale and compress for every screen density
    for assetPath in pngAssetsPaths:
        filename = os.path.basename(assetPath)
        for density in drawablesDensities:
            scaleImage(filename, assetPath, density)
            compressPNG(filename, density.path + filename, density)
        print(filename + ": Processed the asset for every screen density")

# Scale the asset for a given screen density using FFMPEG
def scaleImage(filename, assetPath, drawableDensity):
    print("{0}: SCALING to {1}".format(filename, drawableDensity.name))
    os.system("ffmpeg -loglevel error -y -i {0} -vf scale=iw*{1}:-1 {2}".format(assetPath, drawableDensity.scaleFactor, drawableDensity.path + filename))

# Compress a PNG asset using PNGQuant
def compressPNG(filename, assetPath, drawableDensity):
    print(filename + ": COMPRESSING for " + drawableDensity.name)
    os.system("pngquant {0} --force --output {1}".format(assetPath, drawableDensity.path + filename))

# Goodbye
def goodbye():
    print("WARP complete!")

# Main call
main()
