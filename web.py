import streamlit as st
import pandas as pd
import altair as alt
import requests
import io

st.markdown(
    """
    <style>
        body {
            background-color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("""
Хүн амын эрүүл мэндийн их өгөгдөл (Population based health big data)         
""")

st.subheader("Амьдралын хэв маягийн өгөгдөл (Lifestyle data)")
st.subheader("Стресст өртөх магадлал / ISMA ")

st.text("""
0 -ээс 4 = Стресст өртөх магадлал бага
5 -өөс 14 = Стресст өртөх магадлал өндөр
14 ба түүнээс их = Стрессийн түвшин өндөр
""")

# Excel файлыг URL-ээс унших
url = 'https://raw.githubusercontent.com/Reina0326/App-Visualization/main/modified_Responses.xlsx'
response = requests.get(url)
df = pd.read_excel(io.BytesIO(response.content))

df["Цахим хаяг"] = df["Цахим хаяг"].astype(str)

# Нийт оролцогчдын тоо
parts = len(df["Row of Sum"])

# Түвшин тогтоох функц
def assign_description(row_sum):
    if row_sum <= 4:
        return "Магадлал бага"
    elif row_sum < 14:
        return "Магадлал өндөр"
    else:
        return "Стрессийн түвшин өндөр"

df['Description'] = df['Row of Sum'].apply(assign_description)

# Төрлөөр нь тоолох
count_data = df['Description'].value_counts().to_dict()
minimum_counter = count_data.get("Магадлал бага", 0)
middle_counter = count_data.get("Магадлал өндөр", 0)
high_counter = count_data.get("Стрессийн түвшин өндөр", 0)

# Бар чарт
source = pd.DataFrame({
    'Category': ["Магадлал бага", "Магадлал өндөр", "Стрессийн түвшин өндөр"],
    'Count': [minimum_counter, middle_counter, high_counter]
})
bar_chart = alt.Chart(source).mark_bar(size=50, color='skyblue').encode(
    x='Category',
    y='Count'
).properties(
    title=f"Судалгаанд оролцсон хүмүүсийн ангилал (Нийт оролцогчид: {parts})",
    width=600,  
    height=400
)
st.altair_chart(bar_chart, use_container_width=True)

# Бокс чарт
box_chart = alt.Chart(df).mark_boxplot(size=60, color='pink').encode(
    y=alt.Y('Row of Sum', title='Row of Sum')
).properties(
    title="Стрессийн түвшний тархалт (Box Chart)"
)
st.altair_chart(box_chart, use_container_width=True)

# Pie Chart
source['Percentage'] = (source['Count'] / parts) * 100
pie_chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
    theta=alt.Theta('Count', type='quantitative', title=''),
    color=alt.Color('Category:N', legend=None),
    tooltip=['Category', 'Count', 'Percentage']
).properties(
    width=400,
    height=400,
    title="Судалгаанд оролцсон хүмүүсийн статистик"
)
st.altair_chart(pie_chart, use_container_width=True)

# Histogram
histogram = alt.Chart(df).mark_bar(color='skyblue').encode(
    alt.X('Row of Sum:Q', bin=alt.Bin(maxbins=20), title='Row of Sum Утгууд'),
    alt.Y('count()', title='Давтамж'),
    tooltip=['count()']
).properties(
    width=600,
    height=400,
    title="Нийт хүн амын стрессийн түвшин"
)
st.altair_chart(histogram, use_container_width=True)

# Scatter Chart
scatter = alt.Chart(df).mark_point(color='goldenrod').encode(
    x=alt.X('Row of Sum:Q', title='Row of Sum Утгууд'),
    y=alt.Y('count()', title='Давтамж'),
    tooltip=['count()']
).properties(
    width=600,
    height=400,
    title="Нийт хүн амын стрессийн түвшин (Scatter Chart)"
)
st.altair_chart(scatter, use_container_width=True)

