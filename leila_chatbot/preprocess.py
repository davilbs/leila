import json
import os
import sys
import re

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_text(data):
    items = []
    for item in data['items']:
        description = ""
        nutritional_info = ""
        for attribute in item['custom_attributes']:
            if attribute['attribute_code'] == 'description':
                description = attribute['value']
            if attribute['attribute_code'] == 'informacoes_nutricionais':
                nutritional_info = attribute['value']

        items.append({
            'name': item['name'],
            'price': item['price'],
            'description': description,
            'nutritional_info': nutritional_info
        })
    return items

def format_item(text):
    html_tags = re.compile(r'(<.*?>|\r\n)')
    inner_tags = re.compile(r'(?s:&lt;.*?&gt;)')
    remove_break = re.compile(r'(\n )+')
    remove_nbsp = re.compile(r'(&nbsp;)+')
    name = text['name']
    price = text['price']
    description = text['description'].replace('\"', '')
    description = re.sub(html_tags, "", description)
    description = re.sub(inner_tags, "\n", description)
    description = re.sub(' +', ' ', description).strip()
    description = re.sub(remove_break, '\n', description)
    
    nutritional_info = text['nutritional_info'].replace('\"', '')
    nutritional_info = re.sub(html_tags, '', nutritional_info)
    nutritional_info = re.sub(inner_tags, '', nutritional_info)
    nutritional_info = re.sub(' +', ' ', nutritional_info).strip()
    nutritional_info = re.sub(html_tags, '', nutritional_info)
    nutritional_info = re.sub(remove_nbsp, '\n', nutritional_info)
    return {
        'name': name,
        'price': price,
        'description': description,
        'nutritional_info': nutritional_info
    }

if __name__ == '__main__':
    data_path = os.getcwd() + "/data/" + sys.argv[1]
    output_path = os.getcwd() + "/data/" + sys.argv[2]

    data = load_json(data_path)
    items = extract_text(data)
    formatted_text = {"items": [format_item(item) for item in items]}

    with open(output_path, 'w') as file:
        json.dump(formatted_text, file, indent=4, ensure_ascii=False)