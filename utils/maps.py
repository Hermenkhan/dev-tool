import folium

def distance_map(location1, lat1, lon1, location2, lat2, lon2):
    """Return a folium map with markers and line between two locations."""
    m = folium.Map(location=[(lat1+lat2)/2, (lon1+lon2)/2], zoom_start=4)

    folium.Marker([lat1, lon1], tooltip=location1, icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker([lat2, lon2], tooltip=location2, icon=folium.Icon(color="red")).add_to(m)
    folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="green", weight=3).add_to(m)

    return m
