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

class Colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
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
STORAGE_FILE_NAME = "warp_storage"

def main():
    # Variables
    upToDateFiles = []
    deletedFiles = []
    newFiles = []
    modifiedFiles = []

    greet()
    makeRequiredDirectories()
    processRawFiles(upToDateFiles, deletedFiles, newFiles, modifiedFiles)
    processUpToDateAssets(upToDateFiles)
    processNewAssets(newFiles)
    processModifiedAssets(modifiedFiles)
    processDeletedAssets(deletedFiles)
    goodbye()

# Greet
def greet():
    message = [
    "**********************************",
    "*  _       _____    ____  ____   *",
    "* | |     / /   |  / __ \/ __ \\  *",
    "* | | /| / / /| | / /_/ / /_/ /  *",
    "* | |/ |/ / ___ |/ _, _/ ____/   *",
    "* |__/|__/_/  |_/_/ |_/_/        *",
    "*                                *",
    "*  Wolox Assets Rapid Processor  *",
    "**********************************"
    ]
    for line in message:
        print(Colors.PURPLE + line + Colors.ENDC)

def makeRequiredDirectories():
    # Make required directories
    for directory in allDirectories:
        if not os.path.exists(directory):
            print("Making directory " + directory)
            os.makedirs(directory)

def processRawFiles(upToDateFiles, deletedFiles, newFiles, modifiedFiles):
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
    with open(dirRaw + "." + STORAGE_FILE_NAME, "wb") as hashStorage:
        pickle.dump(filesToHash, hashStorage, pickle.HIGHEST_PROTOCOL)

# Retrieve a dictionary of hashed files
def loadHashedFiles():
    try:
        with open(dirRaw + "." + STORAGE_FILE_NAME, "rb") as hashStorage:
            return pickle.load(hashStorage)
    except IOError:
        return {}

# Process files that we found in a previous run by the script
def processUpToDateAssets(upToDateFiles):
    for path in upToDateFiles:
        print(Colors.BLUE + os.path.basename(path) + ": STATE > UP TO DATE" + Colors.ENDC)

# Process files that are new to the project
def processNewAssets(newFiles):
    for path in newFiles:
        print(Colors.BLUE + os.path.basename(path) + ": STATE > NEW" + Colors.ENDC)
        processPngAsset(path)

# Process files that were modified in the project
def processModifiedAssets(modifiedFiles):
    for path in modifiedFiles:
        assetName = os.path.basename(path)
        print(Colors.BLUE + assetName + ": STATE > CHANGED" + Colors.ENDC)
        deleteAsset(assetName)
        processPngAsset(path)

# Process files that were deleted from the project
def processDeletedAssets(deletedFiles):
    for path in deletedFiles:
        assetName = os.path.basename(path)
        print(Colors.BLUE + assetName + ": STATE > REMOVED" + Colors.ENDC)
        deleteAsset(assetName)

# Scale and compress the asset for every screen density
def processPngAsset(assetPath):
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

# Remove asset in every screen density
def deleteAsset(assetName):
    for density in drawablesDensities:
        os.remove(density.path + assetName)
        print(assetName + ": DELETED asset for " + density.name)

# Goodbye
def goodbye():
    print(Colors.OKGREEN + "WARP complete!" + Colors.ENDC)

# Main call
main()
