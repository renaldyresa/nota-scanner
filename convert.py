import json
import pandas as pd
from PIL import Image


class Convert:

    ITEM = "item"
    LOTS = "lot"
    LOT_PRICE = "price"
    TOTAL = "total"
    STATUS = "status"
    DISC = "discount"
    ODD = "ANEH"
    ANY_WORDS = ["disc", "orig"]

    def __init__(self):
        self.__result = []
        self.__dataFrame = None

    def convert(self, response):
        results = response.get("ParsedResults", {})
        parserText = results[0].get("ParsedText", "")
        parserText = parserText.replace("\t", ' ')
        listResult = parserText.splitlines()
        for index in range(len(listResult)):
            listResult[index] = listResult[index].rstrip().replace(", ", ",")
        self.__result += listResult

    @staticmethod
    def rowStyle(row):
        if row.STATUS == Convert.ODD:
            return pd.Series('background-color: yellow', row.index)
        return pd.Series('', row.index)

    def toInt(self, price, isBefore=False):
        price = price.replace(",", "").replace(".", "").replace("-", "")
        if price.isnumeric():
            return int(price)
        row = len(self.__dataFrame) - 1
        if isBefore:
            row -= 1
        if "or" in price:
            return 1
        self.__dataFrame.at[row, Convert.STATUS] = Convert.ODD
        return 0

    def __setDataFrame(self):
        self.__dataFrame = pd.DataFrame(columns=[Convert.ITEM, Convert.LOTS, Convert.LOT_PRICE,
                                                 Convert.DISC, Convert.TOTAL, Convert.STATUS])
        for text in self.__result:
            listText = text.split(" ")
            if len(listText) <= 3:
                if len(listText) == 1:
                    row = len(self.__dataFrame) - 1
                    lot = 1
                    lotPrice = self.toInt(listText[-1])
                    self.__dataFrame.at[row, Convert.LOTS] = lot
                    self.__dataFrame.at[row, Convert.LOT_PRICE] = lotPrice
                    if lot * lotPrice != self.__dataFrame[Convert.TOTAL][row]:
                        self.__dataFrame.at[row, Convert.STATUS] = Convert.ODD
                elif listText[0] not in Convert.ANY_WORDS:
                    row = len(self.__dataFrame) - 1
                    lot = self.toInt(listText[0])
                    lotPrice = self.toInt(listText[-1])
                    self.__dataFrame.at[row, Convert.LOTS] = lot
                    self.__dataFrame.at[row, Convert.LOT_PRICE] = lotPrice
                    if lot * lotPrice != self.__dataFrame[Convert.TOTAL][row]:
                        self.__dataFrame.at[row, Convert.STATUS] = Convert.ODD
                elif listText[0] == Convert.ANY_WORDS[0]:
                    row = len(self.__dataFrame) - 1
                    disc = self.toInt(listText[-1])
                    self.__dataFrame.at[row, Convert.DISC] = disc
                    prices = self.__dataFrame[Convert.LOTS][row] * self.__dataFrame[Convert.LOT_PRICE][row]
                    if (prices - disc) == self.__dataFrame[Convert.TOTAL][row]:
                        self.__dataFrame.at[row, Convert.STATUS] = ""
                    else:
                        self.__dataFrame.at[row, Convert.STATUS] = Convert.ODD
                elif listText[0] == Convert.ANY_WORDS[1]:
                    row = len(self.__dataFrame) - 1
                    lotPrice = self.toInt(listText[-1])
                    self.__dataFrame.at[row, Convert.LOTS] = 1
                    self.__dataFrame.at[row, Convert.LOT_PRICE] = lotPrice
            else:
                if listText[0] not in Convert.ANY_WORDS:
                    name = ' '.join(listText[:-1])
                    price = self.toInt(listText[-1], isBefore=True)
                    newRow = {Convert.ITEM: name, Convert.TOTAL: price}
                    self.__dataFrame = self.__dataFrame.append(newRow, ignore_index=True)
                    if price < 1000:
                        row = len(self.__dataFrame) - 1
                        self.__dataFrame.at[row, Convert.STATUS] = Convert.ODD
                elif listText[0] == Convert.ANY_WORDS[0]:
                    row = len(self.__dataFrame) - 1
                    disc = self.toInt(listText[-1])
                    self.__dataFrame.at[row, Convert.DISC] = disc
                    prices = self.__dataFrame[Convert.LOTS][row] * self.__dataFrame[Convert.LOT_PRICE][row]
                    if (prices - disc) == self.__dataFrame[Convert.TOTAL][row]:
                        self.__dataFrame.at[row, Convert.STATUS] = ""
                    else:
                        self.__dataFrame.at[row, Convert.STATUS] = Convert.ODD
                elif listText[0] == Convert.ANY_WORDS[1]:
                    row = len(self.__dataFrame) - 1
                    lotPrice = self.toInt(listText[-1])
                    self.__dataFrame.at[row, Convert.LOTS] = 1
                    self.__dataFrame.at[row, Convert.LOT_PRICE] = lotPrice

    def saveToExcel(self):
        try:
            self.__setDataFrame()
            row = len(self.__dataFrame)
            self.__dataFrame = self.__dataFrame.style.apply(Convert.rowStyle, axis=1)
            writer = pd.ExcelWriter("./results/result.xlsx", engine='xlsxwriter')
            self.__dataFrame.to_excel(writer, "TEST", index=False)
            formula = f"=SUM(E2:E{row+1})"
            sheet = writer.sheets['TEST']
            sheet.write_formula(row + 1, 4, formula)
            writer.save()
            print("success create excel")
        except Exception as e:
            print("Gagal create excel")
            print(e)

    def getResultJSON(self):
        self.__setDataFrame()
        return self.__dataFrame.to_json(orient='records')


class ImageConverter:

    def __init__(self, file, filename, pathSave, width=500):
        self.__file = file
        self.__filename = filename
        self.__pathSave = pathSave
        self.width = width

    def resize(self):
        size = self.__file.size
        height = int(self.width/size[0]*size[1])
        self.__file = self.__file.resize((self.width, height), Image.ADAPTIVE)

    @property
    def filename(self):
        return self.__filename

    def save(self):
        self.__file.save(f"{self.__pathSave}/{self.filename}", quality=100)


if __name__ == "__main__":
    filenameImage = "test1.jpeg"
    pathFile = "./images2/test1.jpeg"
    path = "./images"
    fileImage = Image.open(pathFile)
    imageConverter = ImageConverter(fileImage, filenameImage, path)
    imageConverter.resize()
    imageConverter.save()



