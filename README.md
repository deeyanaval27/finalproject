Deeya Naval Final Project
SI 206

Data Source Info:
For my final project I chose to use Yelp as my data source. I accessed data on
Yelp by my implementation of scraping and crawling, allowing my program to
attain data regarding the top restaurants and nightlife in any state of choice.
I used caching and CSV files to store this data.

Functions:
My functions get_restaurant_data and get_nightlife_data are where scraping/crawling
is implemented, as well as caching and writing data into CSV files. I created
separate lists for every type of data collected, such as name, type, address,
price range, hours, etc for both restaurants and nightlife, which I then
combined into dictionaries zipping all of this data together for each
restaurant/nightclub. These dictionaries are called restaurant_dict and
nightlife_dict, which I wrote into rows in separate CSV files. I created a
restaurant table and a nightlife table in my database 'yelp.db' in the function
init_db, and I updated the tables to have my foreign key relation in my function
update_db.

User guide:
1) get_restaurant_data(<your state here>)
   get_nightlife_data(<your state here>)
   Specify the state that you would like to attain the top restaurant/nightlife data for
2) run init_db and update_db
   This will create restaurant and nightlife tables based on your state of choice
3) run interactive_prompt
   This will allow you to visualize the data in the database :)
   There are 4 presentation options, each portraying different groups of data:
   1) Price Ranges of the Top Restaurants in New York (bar graph, color choice)
   2) Price Ranges of the Top Nightlife in New York (bar graph, color choice)
   3) Distribution of Restaurants Grouped By Neighborhood in New York (pie chart)
   4) Distribution of Night Clubs Grouped By Neighborhood in New York (pie chart)
