import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
# from flask import json
from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import dotenv_values


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_copy"
        username = dotenv_values()['USERNAME']
        password = dotenv_values()['PASSWORD']
        self.database_path = f'postgresql://{username}:{password}@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_categories'])
        self.assertTrue(data['categories'])
        self.assertEqual(res.status_code, 200)

    ######## GET /questions ########################
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(res.status_code, 200)

    def test_404_questions(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data['error'], 404)
        self.assertEqual(res.status_code, 404)
    ########END GET /questions ########################

    def test_create_question(self):
        res = self.client().post('/questions/', json={
            'question_text': 'HO HO HO?',
            'answer': 'YEP YEP :>',
            'difficulty': 1,
            'category': 4
        })
        data = json.loads(res.data)
        questions = Question.query.all()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['msg'])
        self.assertEqual(len(questions), data['total_questions'])

    def test_delete_question(self):
        res = self.client().delete('/questions/15')
        data = json.loads(res.data)
        questions = Question.query.all()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['msg'])
        self.assertEqual(data['deleted_question'].get('id'), 15)
        self.assertEqual(len(questions), data['total_questions'])
    ############POST /questions/search###############

    def test_search_question(self):
        res = self.client().post('/questions/search', json={
            'search_text': 'title'
        })
        data = json.loads(res.data)
        questions = Question.query.filter(
            Question.question.ilike('%title%')).all()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(questions), data['total_fetched_questions'])

    def test_search_422_error_question(self):
        res = self.client().post('/questions/search', json={
            'search': 'title'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Make sure that the data sent in the request contains all valid fields and values beforehand.")
        self.assertEqual(data['error'], 422)
    ############END POST /questions/search###############

    ############ GET /questions/category/category_id ###############
    def test_questions_on_category(self):
        res = self.client().get('/questions/category/6')
        data = json.loads(res.data)
        questions = Question.query.filter(
            Question.category == 6).all()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(questions), data['total_fetched_questions'])

    def test_err_404_questions_on_category(self):
        res = self.client().get('/questions/category/11')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')
    ############ END  GET /questions/category/category_id ###############

    ####### POST /question/play ########
    def test_question_play(self):
        res = self.client().post('/questions/play/', json={
            'category': 4,
            'question': {
                'id': 31
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question']['id'] != 31)
        self.assertTrue(data['question']['category'] == 4)

    def test_error_422_question_play(self):
        res = self.client().post('/questions/play/', json={
            'question': {
                'id': 31
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Make sure that the data sent in the request contains all valid fields and values beforehand.")
        self.assertEqual(data['error'], 422)
    #######END  POST /question/play ########

    def test_404_error(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data['error'], 404)

    def test_422_error(self):
        res = self.client().post('/questions/', json={
            'question_text': 'HO HO HO?',
            'answer': 'YEP YEP :>',
            'difficulty': 1,
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(
            data['message'], "Make sure that the data sent in the request contains all valid fields and values beforehand.")
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
