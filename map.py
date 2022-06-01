import openrouteservice
from openrouteservice import convert
import folium
from streamlit_folium import folium_static

def route_map(df):
    BeginTripLng = (df.get('Begin Trip Lng')).tolist()
    BeginTripLat = (df.get('Begin Trip Lat')).tolist()
    DropoffLng = (df.get('Dropoff Lng')).tolist()
    DropoffLat = (df.get('Dropoff Lat')).tolist()

    long1 = BeginTripLng[0]
    lat1 = BeginTripLat[0]
    long2 = DropoffLng[0]
    lat2 = DropoffLat[0]

    client = openrouteservice.Client(key='5b3ce3597851110001cf6248645f4d57ed9c452685012c0fc4c06df3')

    coords = ((long1,lat1),(long2,lat2))

    res = client.directions(coords)
    geometry = client.directions(coords)['routes'][0]['geometry']
    decoded = convert.decode_polyline(geometry)

    m = folium.Map(location=[lat1,long1],zoom_start=10, control_scale=True,tiles="cartodbpositron")
    folium.GeoJson(decoded).add_child(folium.Popup(max_width=300)).add_to(m)

    folium.Marker(
        location=list(coords[0][::-1]),
        icon=folium.Icon(color="green"),
    ).add_to(m)

    folium.Marker(
        location=list(coords[1][::-1]),
        icon=folium.Icon(color="red"),
    ).add_to(m)

    #m.save('map.html')
    folium_static(m)
    return None



