import os
import json
import tqdm

complete_pp = []

for file in tqdm.tqdm(os.listdir('data/')):
    with open(f'data/{file}', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        
    for sentence in json_file.keys():
        words = json_file[sentence]['words']
        
        all_pp = []
        current_phrase = []
    
        for word_data in words:
            word, label = word_data['word'], word_data['label']

            if label in ['NN', 'NNP', 'NNC', 'NNPC', 'NNS']:
                current_phrase.append(word)
            elif label == 'PSP':
                if current_phrase:
                    current_phrase.append(word)
                    all_pp.append(" ".join(current_phrase))
                    current_phrase = []
            else:
                if current_phrase:
                    current_phrase = []

        if current_phrase:
            current_phrase = []

        json_file[sentence]['postpositional_phrases'] = all_pp
        complete_pp.extend(all_pp)
        
    with open(f'data/{file}', 'w', encoding='utf-8') as f:
        json.dump(json_file, f, indent=4, ensure_ascii=False)
             
with open('pp.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(complete_pp))