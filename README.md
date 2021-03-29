# The Magic Bookshelf 
~ a submission to RowdyHacks 2021 ~
Result: 2nd place overall on the General Track! :)
You can find the project on Devpost here: https://devpost.com/software/placeholder-qncfoe

## Workflows
1. Clone the git repository.
2. ~~ Install dependencies manually or using pip install -r requirements.txt :( `pip install {flask, flask_wtf, wtforms, flask_login, sqlalchemy, mysql-connector-python, email_validator, flask_bootstrap, python-dotenv, requests}` ~~ Make sure to utilize the frozen dependencies list from requirements.txt for pip install within a virtual environment.
```
(virtualenv) $ pip freeze > requirements.txt
$ cd copied-project/
$ python3 -m venv virtualenv/
$ python3 -m pip install -r requirements.txt
```
4. There are necessary environment variables located in ```.env``` (api keys, DB password) and ```.flaskenv``` (metadata about the flask app, specifically if it will run it development/production mode and the python file that will serve as the app's driver)  
5. `flask run`
