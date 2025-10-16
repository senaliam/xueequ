import pandas as pd
from shapely.geometry import Point, Polygon
import json

# 1. 读取小区excel
df = pd.read_excel('深圳小区.xlsx')  # building_name, lat, lon

# 2. 读取学校学区边界
with open('baoan.json', encoding='utf-8') as f:
    data = json.load(f)

school_name = data['school']
coords = [(float(p['lng']), float(p['lat'])) for p in data['polygon']]
poly = Polygon(coords)

# 3. 判断每个小区是否在学区范围内
results = []
covered_buildings=[]
for idx, row in df.iterrows():
    pt = Point(row['lon'], row['lat'])
    if poly.contains(pt):
        covered_buildings.append(row['building_name'])
results.append({
    'school': school_name,
    'building_name': covered_buildings
})
filename = school_name + '-小区.xlsx'
# 4. 输出结果
result_df = pd.DataFrame(results)
result_df.to_excel(filename, index=False)