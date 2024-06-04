## CookBook Flask Web Application

This is a Flask web application that requires an SQL database and a configuration file. The application is hosted locally.

### Setup Instructions
1. Create a virtual environment ("venv"). The process of doing this depends on your OS.
   Activate the newly created venv.
   Next, we must install the necessary dependencies. Navigate to the root folder of this app (where the file 'requirements.txt' is placed), and run the command (Linux):
   ```
   pip install -r requirements.txt
   ```

2. Set up your SQL database: Before starting the Flask app, you need to import the `/cookbook.sql` file into your SQL server. The specific steps depend on the database management system (DBMS) you're using. For example, if you're using PostgreSQL you can use the `psql` command-line tool to import the SQL file:
   ```
   pysql -U <username> CookBook < <path_to_cookbook.sql>
   ```
   Replace `<username>` with your PostgreSQL username, and `cookook.sql` with the appropriate path to the SQL file.

3. Edit the configuration file `config.ini` in the root folder, and provide the necessary SQL database information in it. `host` should be `localhost`, `port` should be `5432`, and `database` preferably `cookbook`. The rest depends un the user.
  
4. Run the Flask app: To start your Flask app, head to terminal, navigate to the root file (where the '__init__.py' files is located), and enter the command (Linux):
   ```
   flask run
   ```
   If there is an issue, try entering this:

   ```
   export FLASK_ENV = development

   flask run
   ```
   
   Flask will start a local server, and you can access your web application by visiting the provided URL (usually http://localhost:5000).

### How to use

LANDING PAGE ('index'): When you run our web-app, you will see a page with a pink bar and a cookbook logo - that is all.

SIGN UP: You sign up by clicking the 'Sign Up' button in the top right corner. This will take you to a page where you can enter name, email (e.g. name@mail.dk), and password.

LOGIN: When you have signed up, you login by clicking 'Login' in the top right corner. This takes you to a page where you can enter your login data. Once yoy're logged in, you will have 2 new blue buttons, 'Add New Recipe', and 'View Recipes'.

ADD NEW RECIPE: Here you can add a new recipe by entering a name, comment, ingredients, and amount (integer) of each ingredient. Note: If you want to add 1 oats and 2 milk, the lines in the ingredients and amount have to match e.g.:
Ingredient:
```
oats
milk
```
Amount:
```
1
2
```

VIEW RECIPES: Here you can see the recipes in your database (the five we have created, and the ones you might have added).

SEARCH FOR RECIPES: You can find a recipe in your database by typing its name or parts of the name (this works with ##regular## expression matching). As an example, try typing 'rød', and you will see the recipe for 'rødgrød' and 'risengrød'.

RATE A RECIPE: To rate a recipe, you navigate to your chosen recipe, choose a rating of 1-5 (worst to best), and press 'Submit'.

Happy cooking and rating! 
   
 ### ER-Diagram for the database:
![er_diagram](https://github.com/mikkel-kjaerulf/my_train_list/assets/114149729/1181f28f-42c3-44f4-ad0f-9effcd5fe962)
 
 ### Images
<img width="1440" alt="home_page" src="https://github.com/helenafeldner/CookBook/blob/main/images/First_page.png">
<img width="1440" alt="Sign up" src="https://github.com/helenafeldner/CookBook/blob/main/images/Sign_up.png">
<img width="1440" alt="log in" src="https://github.com/helenafeldner/CookBook/blob/main/images/Log_in.png">
<img width="1440" alt="new front page" src="https://github.com/helenafeldner/CookBook/blob/main/images/Front_pages.png">
<img width="1440" alt="add recipe" src="https://github.com/helenafeldner/CookBook/blob/main/images/Add_recipe.png">
<img width="1440" alt="view recipes" src="https://github.com/helenafeldner/CookBook/blob/main/images/All_recipes.png">
<img width="1440" alt="search result" src="https://github.com/helenafeldner/CookBook/blob/main/images/Search_results.png">


