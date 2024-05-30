## MyTrainList Flask Web Application

This is a Flask web application that requires an SQL database and a configuration file.

### Setup Instructions
   If you have Docker-Compose installed, initializing this webserver is a two-liner. Navigate to the root folder of this repository, and run:
   ```
   sudo docker compose build
   ```
   ```
   sudo docker-compose up -d
   ```
   You can check the logs for the port at which the server is running by executing:
   ```
   sudo docker logs my_train_list-web-1
   ```
   If you dont have Docker-Compose, please follow the following instructions.


1. Install Flask and other dependencies: Make sure you have the dependencies installed in your Python environment. You can install it using `pip` by running:
   ```
   pip install Flask
   ```
   ```
   pip install flask-login
   ```
   ```
   pip install psycopg2
   ```

2. Set up your SQL database: Before starting the Flask app, you need to import the `/services/web/train_list.sql` file into your SQL server. The specific steps depend on the database management system (DBMS) you're using. For example, if you're using PostgreSQL you can use the `psql` command-line tool to import the SQL file:
   ```
   pysql -U <username> <database_name> < <path_to_train_list.sql>
   ```
   Replace `<username>` with your PostgreSQL username, `<database_name>` with the name of your database, and `train_list.sql` with the appropriate path to the SQL file.

3. Edit the configuration file `config.ini` in the `/services/web/project` folder and provide the necessary SQL database information in it. Here you may need to change the `host` variable to `localhost` instead of `db`.
  
4. Run the Flask app: To start your Flask app, run the `__init__.py` file in the `/services/web/project/` folder:
   ```
   python /services/web/project/__init__.py
   ```
   Flask will start a local server, and you can access your web application by visiting the provided URL (usually http://localhost:5000).

### How to use

The web app works a lot like sites such as IMDB and My Anime List. The site can be navigated using the bar in the top of the page. Hovering the mouse above a train, will give a show the trains average rating. Clicking on train will take the user to the trains page where additional information is presented. Here, a user can leave a review and rating for the train provided they are signed in. A user can sign up by providing a user name, email and password. Users can also add trains to their own list. A user can only have one list.
   
 ### ER-Diagram for the database:
![er_diagram](https://github.com/mikkel-kjaerulf/my_train_list/assets/114149729/1181f28f-42c3-44f4-ad0f-9effcd5fe962)
 
 ### Images
<img width="1440" alt="home_page" src="https://github.com/mikkel-kjaerulf/my_train_list/assets/114149729/3b97795e-f36c-47ce-be7b-45df5fb2c4ef">
<img width="1440" alt="train_info" src="https://github.com/mikkel-kjaerulf/my_train_list/assets/114149729/6cbac82e-a844-4ac6-9aff-e839e3029131">
<img width="1440" alt="train_review" src="https://github.com/mikkel-kjaerulf/my_train_list/assets/114149729/8e97af7d-6fdf-44cc-94e8-af472ffad859">
<img width="1440" alt="list_example" src="https://github.com/mikkel-kjaerulf/my_train_list/assets/114149729/cd3047ca-8e7f-4834-a84c-0c94a1838599">


