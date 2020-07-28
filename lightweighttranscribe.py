import sys
import ast
import uuid
import time
import boto3
import textwrap
import logging
from tqdm import tqdm

logging.getLogger().setLevel(logging.INFO)

output_file_name = str(sys.argv[-1])
input_file_name = sys.argv[1]

bucket_name = input('Enter the name of s3 bucket:') or 'krypted'

s3 = boto3.resource('s3')
client = boto3.client('transcribe')

file_identifier = str(uuid.uuid4())

def create_resources(bucket_name):
    if s3.Bucket(bucket_name).creation_date is None:
        s3.create_bucket(Bucket=bucket_name)
        logging.info('Waiting for {} bucket creation...'.format(bucket_name))
        time.sleep(5)

    logging.info('Bucket {} created.'.format(bucket_name))
    logging.info('Uploading {} file...'.format(input_file_name))

    s3.Bucket(bucket_name).upload_file(input_file_name, 'input/{}'.format(input_file_name+'-'+file_identifier))

def convert_speech_to_text(job_name):
    logging.info('Creating job defination.')
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode='en-US',
        MediaFormat=input_file_name.split('.')[1],
        Media={'MediaFileUri':'s3://{}/input/{}'.format(bucket_name, job_name)},
        OutputBucketName=bucket_name
    )

    while True:
        status = client.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        for _ in tqdm(range(100)):
            time.sleep(.7)

    logging.info('Job Ready and starting conversion process.')
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        obj = s3.Object(bucket_name, job_name+'.json')
        text = ast.literal_eval(obj.get()['Body'].read().decode('UTF-8'))['results']['transcripts'][0]['transcript']
        return text
    return 

def write_to_file(speech_text):
    with open(output_file_name, 'wt') as f:
        logging.info('Writing data to {} file.'. format(output_file_name))
        f.write(textwrap.fill(speech_text, width=130))
        logging.info('Saving data to file.')

def resource_cleanup(job_name):
    logging.info('Cleaning-up Resources.')
    client.delete_transcription_job(TranscriptionJobName=job_name)
    logging.info('Process complete.')


job_name = input_file_name+'-'+file_identifier

create_resources(bucket_name)
speech_text = convert_speech_to_text(input_file_name+'-'+file_identifier)
write_to_file(speech_text)
resource_cleanup(job_name)

