import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

# CSV dosyasını oku
csv_file = r"C:\Users\avina\OneDrive\Belgeler\python\dataset.csv"
base_table = pd.read_csv(csv_file)

# İlgili sütunları al
gemini_column = base_table["Gemini"]
gpt_column = base_table["Gpt"]
llama_column = base_table["Llama"]
core_column = base_table["Core"]

# 2D çapraz tabloları oluştur
total_gemini = pd.crosstab(gemini_column, core_column)
total_gpt = pd.crosstab(gpt_column, core_column)
total_llama = pd.crosstab(llama_column, core_column)

# Subplotlar oluştur
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# İlk ısı haritası: Gemini vs Core
sns.heatmap(total_gemini, cmap="coolwarm", linewidths=0.5, annot=True, ax=axes[0], cbar=False,yticklabels=total_gemini.index)
axes[0].set_title("Gemini vs Core")
axes[0].set_xlabel('Core')
axes[0].set_ylabel('')

# İkinci ısı haritası: Gpt vs Core
sns.heatmap(total_gpt, cmap="coolwarm", linewidths=0.5, annot=True, ax=axes[1], cbar=False)
axes[1].set_title("Gpt vs Core")
axes[1].set_xlabel('Core')
axes[1].set_ylabel('')
axes[1].set_yticklabels([])

# Üçüncü ısı haritası: Llama vs Core
sns.heatmap(total_llama, cmap="coolwarm", linewidths=0.5, annot=True, ax=axes[2], cbar=False)
axes[2].set_title("Llama vs Core")
axes[2].set_xlabel('Core')
axes[2].set_ylabel('')
axes[2].set_yticklabels([])

# Grafikleri düzenle
plt.tight_layout()
plt.show()
