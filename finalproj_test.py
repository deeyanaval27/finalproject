import unittest
from finalproj import *
import sqlite3

class TestDatabase(unittest.TestCase):

# testing if data is properly fetched from Restaurants table
    def test_restaurants_table(self):
        conn = sqlite3.connect('yelp.db')
        cur = conn.cursor()
        sql = 'SELECT Name FROM Restaurants'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertTrue(('Upstate',), result_list)
        self.assertEqual(len(result_list), 142)

        sql = '''
            SELECT Name, Type, Address
            FROM Restaurants
            WHERE PriceRange="3"
            ORDER BY Name ASC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 21)
        self.assertEqual(len(result_list[0]), 3)
        self.assertTrue('TongKatsu', result_list)
        self.assertTrue('Japanese', result_list)
        self.assertTrue('215 E 4th St', result_list)

        sql = '''
        SELECT Name, Neighborhood
        FROM Restaurants
        GROUP BY Neighborhood
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertTrue("SoHo", result_list)

        sql = '''
        SELECT Name
        FROM Restaurants
        WHERE NeighborhoodId ="36"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 7)

        conn.close()

# testing if data is properly fetched from Restaurants table
    def test_nightlife_table(self):
        conn = sqlite3.connect('yelp.db')
        cur = conn.cursor()
        sql = 'SELECT Name FROM Nightlife'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertTrue('Shrine', result_list)
        self.assertEqual(len(result_list), 209)

        sql = '''
            SELECT Name, Type, Address
            FROM Nightlife
            WHERE Type="Lounges"
            ORDER BY Name ASC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 69)
        self.assertEqual(len(result_list[0]), 3)
        self.assertTrue('Keybar', result_list)
        self.assertTrue('Lounges', result_list)
        self.assertTrue('110 Wall St', result_list)

        sql = '''
        SELECT Name, Neighborhood
        FROM Restaurants
        GROUP BY Neighborhood
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertTrue("Chelsea", result_list)

        conn.close()

# testing interactive part
class TestInteractive(unittest.TestCase):
    def testGraph1(self):
        conn = sqlite3.connect('yelp.db')
        cur = conn.cursor()
        statement = 'SELECT Name, PriceRange FROM Restaurants'
        restaurant_data = cur.execute(statement).fetchall()
        self.assertEqual(len(restaurant_data), 142)
        conn.close()

    def testGraph2(self):
        conn = sqlite3.connect('yelp.db')
        cur = conn.cursor()
        statement = 'SELECT Name, PriceRange FROM Nightlife'
        nightlife_data = cur.execute(statement).fetchall()
        self.assertEqual(len(nightlife_data), 209)
        conn.close()

    def testGraph3(self):
        conn = sqlite3.connect('yelp.db')
        cur = conn.cursor()
        statement = '''SELECT Neighborhood, COUNT(*) FROM Restaurants
        GROUP BY Neighborhood
        ORDER BY Count(*)'''
        restaurant_data1 = cur.execute(statement).fetchall()
        #self.assertEqual(max(COUNT(*)), 13)
        #self.assertEqual(min(COUNT(*)), 1)
        self.assertEqual(len(restaurant_data1), 52)
        self.assertTrue('Flatiron', restaurant_data1)
        conn.close()

    def testGraph4(self):
        conn = sqlite3.connect('yelp.db')
        cur = conn.cursor()
        statement = '''SELECT Neighborhood, COUNT(*) FROM Nightlife
        GROUP BY Neighborhood
        ORDER BY Count(*)'''
        nightlife_data1 = cur.execute(statement).fetchall()
        #self.assertEqual(max(COUNT(*)), 11)
        #self.assertEqual(min(COUNT(*)), 1)
        self.assertEqual(len(nightlife_data1), 88)
        self.assertTrue('Woodside', nightlife_data1)
        conn.close()

# tests that proper data is being scraped and stored into dictionaries
# class TestDataProcessing(unittest.TestCase):
#     def testDict(self):
#         get_restaurant_data('NY')
#         self.assertTrue(restaurant_names)
#         self.assertTrue(restaurant_dict)
#         get_nightlife_data('NY')
#         self.assertTrue(nightlife_names)
#         self.assertEqual(nightlife_dict)



unittest.main()
