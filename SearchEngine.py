# Steve Regala, CSCI 571 - Information Retrieval & Web Search Engines

import time
from bs4 import BeautifulSoup
from time import sleep
import requests
from random import randint
from html.parser import HTMLParser
import json

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
class SearchEngine:

   def __init__(self):
      pass

   @staticmethod
   def search(query, sleep=True):
      if sleep: # Prevents loading too many pages too soon
         time_to_sleep = randint(10, 100)
         print(str(time_to_sleep) + " seconds...")
         time.sleep(time_to_sleep)
      temp_url = '+'.join(query.split()) #for adding + between words for the query
      #url = 'SEARCHING_URL' + temp_url -----
      url = 'https://www.duckduckgo.com/html/?q=' + temp_url 
      soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
      new_results = SearchEngine.scrape_search_result(soup)
      return new_results

   @staticmethod
   def scrape_search_result(soup):
      #raw_results = soup.find_all("SEARCH SELECTOR") -----
      raw_results = soup.find_all("a", attrs = {"class" : "result__a"})
      results = []
      clean_results = []

      #implement a check to get only 10 results and also check that URLs must not be duplicated
      count = 0
      for result in raw_results:
         if count == 10:
            break

         raw_link = result.get('href')
         # check that there exists no duplicate URL
         link = str(raw_link)
         link = link.replace('http://', '')    # remove http://
         link = link.replace('https://','')    # remove https://
         link = link.replace('www.', '')       # remove www.
         link = link.rstrip('/')               # remove '/' at the end of url

         if link not in clean_results:
            clean_results.append(link)     # clean_results holds cleaned-up links
            results.append(raw_link)       # results holds RAW links
            count+=1

      return results


# main program
def run_program():
   query_list = []  # stores query from text file
   # Read in entries from text file amd store into array
   with open('Queries_Set.txt') as f:
      lines = f.readlines()
      for line in lines:
         query_list.append(line.rstrip(' \n'))

   # instantiate SearchEngine object
   SearchObject = SearchEngine()
   
   # stores query results (key: query number, value: array of search results), 
   # e.g. {Query1: [Result1,...,Result9, Result10],..., Query100:[Result1,...,Result10]}
   query_map = {}

   for count, query in enumerate(query_list, start=1):
      value = SearchObject.search(query)
      key = "Query" + str(count)
      query_map[key] = value
   
   outfile = open("results.json", "w")
   json.dump(query_map, outfile, indent=4)
   outfile.close

if __name__ == '__main__':
   run_program()
