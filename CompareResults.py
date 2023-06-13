# Steve Regala, CSCI 571 - Information Retrieval & Web Search Engines

import json
import csv

class CompareResults:
   def __init__(self):
      pass

   # return number of overlapping results and percent overlap for a query
   @staticmethod
   def percent_overlap(google_res, duck_res):

      num_overlap = 0
      percent_overlap = 0.0

      overlap = {}   # holds all of google results (link, index)
      # holds indices that are equal to each other (google rank as key, duck rank as value), 
      # e.g. (1,1), (5,9), (6,2), (7,6)
      overlap_indices = {}

      # n runtime
      # create map to hold (link, index), called overlap
      for index, google in enumerate(google_res, start=1):
         # clean up links before comparing them with Search Engine Results
         link = str(google).replace('http://', '') # remove http://
         link = link.replace('https://','')        # remove https://
         link = link.replace('www.', '')           # remove www.
         link = link.rstrip('/')                   # remove '/' at the end of url

         overlap[link] = index

      # iterate through duck results and find the overlaps
      for index, duck in enumerate(duck_res, start=1):
         link_duck = str(duck).replace('http://', '')    # remove http://
         link_duck = link_duck.replace('https://','')    # remove https://
         link_duck = link_duck.replace('www.', '')       # remove www.
         link_duck = link_duck.rstrip('/')               # remove '/' at the end of url

         if link_duck in overlap:
            num_overlap += 1
            overlap_indices[overlap[link_duck]] = index

      percent_overlap = (num_overlap / len(google_res))*100
            
      return num_overlap, percent_overlap, overlap_indices

   @staticmethod
   def calc_rho(rank_indices, num_overlaps):
      # Notes: Value of Rho (Spearman Coefficient)
         # if no overlap, rho = 0
         # if n == 1 (i.e. only 1 result matches):
            # if rank in Duck == rank in Google --> rho = 1
            # if rank in Duck != rank in Google --> rho = 0

      if num_overlaps==0:
         return 0
      
      if num_overlaps==1:
         # O(1) to get first key
         first = next(iter(rank_indices))
         if first == rank_indices[first]:
            return 1
         return 0

      # if n > 1
      sum_dist_sqr = 0
      for key in rank_indices:
         sum_dist_sqr += (key-rank_indices[key])**2
      
      calc = (6*sum_dist_sqr)/(num_overlaps*(num_overlaps**2-1))
      final_rho = 1 - calc
      return final_rho


# main program
def run_program():
   with open('Google_Result.json') as json_google:
      google_data = json.load(json_google)
    
   with open('results.json') as json_duck:
      duck_data = json.load(json_duck)
   
   print("Type of google:", type(google_data))
   print("Type of duck:", type(duck_data))
   print("Length of google: ", len(google_data))
   print("Length of duck: ", len(duck_data))

   compare = CompareResults()

   with open('result_analysis.csv', mode='w') as csv_file:
      field_names = ['Queries', ' Number of Overlapping Results', ' Percent Overlap', ' Spearman Coefficient']

      # write titles of different columns for csv file
      output = csv.writer(csv_file)
      output.writerow(field_names)

      avg_num_over = 0.0
      avg_percent_over = 0.0
      avg_spearman = 0.0

      # iterate through each google query's value, which is an array of results
      # pass in json google results --> compare with duckGo's results
      for index, key in enumerate(google_data, start=1):
         duck_key = "Query" + str(index)
         num_over, percent_over, rank_matches = compare.percent_overlap(google_data[key], duck_data[duck_key])
         spearman = compare.calc_rho(rank_matches, num_over)
         print(num_over, percent_over, spearman)

         avg_num_over += num_over
         avg_percent_over += percent_over
         avg_spearman += spearman

         entry = ["Query " + str(index), " " + str(num_over), " " + str(percent_over), " " + str(spearman)]
         output.writerow(entry)
      
      avg_num_over = avg_num_over/100
      avg_percent_over = avg_percent_over/100
      avg_spearman = avg_spearman/100

      avg_total = ["Averages", " " + str(avg_num_over),  " " + str(avg_percent_over), " " + str(avg_spearman)]
      output.writerow(avg_total)
      
      
if __name__ == '__main__':
   run_program()
