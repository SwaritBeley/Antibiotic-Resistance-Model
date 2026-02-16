# streamlit run .\Antibiotic-Resistance-Model\website\app.py
import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
filepath = './website/output.csv'
antibiotic_df = pd.read_csv(filepath)

st.title("Virtual Lab")
bacteria = st.selectbox(
    "Choose a Bacteria?",
    ("Mycoplasma", 
     "Escherichia coli", 
     "Pseudomonas aeruginosa", 
     "Klebsiella pneumoniae", 
     "Salmonella enterica", 
     "Acinetobacter baumannii", 
     "Neisseria gonorrhoeae", 
     "Enterococcus faecium", 
     "Enterobacter cloacae", 
     "Serratia marcescens"),
)

antibiotic = st.selectbox("Choose an Antibiotic?", 
                          ("Penicillins",
                           "Vancomycins",
                           "Carbapenems",
                           "Cephalosporins",
                           "Aminoglycosides",
                           "Macrolides",
                           "Fluoroquinolones",
                           "Tetracyclines"
))

row = antibiotic_df[
    (antibiotic_df["Bacteria Name"] == bacteria) &
    (antibiotic_df["Antibiotic Name"] == antibiotic)
]

st.write(bacteria, "is ", float(row['Resistance']), " resistant to ", antibiotic, ".")
name1 = "bacteria"
chart_data = [
    {"value": round(float(row['cell wall factor']) / float(row['Total Vulnerability']), 2) * 100, "name": "cell wall"},
    {"value": round(float(row['multidrug efflux pump factor']) / float(row['Total Vulnerability']), 2) * 100 , "name": "multidrug efflux pump"},
    {"value": round(float(row['hydrolysis factor']) / float(row['Total Vulnerability']), 2) * 100, "name": "hydrolysis"},
    {"value": round(float(row['porin loss factor']) / float(row['Total Vulnerability']), 2) * 100, "name": "porin loss"},
    {"value": round(float(row['porin mutation factor']) / float(row['Total Vulnerability']), 2) * 100, "name": "porin mutation"},
    {"value": round(float(row['PBP modification factor']) / float(row['Total Vulnerability']), 2) * 100, "name": "PBP modification"},
    {"value": round(float(row['ribosomal methylation factor']) / float(row['Total Vulnerability']), 2) * 100, "name": "ribosomal methylation"},
    {"value": round(float(row['biofilm protection factor']) / float(row['Total Vulnerability']), 2) * 100, "name": "biofilm protection"}
]


chart_data = [item for item in chart_data if item["value"] != 0]

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
</head>
<body>

<div id="main" style="width: 100%; height: 400px;"></div>

<script>

var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom, 'dark');
var option;

option = {{
  title: {{
  text: 'Antibiotic Resistance Percentage by Mechanism',
  left: 'center',
  padding: 20
  }},
  tooltip: {{
    trigger: 'item',
    formatter: '{{d}}%'
  }},
  legend: {{
    top: '5%',
    left: 'center',
    padding: 30
  }},
  series: [
    {{
      name: '',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      top: 50,
      itemStyle: {{
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 0
      }},
      label: {{
        show: false,
        position: 'center'
      }},
      emphasis: {{
        label: {{
          show: true,
          fontSize: 40,
          fontWeight: 'bold'
        }}
      }},
      labelLine: {{
        show: false
      }},
      data: {chart_data}
      
    }}
  ]
}};

option && myChart.setOption(option);

</script>

</body>
</html>
"""
components.html(html_code, height=450)



