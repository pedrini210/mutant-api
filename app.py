#!flask/bin/python
from flask import Flask, request, abort, jsonify
import mutant
import boto3

app = Flask(__name__)

dynamodb_table_name = 'mutant-api'

@app.route('/')
def index():
    return "Health check!\n"


# Challenge Level 2
@app.route('/mutant/', methods=['POST'])
def validate_mutant():
    dynamodb = boto3.resource('dynamodb')
    dynamo_table = dynamodb.Table(dynamodb_table_name)
    req_json = request.get_json(force=True)
    if not req_json or 'dna' not in req_json: return abort(403)
    dna = req_json['dna']
    try:
        if mutant.isMutant(dna):
            # DB Mutant Insert
            dynamo_table.put_item(Item={'dna': ''.join(dna), 'mutant': True})
            return "Homo Superior!\n"
        else:
            # DB Human Insert
            dynamo_table.put_item(Item={'dna': ''.join(dna), 'mutant': False})
            return abort(403)
    except ValueError:  # Not even Homo Sapiens DNA
        return abort(403)


# Challenge Level 3
@app.route('/stats', methods=['GET'])
def mutant_stats():
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')
    operation_parameters = {
        'TableName': dynamodb_table_name,
        'FilterExpression': 'mutant = :x',
        'ExpressionAttributeValues': {
        ':x': {'BOOL': True},
        }
    }
    mutant_stats_dict = {
            "count_mutant_dna": 0,
            "count_human_dna": 0,
            "ratio": 0.0
        }
    population = 0
    mutants_qty = 0
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        population += page['ScannedCount']
        mutants_qty += page['Count']
    if population == 0:
        return jsonify(mutant_stats_dict)
    else:
        humans_qty = population - mutants_qty
        mutant_stats_dict['count_mutant_dna'] = mutants_qty
        if humans_qty != 0:
            mutant_stats_dict['count_human_dna'] = humans_qty
            mutant_stats_dict['ratio'] = round(mutants_qty / humans_qty, 2)
    return jsonify(mutant_stats_dict)


if __name__ == '__main__':
    app.run(debug=False)
