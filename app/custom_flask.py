
import stripe
import os
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse
import hashlib  # For password hashing

app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to parse JawsDB URL and create a connection
def create_connection():
    try:
        jawsdb_url = os.getenv("JAWSDB_URL")
        if not jawsdb_url:
            print("JawsDB URL not found in environment variables.")
            return None

        parsed_url = urlparse(jawsdb_url)
        username = parsed_url.username
        password = parsed_url.password
        hostname = parsed_url.hostname
        port = parsed_url.port
        database = parsed_url.path.lstrip('/')

        connection = mysql.connector.connect(
            host=hostname,
            port=port,
            user=username,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        print(f"Error connecting to JawsDB MySQL: {e}")
        return None

# Function to register new users
def register_user(username, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, hash_password(password)))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error registering user: {e}")
    return False

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({"error": str(e)}), 400

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session["customer_email"]
        customer_name = session["metadata"]["customer_name"]

        # Register the user in the database
        if register_user(customer_name, "default_password"):  # Replace with actual password logic
            print(f"User {customer_name} registered successfully!")
        else:
            print(f"Failed to register user {customer_name}.")

    return jsonify({"success": True}), 200

if __name__ == "__main__":
    app.run(port=4242)