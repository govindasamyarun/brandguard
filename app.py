from flask import Flask

# Create a Flask web application
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # Run the application in development mode
    app.run(debug=True)