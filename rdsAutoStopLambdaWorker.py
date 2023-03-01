import json
import traceback
import time
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
  #RDS-EVENT-0154: DB instance is being started due to it exceeding the maximum allowed time being stopped.
  auto_started_event_id="RDS-EVENT-0154"
  debug_instance="rds-stop-test"
  
  try:
    message = json.loads(event['Records'][0]['Sns']['Message'])
    rds_name = message['Source ID']
    event_id = message['Event ID'].split('#')[1]
    event_message = message['Event Message']         

    client = boto3.client('rds')
    response = client.describe_db_instances(DBInstanceIdentifier=rds_name)
    status = response['DBInstances'][0]['DBInstanceStatus'] 
    print("rds_name={} / event_id={} / event_message={} / status={}".format(rds_name,event_id, event_message, status) )

    # if it is stopped we are done
    if status != "stopped" :
      response = client.stop_db_instance(DBInstanceIdentifier=rds_name)
      if response['DBInstance']['DBInstanceStatus'] != 'stopped':
        logger.warning(f"Could not stop RDS instance '{rds_name}'")
      else:
        logger.info(f"Successfully stopped RDS instance '{rds_name}'")

  except Exception as e:
    logger.error(f"An error occurred while stopping RDS instance '{rds_name}': {e}")
    traceback.print_exc()
    raise e
