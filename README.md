[![Build Status](https://travis-ci.org/pedrini210/mutant-api.svg?branch=master)](https://travis-ci.org/pedrini210/mutant-api) 
[![codecov](https://codecov.io/gh/pedrini210/mutant-api/branch/master/graph/badge.svg)](https://codecov.io/gh/pedrini210/mutant-api)


<img src="https://vignette.wikia.nocookie.net/street-fighter-sprites/images/5/5a/Magneto-XMVSF-Icon.png/revision/latest?cb=20170720074811"/>

# Mutant API 

Magneto as entitled us the mission to study human DNA samples in order to determine if the subject is a Mutant or not.

Based on a clever algorithm and **AWS**, we are going to create a web API to quickly analyze the DNA samples and identify the mutants.

I've used my programming knowledge, the **Python** programming language and the **AWS** cloud to build and deploy this web API as quickly (and cheap) as possible.

## How to build and deploy the API
  1. Install the AWS Cli.
  2. Run `aws configure` and type your AWS ID and access key.
  3. Create and activate a Python virtual environment (`venv`).
  4. Install the requirements: `pip install -r requirements.txt`
  5. Create a DynamoDB Table, name it `mutant-api` and set `dna` as a string primary key. (Forgive the hardcoding here :smiley: )
  6. In the project folder run: `zappa init` to configure the environment and AWS Lambda and API Gateway deployment.
  7. Finally, run `zappa deploy <your_environment>` and you are ready to find mutants!

Zappa is a handy tool to deploy Python (Flask & Django) apps in a serverless fashion. It's easy to configure and lets you deploy a API Gateway and Lambda functions in minutes. You can check Zappa project [here](https://github.com/Miserlou/Zappa).

## Additional Information
The file [`mutant.py`](mutant.py) have the algorithm provided by Margeto to identify mutant DNA.

The method [`isMutant()`](mutant.py#L50) returns `True` when it identifies Mutant DNA, `False` when it encounters Human DNA and raises an exception when the DNA does not belongs to the Homo Sapiens species.

The API is deployed using a *serverless* approach, using AWS Lambda and API Gateway. This approach is really cost effective, because we only pay for the effective use of the API without worrying for any servers at all. Also, the first million of API calls are free!

Please check the [`.travis.yml`](.travis.yml) for tests and code coverage.


Feel free to contact me if you need additional information.


![Magneto](https://vignette.wikia.nocookie.net/street-fighter-sprites/images/5/5f/Magneto-XMVSF-Stance.gif/revision/latest?cb=20170720083633)