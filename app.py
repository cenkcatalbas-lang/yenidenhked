import streamlit as st
import pandas as pd
import json
import os

DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"
PARTICIPANTS = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

st.set_page_config(page_title="HKED Turnuva", layout="wide")
st.title("🏆 HKED Tahmin Turnuvası")

@st.cache_data
def load_main_data():
    return pd.read_excel(DATA_FILE)

def load_results():
    # Eğer dosya yoksa boş bir yapı döndür, hata verme
    if not os.path.exists(RESULT_FILE):
        return {}
    with open(RESULT_FILE, "r", encoding='utf-8') as f:
        return json.load(f)

# Verileri yükle
df = load_main_data()
results = load_results()

# Puan Hesaplama Motoru
scores = {p: 0.0 for p in PARTICIPANTS}

for idx, res in results.items():
    if res in ["1", "0", "2"]:  # Sadece geçerli sonuçları işle
        try:
            row = df.iloc[int(idx)]
            res_int = int(res)
            odd = float(row[res_int])
            
            for p in PARTICIPANTS:
                # Excel'deki katılımcı sütununda o maçın sonucu varsa puan ekle
                if int(row[p]) == res_int:
                    scores[p] += odd
        except (IndexError, KeyError, ValueError):
            continue

# Tabloyu oluştur ve göster
leaderboard = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
leaderboard = leaderboard.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True)
leaderboard.index += 1

st.subheader("📊 Güncel Puan Durumu")
st.dataframe(leaderboard.style.format({"Toplam Puan": "{:.2f}"}), use_container_width=True)
