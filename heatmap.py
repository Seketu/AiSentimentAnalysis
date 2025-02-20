import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# CSV dosyasını oku
csv_file = r"C:\Users\avina\OneDrive\Belgeler\python\new_dataset.csv"
base_table = pd.read_csv(csv_file)

# İlgili sütunları al
gemini_column = base_table["Gemini"]
gpt_column = base_table["Gpt"]
llama_column = base_table["Llama"]
core_column = base_table["Core"]

# 2D çapraz tabloları oluştur ve satırları ters çevir
total_gemini = pd.crosstab(gemini_column, core_column).iloc[::-1]
total_gpt = pd.crosstab(gpt_column, core_column).iloc[::-1]
total_llama = pd.crosstab(llama_column, core_column).iloc[::-1]

# Subplotlar oluştur
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# İlk ısı haritası: Gemini vs Core
sns.heatmap(total_gemini, cmap="coolwarm", linewidths=0.5, annot=True, ax=axes[0], cbar=False, yticklabels=total_gemini.index, annot_kws={"size": 24})
axes[0].set_title("Gemini")
axes[0].set_xlabel('Core')
axes[0].set_ylabel('')

# İkinci ısı haritası: Gpt vs Core
sns.heatmap(total_gpt, cmap="coolwarm", linewidths=0.5, annot=True, ax=axes[1], cbar=False, yticklabels=total_gpt.index, annot_kws={"size": 24})
axes[1].set_title("Gpt")
axes[1].set_xlabel('Core')
axes[1].set_ylabel('')

# Üçüncü ısı haritası: Llama vs Core
sns.heatmap(total_llama, cmap="coolwarm", linewidths=0.5, annot=True, ax=axes[2], cbar=False, annot_kws={"size": 24}, yticklabels=total_llama.index)
axes[2].set_title("Llama")
axes[2].set_xlabel('Core')
axes[2].set_ylabel('')

axes[0].tick_params(axis='y', labelsize=14)  # Gemini için
axes[1].tick_params(axis='y', labelsize=14)  # Gpt için
axes[2].tick_params(axis='y', labelsize=14)  # Llama için

# Tüm eksenler için x-tick yazı boyutunu büyütmek isterseniz:
for ax in axes:
    ax.tick_params(axis='x', labelsize=14)


# Grafikleri düzenle
plt.tight_layout()
plt.show()
