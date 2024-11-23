import matplotlib.pyplot as plt
import pandas as pd 

# CSV dosyasını yükleme
dataset = pd.read_csv(r"C:\Users\avina\OneDrive\Belgeler\python\new_dataset.csv")

# Sütunları belirleme
gemini = dataset["Gemini"]
gpt = dataset["Gpt"] 
llama = dataset["Llama"]
core = dataset["Core"]

# Değerlerin sayısını hesaplama
geminiPositiveCount = (gemini == "Positive").sum()
geminiNotrCount = (gemini == "Notr").sum()
geminiNegativeCount = (gemini == "Negative").sum()

gptPositiveCount = (gpt == "Positive").sum()
gptNotrCount = (gpt == "Notr").sum()
gptNegativeCount = (gpt == "Negative").sum()

llamaPositiveCount = (llama == "Positive").sum()
llamaNotrCount = (llama == "Notr").sum()
llamaNegativeCount = (llama == "Negative").sum()

corePositiveCount = (core == "Positive").sum()
coreNotrCount = (core == "Notr").sum()
coreNegativeCount = (core == "Negative").sum()

# Bar genişliği
bar_width = 0.4
index = ['Gemini', 'GPT', 'Llama', 'Core']

# Yığılmış verileri hazırlama
positive_counts = [geminiPositiveCount, gptPositiveCount, llamaPositiveCount, corePositiveCount]
notr_counts = [geminiNotrCount, gptNotrCount, llamaNotrCount, coreNotrCount]
negative_counts = [geminiNegativeCount, gptNegativeCount, llamaNegativeCount, coreNegativeCount]

# Grafik için figür oluşturma
fig, ax = plt.subplots()

# Pozitif verileri ekleme
bars1 = ax.bar(index, positive_counts, bar_width, label='Positive', color='green')

# Nötr verileri pozitiflerin üzerine ekleme
bars2 = ax.bar(index, notr_counts, bar_width, bottom=positive_counts, label='Notr', color='blue')

# Negatif verileri nötrlerin üzerine ekleme
bars3 = ax.bar(index, negative_counts, bar_width, bottom=[i + j for i, j in zip(positive_counts, notr_counts)], label='Negative', color='red')

# Sayıları renklerin ortasına ekleme
for i, rects in enumerate([bars1, bars2, bars3]):
    counts = [positive_counts, notr_counts, negative_counts][i]
    for bar, count in zip(rects, counts):
        height = bar.get_height()
        bottom = bar.get_y()
        xval = bar.get_x() + bar.get_width() / 2  # Barın merkezi
        ax.text(xval, bottom + height / 2, int(count), ha='center', va='center', fontsize=10, color='white')  # Sayıyı ortala

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

max_value = max([sum(x) for x in zip(positive_counts, notr_counts, negative_counts)])
plt.yticks(range(0, max_value + 2, 10)) 

# Legend'i grafiğin dışına taşıma
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Layout düzenleme
plt.tight_layout()

# Grafiği gösterme
plt.show()
