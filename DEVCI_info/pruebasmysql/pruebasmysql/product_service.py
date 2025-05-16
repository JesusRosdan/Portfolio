from flask import Flask
import requests

app = Flask(__name__)

@app.route('/products', methods=['POST'])
def create_product():
    # Handle product creation logic
    # Make an API call to the user authentication microservice
    response = requests.post('http://localhost:5000/register', json={'nombre': 'Jesus', 'password': 'Hola24'})
    if response.status_code == 200:
        return "Product created and user registered successfully"
    else:
        return "Failed to create product"

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    # Handle product retrieval logic
    return f"Product ID: {product_id}"

@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    # Handle product update logic
    return f"Product ID: {product_id} updated successfully"

@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Handle product deletion logic
    return f"Product ID: {product_id} deleted successfully"

if __name__ == '__main__':
    app.run()
