import pandas as pd

# CSV dosyasını yükle
df = pd.read_csv('dataset.csv')

# "Pozitive" değerlerini "Positive" olarak değiştir
df.replace('Pozitive', 'Positive', inplace=True)

# Değiştirilen DataFrame'i yeni bir CSV dosyasına kaydet
df.to_csv('new_dataset.csv', index=False)
