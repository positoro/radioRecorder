import pandas as pd
import localModuleForMinpou

table = pd.read_csv(localModuleForMinpou.TABLE_FILE)

table_NHK_R1 = table[table['station_id'] == 'JOAK']
table_NHK_FM = table[table['station_id'] == 'JOAK-FM']

table_title_keywords = [
  'ニュース',
]

table_MINPOU = pd.DataFrame()

for keyword in table_title_keywords:
  table_MINPOU = pd.concat([table_MINPOU, table[table['title'].str.contains(keyword)]])

selected_results = pd.concat([
  table_NHK_R1,
  table_NHK_FM,
  table_MINPOU,
])

selected_results.to_csv(localModuleForMinpou.TABLE_FILE, index=None)
