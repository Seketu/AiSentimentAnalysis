import pandas as pd
import matplotlib.pyplot as plt

# Veri setini okuma
dataset = pd.read_csv(r"C:\Users\avina\OneDrive\Belgeler\python\new_dataset.csv")

# Sütunları seçme
geminiColumn = dataset["Gemini"]
gptColumn = dataset["Gpt"]
llamaColumn = dataset["Llama"]
coreColumn = dataset["Core"]

# Core'daki Negative değerlerle eşleşen diğer sütunların Negative değerlerini seçme
gemini_negative_match = ((geminiColumn == "Negative") & (coreColumn == "Negative")).sum()
gpt_negative_match = ((gptColumn == "Negative") & (coreColumn == "Negative")).sum()
llama_negative_match = ((llamaColumn == "Negative") & (coreColumn == "Negative")).sum()

# Her sütun için kalan (eşleşmeyen) Negative değerler
gemini_non_match = (geminiColumn == "Negative").sum() - gemini_negative_match
gpt_non_match = (gptColumn == "Negative").sum() - gpt_negative_match
llama_non_match = (llamaColumn == "Negative").sum() - llama_negative_match

# Pie grafikleri için veri
data = [
    [gemini_negative_match, gemini_non_match],
    [gpt_negative_match, gpt_non_match],
    [llama_negative_match, llama_non_match]
]
labels = ["match", "non-match"]
colors = ["red", "lightgray"]
titles = ["Gemini", "GPT", "Llama"]

# Özelleştirilmiş autopct fonksiyonu
def autopct_with_counts(pct, all_values):
    total = sum(all_values)
    absolute = int(round(pct * total / 100.0))
    return f'{pct:.1f}%\n({absolute})'

# Grafik oluşturma
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for i, ax in enumerate(axes):
    wedges, texts, autotexts = ax.pie(
        data[i],
        labels=None,  # Sadece sayılar göstermek için labels'i kaldırıyoruz
        colors=colors,
        autopct=lambda pct: autopct_with_counts(pct, data[i]),
        textprops={'fontsize': 14}
    )
    ax.set_title(titles[i], fontsize=20)

# Genel legend ekleme
fig.legend(
    handles=[
        plt.Line2D([0], [0], color=color, linewidth=10) for color in colors
    ],
    labels=labels,
    loc="upper right",
    fontsize=14
)

plt.tight_layout()
plt.show()
