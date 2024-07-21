import os

def getFilesAndDirs(dir):
    files = []
    dirs = []
    for item in os.listdir(dir):
        itemPath = os.path.join(dir, item)
        if (os.path.isdir(itemPath)):
            dirs.append(itemPath)
            newfiles, newfolders = getFilesAndDirs(itemPath)
            dirs.extend(newfolders)
            files.extend(newfiles)
        else:
            files.append(itemPath)

    return files, dirs
