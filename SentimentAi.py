import random
import time
from datasets import load_dataset
import openai
import threading
import google.generativeai as genai
from groq import Groq
import csv
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold


#Api Key's
openai.api_key= str(os.getenv("OPENAI_APIKEY"))
genai.configure(api_key= str(os.getenv("GEMINI_APIKEY")))
client = Groq(
     api_key=str(os.getenv("GROQ_APIKEY"))
)

#For Exapmle DataSet
dataset = load_dataset("winvoker/turkish-sentiment-analysis-dataset")

GptResult = []
GeminiResult = []
LlamaResult = []

#Ask to Gpt Def For initialize Apı and Work with openAi 
def askToGpt(prompt, GptResult):
     toPrompt = "Analyze the sentiment of the following tweet and provide a score of **+1** for positive, **0** for neutral, or **-1** for negative, followed by a brief explanation of the sentiment. The score must be included exactly as specified and used only once. tweet : " + prompt
     response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": toPrompt},
        ]
        )
     result = "Error"
     content : str = response.choices[0].message.content

     if "+1" in content:
         result = "Pozitive"
     elif "-1" in content:
         result = "Negative"
     elif "0" in content:
          result = "Notr" 


     GptResult.append(
         {"GptResponse" : result, "GptContent" :content}
         )
     print(result)
 
def askToLlama(prompt : str , LlamaResult : list):
    
    toPrompt = "Analyze the sentiment of the following tweet and provide a score of **+1** for positive, **0** for neutral, or **-1** for negative, followed by a brief explanation of the sentiment. The score must be included exactly as specified and used only once. tweet : " + prompt

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": toPrompt,
        }
     ],
     model="llama3-8b-8192",
     )
    
    content = chat_completion.choices[0].message.content
    result = "Error"
    if "+1" in content:
         result = "Positive"
    elif "-1" in content:
         result = "Negative"
    elif "0" in content:
        result = "Notr"
    
    LlamaResult.append(
         {"LlamaResponse" : result , "LlamaContent" : content}
    )
    print(result)

def askToGemini(prompt : str , GeminiList : list):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    toPrompt = "Analyze the sentiment of the following tweet and provide a score of **+1** for positive, **0** for neutral, or **-1** for negative, followed by a brief explanation of the sentiment. The score must be included exactly as specified and used only once. tweet : " + prompt

    response = model.generate_content(toPrompt,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT : HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH : HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT : HarmBlockThreshold.BLOCK_NONE,
    })
    
    content = response.text
    result = "Error"

    if "+1" in content:
        result = "Positive"
    elif "-1" in content:
        result = "Negative"
    elif "0" in content:
        result = "Notr"

    GeminiList.append(
         {"GeminiContent" : content , "GeminiResponse" : result}
    )
    print(result)



TrainList = dataset["train"]["label"]
text = dataset["train"]["text"]

# Metinler ve etiketleri birleştir
combined = list(zip(text, TrainList))

# 250 rastgele metin-etiket çiftini seç
random_combined = random.sample(combined, 150)

# Seçilen metin ve etiketleri ayrı listelere ayır
promptList, selectedTrainList = zip(*random_combined)

j=0
a = 5
#Start To Models at sub-thread
for i in promptList:
    t1 = threading.Thread(target=askToGemini,args=(i,GeminiResult))
    t2 = threading.Thread(target=askToGpt,args=(i,GptResult))
    t3 = threading.Thread(target=askToLlama,args=(i,LlamaResult))
    
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
    j = j+1
    print(j)
    if j == a:
        time.sleep(60)
        a = a+5


totalList = []

for i in range(len(GeminiResult)):
     combined_result = {
          "Gemini": GeminiResult[i]["GeminiResponse"],
          "Gpt": GptResult[i]["GptResponse"],
          "Llama": LlamaResult[i]["LlamaResponse"],
          "Core": selectedTrainList[i],
          "GeminiContent": GeminiResult[i]["GeminiContent"],
          "GptContent": GptResult[i]["GptContent"],
          "LlamaContent": LlamaResult[i]["LlamaContent"],
          "Tweet": promptList[i]
     }
     totalList.append(combined_result)


def writeToCsv(writeList):
        csv_headers = [
        "Gemini",
        "Gpt",
        "Llama",
        "Core",
        "GeminiContent",
        "GptContent",
        "LlamaContent",
        "Tweet"
        ]
        with open(r"C:\Users\avina\OneDrive\Belgeler\python\dataset.csv", mode="w", newline="",encoding="utf-8") as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=csv_headers)
            writer.writeheader()
            for row in writeList:
                 writer.writerow(row)

writeToCsv(totalList)

