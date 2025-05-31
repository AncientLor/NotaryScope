from log_util import add_log
from pathlib import Path
from json import dump


#################################
#### Active Notaries to JSON ####
#################################

def convert_text_to_json(input_text: Path, output_json: Path)->None:
    
    with open(input_text, 'r', encoding='utf-8') as instream:
        lines: list[str] = instream.readlines()

    # Extract Header Fields from First Line
    headers: list[str] = lines[0].strip().split('\t')

    # Convert Following Lines to Dictionary
    entries: list[dict] = []
    
    for line in lines[1:]:    
        fields: list[str] = line.strip().split('\t')
        
        # Ensure Fields/Headers Align
        if len(fields) == len(headers):
            entry: dict = dict(zip(headers, fields))
            entries.append(entry)
        
        else:
            add_log(f"[WARNING] Skipping malformed line: {line}")

    # Apply Camel Case Format to Business Names
    for e in entries:
        camel_case_list: list = []
        business_name: list[str] = e['Business Name'].split(' ')
        
        if business_name != '': 
            for name in business_name:
                if name == "UPS":
                    camel_case_list.append(name)

                else:
                    camel_case_list.append(name.capitalize())
            
            camel_case_text: str = ' '.join(camel_case_list)
            e['Business Name'] = camel_case_text

    # Write to JSON File
    with open(output_json, 'w', encoding='utf-8') as outfile:
        dump(entries, outfile, indent=2)

    add_log(f"[OK] Conversion complete. {len(entries)} entries written to {output_json}")