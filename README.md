# Pytesseract-Api

Python-tesseract is an optical character recognition (OCR) tool for python. That is, it will recognize and "read" the text embedded in images.

Python-tesseract is a wrapper for Google's Tesseract-OCR Engine. It is also useful as a stand-alone invocation script to tesseract, as it can read all image types supported by the Pillow and Leptonica imaging libraries, including jpeg, png, gif, bmp, tiff, and others. Additionally, if used as a script, Python-tesseract will print the recognized text instead of writing it to a file.

This api uses pytesseract to extract text from image file, url, path.

## Tesseract-ocr
This tools need tesseract-ocr engine. Help yourself with this --

https://github.com/tesseract-ocr/tesseract/wiki

## Requirments
```
Flask==1.1.1
pytesseract==0.3.0
requests==2.22.0
Pillow==6.2.0
```
To install the requirments type in terminal 
```python
pip install -r /path/to/requirements.txt
```

## Usage

Here is an example http post request that is passed to /image_to_text end point
```http
POST /image_to_text HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
cache-control: no-cache
Postman-Token: 139af5cf-6d6e-48be-88e5-e166b3b670c9


Content-Disposition: form-data; name="file"; filename="/C:/Users/talha/Desktop/imgtest/710.0.png


------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

Here is an example http post request that is passed to /url_to_text end point
```http
POST /url_to_text HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/x-www-form-urlencoded
cache-control: no-cache
Postman-Token: 8e35091c-322f-4b24-b15f-34670d0c8e02

{
	"image" : "https://pbs.twimg.com/media/C4Aw20DWMAAOGE9?format=jpg&name=medium"
}
```

## The endpoints

#### /image_to_text
This endpoint recieves an image file in variable called **file** and passes it to the **converter()** to extract text and return the result in a json format
```python
@app.route('/image_to_text', methods=['POST'])
def image_to_text():
    try:
        img = Image.open(request.files['file'].stream)
        return converter(img)
    except:
        return jsonify(
            {"error": "Did you mean to send: {'file': 'some_image'}"}
        )
```
This endpoint recieves an image file in variable called **file** and passes it to the **converter()** to extract text and return the result in a json format

#### /url_to_text
```python
@app.route('/url_to_text', methods=['POST'])
def url_to_text():
    try:
        url = request.get_json('image_url')
        url = url['image_url']
        if os.path.isfile(url):
            return converter(url)
        else:
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            return converter(img)
    except:
        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_image_url_path'}"}
        )
```
#### converter() function
This takes in the image parameter and feeds it to the pytesseract and returns text extracted from image in json format 
```python
def converter(img):
    txt = pytesseract.image_to_string(img, config="--psm 6")
    return jsonify({"Text": repr(txt)})

```
