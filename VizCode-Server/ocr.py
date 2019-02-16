import time 
import requests
import os
import Image


_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'
_key = '3197c93f163c49e2a07e2a1c7e7ac5f4'
_maxNumRetries = 10

def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:
        response = requests.request( 'post', _url, data = data, headers = headers, params = params )

        if response.status_code == 429:
            print( "Message: %s" % ( response.json() ) )
            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 202:
            result = response.headers['Operation-Location']
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )
        break
        
    return result

def getOCRTextResult( operationLocation, headers ):
    """
    Helper function to get text result from operation location

    Parameters:
    operationLocation: operationLocation to get text result, See API Documentation
    headers: Used to pass the key information
    """

    retries = 0
    result = None

    while True:
        response = requests.request('get', operationLocation, data=None, headers=headers, params=None)
        if response.status_code == 429:
            print("Message: %s" % (response.json()))
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break
        elif response.status_code == 200:
            result = response.json()
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break

    return result


def process_image(urlImage):
  params = { 'handwriting' : 'true'}

  headers = dict()
  headers['Ocp-Apim-Subscription-Key'] = _key
  headers['Content-Type'] = 'application/json'

  json = { 'url': urlImage }
  data = None

  result = None
  operationLocation = processRequest(data, headers, params)
  if (operationLocation != None):
    headers = {}
    headers['Ocp-Apim-Subscription-Key'] = _key
    while True:
      time.sleep(1)
      result = getOCRTextResult(operationLocation, headers)
      if result['status'] == 'Succeeded' or result['status'] == 'Failed':
        break

  if result is not None and result['status'] == 'Succeeded':
    return parse_result(result)

def image_resize(image_file):
  try:
    im = Image.open(image_file)
    width, height = im.size
    if width > 3200 or height > 3200:
      ratio = width / float(height)
      height_new = 1500
      width_new = width * ratio
      im.thumbnail((width_new, height_new), Image.ANTIALIAS)
      im.save(image_file, "JPEG")
  except Exception as e:
    raise

def process_image_local(pathToFileInDisk):
  image_resize(pathToFileInDisk)
  with open(pathToFileInDisk, 'rb') as f:
    data = f.read()

  # Computer Vision parameters
  params = {'handwriting' : 'true'}

  headers = dict()
  headers['Ocp-Apim-Subscription-Key'] = _key
  headers['Content-Type'] = 'application/octet-stream'

  json = None
  operationLocation = processRequest(json, data, headers, params)

  result = None
  if (operationLocation != None):
    headers = {}
    headers['Ocp-Apim-Subscription-Key'] = _key
    while True:
      time.sleep(1)
      result = getOCRTextResult(operationLocation, headers)
      if result['status'] == 'Succeeded' or result['status'] == 'Failed':
        break

  if result is not None and result['status'] == 'Succeeded':
    return parse_result(result)

def parse_result(result):
  res = []
  for r in result['recognitionResult']['lines']:
    if 'text' in r:
      res.append(r['text'])
    else:
      break
  return res

if __name__ == '__main__':
  res = process_image('https://s3.us-east-2.amazonaws.com/hacktech2018/IMG_1043.jpg')







