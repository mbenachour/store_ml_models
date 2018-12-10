import http.client as httplib
import os
from pynamodb.exceptions import DoesNotExist, DeleteError, UpdateError
from asset.asset_model import AssetModel
from log_cfg import logger

BUCKET = os.environ['S3_BUCKET']
def event(event, context):
    """
    Triggered by s3 events, object create and remove

    """
    # Sample event:
    #
    # _event = {'Records': [{'eventVersion': '2.0', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1',
    #                        'eventTime': '2017-11-25T23:57:38.988Z', 'eventName': 'ObjectCreated:Put',
    #                        'userIdentity': {'principalId': 'AWS:AROAJWJG5IVL3URF4WKKK:su-xx-test-create'},
    #                        'requestParameters': {'sourceIPAddress': '75.82.111.45'},
    #                        'responseElements': {'x-amz-request-id': '9E39B8F9A3D22C83',
    #                                             'x-amz-id-2': 'GiWcmOHnxnxOJa64k5rkgTsiiwo+JOR3p2DvuQ6txQXl9jC0jNhO+gbDwwP/3WKAl4oPbVZsTE4='},
    #                        's3': {'s3SchemaVersion': '1.0', 'configurationId': 'dad7b639-0cd8-4e47-a2ae-91cc5bf866c8',
    #                               'bucket': {'name': 'su-xx', 'ownerIdentity': {'principalId': 'AEZOG5WRKFUM2'},
    #                                          'arn': 'arn:aws:s3:::su-xx'},
    #                               'object': {'key': 'test/bbc498ea-d23b-11e7-af42-2a31486da301', 'size': 11060,
    #                                          'eTag': 'd50cb2e8d7ad6768d46b3d47ba9b241e',
    #                                          'sequencer': '005A1A0372C5A1D292'}}}]}

    logger.debug('event: {}'.format(event))
    event_name = event['Records'][0]['eventName']
    key = event['Records'][0]['s3']['object']['key']
    asset_id = key.replace('{}/'.format(os.environ['S3_KEY_BASE']), '')
    loadModel(asset_id)
def loadModel(asset_id):
    #BUCKET_NAME = 'ml2m-test' 
    KEY = 'test/'+asset_id     
    s3 = boto3.resource('s3')    
    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, '/tmp/mlpreg_2')
        print("uploaded !")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise   
        