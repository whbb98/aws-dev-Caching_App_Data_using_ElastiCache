import MySQLdb 
from pymemcache.client import base
import json
import datetime;
print("current time:-", datetime.datetime.now())

memcached_client = base.Client(('<FMI_1>', 11211))
TTL_INT = 60 * 3; # Time to Live - 3 minutes cache

mydb = MySQLdb.connect(
  "<FMI_2>",
  "nodeapp",
  "coffee",
  "COFFEE"
)

def main():
    print('Finding all items')
    data = memcached_client.get('all_beans')
    
    if data is None:
        print('Data not found in cache. Retrieving data from the database:')

        db_query = "SELECT * FROM beans"
        mycursor = mydb.cursor()
        mycursor.execute(db_query)

		#getting column names from the cursor metadata
        num_fields = len(mycursor.description)
        field_names = [i[0] for i in mycursor.description]
		#fetching results from the database
        myresults = mycursor.fetchall()
		#combining column names with the data
        output_json = []
        for row in myresults:
            output_json.append(dict(zip(field_names,row)))
        
        output_json = json.dumps(output_json, indent = 2)
		#printing the returned records
        print(output_json)

		#adding data to the cache
        print('Setting result in cache')
        memcached_call = memcached_client.set('all_beans', output_json, TTL_INT)
        print(memcached_call)
        
		#closing the database cursor
        mycursor.close()
        
    else:
        print('Data returned from cache:')
        print(data.decode('utf-8'))
    
    print("current time:-", datetime.datetime.now())


if __name__ == "__main__":
    main()
"""
Copyright @2021 [Amazon Web Services] [AWS]
    
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
