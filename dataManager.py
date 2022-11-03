import os.path


class DataManager:
    # TODO Move image storage location here (original, cutouts)
    files = []
    cutouts = []

    def clearData(self):
        self.files = []

    def addFile(self, path):
        for i in path:
            url = i.path()[1:]
            if self.__isFolder(url):
                self.__addDirContent(url)
            else:
                self.files.append(url)

    def __isImage(self, path):
        fileName = path[path.rfind(".") + 1:]
        if fileName in ["bmp", "jpeg", "jpg", "tiff", "png"]:
            return True
        else:
            return False

    def __isFolder(self, path):
        return os.path.isdir(path)

    def isEmpty(self):
        if len(self.files) == 0:
            return True
        else:
            return False

    def __addDirContent(self, file):
        a = [(file + "/" + x) for x in os.listdir(file)]
        self.files += a

    def getNextImage(self):
        if self.isEmpty():
            return None
        else:
            file = self.files.pop(0)
            if self.__isFolder(file):
                self.__addDirContent(file)
                return self.getNextImage()
            else:
                if self.__isImage(file):
                    return file
                else:
                    return self.getNextImage()
