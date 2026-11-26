# Print the contents of the entire table
query_1= f"""
SELECT * 
FROM Largest_banks;
"""
# Print the average market capitalization of all the banks in Billion GBP.
query_2 = f"""
SELECT 
AVG(MC_GBP_Billion) 
FROM Largest_banks;
"""

# Print only the names of the top 5 banks
query_3 = f"""
SELECT Name 
from Largest_banks 
LIMIT 5;
"""




queries_list = [query_1, query_2, query_3]