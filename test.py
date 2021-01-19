from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_boggle_homepage(self):
        """ testing if highscore and score display on page """
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('boggle_board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_word(self):
        """ testing if word is valid """
        with app.test_client() as client:
            client.get('/')
            resp = client.get('/check-word?word="ghghghgh')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-word')

    def test_score(self):
        """ testing highscore from post request """
        with app.test_client() as client:
            resp = client.post('/user-score', data={'$score': 1})

            self.assertEqual(resp.status_code, 200)
            self.assertIn(resp.json['$score'], 1)
       