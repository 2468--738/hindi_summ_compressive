import pandas
import os
import json
import tqdm
i = 1

for dir in os.listdir('utf/news_articles_and_heritage'):
    for file in tqdm.tqdm(os.listdir(f'utf/news_articles_and_heritage/{dir}')):
        try:
            df = pandas.read_csv(f'utf/news_articles_and_heritage/{dir}/{file}', delimiter='\t', encoding='utf-8',names=list(range(10)))
            
            sentences = {}
            labels = []
            sentence = []
            df = df.dropna()
            for index, row in df.iterrows():
                if row[0] == 1 and index != 0:
                    sentences[' '.join(sentence)] = labels
                    sentence = []
                    labels = []
                labels.append({"word": str(row[1]), "label": row[4]})
                sentence.append(str(row[1]))
                
            sentences[' '.join(sentence)] = labels
            
            with open(f'data/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(sentences, f, indent=4, ensure_ascii=False)
            i += 1
        except Exception as e:
            print(f'utf/news_articles_and_heritage/{dir}/{file}')
            print(e)