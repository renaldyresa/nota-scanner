import json
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Response:

    def __init__(self, status=False, message="", data=[], code=200):
        self.status = status
        self.message = message
        self.data = data
        self.code = code

    def toJSON(self):
        result = json.loads(json.dumps(self, default=lambda o: o.__dict__, indent=4))
        code = result.pop("code", 400)
        return result, code
