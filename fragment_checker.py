import os 
import json
import tqdm

all_fragments = []

for file in tqdm.tqdm(os.listdir('data/')):
    with open(f'data/{file}', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        
    for sentence in json_file.keys():
        words = json_file[sentence]['words']
        
        has_noun = False
        has_verb = False
        
        for word in words:
            if word['label'] in ['PRP', 'NNP', 'NN', 'NNPC', 'NNC', 'DEM', 'PRPC']:
                has_noun = True
                
            if word['label'] in ['VM', 'VAUX', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                has_verb = True        
                
        json_file[sentence]['fragment'] = str(not (has_noun and has_verb))
        if not (has_noun and has_verb):
            all_fragments.append(sentence)
        
    with open(f'data/{file}', 'w', encoding='utf-8') as f:
        json.dump(json_file, f, indent=4, ensure_ascii=False)
                    
with open('fragments.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_fragments))