import models
import unittest
import random
from mock import patch

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board, self.cards = models.import_board_data('./board_graph.json')

    def test_border_countries(self):
        country_A = self.board.countries['alaska']
        country_B = self.board.countries['northwest territory']
        self.assertIn(country_A, country_B.border_countries)
        self.assertIn(country_B, country_A.border_countries)

    def test_not_border_countries(self):
        country_A = self.board.countries['iceland']
        country_B = self.board.countries['northwest territory']
        self.assertNotIn(country_A, country_B.border_countries)
        self.assertNotIn(country_B, country_A.border_countries)


    def test_add_troops(self):
        country_A = self.board.countries['iceland']
        erty = models.Player('Erty')
        erty.choose_country(country_A)
        country_A.troops = 20
        erty.deploy_troops(country_A, 10)
        self.assertEqual(country_A.troops, 30)
    
    def test_add_troops_to_wrong_country(self):
        country_A = self.board.countries['northwest territory']
        erty = models.Player('Erty')
        alex = models.Player('Alex')
        erty.choose_country(country_A)
        country_A.troops = 21
        with self.assertRaises(AssertionError):
            alex.deploy_troops(country_A, 10)

    def test_attack(self):
        country_A = self.board.countries['alaska']
        country_B = self.board.countries['northwest territory']
        players = [models.Player('Erty'),models.Player('Alex')]
        country_A.owner = players[0]
        country_B.owner = players[1]
        country_A.troops = 30
        country_B.troops = 10
        with patch.object(random, 'randint') as mock_method:
            mock_method.side_effect = [6,6,1,1,1]
            country_A.attack(country_B, 3)
            self.assertEqual(country_A.troops, 28)
            self.assertEqual(country_B.troops, 10)


        with patch.object(random, 'randint') as mock_method:
            mock_method.side_effect = [1,1,6,6,6]
            country_A.attack(country_B,3)
            self.assertEqual(country_A.troops, 28)
            self.assertEqual(country_B.troops, 8)

    def test_get_player_set(self):
        country_A = self.board.countries['alaska']
        country_B = self.board.countries['northwest territory']
        players = [models.Player('Erty'),models.Player('Alex')]
        country_A.owner = players[0]
        country_B.owner = players[1]
        player_set = self.board.continents['north america'].get_player_set()
        self.assertEqual(len(player_set), 3)

    def test_cards(self):
        #this is a really dumb test, but it sort of works and I'm too lazy to make it better right now
        card1 = self.cards[0]
        card2 = self.cards[1]
        card3 = self.cards[2]
        card4 = self.cards[3]
        card5 = self.cards[4]
        set1=card1.is_set_with(card2, card3)
        set2=card1.is_set_with(card2, card4)
        set3=card1.is_set_with(card2, card5)
        set4=card1.is_set_with(card3, card4)
        set5=card1.is_set_with(card3, card5)
        set6=card1.is_set_with(card4, card5)
        set7=card2.is_set_with(card3, card4)
        set8=card2.is_set_with(card3, card5)
        set9=card2.is_set_with(card4, card5)
        set10=card3.is_set_with(card4, card5)
        
        self.assertEqual(set1 or set2 or set3 or set4 or set5 or set6 or set7 or set8 or set9 or set10, True)

    def test_continent_bonus(self):
        alex = models.Player('Alex')
        north_america = self.board.continents["north america"]
        for country in north_america.countries.values():
            alex.choose_country(country)
        self.assertEqual(north_america.get_player_set(), {alex})
        self.assertEqual(north_america.bonus, 5)
