# Cosmic AI

Cosmic AI is webcrawler bot which motivates employees to participate into floorball events. It's written in Python 3.7. and is completely serverless implementation running inside AWS.

Webcrawler is started by AWS Cloudwatch schedule which runs four times a week;

    on Mondays at: 09:00 PM
    on Tuesdays at: 14:00 PM
    on Wednesdays at: 09:00 PM
    on Thursdays at: 21:00 PM

Each schedule starts AWS Lamdba -function which will crawl latest floorball events from https://paakonttori.nimenhuuto.com/calendar/csv into CSV -file using Pandas. Latest event is fetched from CSV -file into variable (event website). Latest event website e.g. https://paakonttori.nimenhuuto.com/events/11688102 is crawled for numbers of players in the event. Player number and event name are stored and based on number of signed up players, a different message is posted into Slack #pääkonttorin_säbä using Slack webhook (https://api.slack.com/incoming-webhooks).


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes (using local Python environment instead of Lamdba and without posting into Slack). See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Docker CE installed on local machine for package building
* Python 3.7 (and virtualenv)
* pip3

### Modifying and testing script

* ```cosmic_test.py``` is version for local testing and works on Python environment having necessary pip packages installed
* ```cosmic_test_cancel.py``` is version for local testing of cancel messages
* ```cosmic_ai.py``` is has the same functionality as ```cosmic_test.py```, but has the default ```def lambda_handler(event, context):``` function, which can be used to start the script inside AWS Lambda
* ```cosmic_ai_cancel.py``` separate, similar function as cosmic_ai, but limited to cancelling events

## Deployment

* Install Docker CE https://docs.docker.com/install/
* Copy latest Amazon AMI image using Docker 
```docker run -it dacut/amazon-linux-python-3.6``` 
* In the new AMI make a new directory 
```mkdir lambda```
* In the lamdba directory install needed packages using pip.
```pip3 install pandas, random, arrow```
* Once installation is done, zip all the files in package
```zip -r lambda.zip * ```
* Obtain docker container image ID
```docker ps -a | grep "dacut" | awk '{print $1}'``
* Copy lambda.zip to your local machine
```docker cp $(docker ps -a | grep "dacut" | awk '{print $1}'):/lambda/lambda.zip <PATH_TO_YOUR_LOCAL_DIRECTORY_OF_CHOICE>```
* Add cosmic_ai.py into lambda.zip
```zip -ur lambda.zip cosmic_ai.py```
* Upload lambda.zip to S3
* Create Lambda function for example ```cosmic_ai-slack-ai_integration``` with handler function name as ```cosmic_ai.lambda_handler``` and Runtime as Python 3.6. Give minimum amount of memory 128MB. No VPC and default role.
* Create necessary AWS Cloudwatch rules for starting ```cosmic_ai-slack-ai_integration```

## Built With

* Python 3.7
* Pandas https://pandas.pydata.org/
* Arrow https://arrow.readthedocs.io/en/latest/

## Authors

* **Mika Heino** - *Initial work* - [mikaheino](https://github.com/mikaheino)

## License

This project is licensed under the GNU General Public License v3.0

## Acknowledgments

* Peter Begle for https://medium.com/i-like-big-data-and-i-cannot-lie/how-to-create-an-aws-lambda-python-3-6-deployment-package-using-docker-d0e847207dd6

