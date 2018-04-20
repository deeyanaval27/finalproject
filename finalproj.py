import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import csv
import plotly.plotly as py
import plotly.graph_objs as go

DBNAME = 'yelp.db'
CACHE_FNAME = 'yelp_cache.json'
RESTAURANT_CSV = 'restaurants.csv'
NIGHTLIFE_CSV = 'nightlife.csv'

#implement caching on yelp API
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(base_url):
    return base_url

def make_request_using_cache(url):
    unique_ident = params_unique_combination(url)
    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        #print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

#implement scraping on Yelp Fusion
# class TopRestaurants:
#     def __init__(self,name,type_,neighborhood,address,state,price,hours):
#         self.name = name
#         self.type = type_
#         self.neighborhood = neighborhood
#         self.address = address
#         self.state = state
#         self.price = price
#         self.hours = hours

def get_restaurant_data(state_abbr):
    start = 0
    restaurant_state = []
    restaurant_names = []
    restaurant_addresses = []
    restaurant_prices = []
    restaurant_types = []
    restaurant_neighborhoods = []
    restaurant_hours = []
    restaurant_data = []
    while start < 130:
        base_url = 'https://www.yelp.com/search?find_loc='
        state_url = base_url + state_abbr + '&start=' + str(start) + '&cflt=restaurants'
        html = make_request_using_cache(state_url)
        page_soup = BeautifulSoup(html, 'html.parser')
        start += 10
        names = page_soup.find_all('a',class_='biz-name js-analytics-click')
        for n in names:
            name = n.text
            restaurant_names.append(name)
        restaurants = page_soup.find_all('li', class_='regular-search-result')
        for r in restaurants:
            state = state_abbr
            restaurant_state.append(state)
            try:
                address = r.address.text
                address = address.strip()
            except:
                address = 'Unknown'
            restaurant_addresses.append(address)
            restaurant_url = 'https://www.yelp.com' + r.a['href']
            restaurant_html = make_request_using_cache(restaurant_url)
            page_soup2 = BeautifulSoup(restaurant_html, 'html.parser')
            hours = page_soup2.find_all('dl', class_='short-def-list')
            for s in hours:
                try:
                    hours_today = s.strong.text
                    hours_today = hours_today.strip()
                except:
                    hours_today = "Unknown"
                restaurant_hours.append(hours_today)
        price_range = page_soup.find_all('span', class_="business-attribute price-range")
        for p in price_range:
            try:
                price = p.text
                price = len(price)
            except:
                price = 'Unknown'
            restaurant_prices.append(price)
        category = page_soup.find_all('span', class_="category-str-list")
        for c in category:
            try:
                restaurant_category = c.a.text
            except:
                restaurant_category = 'Unknown'
            restaurant_types.append(restaurant_category)
        places = page_soup.find_all('div', class_="secondary-attributes")
        for n in places:
            try:
                neighborhood = n.span.text
                neighborhood = neighborhood.strip()
                if neighborhood == "Phone Number" or neighborhood == None:
                    neighborhood = 'Unknown'
                    continue
            except:
                neighborhood = 'Unknown'
            restaurant_neighborhoods.append(neighborhood)
    restaurant_dict = []
    restaurant_dict = list(zip(restaurant_names, restaurant_types, restaurant_neighborhoods, restaurant_addresses, restaurant_state, restaurant_prices, restaurant_hours))
    #writes restaurant data into csv file
    csvread = open(RESTAURANT_CSV, "w")
    writer = csv.writer(csvread)
    writer.writerows(restaurant_dict)
    return restaurant_names

def get_nightlife_data(state_abbr):
    start = 0
    nightlife_state = []
    nightlife_names = []
    nightlife_addresses = []
    nightlife_prices = []
    nightlife_types = []
    nightlife_neighborhoods = []
    nightlife_hours = []
    nightlife_data = []
    while start < 150:
        base_url2 = 'https://www.yelp.com/search?find_loc='
        state_url2 = base_url2 + state_abbr + '&start=' + str(start) + '&cflt=nightlife'
        html2 = make_request_using_cache(state_url2)
        page_soup3 = BeautifulSoup(html2, 'html.parser')
        start += 10
        names = page_soup3.find_all('a',class_='biz-name js-analytics-click')
        for n in names:
            name = n.text
            nightlife_names.append(name)
        nightclubs = page_soup3.find_all('li', class_='regular-search-result')
        for n in nightclubs:
            state = state_abbr
            nightlife_state.append(state)
            try:
                address = n.address.text
                address = address.strip()
            except:
                address = 'Unknown'
            nightlife_addresses.append(address)
            nightlife_url = 'https://www.yelp.com' + n.a['href']
            nightlife_html = make_request_using_cache(nightlife_url)
            page_soup4 = BeautifulSoup(nightlife_html, 'html.parser')
        price_range = page_soup3.find_all('span', class_="business-attribute price-range")
        for p in price_range:
            try:
                price = p.text
                price = len(price)
            except:
                price = 'Unknown'
            nightlife_prices.append(price)
        category = page_soup3.find_all('span', class_="category-str-list")
        for c in category:
            try:
                nightlife_category = c.a.text
            except:
                nightlife_category = 'Unknown'
            nightlife_types.append(nightlife_category)
        places = page_soup3.find_all('div', class_="secondary-attributes")
        for n in places:
            try:
                neighborhood = n.span.text
                neighborhood = neighborhood.strip()
                if neighborhood == "Phone Number" or neighborhood == None:
                    neighborhood = 'Unknown'
                    continue
            except:
                neighborhood = 'Unknown'
            nightlife_neighborhoods.append(neighborhood)
    nightlife_dict = []
    nightlife_dict = list(zip(nightlife_names, nightlife_types, nightlife_neighborhoods, nightlife_addresses, nightlife_state, nightlife_prices))
    #writes nightlife data into csv file
    csvread = open(NIGHTLIFE_CSV, "w")
    writer = csv.writer(csvread)
    writer.writerows(nightlife_dict)
    return nightlife_names

#read data from CSV files into a database
def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    drop_bars = 'DROP TABLE IF EXISTS "Restaurants"'
    cur.execute(drop_bars)
    conn.commit()
    drop_countries = 'DROP TABLE IF EXISTS "Nightlife"'
    cur.execute(drop_countries)
    conn.commit()

    #creates table for Restaurants
    create_restaurants = ''' CREATE TABLE IF NOT EXISTS 'Restaurants' (
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Name' TEXT NOT NULL,
    'Type' TEXT NOT NULL,
    'NeighborhoodId' INT,
    'Neighborhood' TEXT NOT NULL,
    'Address' TEXT NOT NULL,
    'State' TEXT NOT NULL,
    'PriceRange' TEXT NOT NULL,
    'HoursToday' TEXT NOT NULL
    )
    '''
    cur.execute(create_restaurants)
    conn.commit()

    #inputs restaurant data into database
    f = open(RESTAURANT_CSV, 'r')
    reader = csv.reader(f)
    for data in reader:
        query = '''
        INSERT INTO 'Restaurants'(Id, Name, Type, NeighborhoodId, Neighborhood, Address, State, PriceRange, HoursToday) VALUES (?,?,?,?,?,?,?,?,?)
        '''
        restaurant_data = (None, data[0], data[1], None, data[2], data[3], data[4], data[5], data[6])
        cur.execute(query, restaurant_data)
        conn.commit()
    f.close()


    #creates table for Nightlife
    create_nightlife = ''' CREATE TABLE IF NOT EXISTS 'Nightlife' (
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Name' TEXT NOT NULL,
    'Type' TEXT NOT NULL,
    'NeighborhoodId' INT,
    'Neighborhood' TEXT NOT NULL,
    'Address' TEXT NOT NULL,
    'State' TEXT NOT NULL,
    'PriceRange' TEXT NOT NULL
    )
    '''
    cur.execute(create_nightlife)
    conn.commit()

    #inputs night life data into database
    f = open(NIGHTLIFE_CSV, 'r')
    reader = csv.reader(f)
    for data in reader:
        query = '''
        INSERT INTO 'Nightlife'(Id, Name, Type, NeighborhoodId, Neighborhood, Address, State, PriceRange) VALUES (?,?,?,?,?,?,?,?)
        '''
        nightlife_data = (None, data[0], data[1], None, data[2], data[3], data[4], data[5])
        cur.execute(query, nightlife_data)
        conn.commit()
    f.close()
    return

def update_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    update1 = '''
    UPDATE Restaurants
    SET NeighborhoodId = (
        SELECT Id
        FROM Nightlife
        WHERE Restaurants.Neighborhood = Nightlife.Neighborhood
    )
    '''
    cur.execute(update1)
    conn.commit()
    update2 = '''
    UPDATE Nightlife
    SET NeighborhoodId = (
        SELECT Id
        FROM Restaurants
        WHERE Restaurants.Neighborhood = Nightlife.Neighborhood
    )
    '''
    cur.execute(update2)
    conn.commit()
    conn.close()
    return

def interactive_prompt():
    conn = conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    state_abbr_dict = {
            'ak': 'Alaska',
            'al': 'Alabama',
            'ar': 'Arkansas',
            'as': 'American Samoa',
            'az': 'Arizona',
            'ca': 'California',
            'co': 'Colorado',
            'ct': 'Connecticut',
            'dc': 'District of Columbia',
            'de': 'Delaware',
            'fl': 'Florida',
            'ga': 'Georgia',
            'gu': 'Guam',
            'hi': 'Hawaii',
            'ia': 'Iowa',
            'id': 'Idaho',
            'il': 'Illinois',
            'in': 'Indiana',
            'ks': 'Kansas',
            'ky': 'Kentucky',
            'la': 'Louisiana',
            'ma': 'Massachusetts',
            'md': 'Maryland',
            'me': 'Maine',
            'mi': 'Michigan',
            'mn': 'Minnesota',
            'mo': 'Missouri',
            'mp': 'Northern Mariana Islands',
            'ms': 'Mississippi',
            'mt': 'Montana',
            'na': 'National',
            'nc': 'North Carolina',
            'nd': 'North Dakota',
            'ne': 'Nebraska',
            'nh': 'New Hampshire',
            'nj': 'New Jersey',
            'nm': 'New Mexico',
            'nv': 'Nevada',
            'ny': 'New York',
            'oh': 'Ohio',
            'ok': 'Oklahoma',
            'or': 'Oregon',
            'pa': 'Pennsylvania',
            'pr': 'Puerto Rico',
            'ri': 'Rhode Island',
            'sc': 'South Carolina',
            'sd': 'South Dakota',
            'tn': 'Tennessee',
            'tx': 'Texas',
            'ut': 'Utah',
            'va': 'Virginia',
            'vi': 'Virgin Islands',
            'vt': 'Vermont',
            'wa': 'Washington',
            'wi': 'Wisconsin',
            'wv': 'West Virginia',
            'wy': 'Wyoming'
    }
    # print("Best restaurants in " + user_input.upper())
    #     count = 1
    #     for x in rows[:20]:
    #         print(str(count) + " " + x[0])
    #         count += 1
    user_input = ''
    while user_input != 'exit':
        user_input = input('''Pick a graph you would like to see:
        1) Price Ranges of the Top Restaurants in New York
        2) Price Ranges of the Top Nightlife in New York
        3) Distribution of Restaurants Grouped By Neighborhood in New York
        4) Distribution of Night Clubs Grouped By Neighborhood in New York
        ''')
        if user_input == "1":
            user_input = input('Pick a color for your graph(red/green/blue): ')
            if "red" in user_input:
                user_color = "rgb(255,0,0)"
            elif "green" in user_input:
                user_color = "rgb(0,255,0)"
            elif "blue" in user_input:
                user_color = "rgb(0,0,255)"
            else:
                user_color = "rgb(255,255,0)"
            statement = 'SELECT Name, PriceRange FROM Restaurants'
            restaurant_data = cur.execute(statement).fetchall()
            trace1 = go.Bar(
            x = [z[0] for z in restaurant_data],
            y = [z[1] for z in restaurant_data],
            marker=dict(
                color=user_color,
                line=dict(color='rgb(0,0,0)', width=2
                    )
                ),
            opacity=1
            )
            data = [trace1]
            layout = go.Layout(
            title = 'Top Restaurants vs Price Range in New York',
            xaxis=dict(title='Restaurants in New York'),
            yaxis=dict(title='Price Range (1-cheapest, 4-most expensive)')
            )
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='text-hover-bar')
        elif user_input == "2":
            user_input = input('Pick a color for your graph(red/green/blue): ')
            if "red" in user_input:
                user_color = "rgb(255,0,0)"
            elif "green" in user_input:
                user_color = "rgb(0,255,0)"
            elif "blue" in user_input:
                user_color = "rgb(0,0,255)"
            else:
                user_color = "rgb(255,255,0)"
            statement = 'SELECT Name, PriceRange FROM Nightlife'
            nightlife_data = cur.execute(statement).fetchall()
            trace2 = go.Bar(
            x = [z[0] for z in nightlife_data],
            y = [z[1] for z in nightlife_data],
            marker=dict(
                color=user_color,
                line=dict(color='rgb(0,0,0)', width=2
                    )
                ),
            opacity=1
            )
            data = [trace2]
            layout = go.Layout(
            title = 'Top Nightlife vs Price Range in New York',
            xaxis=dict(title='Night Clubs in New York'),
            yaxis=dict(title='Price Range (1-cheapest, 4-most expensive)')
            )
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='text-hover-bar')
        elif user_input == "3":
            statement = '''SELECT Neighborhood, COUNT(*) FROM Restaurants
            GROUP BY Neighborhood
            ORDER BY Count(*)'''
            restaurant_data1 = cur.execute(statement).fetchall()
            labels = [z[0] for z in restaurant_data1]
            values = [z[1] for z in restaurant_data1]
            colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']

            trace3 = go.Pie(labels=labels, values=values,
                hoverinfo='label+percent', textinfo='value',
                textfont=dict(size=20),
                marker=dict(colors=colors,
                        line=dict(color='#000000', width=2)))
            data = [trace3]
            layout = go.Layout(
            title = 'Distribution of Top Restaurants Grouped By Neighborhood in New York',
            )
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='text-hover-bar')
        elif user_input == "4":
            statement = '''SELECT Neighborhood, COUNT(*) FROM Nightlife
            GROUP BY Neighborhood
            ORDER BY Count(*)'''
            nightlife_data1 = cur.execute(statement).fetchall()
            labels = [z[0] for z in nightlife_data1]
            values = [z[1] for z in nightlife_data1]
            colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']

            trace4 = go.Pie(labels=labels, values=values,
                hoverinfo='label+percent', textinfo='value',
                textfont=dict(size=20),
                marker=dict(colors=colors,
                        line=dict(color='#000000', width=2)))
            data = [trace4]
            layout = go.Layout(
            title = 'Distribution of Top Nightlife Grouped By Neighborhood in New York',
            )
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='text-hover-bar')
        elif user_input == "5":
            None
        else:
            print("Invalid input. Try Again.")
    print('Goodbye!')

#get_restaurant_data('NY')
#get_nightlife_data('NY')
#init_db()
#update_db()
#interactive_prompt()
