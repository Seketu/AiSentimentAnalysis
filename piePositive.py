import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Veri setini yükleme
dataset = pd.read_csv(r"C:\Users\avina\OneDrive\Belgeler\python\new_dataset.csv")

# Sütunları seçme
geminiColumn = dataset["Gemini"]
gptColumn = dataset["Gpt"]
llamaColumn = dataset["Llama"]
coreColumn = dataset["Core"]

# Her bir sütunun "Positive" ve diğer değerlerini hesaplama
columns = {
    "Gemini": geminiColumn,
    "GPT": gptColumn,
    "Llama": llamaColumn,
    "Core": coreColumn
}

# Pie grafikleri için hazırlık
fig, axes = plt.subplots(1, len(columns), figsize=(16, 6))

# Renkleri tanımlama
colors = ['green', 'lightgray']
legend_labels = ['Positive', 'Others']

for ax, (name, column) in zip(axes, columns.items()):
    positive_count = (column == "Positive").sum()
    other_count = len(column) - positive_count
    values = [positive_count, other_count]
    
    # Pie grafiği
    wedges, texts, autotexts = ax.pie(
        values,
        labels=[f'\n({positive_count})', f'\n({other_count})'],
        autopct='%1.1f%%',  # Yüzde gösterimi
        startangle=90,
        colors=colors,
        textprops={'fontsize': 14}
    )
    ax.set_title(f'{name}', fontsize=16)

# Genel bir legend ekleme
fig.legend(
    handles=[Patch(color=color) for color in colors],
    labels=legend_labels,
    loc="upper right",
    fontsize=14
)

plt.tight_layout()
plt.show()
