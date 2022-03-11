from crypt import methods
from pdb import post_mortem
from threading import local
from tkinter.messagebox import RETRYCANCEL
from urllib import response
from flask import Flask, jsonify, request
import requests
import socket

app = Flask(__name__)

class Participants:
  def __init__(self, id, name):
    self.id = id
    self.name = name

  def serialize(self):
    return {"id" : self.id, "name": self.name}

class Prizes:
  def __init__(self, id, description):
    self.id = id
    self.description = description

  def serialize(self):
    return {"id" : self.id, "description": self.description}


def max_in_promo():
  max_id = 0
  for promoaction in promoactions:
    if promoaction['id'] > max_id:
      max_id = promoaction['id']
  return max_id

promoactions = [
  {'id': 1, 'name': 'milk', 'description': 'House in village - the best milk in the World.', 'prizes': [Prizes(1, 'money'), Prizes(2, 'ticket to Europe tour'), Prizes(3, 'a car')], 'participants': [Participants(1, 'John'), Participants(2, 'Ivan'), Participants(3, 'Masha')]},
  
  {'id': 2, 'name': 'snickers', 'description': 'do not slow down - eat snickers', 'prizes': [Prizes(1, 'money'), Prizes(2, 'ticket to Europe tour')], 'participants': [Participants(1, 'John'), Participants(2, 'Ivan'), Participants(3, 'Masha'), Participants(4, 'Vasya')]}
]

@app.route('/')
def homepage():
    return 'Welcome to the homepage!'

@app.route('/promoactions', methods=['GET'])
def get_promoactions():
  answer = []
  for promo in promoactions:
    promo_to_ad = {}
    promo_to_ad['id'] = promo['id']
    promo_to_ad['name'] = promo['name']
    promo_to_ad['description'] = promo['description']
    answer.append(promo_to_ad)

  return jsonify(answer), 201


@app.route('/promoactions/<int:promoaction_id>', methods=['GET'])
def get_promoaction(promoaction_id):
  answer = []
  for promo in promoactions:
    promo_to_ad = {}
    promo_to_ad['id'] = promo['id']
    promo_to_ad['name'] = promo['name']
    promo_to_ad['description'] = promo['description']
    promo_to_ad['participants'] = [part.serialize() for part in promo['participants']]
    promo_to_ad['prizes'] = [part.serialize() for part in promo['prizes']]
    answer.append(promo_to_ad)
  return jsonify(answer[promoaction_id]), 201


@app.route('/promoactions', methods=['POST'])
def add_product():
  req = request.get_json()
  promo_to_add = {}
  if ('name' not in req):
    return "You need to specify name before putting it.", 505
  else:
    promo_to_add['name'] = req['name']
  
  if ('description' not in req):
    promo_to_add['description'] = ""
  else:
    promo_to_add['description'] = req['description']
  
  promo_to_add['participants'] = []
  promo_to_add['prizes'] = []
  promo_to_add['id'] = max_in_promo() + 1
  promoactions.append(promo_to_add)
  
  return jsonify(promoactions[-1]["id"]), 201

@app.route('/products/<int:promo_id>', methods=['PUT'])
def put_product(promo_id):
  req = request.get_json()
  if (not req['name']):
    return "You can't change the name of the promo to empty", 505
  else:
    promoactions[promo_id]['name'] = req['name']
  
  promoactions[promo_id]["description"] = req['description']

  return jsonify(promoactions[promo_id])

'''@app.route('/products', methods=['POST'])
def add_product():
  products.append(request.get_json())
  return '', 204

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
  return jsonify(products[product_id])

@app.route('/products/<int:product_id>', methods=['PUT'])
def put_product(product_id):
  products[product_id]['description'] = 'XYZ'
  return jsonify(products[product_id])

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
  products.remove(products[product_id])
  return jsonify({'result': True})

@app.route('/products/<string:product_string>', methods=['GET'])
def get_product_string(product_string):
  answer = []

  for product in products:
    if product_string == product['category_id'] or product_string == product['name'] or product_string == product['description']:
      answer.append(product)
  if len(answer) == 0:
    return 504
  return jsonify(answer), 204'''
