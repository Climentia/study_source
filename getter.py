# 陰影図に各PVの情報や円を追加
import pandas as pd
import folium

# 持っている全てのPVのidを追加
df = pd.read_csv('./id_all_data.csv', encoding='cp932')
# locationの地点を中心として国土地理院の陰影起伏図をダウンロード
folium_map = folium.Map(location=[35.78, 140.04], zoom_start=9, tiles='https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png', attr='国土地理院 陰影起伏図')
# 円を追加(65km)
folium.Circle(
    location=[35.78, 140.04],
    radius=65000,
    color='#3186cc',
    fill_color='#3186cc'
).add_to(folium_map)
# 円を追加(15km)
folium.Circle(
    location=[35.78, 140.04],
    radius=15000,
    color='#9ACD32',
    fill_color='#9ACD32'
).add_to(folium_map)
folium.CircleMarker(location=[35.78, 140.04],
                    popup='選定地点',
                    icon=folium.Icon(color='black'),
                    radius=1,
                    fill=True,
                    fill_color='black',
                    color='black'
                    ).add_to(folium_map)
for i, row in df.iterrows():
    folium.CircleMarker(location=[row['id_lat'], row['id_lng']],
                        popup=row['id'],
                        icon=folium.Icon(color='red'),
                        radius=1,
                        fill=True,
                        fill_color='#FF4500',
                        color='#FF4500'
                        ).add_to(folium_map)
folium_map.save("pv_point.html")
