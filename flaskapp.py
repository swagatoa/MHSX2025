from flask  import Flask, render_template, send_from_directory, request, jsonify, send_file
import expensecategorization
import os
import sqlite3
import json
import time
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
import extrapolation
import inference
import numpy
import aisearch

# Connect to the existing database
conn = sqlite3.connect("sales.db", check_same_thread=False)
cursor = conn.cursor()

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
    return {"labels": item_names, "data": revenues}

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
    weeks = [row[0] for row in data]
    revenues = [row[1] for row in data]
    return {"weeks": weeks, "data": revenues}

def demand_by_week():
    # Query count of items sold grouped by year and week number
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            strftime('%Y-%W', date) AS year_week,
            COUNT(*) as items_sold
        FROM sales
        GROUP BY year_week
        ORDER BY year_week
    """)
    data = cursor.fetchall()
    weeks = [row[0] for row in data]
    counts = [row[1] for row in data]
    return {"dates": weeks, "values": counts}

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

#heatmap()

bills = [ "bill1.jpeg","receipt_683b6a2a11720.jpg", "receipt_683b6aa7e0053.jpg"]
expenses_distribution, expenses_weekly, expenditure = expensecategorization.produce_graphs(bills)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('website.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/api/expenses/distribution")
def expensespie():
    global expenses_distribution
    return expenses_distribution

@app.route("/api/expenses/weekly")
def expensesline():
    global expenses_weekly
    return extrapolation.extrapolate(expenses_weekly, 4)["forecast_line"]

@app.route("/api/revenue/distribution")
def revenuepie():
    return pie_chart()

@app.route("/api/revenue/weekly")
def revenueline():
    return extrapolation.extrapolate(revenue_by_week_line_graph(), 4)["forecast_line"]

@app.route("/api/demand")
def demand():
    """
    Returns the number of items sold per week.
    Each row in the 'sales' table is considered one item sold.
    The result is grouped by year-week (e.g., "2025-22"), sorted chronologically.
    """
    return demand_by_week()

@app.route("/api/summary")
def summary():
    global expenditure
    summaryreturn = {
        "may_expenditure": expenditure,
        "june_expenditure_projection": extrapolation.extrapolate(expenses_weekly, 1)["forecast"][-1],
        "june_revenue_projection": extrapolation.extrapolate(revenue_by_week_line_graph(), 1)["forecast"][-1]
    }
    summaryreturn["may_revenue"] = round(sum(pie_chart()["data"]) / 100, 2)
    return summaryreturn

@app.route('/upload_bills', methods=['POST'])
def upload_bills():
    global bills, expenses_distribution, expenses_weekly, expenditure
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files[]')
    bills = []

    for file in files:
        if file.filename == '':
            continue  # Skip files without a name
        filename = file.filename
        file_path = os.path.join(os.getcwd(), filename)
        file.save(file_path)
        bills.append(filename)

    expenses_distribution, expenses_weekly, expenditure = expensecategorization.produce_graphs(bills)

    return jsonify({'message': 'Files uploaded successfully'}), 200

@app.route('/api/projected-sales')
def projected_sales():
    return {
        "labels": ["Product A", "Product B", "Product C", "Product D", "Service X"],
        "data": [12500, 9800, 7400, 6200, 8800]
    }

@app.route("/api/heatmap-image")
def heatmap_image():
    return send_file("revenue_heatmap_nj.png", mimetype="image/png")

@app.route("/api/pricemodel", methods=["POST"])
def pricemodel():
    data = request.get_json()
    week = [float(data['y'][i]) for i in range(len(data['y']))]
    year = 2019
    competitors = float(data['competitors'])
    x = [float(data['x'][i]) for i in range(len(data['x']))]

    print(len(x))

    outputs = inference.run_inference(x, [competitors for i in range(len(x))], [year for i in range(len(x))], week)

    return jsonify({"z":outputs.tolist()})

@app.route('/api/findprice', methods=["POST"])
def findprice():
    data = request.get_json()
    product=data['productdescription']

    return {"price":int(aisearch.complete_search(product))}


if __name__ == '__main__':
    app.static_folder = 'templates'
    app.run(debug=True, port=8080)