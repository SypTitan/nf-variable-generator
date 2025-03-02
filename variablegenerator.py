from variableprocessor import ID, INDIVIDUAL, GROUPS

def generate_individuals(data: dict[str, dict[str, str|list[str]]], line_start: str = "  ", namespace: str = "global") -> str:
    out: str = ""
    
    for i in data:
        if (type(data[i][INDIVIDUAL]) == str):
            # Single individual ID
            out += line_start + f"{namespace}|{data[i][INDIVIDUAL]}: {data[i][ID]}" + '\n'
            
        elif (type(data[i][INDIVIDUAL]) == list):
            # Multiple individual IDs
            for j in data[i][INDIVIDUAL]:
                out += line_start + f"{namespace}|{j}: {data[i][ID]}" + '\n'
        else:
            raise ValueError(f"Unknown type: {type(data[i][INDIVIDUAL])}")
        
    return out

def generate_groups(data: dict[str, dict[str, str|list[str]]], line_start: str = "  ", namespace: str = "global") -> str:    
    out: str = ""
    
    groups: dict[str, list[str]] = group_data(data)
    
    for i in groups:
        out += line_start + f"{namespace}|{i}: {', '.join(groups[i])}" + '\n'
        
    return out

def group_data(data: dict[str, dict[str, str|list[str]]]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    
    for i in data:
        for j in data[i][GROUPS]:
            if (j not in out.keys()):
                out[j] = []
            out[j].append(data[i][ID])
    
    return out

def generate_output(data: dict[str, dict[str, str|list[str]]]) -> str:
    out: str = ""
    
    out += 'variables:\n'
    out += '  # Individual variables\n'
    out += generate_individuals(data)
    out += '\n  # Group variables\n'
    out += generate_groups(data)
    
    return out

def generate_output_file(data: dict[str, dict[str, str|list[str]]], file: str) -> None:
    with open(file, 'w') as f:
        f.write(generate_output(data))