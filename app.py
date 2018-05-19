#!flask/bin/python
from flask import Flask, request, abort, jsonify
import mutant
import boto3

app = Flask(__name__)

dynamodb_table_name = 'mutant-api'
dynamodb = boto3.resource('dynamodb')
dynamo_table = dynamodb.Table(dynamodb_table_name)


@app.route('/')
def index():
    return "Health check!\n"

#Challenge Level 2
@app.route('/mutant/', methods=['POST'])
def validate_mutant():
    if not request.json or 'dna' not in request.json: return abort(403)
    dna = request.json['dna']
    try:
        if mutant.isMutant(dna):
            # DB Mutant Insert
            dynamo_table.put_item(Item={'dna': ''.join(dna), 'mutant': True})
            return "OK!\n"
        else:
            # DB Human Insert
            dynamo_table.put_item(Item={'dna': ''.join(dna), 'mutant': False})
            return abort(403)
    except ValueError:  # Not even Homo Sapiens DNA
        return abort(403)

# Challenge Level 3
@app.route('/stats', methods=['GET'])
def mutant_stats():
    mutant_stats_dict = {
        "count_mutant_dna": 0,
        "count_human_dna": 0,
        "ratio": 0.0
    }
    query_dynamo = dynamo_table.scan()
    if query_dynamo['Count'] == 0:
        return jsonify(mutant_stats_dict)
    else:
        items = query_dynamo['Items']
        mutants_qty = len([item for item in items if item['mutant'] is True])
        humans_qty = len([item for item in items if item['mutant'] is False])
        mutant_stats_dict['count_mutant_dna'] = mutants_qty
        if humans_qty != 0:
            mutant_stats_dict['count_human_dna'] = humans_qty
            mutant_stats_dict['ratio'] = round(mutants_qty / humans_qty, 2)
    return jsonify(mutant_stats_dict)


if __name__ == '__main__':
    app.run(debug=False)
