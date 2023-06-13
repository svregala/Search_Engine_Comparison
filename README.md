# Search_Engine_Comparison
 
For the full, detailed project description, please take a look at Project_Description.pdf. This project utilizes 2 main files: SearchEngine.py and CompareResults.py; in short, SearchEngine.py scrapes the top 10 results from the search engine DuckDuckGo for each query in Queries_Set.txt, and CompareResults.py compares the results from SearchEngine.py with the results from Google (in Google_Result.json) by determining percent overlap and Spearman Coefficient . To run each file, run the following commands, respectively:

python SearchEngine.py --> reads in "Queries_Set.txt" and writes out to "results.json"
python CompareResults.py --> reads in "Google_Results.json" (given) and "results.json" (from above), and writes out to "results_analysis.csv"

**Synopsis**: In this project, we compare the search results from Google with the results from DuckDuckGo specifically (or other search engines like Bing, Yahoo, and Ask, if edited). In particular, we:

(1) Scrape the results from DuckDuck Go (SearchEngine.py).
(2) Determine the Pecent Overlap and Spearman Coefficient, compared against given Google results (CompareResults.py).

In (1), SearchEngine.py takes all 100 queries in Queries_Set.txt, acquires the top 10 results for each query from DuckDuckGo (or any specified search engine), and cleans up each link and prevents any duplicate results, and writes to results.json.
In (2), CompareResults takes in the 10 search results from each query (in results.json) and compares them with the 10 results from each query acquired from Google search (in Google_Result.json). For the method of comparison, I utilized percent overlap (percentage of identical results within the 10 results for each query) and Spearman's rank correlation coefficient or Spearman's rho (measure of the statistical dependence between the rankings of two variables; it assesses how well the relationship between two variables can be described -- Spearman correlation between two variables will be high when observations have a similar rank, and low when observations have a dissimilar rank). The results are written to results_analysis.csv.