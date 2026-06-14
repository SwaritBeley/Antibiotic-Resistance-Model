import streamlit as st
import streamlit.components.v1 as components

import pandas as pd

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

formula_model_filepath = BASE_DIR / 'data set' / 'supertable.csv'
formula_model_df = pd.read_csv(formula_model_filepath)

predictive_model_filepath = BASE_DIR / 'data set' / 'predictions.csv'
predictive_model_df = pd.read_csv(predictive_model_filepath)

# Setting up data for the piechart
def process_input():
  global formula_model_row
  global predictive_model_row
  global chart_data
  
  # Pulls from bacteria and antibiotic name for dropdown
  formula_model_row = formula_model_df[
      (formula_model_df["Bacteria Name"] == bacteria) &
      (formula_model_df["Antibiotic Name"] == antibiotic)
  ]

  predictive_model_row = predictive_model_df[
      (predictive_model_df["bacterium"] == bacteria) &
      (predictive_model_df["antibiotic"] == antibiotic)
  ]

  vulnerability_total = float(formula_model_row['Total Vulnerability'])

  # Go through each factor and create data entries for the chart                            
  factor_columns = [column for column in formula_model_df.columns if column.endswith(" factor")]
  chart_data = [{ 
                "value": float(formula_model_row[factor]) / vulnerability_total,
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
    sorted(set(formula_model_df["Bacteria Name"]))
)

antibiotic = st.selectbox("Choose an Antibiotic?", 
    sorted(set(formula_model_df["Antibiotic Name"]))
)

process_input()

st.write('Formula-based Prediction: ', float(formula_model_row['Resistance']))

st.write('Predictive Model Prediction: ', float(predictive_model_row['predicted']))

if pd.isna(predictive_model_row['observed'].values[0]):
  st.write('No comparative data provided from ATLAS')
else:
  st.write('Observed (real) Value: ', float(predictive_model_row['observed']))

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



