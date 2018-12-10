from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import cgi
from sklearn.externals import joblib
import json
import numpy as np
import boto3
import botocore

class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):
        self._set_headers()
        #print (self.path)
        input = parse_qs(self.path[2:])
        print (input['input'][0])
        asset_id = input['input'][0]
        #x = float(input['input'][0])
        #y_predict = self.predict(x)
        #y_actual = np.sin(2 * np.pi * np.tan(x).ravel())
        #self.wfile.write("** predicted :"+ str(y_predict)+"**   actual :"+str(y_actual))
        self.download(asset_id)
        reg = joblib.load('/tmp/'+asset_id)
        self.wfile.write(str(reg.get_params()))

    def download(self,asset_id):
      BUCKET_NAME = 'ai-models-upload-20181115' # replace with your bucket name
      KEY = 'test/'+asset_id # replace with your object key

      s3 = boto3.resource('s3')

      try:
              s3.Bucket(BUCKET_NAME).download_file(KEY, '/tmp/'+asset_id)
      except botocore.exceptions.ClientError as e:
              if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
              else:
                raise

def run(server_class=HTTPServer, handler_class=GP, port=8088):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Server running at localhost:8088...'
    httpd.serve_forever()

run()
