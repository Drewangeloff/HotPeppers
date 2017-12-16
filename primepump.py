import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime
from google.cloud import bigquery
from oauth2client.service_account import ServiceAccountCredentials

scopes = ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/bigquery']

bigquery_client = bigquery.Client.from_service_account_json(
        'HotPeppers-5f416acf6ee1.json', project ='hotpeppers-186922')

dataset_ref = bigquery_client.dataset('HotPeppersDataSet')
dataset = bigquery.Dataset(dataset_ref)
dataset.description = 'hot peppers dataset'

table_ref = dataset.table('HotPeppersTable')
table = bigquery.Table(table_ref)

#blow away the table if it exists
try:
    print "trying to get existing table..."
    table = bigquery_client.get_table(table)
except:
    print "table didn't exist..."
    # Set the table schema
    table.schema = (
    bigquery.SchemaField('DATETIME', 'DATETIME'),
    bigquery.SchemaField('TEMPERATURE', 'FLOAT'),
    bigquery.SchemaField('HUMIDITY', 'FLOAT'),
    bigquery.SchemaField('MOISTURE', 'INTEGER'),
    )
    table = bigquery_client.create_table(table)

ROWS_TO_INSERT = [
        (u'1000-01-01 00:00:00', 2.0,1.0,1),
    ]

errors = bigquery_client.create_rows(table, ROWS_TO_INSERT)  # API request
print errors

for row in bigquery_client.list_rows(table):  # API request
    print(row)

print('Created table {} in dataset {}.'.format(table.table_id, dataset.dataset_id))


#set up GPIO into BCM as opposed to BOARD
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#map GPIO pins to relays
PumpRelay = 4
GPIO.setup(PumpRelay,GPIO.OUT)
GPIO.output(PumpRelay,GPIO.LOW)

for i in range(1,100):
	print i
	GPIO.setup(PumpRelay,GPIO.OUT)
	GPIO.output(PumpRelay,GPIO.LOW)
	time.sleep(.2)
	GPIO.output(PumpRelay,GPIO.HIGH)
	time.sleep(.2)

GPIO.cleanup()
