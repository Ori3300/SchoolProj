import plotly.express as px

fig = px.scatter_mapbox(
    lat=[37.7749],
    lon=[-122.4194],
    text=["Sample Location"],
    zoom=12,
    height=500
)

fig.update_layout(
    mapbox_style="mapbox://styles/mapbox/streets-v11",
    mapbox_accesstoken=MAPBOX_ACCESS_TOKEN
)

fig.show()


print("Suiiiii")