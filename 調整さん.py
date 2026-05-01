import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- スプレッドシート設定 ---
# 1. 接続設定
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# --- スプレッドシート設定 ---
# (前略：接続設定の部分はそのまま)
sheet = client.open("日程調整データ").sheet1 

# --- 1行目（候補日）の自動読み込み ---
# sheet.row_values(1) で1行目のすべての値を取得
# 1列目は「お名前」なので、2列目以降を候補日リストとして取得する
all_header_values = sheet.row_values(1)
dates = all_header_values[1:] # 0番目の「お名前」を除外して1番目から最後まで

# --- アプリ画面構成 ---
st.title("📅 日程調整ツール")

# 入力フォーム
with st.form("adjustment_form"):
    user_name = st.text_input("お名前")
    responses = {}
    
    # スプレッドシートから読み込んだ日付で選択肢を表示
    for d in dates:
        responses[d] = st.radio(d, ["〇", "△", "×"], horizontal=True)
    
    submitted = st.form_submit_button("回答を送信")

if submitted:
    if not user_name:
        st.error("お名前を入力してください")
    elif not dates:
        st.error("スプレッドシートの1行目に候補日が入力されていません")
    else:
        # 書き込み用データ作成
        row = [user_name] + [responses[d] for d in dates]
        sheet.append_row(row)
        st.success("回答を保存しました！")

# (以下、集計表示部分はそのまま)
# --- 集計表示（スプレッドシートから読み込み） ---
st.divider()
st.subheader("現在の集計状況")
data = sheet.get_all_records()
if data:
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)