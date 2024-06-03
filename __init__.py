from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
from flask_bcrypt import Bcrypt
import configparser
import os
from flask_login import current_user

# Get the directory of the Flask app
app_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(app_dir, 'config.ini')

# Read the configuration file
config = configparser.ConfigParser()
config.read(config_file_path)

# Get the database credentials from the configuration file
db_host = config['Database']['host']
db_port = config['Database']['port']
db_name = config['Database']['database']
db_user = config['Database']['user']
db_password = config['Database']['password']

# Construct the SQLALCHEMY_DATABASE_URI
db_uri = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'trust me bro'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create the User class usermixing from flask_login
class User(UserMixin):
    def __init__(self, user):
        self.id = user[0]
        self.name = user[1]
        self.mail = user[2]
        self.password = user[3]

    def __repr__(self):
        return f'<User: {self.name}>'

@login_manager.user_loader
def load_user(user_id):
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
    query = "SELECT id, name, mail, password FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return User(result)

def get_db_connection():
    connection = psycopg2.connect(
        port=db_port,
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    return connection

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        connection = get_db_connection()
        cursor = connection.cursor()
        mail = request.form['mail']
        password = request.form['password']
        query = "SELECT id, name, mail, password FROM users WHERE mail = %s"
        cursor.execute(query, (mail,))
        result = cursor.fetchone()
        if result and bcrypt.check_password_hash(result[3], password):
            user = User(result)
            login_user(user)
            return jsonify({'redirect': True})
        else:
            return jsonify({'redirect': False, 'message': 'Invalid mail or password'})
        cursor.close()
        connection.close()
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        mail = request.form.get('mail')
        name = request.form.get('name')
        password = request.form.get('password')

        if not mail or not name or not password:
            return jsonify({'redirect': False, 'message': 'All fields are required'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE mail = %s", (mail,))
        user = cursor.fetchone()
        if user:
            return jsonify({'redirect': False, 'message': 'User already exists'}), 400

        # Determine the new user's id
        cursor.execute("SELECT MAX(id) FROM users")
        max_id = cursor.fetchone()[0]
        uid = (max_id + 1) if max_id is not None else 1

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert the new user into the database
        cursor.execute(
            "INSERT INTO users (id, name, mail, password) VALUES (%s, %s, %s, %s)",
            (uid, name, mail, hashed_password)
        )
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'redirect': True})

    return render_template('signup.html')




@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        comment = request.form.get('comment')
        ingredients = [ingredient.strip() for ingredient in request.form.get('ingredient').split('\n')]
        quantities = [quantity.strip() for quantity in request.form.get('quantities').split('\n')]
        print("Received Ingredients:", ingredients)
        print("Received Quantities:", quantities)

        # Process the form data (e.g., insert into the database)
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Insert the new recipe
            cursor.execute(
                "INSERT INTO opskrift (titel, comment) VALUES (%s, %s) RETURNING oid",
                (title, comment)
            )
            oid = cursor.fetchone()[0]  # Get the ID of the newly inserted recipe

            # Commit the transaction for inserting into "opskrift" table
            connection.commit()

            # Insert ingredients for the recipe
            for ingredient, quantity in zip(ingredients, quantities):
                # Check if the ingredient already exists in the ingredienser table
                cursor.execute("SELECT name FROM ingredienser WHERE name = %s", (ingredient,))
                existing_ingredient = cursor.fetchone()
                if not existing_ingredient:
                    # If the ingredient doesn't exist, insert it into the ingredienser table
                    cursor.execute("INSERT INTO ingredienser (name) VALUES (%s)", (ingredient,))
                # Insert the ingredient into the opskriftingrediens table
                cursor.execute(
                    "INSERT INTO opskriftingredienser (oid, name, mængde) VALUES (%s, %s, %s)",
                    (oid, ingredient.strip(), quantity.strip())  # Remove leading/trailing whitespace
                )

            # Commit the transaction
            connection.commit()

            flash('Recipe added successfully!', 'success')
            return redirect('/')
        except Exception as e:
            connection.rollback()
            flash(f'Failed to add recipe: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    
    # If the request method is GET, simply render the form
    return render_template('add_recipe.html')



# Update your Flask routes
@app.route('/view_recipes')
def view_recipes():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch all recipes
    cursor.execute("SELECT titel FROM opskrift")
    recipes = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('view_recipes.html', recipes=recipes)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search')
        return redirect(url_for('search', query=search_query))
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT o.titel, o.comment, COALESCE(AVG(r.stjerner), 0) AS rating
        FROM opskrift o
        LEFT JOIN opskriftrating r ON o.oid = r.oid
        GROUP BY o.oid
        ORDER BY rating DESC;
    """)
    results = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    cursor.close()
    connection.close()
    user_logged_in = current_user.is_authenticated  # Check if the user is logged in
    return render_template('index.html', recipes=results, headers=headers, user_logged_in=user_logged_in)




if __name__ == '__main__':
    app.run(debug=True)