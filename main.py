import notionapi as na
import variablegenerator as vg
import variableprocessor as vp

import argparse
import dotenv
import os

def main() -> None:
    parser = argparse.ArgumentParser(prog='vargen', description='Generate variables from Notion database')

    parser.add_argument('-d', '--database', type=str, help='Database ID')
    parser.add_argument('-g', '--groupbase', type=str, help='Group database ID')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    parser.add_argument('-t', '--token', type=str, help='Notion API token')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    dotenv.load_dotenv()
    
    output: str
    if (args.output is None):
        output = 'variables.yml'
    else:
        output = args.output
    
    token: str
    if (args.token is None):
        token = os.environ.get('TOKEN')
    else:
        token = args.token
        
    if (token == None):
        exit("Token is not set. Either use the -t flag or set the TOKEN environment variable")
    
    na.set_token(token)
    
    db_id: str
    if (args.database is None):
        db_id = os.environ.get('DATABASE')
    else:
        db_id = args.database
        
    if (db_id == None):
        exit("Database is not set. Either use the -d flag or set the DATABASE environment variable")
        
    rel_id: str
    if (args.groupbase is None):
        rel_id = os.environ.get('GROUPBASE')
    else:
        rel_id = args.groupbase
        
    if (rel_id == None):
        exit("Groupbase is not set. Either use the -g flag or set the GROUPBASE environment variable")
        
    verbose: bool = args.verbose
    
    if (verbose):
        print("Querying database...")
    
    raw_db: dict = na.query_database(db_id, {'sorts': [{'property': 'Item', 'direction': 'ascending'}]})
    
    if (verbose):
        print(f"Found {len(raw_db)} entries")
        print("Querying groups database...")
    
    rel_db: dict = na.query_database(rel_id)
    
    if (verbose):
        print(f"Found {len(rel_db)} groups")
        print("Processing data...")
        
    db: dict = vp.process_full(raw_db, rel_db)
    
    if (verbose):
        print("Generating output...")
        
    vg.generate_output_file(db, output)
        
    print(f"Wrote {len(db)} variables and {len(rel_db)} groups to {output}")
    
if __name__=="__main__":
    main()