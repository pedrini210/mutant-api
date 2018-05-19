import unittest
import json
import app
import boto3
from moto import mock_dynamodb2


class FlaskApiTests(unittest.TestCase):
    def setUp(self):
        self.dynamo_mock = mock_dynamodb2()
        self.dynamo_mock.start()
        self.api = app.app.test_client()
        self.human_dna = {'dna': ["ATGCGA", "CCGTGC", "TTATCT", "AGAACG", "CGCCTA", "TCACTG"]}
        self.mutant_dna = {'dna': ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}
        self.bad_dna = {'dna': ["CCGTGC", "TTATCT", "AGAACG", "CGCCTA", "TCACTG"]}
        dynamo = boto3.resource('dynamodb')
        dynamo.create_table(
            TableName=app.dynamodb_table_name,
            KeySchema=[
                {
                    'AttributeName': 'dna',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'dna',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

    def test_index(self):
        self.assertEqual(self.api.get('/').get_data().decode('utf-8'), app.index())

    def test_validate_mutant(self):
        self.assertEqual(self.api.post('/mutant/', json=self.mutant_dna).status_code, 200)
        self.assertEqual(self.api.post('/mutant/', json=self.human_dna).status_code, 403)
        self.assertEqual(self.api.post('/mutant/', json=self.bad_dna).status_code, 403)

    def test_mutant_stats(self):
        expected_dict_0 = {
            "count_mutant_dna": 0,
            "count_human_dna": 0,
            "ratio": 0.0
        }
        expected_dict_1 = {
            "count_mutant_dna": 1,
            "count_human_dna": 0,
            "ratio": 0.0
        }
        expected_dict_2 = {
            "count_mutant_dna": 1,
            "count_human_dna": 1,
            "ratio": 1.0
        }
        self.assertEqual(json.loads(self.api.get('/stats').get_data().decode('utf-8')), expected_dict_0)
        self.api.post('/mutant/', json=self.mutant_dna)
        self.assertEqual(json.loads(self.api.get('/stats').get_data().decode('utf-8')), expected_dict_1)
        self.api.post('/mutant/', json=self.human_dna)
        self.assertEqual(json.loads(self.api.get('/stats').get_data().decode('utf-8')), expected_dict_2)

    def tearDown(self):
        self.dynamo_mock.stop()
