import json
import os
from config import API_KEY, URL_OCR, URL, PORT
from convert import Convert, ImageConverter
from ocr import Ocr
from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from helper import allowedFile, Response
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = "./images"

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    return render_template("index.html", url=f"http://{URL}:{PORT}")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    response = Response()
    if request.method == 'POST':
        files = request.files
        listFilename = []
        isSuccessLoad = True
        for filename in files:
            file = files[filename]
            if file and allowedFile(file.filename):
                name = secure_filename(file.filename)
                listFilename.append(name)
                file.save(os.path.join(UPLOAD_FOLDER, name))
            else:
                isSuccessLoad = False
        if isSuccessLoad:
            ocr = Ocr(API_KEY, URL_OCR, UPLOAD_FOLDER)
            convert = Convert()
            for path in listFilename:
                responseData = json.loads(ocr.getOrcFile(path, overlay=False))
                convert.convert(responseData)
            # convert.saveToExcel()
            response.status = True
            response.message = "Berhasil Scan"
        else:
            response.status = False
            response.message = "Gagal Scan"
            response.code = 400
    else:
        response.status = False
        response.message = "Gagal Scan"
        response.code = 400
    return response.toJSON()


@app.route("/download")
def download():
    path = "./results/result.xlsx"
    return send_file(path, as_attachment=True)


@app.route("/v2")
def index_v2():
    return render_template("index_v2.html", url=f"http://{URL}:{PORT}")


@app.route("/v2/convert", methods=["POST"])
def convert_v2():
    filenames = json.loads(request.form.get("filenames"))
    ocr = Ocr(API_KEY, URL_OCR, UPLOAD_FOLDER)
    convert = Convert()
    for filename in filenames:
        responseData = json.loads(ocr.getOrcFile(filename, overlay=False))
        convert.convert(responseData)
    return convert.getResultJSON()


@app.route('/v2/upload', methods=['GET', 'POST'])
def upload_file_v2():
    response = Response()
    if request.method == 'POST':
        files = request.files
        listFilename = []
        isSuccessLoad = True
        for filename in files:
            file = files[filename]
            if file and allowedFile(file.filename):
                name = secure_filename(file.filename)
                imagePil = Image.open(file)
                imageConverter = ImageConverter(imagePil, name, UPLOAD_FOLDER, width=400)
                imageConverter.resize()
                imageConverter.save()
                listFilename.append(name)
            else:
                isSuccessLoad = False
        if isSuccessLoad:
            response.status = "server"
            response.message = "Berhasil Scan"
        else:
            response.status = "error"
            response.message = "Gagal Scan"
            response.code = 400
    else:
        response.status = "error"
        response.message = "Gagal Scan"
        response.code = 400
    return response.toJSON()


if __name__ == "__main__":
    app.run(host=URL, port=PORT, debug=True)