import folium
from flask import render_template

from creating_trip.algorythm_models.trajectory import Trajectory

map_center = (50.0619474, 19.9368564)


def create_map(trajectory: Trajectory) -> folium.Map:
    path = trajectory.get_events()
    m = folium.Map(location=map_center, zoom_start=12)
    if len(path) == 0:
        return m

    total_lat = 0
    total_lon = 0
    for event in path:
        total_lat += event.poi.lat
        total_lon += event.poi.lon
    m = folium.Map(location=(total_lat/len(path), total_lon/len(path)), zoom_start=12)
    
    trail = []
    for i in range(len(path)):
        wiki = None
        if path[i].poi.wiki is not None:
            lang, wiki_art = path[i].poi.wiki.split(':')
            wiki=f"https://{lang}.wikipedia.org/wiki/{wiki_art}"
        folium.Marker(
            location=(path[i].poi.lat, path[i].poi.lon),
            popup=render_template('map/popup.html',
                                  name=path[i].poi.name,
                                  website=path[i].poi.website,
                                  wiki=wiki,
                                  start=path[i].start,
                                  end=path[i].end),
            icon=folium.Icon(color=color(i))
        ).add_to(m)
        trail.append((path[i].poi.lat, path[i].poi.lon))

    if len(trail) > 0:
        folium.PolyLine(trail).add_to(m)

    return m


def color(i):
    if i == 0:
        return "orange"
    else:
        return 'blue'
