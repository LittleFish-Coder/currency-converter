import streamlit as st
import requests

currency_list = ["USD", "JPY", "CNY", "EUR", "KRW", "TWD"]

# set the app icon
st.set_page_config(
    page_title="貨幣轉換器",
    page_icon="💱",
    layout="centered",
)


def english_to_chinese(code):
    country = {
        "USD": "美金",
        "JPY": "日圓",
        "CNY": "人民幣",
        "EUR": "歐元",
        "KRW": "韓元",
        "TWD": "台幣",
    }

    return country[code]


def source_to_target_rate(source, target):
    source = "USD" + source
    target = "USD" + target
    usd_to_source = currency[source]["Exrate"]
    usd_to_target = currency[target]["Exrate"]
    rate = usd_to_target / usd_to_source

    return rate


@st.cache_data()
def get_currency():
    response = requests.get("http://tw.rter.info/capi.php")
    currency = response.json()
    print(currency)
    return currency


st.title("貨幣轉換器")
currency = get_currency()
source = st.selectbox("貨幣", currency_list, index=1)
target = st.selectbox("貨幣", currency_list, index=5)
rate = source_to_target_rate(source, target)

st.write(f"{english_to_chinese(source)} - {english_to_chinese(target)} 的匯率是", rate)

# a place for user to input the amount
amount = st.number_input("請輸入金額", min_value=0.0, step=0.01, value=1.0)
convert_btn = st.button("轉換")

if convert_btn or amount:
    result = round(amount * rate, 2)
    st.write(f"{amount} {english_to_chinese(source)} = {result} {english_to_chinese(target)}")
