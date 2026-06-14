import streamlit as st
import pandas as pd
import json
import os

# Ayarlar
DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"
PARTICIPANTS = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

st.set_page_config(page_title="HKED Turnuva", layout="wide")
st.title("🏆 HKED Tahmin Turnuvası")

# Veri Yükleme ve Kaydetme Fonksiyonları
def load_results():
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "r") as f:
            return json.load(f)
    return {}

def save_results(results):
    with open(RESULT_FILE, "w") as f:
        json.dump(results, f)

@st.cache_data
def load_main_data():
    return pd.read_excel(DATA_FILE)

# Ana Mantık
try:
    df = load_main_data()
    results = load_results()

    # Sidebar: Maç Sonucu Girişi
    st.sidebar.header("⚙️ Admin: Maç Sonuçları")
    
    new_results = results.copy()
    for index, row in df.iterrows():
        match_name = f"{row['TAKIM - 1']} - {row['TAKIM - 2']}"
        current_val = results.get(str(index), "Oynanmadı")
        
        res = st.sidebar.selectbox(
            match_name,
            options=["Oynanmadı", "1", "0", "2"],
            index=["Oynanmadı", "1", "0", "2"].index(current_val),
            key=f"match_{index}"
        )
        new_results[str(index)] = res

    if st.sidebar.button("💾 Sonuçları Kaydet"):
        save_results(new_results)
        st.sidebar.success("Güncellendi!")
        st.rerun()

    # Puan Hesaplama
    scores = {p: 0.0 for p in PARTICIPANTS}
    for idx, res in new_results.items():
        if res != "Oynanmadı":
            idx = int(idx)
            row = df.iloc[idx]
            res_int = int(res)
            odd = float(row[res_int])
            
            for p in PARTICIPANTS:
                if int(row[p]) == res_int:
                    scores[p] += odd

    # Puan Durumu Tablosu
    leaderboard = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Puan'])
    leaderboard = leaderboard.sort_values(by='Puan', ascending=False).reset_index(drop=True)
    leaderboard.index += 1

    # Görselleştirme
    st.subheader("📊 Güncel Puan Durumu")
    st.dataframe(leaderboard.style.format({"Puan": "{:.2f}"}), use_container_width=True)

    with st.expander("📅 Tüm Fikstür ve Tahminler"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Hata: {e}")
