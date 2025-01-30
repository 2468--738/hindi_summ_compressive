import os 
import json
import tqdm

all_labels = {}

for file in tqdm.tqdm(os.listdir('data/')):
    with open(f'data/{file}', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        
    for sentence in json_file.keys():
        words = json_file[sentence]['words']
        
        for word in words:
            if word['label'] not in all_labels:
                all_labels[word['label']] = True
                
with open('all_labels.txt', 'w') as f:
    f.write('\n'.join(all_labels.keys()))
                    