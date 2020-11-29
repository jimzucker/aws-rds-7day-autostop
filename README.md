# aws-rds-7day-autostop
# Goal
Monitor RDS Events servers auto started due to 7-day rule, "RDS-EVENT-0154 The DB instance is being started due to it exceeding the maximum allowed time being stopped.", and stop them.

## AWS Architecture
![Image of CloudWatch](https://github.com/jimzucker/aws-rds-7day-autostop/blob/main/images/aws_architecture.png)

## User Story
As an AWS Solution Architect I want to monitor for RDS being auto-started by AWS due to it exceedn the maximum allows time being stopped so that I can stop them automatically to achieve the 'Well Architected' pillar of 'Cost Optimization'.

![Image of CloudWatch](https://github.com/jimzucker/aws-rds-7day-autostop/blob/main/images/cloudwatch_autostop.png)

## Acceptance Criteria
1. Detect and stop RDS intance auto started by AWS
2. Create a cloudformation template.yaml
3. Provide a way to test for future development using a server named rds-stop-test


# How does it work?
There are 3 components
1. A lambda that monitors events from RDS on an SNS topic and ignores all events except 'RDS-EVENT-0154'. It then triggers a Step Function.

2. The step function will call another lambda to actually stop the instance.  We used a step function here for 2 reasons
a. When we get the 'DB Started' event, the instance is not in a valid state to issue a stop so we use the step function to keep checking until we can stop it.
b. Overall this operation can take longer that the max time for a lambda and the step function can run interatively as many times as we want. (So we try for about 2 hours before we give up).  You can see in this cloudwatch log how the calls fail until the last one when the server is 'available'

3. The second lambda actually stop the instance via the API.


### Example of api failing when server not 'available'
This cloudwatch log demonstrates why we needed to use the step function to sleep and retry interatively until the server is available.

![Image of CloudWatch](https://github.com/jimzucker/aws-rds-7day-autostop/blob/main/images/cloudwatch_not_avail.png)




