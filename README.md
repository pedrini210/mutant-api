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


