import json
import boto3
import traceback
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
  try:
    logger.info(f"Received event: {json.dumps(event)}")
    #RDS-EVENT-0154: DB instance is being started due to it exceeding the maximum allowed time being stopped.
    auto_started_event_id="RDS-EVENT-0154"

    #this is for debuggins
    debug_instance="rds-stop-test"

    state_machine = os.environ['RDS_STATE_MACHINE_ARN']
    message = json.loads(event['Records'][0]['Sns']['Message'])
    rds_name = message['Source ID']
    event_id = message['Event ID'].split('#')[1]     
    event_message = message['Event Message']         
    logger.info(f"rds_name={rds_name} / event_id={event_id} / event_message={event_message}")

    #for debugging
    if rds_name == debug_instance :
      logger.info(f"Debugging instance: {debug_instance}")
      logger.info(f"Event: {json.dumps(event)}")
      logger.info(f"State machine ARN: {state_machine}")

    #
    # trigger if we are not stopping and its and auto_started_event or debug_instance
    #
    if event_id == auto_started_event_id or rds_name == debug_instance :
      client = boto3.client('stepfunctions')
      response = client.start_execution(
        stateMachineArn=state_machine,
        input=json.dumps(event)
      )
      logger.info(f"Started execution of state machine {state_machine}: {response}")

  except Exception as e:
    logger.error(f"An error occurred: {str(e)}")
    logger.error(traceback.format_exc())

