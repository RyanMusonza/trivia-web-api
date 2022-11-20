import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Method to get a list of paginated questions to be used through out route handlers

def get_paginated_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={'/': {'origins': '*'}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(res):
        res.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        res.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')

        return res

        
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()


        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions')
    def get_questions():
                
        questions = Question.query.all()
        current_questions = get_paginated_questions(request, questions)
        categories = Category.query.all()
        # If for whatever reason the user lands on a page out of bounds, we want to return an error
        if (len(current_questions)==0):
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': None,
            'categories': {category.id: category.type for category in categories}
        }), 200
        

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()

            return jsonify({
                'success': True,
                'message': 'Question successfully deleted'
            }), 200

        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        try:
            new_question = data.get('question')
            new_answer = data.get('answer')
            new_difficulty = data.get('difficulty')
            new_category = data.get('category')

            question = Question(question = new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()

            return jsonify({
                'success': True,
                'messgae': 'Question successfully created'
            }), 201

        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        data = request.get_json()
        search_term = data.get('searchTerm', '')

        try:
            search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            current_questions = get_paginated_questions(request, search_results)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'current_category': None
            }), 200
        except:
            abort(404)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.
    """

    @app.route('/categories/<int:cat_id>/questions')
    def get_questions_by_category(cat_id):
        try:
            cats = Category.query.with_entities(Category.type).filter(Category.id == cat_id).first()
            
            total_questions = Question.query.all()
            questions = Question.query.filter(Question.category == str(cat_id)).all()
            current_questions = get_paginated_questions(request, questions)

            return jsonify({
                'success': True,
                'question': current_questions,
                'total_questions': len(total_questions),
                'current_category': cats[0] 
            }), 200
        except:
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    
    
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():

        try:
            body = request.get_json()
            prev_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')

            # Zero is the default value for categories. If that is provided then all of the questions can be used for the active quiz
            if (quiz_category['id'] == 0):
                questions = Question.query.all()
            else: 
                questions = Question.query.filter_by(category = quiz_category['id']).all()
            
            # Code to get a random index for the questions. -1 because indexes start at 0 and the results of the questions start from 1
            randomizerIndex = random.randint(0, len(questions)-1)
            next_question = questions[randomizerIndex]

            active_questions = True
            
            # While loop to use all of the remaining questions as next questions. If it finds 
            # the next question's id in the list of previous questions, it should assign a new random index to the next question
            while active_questions: 
                if next_question.id in prev_questions:
                    next_question = questions[randomizerIndex]
                else:
                    active_questions = False
                    # Once there are no more active questions left it should return a message informing the user
                    return jsonify({
                        'success': True,
                        'message': 'No more questions left'
                    })
                    
            return jsonify({
                        'success': True,
                        'question': next_question.format()
                    }), 200
        
        except:
            abort(404)
        
    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request error"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def invalid_method(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Invalid method"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable resource"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'An internal error has occured, please try again'
        }), 500

    return app

