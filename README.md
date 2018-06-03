# Wedding / Event table planner

## Dependencies
* python
* graphviz 
* pygraphviz
    * install via:
         > sudo apt install libgraphviz-dev python-pip
         > pip install pygraphviz

## csv format
> <person(s) A>, <number of persons>, <person perference 1>, <person perference 2>, ...
 <person(s) B>, <number of persons>, <person perference 1>, <person perference 2>, ...
 ...
 
### table setup
change the lines:
    num_tables = 3
    places_per_table = 5
in table_planner.py to match your needs.
 
 
# run
    python table_planner.py
The score represents the number of preferences that was met with a valid solution.

# limitations
* currently tables all have the same number of seats 
