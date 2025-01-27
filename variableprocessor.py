NAME: str = 'Item'
ID: str = 'Debug Name'
INDIVIDUAL: str = 'Individual Pipe IDs'
GROUPS: str = 'Group Pipe IDs'

CRASH_ON_ERROR: bool = False
WARN_ON_ERROR: bool = True

def process_single(data: list[dict]) -> dict:
    out = {}
    
    for i in data:
        processed: dict = row_to_dict(i)
        if (processed != None):
            out[processed.get(NAME)] = processed
            
    return out

def row_to_dict(row: dict) -> dict:
    data: dict = row.get('properties')
    
    if (data == None):
        if (CRASH_ON_ERROR):
            raise ValueError("Row empty")
        elif (WARN_ON_ERROR):
            print("Row empty")
        return {}
    
    out: dict = {}
    
    for i in data:
        out[i] = process(data[i])
        
    return out
        
def process(data: dict) -> str|list[str]:
    if ('type' not in data.keys()):
        print("Found keys:" + str(data.keys()))
        if (CRASH_ON_ERROR):
            raise ValueError("Type not found")
        elif (WARN_ON_ERROR):
            print("Type not found")
        return None
    try:
        if (data['type'] == 'title'):
            return data['title'][0]['plain_text']
        if (data['type'] == 'rich_text'):
            out = data['rich_text'][0]['plain_text']
            if '\n' in out:
                out = [s for s in [i.strip() for i in out.split('\n')] if len(s) > 0]
            return out
        if (data['type'] == 'multi_select'):
            return [i['name'] for i in data['multi_select']]
        if (data['type'] == 'relation'):
            return [i['id'] for i in data['relation']]
        else:
            if (CRASH_ON_ERROR):
                raise ValueError(f"Unknown type: {data['type']}")
            elif (WARN_ON_ERROR):
                print(f"Unknown type: {data['type']}")
            return None
    except IndexError:
        if (CRASH_ON_ERROR):
            raise ValueError("Index error. Do not leave fields empty")
        elif (WARN_ON_ERROR):
            print("Index error. Do not leave fields empty")
        return None
    except ValueError as e:
        raise e
    except Exception as e:
        raise e
        

def process_relations(data: list[dict]) -> dict:
    out: dict = {}
    
    for i in data:
        processed: tuple[str, str] = row_to_relation(i)
        if (processed != None):
            out[processed[0]] = processed[1]
            
    return out
    
def row_to_relation(row: dict) -> tuple[str, str]:
    name: str = process(row.get('properties').get('Name'))
    id: str = row.get('id')
    
    return (id, name)

def reference_groups(data: dict, relations: dict) -> None:
    for i in data:
        reference_group_row(data[i], relations)

def reference_group_row(row: dict, relations: dict) -> None:
    new_groups: list[str] = []
    for i in row.get(GROUPS):
        new_groups.append(relations.get(i))
        
    row[GROUPS] = new_groups

def generate_individual(data: dict[str, list]) -> list[tuple[str, str]]:
    assert(ID in data.keys() and INDIVIDUAL in data.keys())
    assert(len(data[ID]) == len(data[INDIVIDUAL]))
    
    out: list[tuple[str, str]] = []
    
    for i in range(len(data[ID])):
        out.append((data[INDIVIDUAL][i], data[ID][i]))
    
    return out

def process_full(data: list[dict], relations: list[dict]) -> dict[str, dict[str, str|list[str]]]:
    db: dict[str, dict[str, str|list[str]]] = process_single(data)
    rel_db: dict = process_relations(relations)
    
    reference_groups(db, rel_db)
    
    return db

if __name__=="__main__":
    # Intended for testing purposes ONLY
    
    import json
    
    data: list[dict] = []
    
    with open('data.json', 'r') as f:
        data = json.load(f)
        
    db: str = process_single(data)
    
    
    relation_data = list[dict]
    
    with open('relations.json', 'r') as f:
        relation_data = json.load(f)
        
    rel_db: dict = process_relations(relation_data)
    
    reference_groups(db, rel_db)
    
    target: str = ""
    
    while (target != "exit"):
        target = input("Enter target: ")
        print(db.get(target))