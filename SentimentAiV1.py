import random
import time
from datasets import load_dataset
import openai
import threading
import google.generativeai as genai
from groq import Groq
import csv
import os
import sys
import re
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Api Key's
openai.api_key = str(os.getenv("OPENAI_APIKEY"))
genai.configure(api_key=str(os.getenv("GEMINI_APIKEY")))
client = Groq(
    api_key=str(os.getenv("GROQ_APIKEY"))
)

def extract_sentiment(content):
    """
    Açık sayısal skorlara öncelik veren geliştirilmiş duygu skorlama fonksiyonu.
    Öncelikle skor göstergelerini (+1, -1, 0) uygun bağlam doğrulamasıyla bulmaya odaklanır.
    """
    # Birinci aşama: Doğrudan skor göstergelerini arama
    # Pozitif skorlar (tam eşleşme)
    if re.search(r'\*\*\+1\*\*', content) or re.search(r'(?<!\-)\b\+1\b', content):
        return "Positive"
    
    # Negatif skorlar (tam eşleşme)
    if re.search(r'\*\*\-1\*\*', content) or re.search(r'\b\-1\b', content):
        return "Negative"
    
    # Nötr skorlar (tam eşleşme) - en yüksek öncelikli kontrol
    if re.search(r'\*\*0\*\*', content) or re.search(r'(?<![1-9])\b0\b(?![1-9])', content):
        return "Notr"
    
    # İkinci aşama: Duygu/skor kelimeleriyle birlikte skor göstergeleri
    score_statement_patterns = [
        # Nötr için tam eşleşmeler (en yüksek öncelik)
        (r'(?:score|sentiment|rating)[\s\:]+(is[\s\:]+)?0\b', "Notr"),
        
        # Pozitif için tam eşleşmeler
        (r'(?:score|sentiment|rating)[\s\:]+(is[\s\:]+)?\+1\b', "Positive"),
        (r'(?:score|sentiment|rating)[\s\:]+(is[\s\:]+)?(?<!\-)1\b', "Positive"),
        
        # Negatif için tam eşleşmeler
        (r'(?:score|sentiment|rating)[\s\:]+(is[\s\:]+)?\-1\b', "Negative")
    ]
    
    for pattern, result in score_statement_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return result
    
    # Üçüncü aşama: Duygu anahtar kelimelerini sadece skor göstergeleriyle eşleştiğinde kontrol et
    sentiment_score_patterns = [
        (r'sentiment.*?\bis\b.*?\bpositive\b.*?\+1\b', "Positive"),
        (r'sentiment.*?\bis\b.*?\bnegative\b.*?\-1\b', "Negative"),
        (r'sentiment.*?\bis\b.*?\bneutral\b.*?0\b', "Notr"),
        (r'\+1\b.*?positive', "Positive"),
        (r'\-1\b.*?negative', "Negative"),
        (r'0\b.*?neutral', "Notr")
    ]
    
    for pattern, result in sentiment_score_patterns:
        if re.search(pattern, content, re.IGNORECASE) or re.search(pattern[::-1], content, re.IGNORECASE):
            return result
    
    # Son aşama: İçerikteki herhangi bir sayısal göstergeyi ara
    # Tüm potansiyel skor değerlerini çıkar (0, 1, +1, -1)
    number_matches = re.findall(r'(?<!\w)(\+?\-?[01])(?!\w)', content)
    if number_matches:
        # Sadece 0, 1, +1, -1 değerlerine odaklan
        valid_scores = [match for match in number_matches if match in ['0', '1', '+1', '-1']]
        if valid_scores:
            # Genellikle son kullanılan skor en geçerli olandır
            last_score = valid_scores[-1]
            if last_score == '0':
                return "Notr"
            elif last_score in ['1', '+1']:
                return "Positive"
            elif last_score == '-1':
                return "Negative"
    
    # Özel durum: Çok net olan skor/duygu ifadelerini ara
    final_sentiment_patterns = [
        (r'score.*?positive', "Positive"),
        (r'sentiment.*?positive', "Positive"),
        (r'score.*?negative', "Negative"),
        (r'sentiment.*?negative', "Negative"),
        (r'score.*?neutral', "Notr"),
        (r'sentiment.*?neutral', "Notr")
    ]
    
    for pattern, result in final_sentiment_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            context_match = re.search(pattern, content, re.IGNORECASE)
            if context_match:
                # Eşleşmenin etrafında 50 karakterlik bir bağlam al
                start = max(0, context_match.start() - 25)
                end = min(len(content), context_match.end() + 25)
                context = content[start:end].lower()
                
                # Çelişen duygu göstergeleri var mı kontrol et
                if result == "Positive" and "negative" in context:
                    continue
                elif result == "Negative" and "positive" in context:
                    continue
                elif result == "Notr" and ("positive" in context or "negative" in context):
                    # Çelişki yoksa nötr kabul et
                    if not ("neither positive nor negative" in context or "balanced sentiment" in context):
                        continue
                
                return result
    
    # Varsayılan durum - gerçekten belirlenemiyorsa
    return "Notr"

def writeToCsv(writeList):
    """Write results to CSV file"""
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
    filepath = r"C:\Users\avina\OneDrive\Belgeler\python\dataset.csv"
    
    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=csv_headers)
            writer.writeheader()
            for row in writeList:
                writer.writerow(row)
        print(f"Results successfully saved to: {filepath}")
    except Exception as e:
        print(f"Error saving to main CSV: {str(e)}")
        # If main save fails, try backup save
        save_and_exit(writeList, f"Main save failed: {str(e)}")

def save_and_exit(total_list, error_msg="Unknown error"):
    """Save current results and exit program"""
    print(f"\nError occurred: {error_msg}")
    print(f"Saving {len(total_list)} results collected so far...")
    
    try:
        csv_headers = [
            "Gemini", "Gpt", "Llama", "Core",
            "GeminiContent", "GptContent", "LlamaContent", "Tweet"
        ]
        
        # Save with timestamp to avoid overwriting
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filepath = f"C:\\Users\\avina\\OneDrive\\Belgeler\\python\\dataset_partial_{timestamp}.csv"
        
        with open(filepath, mode="w", newline="", encoding="utf-8") as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=csv_headers)
            writer.writeheader()
            for row in total_list:
                writer.writerow(row)
        print(f"Partial results saved to: {filepath}")
    except Exception as e:
        print(f"Critical error - Could not save results: {str(e)}")
    finally:
        sys.exit(1)

def askToGpt(prompt, GptResult):
    try:
        toPrompt = "Analyze the sentiment of the following tweet and provide a score of **+1** for positive, **0** for neutral, or **-1** for negative, followed by a brief explanation of the sentiment. The score must be included exactly as specified and used only once. tweet : " + prompt
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": toPrompt},
            ]
        )
        content = response.choices[0].message.content
        result = extract_sentiment(content)
        
        GptResult.append(
            {"GptResponse": result, "GptContent": content}
        )
        print("GPT:", result)
    except Exception as e:
        writeToCsv(totalList)    
        error_msg = f"GPT API Error: {str(e)}"
        raise Exception(error_msg)

def askToLlama(prompt: str, LlamaResult: list):
    try:
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
        result = extract_sentiment(content)

        LlamaResult.append(
            {"LlamaResponse": result, "LlamaContent": content}
        )
        print("Llama:", result)
    except Exception as e:
        writeToCsv(totalList)
        error_msg = f"Llama API Error: {str(e)}"
        raise Exception(error_msg)

def askToGemini(prompt: str, GeminiList: list):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        toPrompt = "Analyze the sentiment of the following tweet and provide a score of **+1** for positive, **0** for neutral, or **-1** for negative, followed by a brief explanation of the sentiment. The score must be included exactly as specified and used only once. tweet : " + prompt
        
        response = model.generate_content(toPrompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            })

        content = response.text
        result = extract_sentiment(content)

        GeminiList.append(
            {"GeminiContent": content, "GeminiResponse": result}
        )
        print("Gemini:", result)
    except Exception as e:
        error_msg = f"Gemini API Error: {str(e)}"
        writeToCsv(totalList)
        raise Exception(error_msg)

# Main execution
try:
    # Initialize result lists
    GptResult = []
    GeminiResult = []
    LlamaResult = []

    # Load dataset
    dataset = load_dataset("winvoker/turkish-sentiment-analysis-dataset")
    TrainList = dataset["train"]["label"]
    text = dataset["train"]["text"]

    # Prepare data
    combined = list(zip(text, TrainList))
    random_combined = random.sample(combined, 150)
    promptList, selectedTrainList = zip(*random_combined)

    j = 0
    a = 3
    totalList = []

    # Process each prompt
    for i, prompt in enumerate(promptList):
        try:
            print(f"\nProcessing item {i+1}/2000")
            
            t1 = threading.Thread(target=askToGemini, args=(prompt, GeminiResult))
            t2 = threading.Thread(target=askToGpt, args=(prompt, GptResult))
            t3 = threading.Thread(target=askToLlama, args=(prompt, LlamaResult))

            t1.start()
            t2.start()
            t3.start()

            t1.join()
            t2.join()
            t3.join()

            # Create combined result after successful processing
            combined_result = {
                "Gemini": GeminiResult[-1]["GeminiResponse"],
                "Gpt": GptResult[-1]["GptResponse"],
                "Llama": LlamaResult[-1]["LlamaResponse"],
                "Core": selectedTrainList[i],
                "GeminiContent": GeminiResult[-1]["GeminiContent"],
                "GptContent": GptResult[-1]["GptContent"],
                "LlamaContent": LlamaResult[-1]["LlamaContent"],
                "Tweet": prompt
            }
            totalList.append(combined_result)

            j += 1
            if j == a:
                time.sleep(30)
                a += 5

        except Exception as e:
            save_and_exit(totalList, str(e))

    # If everything completes successfully, save final results
    writeToCsv(totalList)
    print("Processing completed successfully!")

except Exception as e:
    save_and_exit(totalList, str(e))