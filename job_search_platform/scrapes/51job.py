from googletrans import Translator
import pandas as pd

df = pd.read_json("./jobsData.json")
df = df.iloc[0:10]  # limiting the range as this process takes time

def translate_text(text):
    translator = Translator()
    translated = translator.translate(text, src='zh-cn', dest='en').text
    return translated

df['title_en'] = df['title'].apply(translate_text)
print(df['title_en'])

# save df later to another file, in order to translate only once, then makes something to just translate new data
# makes a df diff between new and old data, choosing some kind of key to match to translate new data only