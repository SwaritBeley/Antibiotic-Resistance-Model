# streamlit run .\Antibiotic-Resistance-Model\website\app.py
import streamlit as st
import streamlit.components.v1 as components

import pandas as pd

filepath = './website/data/output.csv'
antibiotic_df = pd.read_csv(filepath)

def process_input():
  global row
  global chart_data
  
  row = antibiotic_df[
      (antibiotic_df["Bacteria Name"] == bacteria) &
      (antibiotic_df["Antibiotic Name"] == antibiotic)
  ]

  vulnerability_total = float(row['Total Vulnerability'])

  # Go through each factor and create data entries for the chart                            
  factor_columns = [column for column in antibiotic_df.columns if column.endswith(" factor")]
  chart_data = [{ 
                "value": float(row[factor]) / vulnerability_total,
                "name": factor.replace(' factor', '')
                } 
                for factor in factor_columns]

  # Goes through each item in chart data and includes it if the item value is not equal to 0.
  # Did this so it wouldn't show up in the chart
  chart_data = [item for item in chart_data if item["value"] != 0]



st.set_page_config(page_title="Virtual Lab", page_icon="🦠")

st.sidebar.header("Virtual Lab")
st.title("Virtual Lab")

bacteria = st.selectbox(
    "Choose a Bacteria?",
    set(antibiotic_df["Bacteria Name"])
)

antibiotic = st.selectbox("Choose an Antibiotic?", 
    set(antibiotic_df["Antibiotic Name"])
)

process_input()

st.write(bacteria, "is ", float(row['Resistance']), " resistant to ", antibiotic, ".")

# pulled code from echartsapache.org which creates the pie chart
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



