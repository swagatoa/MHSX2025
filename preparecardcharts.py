import sqlite3
import json
import time
import os
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt

# Connect to the existing database
conn = sqlite3.connect("sales.db")


def pie_chart():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT item_name, SUM(amount_spent) as total_revenue
        FROM sales
        GROUP BY item_name
    """)

    data = cursor.fetchall()
    item_names = [row[0] for row in data]
    revenues = [row[1] for row in data]
    return {"labels":item_names,"data":revenues}

def revenue_by_week_line_graph():
    cursor = conn.cursor()
    # Query total revenue grouped by year and week number
    cursor.execute("""
        SELECT 
            strftime('%Y-%W', date) AS year_week,
            SUM(amount_spent) as total_revenue
        FROM sales
        GROUP BY year_week
        ORDER BY year_week
    """)

    data = cursor.fetchall()
    
    # Extract weeks and revenues
    weeks = [row[0] for row in data]
    revenues = [row[1] for row in data]
    return {"weeks":weeks,"data":revenues}

def heatmap():
    # Load geocode cache
    cache_file = "geocode_cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            geocode_cache = json.load(f)
    else:
        geocode_cache = {}
    cursor = conn.cursor()
    # Aggregate revenue by location
    cursor.execute("""
        SELECT location, SUM(amount_spent) as total_revenue
        FROM sales
        GROUP BY location
    """)
    location_revenues = cursor.fetchall()

    # Initialize geolocator
    geolocator = Nominatim(user_agent="sales_heatmap_app")

    coords = []
    for loc, revenue in location_revenues:
        if loc in geocode_cache:
            lat, lon = geocode_cache[loc]
        else:
            try:
                location = geolocator.geocode(loc)
                if location:
                    lat, lon = location.latitude, location.longitude
                    geocode_cache[loc] = (lat, lon)
                    with open(cache_file, "w") as f:
                        json.dump(geocode_cache, f)
                    time.sleep(1)
                else:
                    print(f"Could not geocode: {loc}")
                    continue
            except Exception as e:
                print(f"Error geocoding {loc}: {e}")
                continue
        coords.append([lat, lon, revenue])

    # Create folium map centered on New Jersey
    nj_center = [40.0583, -74.4057]  # Approximate geographic center of NJ
    m = folium.Map(location=nj_center, zoom_start=8)

    # Add heatmap
    HeatMap(coords, radius=25, max_zoom=13).add_to(m)

    # Save map to HTML temporarily
    temp_html = "temp_heatmap.html"
    m.save(temp_html)

    # Use Selenium to open HTML and save PNG screenshot
    def save_map_as_png(html_path, png_path):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1200,800")
        chrome_options.add_argument("--hide-scrollbars")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"file://{os.path.abspath(html_path)}")
        time.sleep(3)  # wait for map to load
        driver.save_screenshot(png_path)
        driver.quit()

    output_png = "revenue_heatmap_nj.png"
    save_map_as_png(temp_html, output_png)
    print(f"Heatmap saved as PNG: {output_png}")

    # Optionally delete the temporary HTML file
    os.remove(temp_html)

if __name__ == "__main__":
    pie_chart()
    revenue_by_week_line_graph()
    heatmap()