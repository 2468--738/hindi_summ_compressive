import os 
import json
import tqdm

complete_adjp = []

for file in tqdm.tqdm(os.listdir('data/')):
    with open(f'data/{file}', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        
    for sentence in json_file.keys():
        words = json_file[sentence]['words']
        
        n = len(words)
        i = 0
        phrase = []
        all_adjp = []
    
        for i, entry in enumerate(words):
            word = entry["word"]
            label = entry["label"]
            
            if label in ["RB", "DEM", "JJ", "INTF"]:
                phrase.append(word)
            else:
                if phrase:
                    all_adjp.append(" ".join(phrase))
                    phrase = [] 

        json_file[sentence]['ajectival_phrases'] = all_adjp
        if all_adjp:
            complete_adjp.extend(all_adjp)
        
    with open(f'data/{file}', 'w', encoding='utf-8') as f:
        json.dump(json_file, f, indent=4, ensure_ascii=False)
             
with open('adjp.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(complete_adjp))      