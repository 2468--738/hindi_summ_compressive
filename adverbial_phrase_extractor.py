import os 
import json
import tqdm

complete_advp = []

for file in tqdm.tqdm(os.listdir('data/')):
    with open(f'data/{file}', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        
    for sentence in json_file.keys():
        words = json_file[sentence]['words']
        
        n = len(words)
        i = 0
        all_advp = []
        current_phrase = []
        for word_data in words:
            word = word_data['word']
            label = word_data['label']
            
            if label in ['RB', 'INTF', 'RP', 'QF', 'QCC', 'RBC']:
                current_phrase.append(word)
            
            elif label == 'JJ' and current_phrase and current_phrase[-1] in ['INTF', 'RB']:
                current_phrase.append(word)
            
            elif current_phrase:
                all_advp.append(' '.join(current_phrase))
                current_phrase = [] 

        json_file[sentence]['adverbial_phrases'] = all_advp
        if all_advp:
            complete_advp.extend(all_advp)
        
    with open(f'data/{file}', 'w', encoding='utf-8') as f:
        json.dump(json_file, f, indent=4, ensure_ascii=False)
             
with open('advp.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(complete_advp))      