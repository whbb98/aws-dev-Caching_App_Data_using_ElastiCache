import MySQLdb 
from pymemcache.client import base

memcached_client = base.Client(('<FMI_1>', 11211))
TTL_INT = 60 * 3; # 3 min cache

mydb = MySQLdb.connect(
  "<FMI_2>",
  "nodeapp",
  "coffee",
  "COFFEE"
)

def main():
    print('Updating a bean item')

    db_query = "UPDATE beans SET supplier_id=%s, type=%s, product_name=%s, price=%s, description=%s, quantity=%s WHERE id=%s"
    vals = (1, "Arabica Arabica","Best bean EVER","28.00","So delicious, smooth coffee.", 800, 1)

    mycursor = mydb.cursor()
    try:
        mycursor.execute(db_query, vals)
        print(mycursor.rowcount, "record(s) updated in RDS.")
        mydb.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        mycursor.close()
        return None
        exit()

    #closing the database cursor
    mycursor.close()

    print("FLUSH the CACHE as it is stale")
    #we could update just this item if we stored each item in the cache but this is fine for testing.
    try:
        memcached_call = memcached_client.delete('all_beans')
        print('Cache purged.')
    except:
        print('There was a problem flushing the cache' )

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
