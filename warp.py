#!/usr/bin/python
import os
import glob
import hashlib
import pickle

######################### Classes ##############################
class DrawableDensity:
    def __init__(self, name, path, scaleFactor):
        self.name = name
        self.path = path
        self.scaleFactor = scaleFactor
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

# Variables
upToDateFiles = []
deletedFiles = []
newFiles = []
modifiedFiles = []

def main():
    greet()
    makeDirectories()
    processRawFiles()
    processUpToDateAssets()
    processNewAssets()
    processModifiedAssets()
    processDeletedAssets()
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

def processRawFiles():
    # Dictionary of previously hashed files: <file path, MD5 hash>
    storedHashedFiles = loadHashedFiles()
    # Dictionary of newly hashed files and ready to compare for diff: <file path, MD5 hash>
    recentlyHashedFiles = hashRawFiles()

    saveHashedFiles(recentlyHashedFiles)

    # Classify files by comparing recent hashes with previously hased files
    for path, md5 in recentlyHashedFiles.iteritems():
        if path in storedHashedFiles:
            # CASE 1: The file is present and the hashes are the same (the file is the same)
            if md5 == recentlyHashedFiles[path]:
                upToDateFiles.append(path)
            # CASE 2: The file is present, but the hashes doesn't match (the file has been modified)
            else:
                modifiedFiles.append(path)

            del storedHashedFiles[path] # Removed the processed entry
        # CASE 3: The file isn't present on the previous hash dictinoary, it must be a new file
        else:
            newFiles.append(path)

    # The leftovers in the previous hash dictionary must be the deleted files
    for path in storedHashedFiles:
        deletedFiles.append(path)

# Hash (MD5) files in the raw directory and return them as a dictionary <file path, MD5 hash>
def hashRawFiles():
    BLOCKSIZE = 65536
    hashedFiles = {}
    # Hash files in the raw directory
    for filePath in glob.glob(dirRaw + "*.png"):
        hasher = hashlib.md5()
        with open(filePath, 'rb') as fileToHash:
            buf = fileToHash.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = fileToHash.read(BLOCKSIZE)
        hashedFiles.update({filePath:hasher.hexdigest()})
    return hashedFiles

# Store a dictionary of files to Hash
def saveHashedFiles(filesToHash):
    with open(dirRaw + "warp_storage.pkl", 'wb') as hashStorage:
        pickle.dump(filesToHash, hashStorage, pickle.HIGHEST_PROTOCOL)

# Retrieve a dictionary of hashed files
def loadHashedFiles():
    try:
        with open(dirRaw + "warp_storage.pkl", 'rb') as hashStorage:
            return pickle.load(hashStorage)
    except IOError:
        return {}

# Process files that shouldn't be compress or reescaled
def processUpToDateAssets():
    for path in upToDateFiles:
        print(os.path.basename(path) + ": UP TO DATE")

def processNewAssets():
    for path in newFiles:
        print(os.path.basename(path) + ": NEW")
        processPngAsset(path)

def processModifiedAssets():
    for path in modifiedFiles:
        print("TODO: process modified asset (" + os.path.basename(path) + ")")

def processDeletedAssets():
    for path in deletedFiles:
        print("TODO: process deleted asset (" + os.path.basename(path) + ")")

def processPngAsset(assetPath):
    # Scale and compress the asset for every screen density
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
