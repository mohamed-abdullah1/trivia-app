import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from models import setup_db, Question, Category, db
from random import randint

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    HELPER FUNCTIONS
    """
    def find_random_id(prev_question_id):
        ids = [q.format()['id'] for q in Question.query.all()]
        while (True):
            random_id = randint(0, len(ids)-1)
            if ids[random_id] != prev_question_id:
                return ids[random_id]

    def find_random_id_for_category(prev_question_id, cat):
        ids = [q.format()['id'] for q in Question.query.all()
               if q.format()['category'] == cat]
        while (True):
            random_id = randint(0, len(ids)-1)
            if ids[random_id] != prev_question_id:
                return ids[random_id]
    """
    !DONE ✅
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    !DONE ✅
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        # response.headers.add('Access-Control-Allow-Headers',
        #                      'Content-Type,Authorization,true')
        # response.headers.add('Access-Control-Allow-Methods',
        #                      'GET,PATCH,POST,DELETE,OPTIONS')
        # response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers['Access-Control-Allow-Methods'] = '*'
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    """
    !DONE ✅
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_all_cats():
        try:
            cats = [cat.format() for cat in Category.query.all()]
            if len(cats) == 0:
                abort(400)
            return jsonify({
                'success': True,
                'categories': cats,
                'total_categories': len(cats)
            })
        except Exception as e:
            print('😞', e)
            db.session.rollback()
            print(sys.exc_info())
            abort(400)
        finally:
            db.session.close()

    """
    !DONE PUT REVIEW AGAIN 💠
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page-1)*10
        end = start+10
        err_404 = False
        try:
            questionQuery = Question.query.all()
            questions = [q.format() for q in questionQuery]
            allCats = [c.format()['type'] for c in Category.query.all()]
            cats = []
            for q in questionQuery[start:end]:
                q_id = q.format().get('category', None)
                cats.append(allCats[q_id-1])
            if len(questions[start:end]) == 0:
                err_404 = True
                abort(404)
            return jsonify({
                'success': True,
                'questions': questions[start:end],
                'total_questions': len(questionQuery),
                'categories': list(set(cats))
            })
        except Exception as e:
            print('😁', e)
            db.session.rollback()
            print(sys.exc_info())
            if err_404:
                abort(404)
            abort(400)
        finally:
            db.session.close()

    """
    !DONE ✅
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        err_404 = False
        try:
            question = Question.query.filter_by(id=question_id).first()
            if question is None:
                err_404 = True
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'deleted_question': question.format(),
                'total_questions': len(Question.query.all()),
                'msg': 'Question Has Been Deleted Successfully!'
            })
        except Exception as e:
            print('😁', e)
            db.session.rollback()
            if err_404:
                abort(404)
            abort(400)
        finally:
            db.session.close()

    """
    !DONE ✅
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions/', methods=['POST'])
    def create_question():
        question_text = request.get_json().get('question_text', None)
        answer = request.get_json().get('answer', None)
        difficulty = request.get_json().get('difficulty', None)
        category = request.get_json().get('category', None)
        try:
            if (question_text is None) or (answer is None) or (difficulty is None) or (category is None):
                abort(422)
            newQuestion = Question(question=question_text,
                                   answer=answer, difficulty=difficulty, category=category
                                   )
            newQuestion.insert()
            return jsonify({
                'success': True,
                'created_question': newQuestion.format(),
                'msg': 'Question Has Been Created Successfully!',
                'total_questions': len(Question.query.all())
            })
        except Exception as e:
            print('😁', e)
            db.session.rollback()
            print(sys.exc_info())
            # if err_422:
            #     abort(422)
            abort(422)
        finally:
            db.session.close()
    """
    !DONE ✅
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_text = request.get_json().get('search_text', None)
        err_422 = False
        try:
            if search_text is None:
                err_422 = True
                abort(422)
            questions_result = Question.query.filter(
                Question.question.ilike(f'%{search_text}%')).all()
            questions = [q.format() for q in questions_result]
            return jsonify({
                'success': True,
                'questions': questions,
                'total_fetched_questions': len(questions)
            })
        except Exception as e:
            print('😁', e)
            db.session.rollback()
            print(sys.exc_info())
            if err_422:
                abort(422)
            abort(400)
        finally:
            db.session.close()
    """
    !DONE ✅
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/questions/category/<category_id>', methods=['GET'])
    def get_questions_for_category(category_id):
        err_404 = False
        try:
            categories_ids = [c.format()['id'] for c in Category.query.all()]
            if int(category_id) not in categories_ids:
                err_404 = True
                abort(404)
            questions_result = Question.query.filter_by(
                category=category_id).all()
            if len(questions_result) == 0:
                err_404 = True
                abort(404)
            questions = [q.format() for q in questions_result]
            return jsonify({
                'success': True,
                'questions': questions,
                'total_fetched_questions': len(questions),
            })
        except Exception as e:
            print('😁', e)
            db.session.rollback()
            print(sys.exc_info())
            if err_404:
                abort(404)
            abort(400)
        finally:
            db.session.close()
    """
    !DONE ✅
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/questions/play/', methods=['POST'])
    def question_play():
        category = request.get_json().get('category', None)
        prev_question = request.get_json().get('question', None)
        err_422 = False
        try:
            if (category is None) or (prev_question is None):
                err_422 = True
                abort(422)
            question = {}
            if category == 'all':  # check for the category
                new_question_id = find_random_id(prev_question['id'])
                question = Question.query.filter(
                    Question.id == new_question_id).first()
            else:
                new_question_id = find_random_id_for_category(
                    prev_question['id'],
                    category
                )
                question = Question.query.filter(
                    Question.category == category, Question.id == new_question_id).first()
                print(question)
            return jsonify({
                'success': True,
                'question': question.format()
            })
        except Exception as e:
            print('😁', e)
            db.session.rollback()
            print(sys.exc_info())
            if err_422:
                abort(422)
            abort(400)
        finally:
            db.session.close()
    """
    !DONE ✅
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.@
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Make sure that the data sent in the request contains all valid fields and values beforehand."
        }), 422
    return app
