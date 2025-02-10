import pandas
from tqdm import tqdm
import stanza
from openai import OpenAI
API_KEY = ''

openai_api_key = API_KEY
openai_api_base = "server url"

model_name = "mistralai/mixtral-8x22B-instruct-v0.1"
stopsequence = ["?", ".", "<EOD>", "[/User]"]

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    default_headers={"RITS_API_KEY": openai_api_key},
)

def rits_request(queries):
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": queries}],
        max_tokens=4000,
        stop=stopsequence,
        temperature=0.75,
        top_p=0.95,
    )

    result = completion.choices[0].message.content.strip()

    return result

# logics for the various phrases

def remove_adjectival_phrases(text: list):
    def remove_from_sent(sentence: list):
        indices_to_be_removed = []
        phrase = []
        
        for i, entry in enumerate(sentence):
            word = entry["word"]
            label = entry["label"]
            
            if label in ["RB", "DEM", "JJ", "INTF"]:
                phrase.append(i)
            else:
                if phrase:
                    indices_to_be_removed.extend(phrase)
                    phrase = [] 
                    
        new_sent = []
        for i in range(len(sentence)):
            if indices_to_be_removed and i == indices_to_be_removed[0]:
                del indices_to_be_removed[0]
            else:
                new_sent.append(sentence[i])
        return new_sent
                
    return [remove_from_sent(sentence) for sentence in text]


def remove_adveribial_phrases(text):
    def remove_from_sent(sentence: list):
        indices_to_be_removed = []
        phrase = []
        
        for i, entry in enumerate(sentence):
            word = entry["word"]
            label = entry["label"]
            
            if label in ['RB', 'INTF', 'RP', 'QF', 'QCC', 'RBC']:
                phrase.append(i)
            
            elif label == 'JJ' and phrase and sentence[phrase[-1]]['label'] in ['INTF', 'RB']:
                phrase.append(i)
            
            elif phrase:
                indices_to_be_removed.extend(phrase)
                phrase = [] 
                  
        new_sent = []
        for i in range(len(sentence)):
            if indices_to_be_removed and i == indices_to_be_removed[0]:
                del indices_to_be_removed[0]
            else:
                new_sent.append(sentence[i])
        return new_sent
                
    return [remove_from_sent(sentence) for sentence in text]


def remove_fragments(text):
    def is_not_fragment(sentence):
        has_noun = False
        has_verb = False
        
        for word in sentence:
            if word['label'] in ['PRP', 'NNP', 'NN', 'NNPC', 'NNC', 'DEM', 'PRPC']:
                has_noun = True
                
            if word['label'] in ['VM', 'VAUX', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                has_verb = True
                
        return has_noun and has_verb
    
    return [sentence for sentence in text if is_not_fragment(sentence)]   


def remove_parentheticals(text: list):
    def remove_from_sent(sentence: list):
        is_parenthetical = False
        
        for i, entry in enumerate(sentence):
            word = entry['word']
            if word == '(':
                is_parenthetical = True
                
            if word == ')':
                is_parenthetical = False
                sentence[i] = "deleted"
                
            if is_parenthetical:
                sentence[i] = "deleted"
        print(sentence)
        return [word for word in sentence if word != "deleted"]
        
    return [remove_from_sent(sentence) for sentence in text]


def remove_prepositional_phrases(text):
    def remove_from_sent(sentence: list):
        indices_to_be_removed = []
        phrase = []
        
        for i, entry in enumerate(sentence):
            word = entry["word"]
            label = entry["label"]
            
            if label in ['NN', 'NNP', 'NNC', 'NNPC', 'NNS']:
                phrase.append(i)
            elif label == 'PSP':
                if phrase:
                    phrase.append(i)
                    indices_to_be_removed.extend(phrase)
                    phrase = []
            else:
                if phrase:
                    phrase = []
                    
        new_sent = []
        for i in range(len(sentence)):
            if indices_to_be_removed and i == indices_to_be_removed[0]:
                del indices_to_be_removed[0]
            else:
                new_sent.append(sentence[i])
                
        return new_sent
                
    return [remove_from_sent(sentence) for sentence in text]


def delete_required_parts(text: list):
    new_text = remove_adveribial_phrases(text)
    new_text = remove_adjectival_phrases(new_text)
    new_text = remove_fragments(new_text)
    new_text = remove_parentheticals(new_text)
    new_text = remove_prepositional_phrases(new_text)
    return new_text


def get_text_output(text: list):
    final_text = []
    for sentence in text:
        final_text.append(' '.join([word['word'] for word in sentence]))
    return ' '.join(final_text)

stanza.download('hi')
nlp = stanza.Pipeline('hi')

def get_pos_tags(text, pipeline):
    text_tagged = []
    
    doc = pipeline(text)
    for sentence in doc.sentences:
        sent = []
        for word in sentence.words:
            sent.append({"word": word.text, "label": word.xpos})
        text_tagged.append(sent) 
        
    return text_tagged   
    
# Example output
hindi_text = "अफ्रीका का वन्यजीवन दुनिया भर में अपनी विविधता और अनोखेपन के लिए प्रसिद्ध है। यहाँ के विस्तृत सवाना, घने जंगल और विशाल रेगिस्तान असंख्य प्रजातियों का घर हैं। अफ्रीका में शेर, चीता, तेंदुआ, हाथी, गैंडा और भैंस जैसे बड़े जानवरों से लेकर जिराफ, ज़ेब्रा और हिप्पोपोटामस तक कई अद्भुत प्राणी पाए जाते हैं। इसके अलावा, यहाँ पक्षियों की भी हजारों प्रजातियाँ देखने को मिलती हैं। अफ्रीका के राष्ट्रीय उद्यान और संरक्षित क्षेत्र, जैसे कि मसाई मारा, क्रूगर नेशनल पार्क और सेरेनगेटी, वन्यजीवन संरक्षण के महत्वपूर्ण केंद्र हैं। हालाँकि, शिकार और वनों की कटाई के कारण कई प्रजातियाँ खतरे में हैं। इनके संरक्षण के लिए अनेक प्रयास किए जा रहे हैं, ताकि भविष्य की पीढ़ियाँ भी इस अद्भुत वन्यजीवन का आनंद ले सकें।"
tagged_hindi_text = get_pos_tags(hindi_text, pipeline=nlp)
for sentence in tagged_hindi_text:
    print(sentence)
    
summary_prompt = "Generate a summary of the following piece of text in Hindi Language in %d words. Do not use any words fron any other language. Be concise and informative. Do not generate any text other than the summary. The text starts from below:\n%s"
compression_prompt = "I want to compress the below Hindi text by removing parts that are not required to get the complete meaning of the text. Please delete the words and phrases that can be deleted without affecting the meaning of the text. Do not generate words other than the compressed summary. The summary starts from below:\n%s"
add_more_words_prompt = "I have a piece of Hindi text below:\n%s\nCould you please add %d more words to the following summary so that it becomes more informative and complete? Do not use any words other than Hindi language. Generate only the summary, and no other words. The summary starts from below:\n%s"
system_role = "You are an expert Hindi linguist."


def generate_summary_pipeline(text, summary_prompt, compression_prompt, add_more_words_prompt, compression_factor):
    words_in_text = len(text.split())
    words_in_final_summary = int(words_in_text * compression_factor)
    global system_role
    
    client = OpenAI(api_key=API_KEY)
    
    # generate summary
    messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": summary_prompt % (words_in_final_summary, text)},
            ]
    first_summary = rits_request(messages)
    
    # compress the summary
    messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": compression_prompt % first_summary},
            ]
    first_summary = rits_request(messages)
    
    print("Loop 0:", first_summary)

    current_summary_words = len(first_summary.split())
    new_summary = first_summary
    
    loops = 0
    try:
        while abs(words_in_final_summary - current_summary_words) > 20 and loops < 10:
            print("Required words:", words_in_final_summary)
            print("Current words:", current_summary_words)
            
            
            # add words to compressed summary
            messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": add_more_words_prompt % (text, words_in_final_summary - current_summary_words, new_summary)},
                ]
            new_summary = rits_request(messages)
            
            # compress the summary
            messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": compression_prompt % new_summary},
                ]
            new_summary = rits_request(messages)
            
            current_summary_words = len(new_summary.split())
            loops += 1
            
            print(f"Loop {loops}:", new_summary)
    except:
        pass
        
    return (loops, new_summary)


rows_provided = 50

data = pandas.read_excel(r'./new_generated.xlsx', nrows=rows_provided)
data.head()

try:
    summaries = data[f"llm_deletions_{model_name}"].tolist()
except:
    summaries = [""] * 50
    
for i, text in enumerate(data['text']):
    if summaries[i] != "":
        continue
    print("Text:", text)
    print()
    summary = generate_summary_pipeline(text, summary_prompt, compression_prompt, add_more_words_prompt, 0.2)
    summaries[i] = summary[1]
    print(summaries)
    print("Summary:", summary)
    data[f'llm_deletions_{model_name}'] = summaries
    data.to_excel(r'.\new_generated.xlsx', index=False)
    print()
    print()

data[f'llm_deletions_{model_name}'] = summaries
data.to_excel(r'.\new_generated.xlsx', index=False)

summary_prompt = "Generate a summary of the following piece of text in Hindi Language in %d words. Do not use any words fron any other language. Be concise and informative. Do not generate any text other than the summary. The text starts from below:\n%s"
compression_prompt = "I want to compress the below Hindi text by removing parts that are not required to get the complete meaning of the text. Please delete the words and phrases that can be deleted without affecting the meaning of the text. Do not generate words other than the compressed summary. The summary starts from below:\n%s"
add_more_words_prompt = "I have a piece of Hindi text below:\n%s\nCould you please add %d more words to the following summary so that it becomes more informative and complete? Do not use any words other than Hindi language. Generate only the summary, and no other words. The summary starts from below:\n%s"
system_role = "You are an expert Hindi linguist."

def generate_summary_pipeline_logic(text, summary_prompt, add_more_words_prompt, compression_factor):
    words_in_text = len(text.split())
    words_in_final_summary = int(words_in_text * compression_factor)
    global system_role
    
    client = OpenAI(api_key=API_KEY)
    
    # generate summary
    messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": summary_prompt % (words_in_final_summary, text)},
            ]
    first_summary = rits_request(messages)
    
    # compress the summary
    processed_text = get_pos_tags(first_summary, pipeline=nlp)
    deleted_required_parts = delete_required_parts(processed_text)
    first_summary = get_text_output(deleted_required_parts)
    
    print("Loop 0:", first_summary)

    current_summary_words = len(first_summary.split())
    new_summary = first_summary
    
    loops = 0
    try:
        while words_in_final_summary - current_summary_words > 20 and loops < 10:
            print("Required words:", words_in_final_summary)
            print("Current words:", current_summary_words)
            
            # add words to compressed summary
            messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": add_more_words_prompt % (text, words_in_final_summary - current_summary_words, new_summary)},
                ]
            new_summary = rits_request(messages)
            
            # compress the summary
            processed_text = get_pos_tags(new_summary, pipeline=nlp)
            deleted_required_parts = delete_required_parts(processed_text)
            new_summary = get_text_output(deleted_required_parts)
            
            current_summary_words = len(new_summary.split())
            loops += 1
            
            print(f"Loop {loops}:", new_summary)
    except:
        pass
        
    return (loops, new_summary)

try:
    summaries = data[f"logic_deletions_{model_name}"].tolist()
except:
    summaries = [""] * 50
    
for i, text in enumerate(data['text']):
    if summaries[i] != "":
        continue
    print("Text:", text)
    print()
    summary = generate_summary_pipeline(text, summary_prompt, compression_prompt, add_more_words_prompt, 0.2)
    summaries[i] = summary[1]
    print(summaries)
    print("Summary:", summary)
    data[f'logic_deletions_{model_name}'] = summaries
    data.to_excel(r'.\new_generated.xlsx', index=False)
    print()
    print()

data[f'logic_deletions{model_name}'] = summaries
data.to_excel(r'.\new_generated.xlsx', index=False)