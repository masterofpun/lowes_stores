import requests
import sqlite3

DB_FILE = 'data.sqlite'
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS data (no,name,address,phone,fax,state,zip,lat,lng)")

headers = {'User-Agent':'Just a script gathering a list of stores, will poll once a day after an initial dump; contact at: reddit.com/u/hypd09', 'Accept-Encoding': 'gzip', 'Content-Encoding': 'gzip'}
req = requests.Session()
detail_url = 'https://m.lowes.com/store/NC-Wilkesboro/{0}'
base_url = 'http://lowes.know-where.com/lowes/cgi/region?country=US&region={0}&design=default&lang=en&option=&mapid=US'
states = ['AL','MT','AK','NE','AZ','NV','AR','NH','CA','NJ','CO','NM','CT','NY','DE','NC','FL','ND','GA','OH','HI','OK','ID','OR','IL','PA','IN','RI','IA','SC','KS','SD','KY','TN','LA','TX','ME','UT','MD','VT','MA','VA','MI','WA','MN','WV','MS','WI','MO','WY']


c.execute('SELECT no FROM data ORDER BY no ASC')
done_stores = [done[0] for done in c.fetchall()]
print('done stores',done_stores)

for state in states:
    state_list = req.get(base_url.format(state), headers=headers).text
    state_list = state_list.split('store-locator-results-table',1)[1].split('<table',1)[0]
    for stores_data in state_list.split('<tr')[2:]:
        data = []
        store_number = stores_data.split("updateLocalStore('",1)[1].split("')",1)[0]
        if store_number in done_stores:
            continue
        data.append(store_number)
        data.append(stores_data.split('<h4>',1)[1].split('</h4>',1)[0])
        address = stores_data.split('class="address">',1)[1].split('</ul>',1)[0].strip()
        address = address.replace('<li>','').strip()
        address = ', '.join([a.strip() for a in address.split('</li>')][1:-2])
        data.append(address)
        data.append(stores_data.split('Phone:',1)[1].split('</li>',1)[0].strip())
        try:
            data.append(stores_data.split('FAX:',1)[1].split('</li>',1)[0].strip())
        except IndexError:
            data.append('')
        data.append(state)
        info = req.get(detail_url.format(store_number),headers=headers).text
        info = info.split('StoreDetails',1)[1].split('</script>',1)[0]
        data.append(info.split('ZIP:',1)[1].split(',',1)[0].replace("'",'').strip())
        data.append(info.split('lat:',1)[1].split(',',1)[0].strip())
        data.append(info.split('lng:',1)[1].split(',',1)[0].strip())
        print(data)
        c.execute('INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?)',data)
        conn.commit()
c.close()
import requests
import sqlite3

DB_FILE = 'data.sqlite'
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS data (no,name,address,phone,fax,state,zip,lat,lng)")

headers = {'User-Agent':'Just a script gathering a list of stores, will poll once a day after an initial dump; contact at: reddit.com/u/hypd09', 'Accept-Encoding': 'gzip', 'Content-Encoding': 'gzip'}
req = requests.Session()
detail_url = 'https://m.lowes.com/store/NC-Wilkesboro/{0}'
base_url = 'http://lowes.know-where.com/lowes/cgi/region?country=US&region={0}&design=default&lang=en&option=&mapid=US'
states = ['AL','MT','AK','NE','AZ','NV','AR','NH','CA','NJ','CO','NM','CT','NY','DE','NC','FL','ND','GA','OH','HI','OK','ID','OR','IL','PA','IN','RI','IA','SC','KS','SD','KY','TN','LA','TX','ME','UT','MD','VT','MA','VA','MI','WA','MN','WV','MS','WI','MO','WY']


c.execute('SELECT no FROM data ORDER BY no ASC')
done_stores = [done[0] for done in c.fetchall()]
print('done stores',done_stores)

for state in states:
    state_list = req.get(base_url.format(state), headers=headers).text
    state_list = state_list.split('store-locator-results-table',1)[1].split('<table',1)[0]
    for stores_data in state_list.split('<tr')[2:]:
        data = []
        store_number = stores_data.split("updateLocalStore('",1)[1].split("')",1)[0]
        if store_number in done_stores:
            continue
        data.append(store_number)
        data.append(stores_data.split('<h4>',1)[1].split('</h4>',1)[0])
        address = stores_data.split('class="address">',1)[1].split('</ul>',1)[0].strip()
        address = address.replace('<li>','').strip()
        address = ', '.join([a.strip() for a in address.split('</li>')][1:-2])
        data.append(address)
        data.append(stores_data.split('Phone:',1)[1].split('</li>',1)[0].strip())
        data.append(stores_data.split('FAX:',1)[1].split('</li>',1)[0].strip())
        data.append(state)
        info = req.get(detail_url.format(store_number),headers=headers).text
        info = info.split('StoreDetails',1)[1].split('</script>',1)[0]
        data.append(info.split('ZIP:',1)[1].split(',',1)[0].replace("'",'').strip())
        data.append(info.split('lat:',1)[1].split(',',1)[0].strip())
        data.append(info.split('lng:',1)[1].split(',',1)[0].strip())
        print(data)
        c.execute('INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?)',data)
        conn.commit()
c.close()

