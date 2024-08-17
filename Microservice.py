import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

amazon_api_endpoint = "https://api.amazon.com/products"
flipkart_api_endpoint = "https://api.flipkart.com/products"
myntra_api_endpoint = "https://api.myntra.com/products"

def fetch_products(endpoint, category, min_price, max_price):
  params = {
    "category": category,
    "min_price": min_price,
    "max_price": max_price
  }
  response = requests.get(endpoint, params=params)
  if response.status_code == 200:
    return response.json()
  else:
    # Handle error
    return []

def filter_and_sort_products(products):
  filtered_products = [p for p in products if min_price <= p['price'] <= max_price]
  sorted_products = sorted(filtered_products, key=lambda p: p['rating'], reverse=True)
  return sorted_products

@app.route('/categories/<category>/products')
def get_products(category):
  min_price = float(request.args.get('min_price', 0))
  max_price = float(request.args.get('max_price', 10000))

  amazon_products = fetch_products(amazon_api_endpoint, category, min_price, max_price)
  flipkart_products = fetch_products(flipkart_api_endpoint, category, min_price, max_price)
  myntra_products = fetch_products(myntra_api_endpoint, category, min_price, max_price)

  all_products = amazon_products + flipkart_products + myntra_products
  filtered_and_sorted_products = filter_and_sort_products(all_products)

  return jsonify(filtered_and_sorted_products)

if __name__ == '__main__':
  app.run(debug=True)

