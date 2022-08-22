from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd
import json

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
#print(tonight.prettify())

period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()
#print(period)
#print(short_desc)
#print(temp)

img = tonight.find("img")
desc = img['title']
#print(desc)
#Extracting all the information from the page
period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
#print(periods)

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
#print(short_descs)
#print(temps)
#print(descs)

#import pandas as pd
weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc": descs
})
#print(weather)
import re
temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
#print(temp_nums)
print(weather["temp_num"].mean())

is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
print(is_night)
print(weather["is_night"])

"""""
Web Scraping is an automatic way to retrieve unstructured data from a website and store them in a structured format.
Can you scrape from all the websites?
Scraping makes the website traffic spike and may cause the breakdown of the website server. 
Thus, not all websites allow people to scrape. How do you know which websites are allowed or not? You can look at the ‘robots.txt’ file of the website. You just simply put robots.txt after the URL that you want to 
scrape and you will see information on whether the website host allows you to scrape the website.



We can also search for items using CSS selectors. These selectors are how the CSS language allows developers to specify HTML tags to style. Here are some examples:

p a — finds all a tags inside of a p tag.
body p a — finds all a tags inside of a p tag inside of a body tag.
html body — finds all body tags inside of an html tag.
p.outer-text — finds all p tags with a class of outer-text.
p#first — finds all p tags with an id of first.
body p.outer-text — finds any p tags with a class of outer-text inside of a body tag.

^^^Examples

**BeautifulSoup objects support searching a page via CSS selectors using the select method. We can use CSS selectors to find all the p tags in our page that are inside of a div like this:
==>soup.select("div p")

**search for elements by id:
==>soup.find_all(id="first")

**look for any tag that has the class outer-text:
==>soup.find_all(class_="outer-text")


**we can use the find_all method to search for items by class or by id. In the below example, we’ll search for any p tag that has the class outer-text:
==>soup.find_all('p', class_='outer-text')

**Note that find_all returns a list, so we’ll have to loop through, or use list indexing, it to extract text:
==>soup.find_all('p')[0].get_text()


**if you instead only want to find the first instance of a tag, you can use the find method, which will return a single BeautifulSoup object:
==>soup.find('p')
"""