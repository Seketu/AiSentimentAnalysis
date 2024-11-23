from matplotlib import pyplot as plt
import pandas as pd
import csv 


data = pd.read_csv(r"C:\Users\avina\OneDrive\Belgeler\python\new_dataset.csv")

geminiResponse = data["Gemini"]
gptResponse = data["Gpt"]
llamaResponse = data["Llama"]
coreResponse = data["Core"]

index = coreResponse.sum()

geminiPositiveResponse = (geminiResponse == "Positive").sum()
gptPositiveResponse = (gptResponse == "Positive").sum()
llamaPositiveResponse = (llamaResponse == "Positive").sum()
corePositiveResponse = (coreResponse == "Positive").sum()


fig, ax = plt.subplots()

ax.bar(index , geminiPositiveResponse ,width= 0.2)

plt.show()