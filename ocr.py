import requests


class Ocr:

    def __init__(self, apiKey, url, path, language="eng"):
        self.__apiKey = apiKey
        self.__url = url
        self.__path = path
        self.__language = language

    def getOrcFile(self, filename, overlay=False):
        payload = {
            'isOverlayRequired': overlay,
            'apikey': self.__apiKey,
            'language': self.__language,
            'OCREngine': 2,
            'isCreateSearchablePdf': True,
            'isSearchablePdfHideTextLayer': True,
            'isTable': True
        }
        pathFile = f"{self.__path}/{filename}"
        with open(pathFile, 'rb') as f:
            r = requests.post(
                self.__url,
                files={filename: f},
                data=payload
            )
        return r.content.decode()