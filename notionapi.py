import requests

# dotenv.load_dotenv()

# TOKEN: str = os.environ.get('TOKEN')
BASE_URL: str = 'https://api.notion.com/v1/'

# if (TOKEN is None):
#     raise ValueError("Token is not set")

BASE_HEADERS: dict = {
    'Authorization': 'Bearer ' + 'None',
    'Notion-Version': '2022-06-28',
}

def set_token(token: str) -> None:
    BASE_HEADERS['Authorization'] = 'Bearer ' + token

def get_page_raw(page_id: str) -> dict:
    url: str = BASE_URL + f'pages/{page_id}'
    response: requests.Response = requests.get(url, headers=BASE_HEADERS)
    return response.json()

def get_database_raw(database_id: str) -> dict:
    url: str = BASE_URL + f'databases/{database_id}'
    response: requests.Response = requests.get(url, headers=BASE_HEADERS)
    return response.json()

def query_database_raw(database_id: str, filter: dict = None) -> dict:
    url: str = BASE_URL + f'databases/{database_id}/query'
    response: requests.Response = requests.post(url, headers=BASE_HEADERS, json=filter)
    return response.json()

def get_databse(database_id: str) -> dict:
    response: dict = get_database_raw(database_id)
    if ('message' in response.keys()):
        raise ValueError(response['message'])
    
    # print(response.keys())
    # for i in response:
    #     print(f"{i}: {str(response[i])[:100]}")
    
    data: dict = response.get('properties')
    
    if (data == None):
        raise ValueError("Database not found")
    
    return data

def query_database(database_id: str, filter: dict = None) -> dict:
    response: dict = query_database_raw(database_id, filter)
    if ('message' in response.keys()):
        raise ValueError(response['message'])
    
    data: dict = response.get('results')
    
    if (data == None):
        raise ValueError("Database not found")
    
    if (response.get('has_more') == True):
        if (filter is None):
            filter = {}
        filter['start_cursor'] = response.get('next_cursor')
        data += query_database(database_id, filter)
    
    return data

if __name__=="__main__":
    # Intended for testing purposes ONLY
    
    import dotenv, os
    
    dotenv.load_dotenv()
    
    token: str = os.environ.get('TOKEN')
    
    if (token is None):
        raise ValueError("Token is not set")
    
    set_token(token)
    
    db_id: str = os.environ.get('DATABASE')
    if (db_id is None):
        raise ValueError("Database is not set")
    
    raw_db: dict = query_database(db_id, {'sorts': [{'property': 'Item', 'direction': 'ascending'}]})
    
    print(f"Found {len(raw_db)} entries")
    
    rel_id: str = os.environ.get('GROUPBASE')
    if (rel_id is None):
        raise ValueError("Groupbase is not set")
    
    rel_db: dict = query_database(rel_id)
    
    print(f"Found {len(rel_db)} groups")
    
    import variableprocessor as vp
    
    db = vp.process_full(raw_db, rel_db)
    
    # target: str = input("Enter target: ")
    
    # while (target != "exit"):
    #     print(db.get(target))
    #     target = input("Enter target: ")
    
    import variablegenerator as vg
    
    vg.generate_output_file(db, 'variables.yml')
    
    # print(db.keys())
    
    # print(db.get('results')[0])
    
    # for i in db:
    #     print(f"{i}: {str(db[i])[:100]}")
        
    # print(len(db))
    
    # with open('relations.json', 'w') as f:
    #     json.dump(db, f)
    
    # exit()
    
    # print(f"IDs: {len(db.get('Debug Name'))}")
    # print(f"Individuals: {len(db.get('Individual Pipe IDs'))}")
    
    # print(db.get('Individual Pipe IDs').keys())
    # print(db.get('Category').get('multi_select').get('options')[1])
    
    # for i in db:
    #     print(f"{i}: {str(db[i])[:150]}")
        # if (db[i].get('type') == 'multi_select'):
        #     print(f"{i}: {db[i].get('multi_select').get('options')[0]}")
        # elif (db[i].get('type') == 'title'):
        #     print(f"{i}: {db[i].get('title')}")
        # elif (db[i].get('type') == 'relation'):
        #     print(f"{i}: {db[i].get('relation')}")
        # elif (db[i].get('type') == 'rich_text'):
        #     print(f"{i}: {db[i].get('rich_text')}")
        # else:
        #     print(f"{i}: {db[i].get('type')}")