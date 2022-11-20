# Trivia API

Trivia API is a web based application that allows users to hold trivia games. The app allows a user to:

1) Display questions - both all questions and by category. Questions should show the question, category, and difficulty rating by default and can show/hide the answer.
2) Delete questions.
3) Add questions and require that they include the question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

## Getting started

### Installing Dependencies

#### Python 3.7 

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment  

Working within a virtual environment is recommended as it keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies 

Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

##### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Setting up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

## API Reference

### Getting Started

* Backend Base URL: `http://127.0.0.1:5000/`
* Frontend Base URL: `http://127.0.0.1:3000/`
* Authentication: This version of the application does not require authentication or API keys

### Error Handling

Errors are returned as JSON objects in the following format:

```json
      {
        "success": "False",
        "error": 404,
        "message": "Resource not found",
      }
```
The API will currently return 5 error types when requests fail:

* 400 – Bad request
* 404 – Resource not found
* 405 – Invalid method
* 422 – Unprocessable resource
* 500 – Internal server error


### Endpoints

#### GET /categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample:  `curl http://127.0.0.1:5000/categories`

```json
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "success": true
    }
```

#### GET /questions

- Fetches questions which are paginated, total number of questions as well as the categories
- Request Arguments: None
- Returns: A paginated list of questions (10 questions per page), a list of all the categories, total number of questions in the database
- Sample: `curl http://127.0.0.1:5000/questions`

```json
    {
        "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
        },
        "current_category": null,
        "questions": [
          {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
          },
          {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
          },
          {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
          },
          {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
          },
          {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
          },
          {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
          },
          {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
          },
          {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
          },
          {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
          },
          {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
          }
        ],
        "success": true,
        "total_questions": 19
    }
```

#### GET /categories/<int:id>/questions

- Fetches category specific questions
- Request Arguments: id 
- Returns: A paginated list of category specific questions (10 questions per page), the name of the current category and the total number of questions in the database
- Sample: `curl http://127.0.0.1:5000/category/1/questions`

```json
    {
        "current_category": "Science",
        "question": [
          {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
          },
          {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
          },
          {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
          }
        ],
        "success": true,
        "total_questions": 19
    }
```

#### POST /questions/

- Sends a post request to add a new question to the database
- Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"question\": \"Who wears jersey no. 11 for Liverpool FC?\", \"answer\": \"Mohammed Salah\", \"difficulty\": 2, \"category\": \"6\" }" http://127.0.0.1:5000/questions`

```json
    {
        "message": "Question successfully created",
        "success": true
    }
```

#### POST /questions/search

- Sends a post request to search for a question(s) from the database using a search term provided by the user
- Request Arguments: searchTerm 
- Returns: A paginated list of questions that match the search term provided by the user, the total number of questions
- Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"searchTerm\": \"Liverpool\"}" http://127.0.0.1:5000/questions/search`

```json
    {
        "current_category": null,
        "questions": [
          {
            "answer": "Mohammed Salah",
            "category": 6,
            "difficulty": 2,
            "id": 24,
            "question": "Who wears jersey no. 11 for Liverpool FC?"
          }
        ],
        "success": true,
        "total_questions": 20
    }
```

#### DELETE /questions/<int:id>

- Deletes a question from the database using its id
- Request Arguments: id 
- Returns: A message stating that the question was successfully deleted
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/24`

```json
    {
        "message": "Question successfully deleted",
        "success": true
    }
```

#### POST /quizzes

- Sends a post request to get the next question from the database taking into account the previous questions as well as the quiz category
- Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"previous_questions\": [], \"quiz_category\": {\"type\":\"History\", \"id\": \"4\"}}" http://127.0.0.1:5000/quizzes`

```json
    {
        "question": {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        },
        "success": true
    } 
```

## Authors

* Ryan Musonza worked on the API implenting the backend code, integrating the front end with the back end as well as the test suite
* Udacity for providing the database, front end code as well as all backend skeleton code 

