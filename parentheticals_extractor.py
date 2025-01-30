import os 
import json
import tqdm

complete_parentheticals = []

for file in tqdm.tqdm(os.listdir('data/')):
    with open(f'data/{file}', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        
    for sentence in json_file.keys():
        words = json_file[sentence]['words']
        
        all_parentheticals = []
        parenthetical = []
        is_parenthetical = False
        for word in words:
            if word['word'] == '(':
                is_parenthetical = True
                
            if is_parenthetical:
                parenthetical.append(word['word'])
                
            if word['word'] == ')':
                all_parentheticals.append(' '.join(parenthetical))
                parenthetical = []
                is_parenthetical = False
                
        json_file[sentence] = {'words': words, 'parentheticals': all_parentheticals}
        if all_parentheticals:
            complete_parentheticals.extend(all_parentheticals)
        
    with open(f'data/{file}', 'w', encoding='utf-8') as f:
        json.dump(json_file, f, indent=4, ensure_ascii=False)
             
with open('parentheticals.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(complete_parentheticals))      