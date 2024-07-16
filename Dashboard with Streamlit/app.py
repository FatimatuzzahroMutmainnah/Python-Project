
import streamlit as st
import plotly.graph_objects as go
import locale
from pyngrok import ngrok
import subprocess

# Fungsi untuk memformat angka dengan titik sebagai pemisah ribuan
def format_number(number):
    return f"{number:,}"

# Atur konfigurasi halaman
st.set_page_config(page_title="Training Submission Dashboard",
                   layout="wide"
                   )

theme_plotly = None

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

#-----------------------------------------------------------------------------------

#Import Data
def get_data_from_excel():
  df = pd.read_excel("/content/drive/MyDrive/Biaya Pelatihan.xlsx", sheet_name='External & Certification Ra (2)')
  data = df.iloc[:2119, :15]
  # Nama kolom yang ingin dipindahkan ke paling akhir
  column_to_move = ' PLAN BIAYA R4 (Bold merah: adanya adjustment dari budget sebelumnya)'
  # Memindahkan kolom ke paling akhir
  data = data[[*data.drop(columns=column_to_move), column_to_move]]
  # Mengubah nama kolom
  data.rename(columns={' PLAN BIAYA R4 (Bold merah: adanya adjustment dari budget sebelumnya)': 'PLAN BIAYA'}, inplace=True)
  #mengahpus kolom yang tidak digunakan
  data.drop(columns=['NRP', 'NAMA', 'JABATAN', 'AREA', 'JENIS KOMPETENSI', 'Grouping2'], inplace=True)
  # Mengganti nilai di kolom 'GROUPING'
  data['Grouping'] = data['Grouping'].replace('External - Inhouse Training', 'External - InHouse Training')
  cut_labels = ['Kecil', 'Menengah', 'Besar']
  data['Cost_segment'] = pd.qcut(data['PLAN BIAYA'][data['PLAN BIAYA']>0],q=[0, .25, .75, 1], labels=cut_labels).astype("object")
  # Menghapus outlier
  data.drop(data[data['PLAN BIAYA'] == 261000000].index, inplace=True)
  #Mengubah nama kolom
  data.columns = ['DIVISI', 'AREA', 'POSISI', 'GRUP POSISI', 'GRUP TALENT', 'KOMPETENSI', 'PLAN JUDUL', 'JENIS PELATIHAN', 'PLAN BIAYA', 'KLASIFIKASI BIAYA']
  return data

data = get_data_from_excel()

st.markdown("""
    <style>
    .main .block-container {
        padding-top: 50px;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Training Submission Dashboard")

#-----------------------------------------------------------------------------------
st.markdown("""
  <style>
    .stMultiSelect div[role='listbox'] {
        background-color: blue !important; /* Mengubah warna hitam menjadi biru */
    }
    .stMultiSelect div[role='listbox'] span[data-baseweb='tag'] {
        background-color: white !important; /* Mengubah warna hitam menjadi biru */
        color: black !important;
    }
    .stMultiSelect div[role='listbox'] span[data-baseweb='tag'] svg {
        fill: blue !important; 
    }    
    .stMultiSelect label {
        color: black !important;
        font-size: 20px !important;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }    
    div[data-testid="stVerticalBlock"] > div {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
  </style>
""", unsafe_allow_html=True)

# Layout filter
left_column, right_column = st.columns(2)

#Filter 1 jenis pelatihan
with left_column:
  jenis_pelatihan = data['JENIS PELATIHAN'].unique()
  selected_jenis_pelatihan = st.multiselect('Type of Submission :',
                                            jenis_pelatihan,
                                             ['External - InHouse Training', 'Certification']
                                            )

#Filter 2 area
with right_column:
  area = data['AREA'].unique()
  selected_area = st.multiselect('Work Area :',
                                 area,
                                  ['HO', 'Non HO']
                                  )

# Memastikan variabel selalu terdefinisi
if not selected_jenis_pelatihan:
    selected_jenis_pelatihan = jenis_pelatihan

if not selected_area:
    selected_area = area

# Filter the data
filtered_data = data[
    (data['JENIS PELATIHAN'].isin(selected_jenis_pelatihan))
    & (data['AREA'].isin(selected_area))
]

#-----------------------------------------------------------------------------------
# Menambahkan CSS

st.markdown("""
    <style>
    body {
        background: url('https://www.thehoneylady.co.id/wp-content/uploads/2022/07/standar-ruang-kantor.jpg') no-repeat center center fixed !important;
        background-size: cover;
        color: black;
    }
    .main .block-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        color: black;
    }
    .metric-container {
        border: 2px solid black;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        background-color: rgba(95, 158, 160, 0.8);
        color: black;
    }
    .metric-container-bg {
        background-color: #5F9EA0;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        color: black;
    }
    .column-content {
        margin: 0;
        color: black;
    }
    h1 {
        color: black;
    }
    h2 {
        color: black;
    }
    .stMetric {
        background-color: #48D1CC; /* Change background to blue */
        border: 2px solid black;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        color: black; /* Change text color to white */
    }
    .stMetric-label {
        font-size: 18px;
        color: black; /* Ensure the label text is white */
    }
    .stMetric-value {
        font-size: 24px;
        font-weight: bold;
        color: black; /* Ensure the value text is white */
    }
    .separator {
        margin-top: 20px;
        margin-bottom: 20px;
        border: none;
        border-top: 2px solid gray; /* Gray border */
    }
    </style>
    """, unsafe_allow_html=True)

#Summary
st.markdown('<h2 style="color: black">Training Submission in 2024</h2>', unsafe_allow_html=True)

number_of_submission = int(filtered_data["PLAN BIAYA"].count())
number_of_training = len(filtered_data["PLAN JUDUL"].unique())
total_expenditure = int(filtered_data["PLAN BIAYA"].sum())

left_column, middle_column, right_column = st.columns(3, gap='small')
with left_column:
    st.markdown('<div class="stMetric"><div class="stMetric-label"><span>📑</span><span>Number of Submission</span></div><div class="stMetric-value"><span>{}</span></div></div>'.format(format_number(number_of_submission)), unsafe_allow_html=True)
with middle_column:
    st.markdown('<div class="stMetric"><div class="stMetric-label"><span>📋</span><span>Number of Training</span></div><div class="stMetric-value"><span>{}</span></div></div>'.format(number_of_training), unsafe_allow_html=True)
with right_column:
    st.markdown('<div class="stMetric"><div class="stMetric-label"><span>💰</span><span>Total Expenditure</span></div><div class="stMetric-value"><span>Rp {}</span></div></div>'.format(format_number(total_expenditure)), unsafe_allow_html=True)

# Adding a gray horizontal line as a separator
st.markdown('<hr class="separator">', unsafe_allow_html=True)


st.write("")
#-----------------------------------------------------------------------------------

# Graph

#Graph 1 : Bar Chart TOP 10 JUDUL

#Hitung top 10 frekuensi setiap nilai di kolom 'PLAN JUDUL'
top_10_plan_judul = filtered_data['PLAN JUDUL'].value_counts().head(10)

#Buat DataFrame dari hasil perhitungan
top_10_plan_judul_df = top_10_plan_judul.reset_index()
top_10_plan_judul_df.columns = ['PLAN JUDUL', 'Total']

#barchart top 10
fig_plan_judul = px.bar(
    top_10_plan_judul_df,
    x="Total",
    y="PLAN JUDUL",
    orientation="h",
    text="Total",
    title="<b>Top 10 Training Submission</b>",
    color_discrete_sequence=["#0083B8"] * len(top_10_plan_judul_df),
    template="plotly_white",
)

# Mengatur label dan urutan kategori
fig_plan_judul.update_traces(texttemplate='%{text}', textposition='outside')
fig_plan_judul.update_layout(
    title={
        'text': "<span style='font-weight:normal'>Top 10 Training Submission</span>",
        'x':0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': 'black'}
    },
    yaxis=dict(categoryorder='total ascending',
               title='Training Title',
               titlefont=dict(color='black'),
               tickfont=dict(color='black')
    ),
    xaxis=dict(title='Total',
               titlefont=dict(color='black'),
               tickfont=dict(color='black'),
               range=[0, 300]
    ),
    showlegend=False,
    margin=dict(r=30),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='black')
)

#Graph 2 : Pie Chart Kategori Biaya

# Hitung frekuensi setiap nilai di kolom 'KLASIFIKASI BIAYA'
Cost = filtered_data['KLASIFIKASI BIAYA'].value_counts()
label = Cost.index
counts = Cost.values

# Membuat pie chart
colors = ['gold','lightgreen']
fig_klasifikasi_biaya = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig_klasifikasi_biaya.update_layout(
    title={
        'text':"<span style='font-weight:normal'>Cost Classification</span>",
        'x':0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': 'black'}
        },
    legend={
        'font': {'color': 'black'}
    },
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='black')
    )
fig_klasifikasi_biaya.update_traces(hoverinfo='label+value',
                                    textinfo='percent',
                                    textfont=dict(size=20, color='black'),
                                    marker=dict(colors=colors, line=dict(color='black', width=2))
                                    )
# layout graph
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_plan_judul, use_container_width=True)
right_column.plotly_chart(fig_klasifikasi_biaya, use_container_width=True)

#-----------------------------------------------------------------------------------
#Graph 3 : Pie Grup talent

# Hitung frekuensi setiap nilai di kolom 'GRUP TALENT'
talent = filtered_data['GRUP TALENT'].value_counts()
label = talent.index

# Membuat pie chart
counts = talent.values
colors = ['gold', 'lightgreen', 'red', 'blue']
fig_talent = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig_talent.update_layout(
    title={
        'text':"<span style='font-weight:normal'>Talent Group</span>",
        'x':0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': 'black'}
        },
    legend={
        'font': {'color': 'black'}
    },
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='black')
    )
fig_talent.update_traces(hoverinfo='label+value',
                         textinfo='percent',
                         textfont=dict(size=20, color='black'),
                         marker=dict(colors=colors, line=dict(color='black', width=2))
                         )

#Graph 4 : Bar Chart Kompetensi

# Hitung frekuensi setiap nilai di kolom 'KOMPETENSI'
filtered_data['KOMPETENSI'] = filtered_data['KOMPETENSI'].replace({"TOC": 'Technical Operation Competency',
                                                                   "EL": 'English Literacy',
                                                                   "BMC": 'Business Management Competency',
                                                                   "BC": 'Behaviour Competency'})
kompetensi = filtered_data['KOMPETENSI'].value_counts()
label = ['Technical Operation<br>Competency', 'Safety', 'Expert', 'English Literacy', 'Business<br>Management<br>Competency', 'Behaviour Competency']
ordered_labels = [label[filtered_data['KOMPETENSI'].value_counts().index.tolist().index(l)] for l in filtered_data['KOMPETENSI'].value_counts().index]
counts = kompetensi.values
colors = ['gold', 'lightgreen', 'red', 'blue', 'purple', 'orange']

# Membuat bar chart
fig_kompetensi = go.Figure(data=[go.Bar(x=ordered_labels,
                                        y=counts,
                                        marker_color=colors)]
                           )

# Mengatur tata letak
fig_kompetensi.update_layout(
    title={
        'text': "<span style='font-weight:normal'>Competency Type</span>",
        'x':0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': 'black'}
    },
    xaxis=dict(tickangle=0,
               tickmode='array',
               tickvals=list(range(len(ordered_labels))),
               ticktext=ordered_labels,
               automargin=True,
               title='Competency Type',
               titlefont=dict(color='black'),
               tickfont=dict(color='black'),
    ),
    yaxis=dict(title='Count',
               titlefont=dict(color='black'),
               tickfont=dict(color='black'),
               showgrid=False
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='black'),
    bargap=0.2
    )

# Menambahkan data label pada setiap batang
fig_kompetensi.update_traces(texttemplate='%{y}', textposition='outside')

# layout graph
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_kompetensi, use_container_width=True)
right_column.plotly_chart(fig_talent, use_container_width=True)

#-----------------------------------------------------------------------------------
