from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager
from psycopg2 import sql
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
import os

# encrypt passwords with flask-bcrypt
from flask_bcrypt import Bcrypt

import configparser

# Get the directory of the Flask app
app_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config.ini file relative to the app directory
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

    if result is not None:
        user_id, name, mail, password = result
        user = User([user_id, name, mail, password])
        return user

    conn.close()

# Configure the database connection
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
        return redirect('/')  # Redirect to another page (e.g., dashboard) if user is already logged in

    if request.method == 'POST':

        # open connection to the database
        connection = get_db_connection()
        cursor = connection.cursor()
        mail = request.form['mail']
        password = request.form['password']
        # get user with the same mail and check if the password is correct
        query = "SELECT id, name, mail, password FROM users WHERE mail = %s"
        cursor.execute(query, (mail,))
        result = cursor.fetchone()
        if result and bcrypt.check_password_hash(result[3], password):
            user = User(result)
            login_user(user)
            return jsonify({'redirect': True})  # Return JSON response for successful login
        else:
            return jsonify({'redirect': False, 'message': 'Invalid mail or password'})  # Return JSON response for unsuccessful login
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search')
        return redirect(url_for('search', query=search_query))

    print('reached')

    # get the trains ordered by rating
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT name, operators, family, picture, round AS rating FROM trains AS t LEFT JOIN (SELECT r.tid, ROUND(AVG(r.rating),2), COUNT(r.rating) FROM reviews r GROUP BY r.tid) AS r ON t.id = r.tid ORDER BY r.round DESC nulls last;")
    results = cursor.fetchall()

    # get the header
    headers = [desc[0] for desc in cursor.description]

    # get the rating based on the header
    rating = headers.index('rating')

    # get the latest trains
    cursor.execute(f"SELECT name, operators, family, picture, round AS rating FROM trains AS t LEFT JOIN (SELECT r.tid, ROUND(AVG(r.rating),2), COUNT(r.rating) FROM reviews r GROUP BY r.tid) AS r ON t.id = r.tid ORDER BY t.in_service DESC nulls last LIMIT 20;")
    lresults = cursor.fetchall()


    # get the trains ordered by speed
    cursor.execute(f"SELECT name, operators, family, picture, round AS rating, max_speed_record as speed FROM trains AS t LEFT JOIN (SELECT r.tid, ROUND(AVG(r.rating),2), COUNT(r.rating) FROM reviews r GROUP BY r.tid) AS r ON t.id = r.tid ORDER BY t.max_speed_record DESC nulls last LIMIT 20;")
    rsresults = cursor.fetchall()

    # if user logged in get trains from their list
    user_logged_in = False
    uresults = None
    if current_user.is_authenticated:
        cursor.execute(f"SELECT name, operators, family, picture, round AS rating FROM trains AS t LEFT JOIN (SELECT r.tid, ROUND(AVG(r.rating),2), COUNT(r.rating) FROM reviews r GROUP BY r.tid) AS r ON t.id = r.tid WHERE t.id IN (SELECT tid FROM listed_trains WHERE uid = {current_user.id});")
        uresults = cursor.fetchall()
        if len(uresults) > 0:
            user_logged_in = True
    cursor.close()
    connection.close()
    

    return render_template('index.html', top_rows=results, headers=headers, column_with_image_index=3, rating=rating, latest_rows=lresults, column_with_train_name_index=0, rspeed_rows=rsresults, user_logged_in=user_logged_in, user_rows=uresults)

@app.route('/users', methods=['GET', 'POST'])
def users():

    # get users by name if search is performed
    if request.method == 'POST':
        search_query = request.form.get('search')
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT name FROM users WHERE name ILIKE '%{search_query}%';")
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('users.html', users=results)


    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM users;")
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('users.html', users=results)

@app.route('/list/<name>', methods=['GET', 'POST'])
def mylist(name):
    if request.method == 'POST':
        search_query = request.form.get('search')
        return redirect(url_for('search', query=search_query))


    # get the trains by user
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT t.name, t.picture, r.rating FROM trains AS t RIGHT JOIN listed_trains AS lt ON t.id = lt.tid LEFT JOIN reviews AS r ON r.tid=lt.tid AND r.uid = lt.uid  WHERE lt.uid = (SELECT u.id FROM users u WHERE u.name='{name}');")
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    # get the header
    headers = [desc[0] for desc in cursor.description]

    # get the rating based on the header
    rating = headers.index('rating')

    return render_template('mylist.html', rows=results, headers=headers, column_with_image_index=1, column_with_train_name_index=0, name=name, rating_index=rating)


@app.route('/search')
def search():
    query = request.args.get('query')

    # Perform search in the database based on the query
    connection = get_db_connection()
    cursor = connection.cursor()
    # Define the search query

    # Build the dynamic query
    columns_query = '''
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'trains'
    '''
    cursor.execute(columns_query)
    columns = [column[0] for column in cursor.fetchall()]

    # drop the id column
    columns.pop(0)

    search_condition = ' OR '.join(f"{column} ILIKE '%{query}%'" for column in columns)
    dynamic_query = f"SELECT * FROM trains WHERE {search_condition}"

    # Execute the dynamic query
    cursor.execute(dynamic_query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    # get the header
    headers = [desc[0] for desc in cursor.description]

    return render_template('search.html', results=results, headers=headers, column_with_image_index=10, column_with_train_name_index=1)

@app.route('/table')
def render_table():
    # Establish a connection to the PostgreSQL database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the sorting option from the request parameters
    sort_option = request.args.get('sort', 'default')

    # Build the SQL query with the sorting option
    if sort_option == 'train_name':
        query = 'SELECT * FROM trains ORDER BY name'
    elif sort_option == 'max_op_speed':
        query = 'SELECT * FROM trains ORDER BY max_speed_operational DESC NULLS LAST'
    elif sort_option == 'max_design_speed':
        query = 'SELECT * FROM trains ORDER BY max_speed_design DESC NULLS LAST'
    elif sort_option == 'max_speed_record':
        query = 'SELECT * FROM trains ORDER BY max_speed_record DESC NULLS LAST'
    elif sort_option == 'year_in_service':
        query = 'SELECT * FROM trains ORDER BY in_service DESC NULLS LAST'
    else:
        query = 'SELECT * FROM trains'

    # Execute the SQL query
    cursor.execute(query)
    # Fetch all rows from the result set
    rows = cursor.fetchall()



    # get the header
    headers = [desc[0] for desc in cursor.description]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Render the HTML template with the table data
    return render_template('table.html', rows=rows, headers=headers, column_with_image_index=10, column_with_train_name_index=1)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect('/')  # Redirect to another page (e.g., dashboard) if user is already logged inesult[3] == password
    if request.method == "POST":
        # Establish a connection to the PostgreSQL database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get input data
        name = request.form.get("fname")
        mail = request.form.get("femail")
        password = request.form.get("fpassword")
        # encrypt password with bcrypt
        password = bcrypt.generate_password_hash(password).decode('utf-8')
                                            
        # Check if email already exists in the database
        cursor.execute("SELECT * FROM users WHERE mail = %s", (mail,))
        existing_user_mail = cursor.fetchone()

        # check if name already exists in the database
        cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
        existing_user_name = cursor.fetchone()

        if existing_user_mail:
            # Display popup message if email already exists
            return jsonify({'redirect': False, 'message': 'Email already used'})

        if existing_user_name:
            # Display popup message if name already exists
            return jsonify({'redirect': False, 'message': 'Name already used'})

        # Insert new user into the database
        # Get max uid and add 1 to get new id for user
        cursor.execute("SELECT MAX(id) FROM users;")
        uid = cursor.fetchall()[0][0] + 1
        cursor.execute("INSERT INTO users (id, name, mail, password) VALUES (%s, %s, %s, %s)", (uid, name, mail, password))
        conn.commit()
        cursor.close()
        conn.close()

        login_user(User([uid, name, mail, password]))
        # Redirect to a success page or perform any other action
        return jsonify({'redirect': True})

    return render_template('signup.html')

@app.route('/train/<name>', methods=["GET", "POST"])
def train_view(name):
    # Establish a connection to the PostgreSQL database
    conn = get_db_connection()
    cursor = conn.cursor()

    # get train info
    cursor.execute("SELECT * FROM trains WHERE trains.name = '%s';" % (name) )
    row = cursor.fetchall()
    train_id = row[0][0]
    train_name = row[0][1]
    train_operator = row[0][2]
    train_family = row[0][3]
    train_manufacturer = row[0][4]
    train_power_supply = row[0][5]
    train_max_speed_op = row[0][6]
    train_max_speed_d = row[0][7]
    train_max_speed_rec = row[0][8]
    train_in_service = row[0][9]
    train_picture = row[0][10]
    cursor.close()
    conn.close()

    # get the reviews
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT u.name, r.rating, r.comment FROM users u RIGHT JOIN reviews r ON r.uid = u.id WHERE r.tid = %s;" % (train_id) )
    reviews = cursor.fetchall()
    usernames = [review[0] for review in reviews]
    ratings = [review[1] for review in reviews]
    comments = [review[2] for review in reviews]

    # get average rating of the train
    query = sql.SQL("""SELECT ROUND(AVG(rating),2) FROM reviews WHERE tid = %s;""").format()
    cursor.execute(query, [train_id])
    avg_rating = cursor.fetchall()[0][0]

    # get whether the train is already on user list
    query = sql.SQL("""SELECT * FROM users u RIGHT JOIN listed_trains lt ON u.id = lt.uid WHERE u.id = %s AND lt.tid = %s """).format()
    cursor.execute(query, [current_user.get_id(), train_id])
    matches = cursor.fetchall()

    if matches:
        in_user_list = True
    else:
        in_user_list = False

    cursor.close()
    conn.close()


    if request.method == "POST":
        if not current_user.is_authenticated:
            return redirect('/signup')

        conn = get_db_connection()
        cursor = conn.cursor()

        if request.form['form_name'] == 'add-to-list':

            query = sql.SQL("INSERT INTO listed_trains (uid, tid) VALUES (%s, %s)").format()
            cursor.execute(query, [current_user.get_id(), train_id])
            conn.commit()

            cursor.close()
            conn.close()
            return redirect(url_for('train_view', name=name))

        elif request.form['form_name'] == 'remove-from-list':
            query = sql.SQL("""DELETE FROM listed_trains lt WHERE lt.uid = %s AND lt.tid = %s""").format()
            cursor.execute(query, [current_user.get_id(), train_id])
            conn.commit()

            cursor.close()
            conn.close()
            return redirect(url_for('train_view', name=name))

        elif request.form['form_name'] == 'review':
            # get typed comment and rating
            comment = request.form.get("freviewtext")
            rating = request.form.get('fscore')

            # check if user has already left a review for this train
            query = sql.SQL("""SELECT COUNT(1) FROM reviews WHERE tid = %s AND uid = %s;""")
            cursor.execute(query, [train_id, current_user.get_id()])
            res = cursor.fetchall()[0][0]

            # if user has not left a review, insert into table
            if (res == 0):
                query = sql.SQL("""INSERT INTO reviews (uid, tid, rating, comment) VALUES (%s, %s, %s, %s)""").format()
                cursor.execute(query, (current_user.get_id(), train_id, rating, comment))
                conn.commit()
            # if user has left a review, update it
            else:
                query = sql.SQL("""UPDATE reviews SET rating = %s, comment = %s WHERE tid = %s AND uid = %s;""").format()
                cursor.execute(query, (rating, comment, train_id, current_user.get_id()))
                conn.commit()

            cursor.close()
            conn.close()

            # redirect to the same page to update the reviews
            return redirect(url_for('train_view', name=name))

    return render_template(
        'trainview.html',
        name = train_name,
        operator = train_operator,
        family = train_family,
        manufacturer = train_manufacturer,
        power_supplu = train_power_supply,
        max_speed_op = train_max_speed_op,
        max_speed_d = train_max_speed_d,
        max_speed_rec = train_max_speed_rec,
        in_service = train_in_service,
        picture = train_picture,
        usernames = usernames,
        ratings = ratings,
        comments = comments,
        avg_rating = avg_rating,
        in_user_list = in_user_list)

# run server if this file is run directly
if __name__ == '__main__':
    app.run(debug=True)