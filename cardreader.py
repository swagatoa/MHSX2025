import sqlite3
import random
from datetime import datetime, timedelta
import json

# Connect to or create the database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Update table schema to include a 'date' column
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    amount_spent REAL NOT NULL,
    location TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

conn.commit()

# Sample data
item_names = [
    "Wireless Bluetooth Headphones",
    "Stainless Steel Water Bottle",
    "USB-C Charging Cable",
    "LED Desk Lamp",
    "Portable Power Bank",
    "Ergonomic Office Chair",
    "Noise-Canceling Earbuds",
    "4K Ultra HD Monitor",
    "Smart Home Thermostat",
    "Mechanical Gaming Keyboard"
]
data = '''
    {"type":"Feature","properties":{"hash":"8b5432914210af1b","number":"5","street":"TROLL LN","unit":"","city":"ROCKAWAY","district":"","region":"NJ","postcode":"07866","id":""},"geometry":{"type":"Point","coordinates":[-74.495841,40.9569259]}}
    {"type":"Feature","properties":{"hash":"574e56298f46fd12","number":"15","street":"LAFAYETTE PL","unit":"","city":"DENVILLE","district":"","region":"NJ","postcode":"07834","id":""},"geometry":{"type":"Point","coordinates":[-74.4865797,40.9032092]}}
    {"type":"Feature","properties":{"hash":"8ba59d23e782817a","number":"78","street":"WOODLAND RD","unit":"","city":"CHATHAM","district":"","region":"NJ","postcode":"07928","id":""},"geometry":{"type":"Point","coordinates":[-74.3974325,40.7435201]}}
    {"type":"Feature","properties":{"hash":"2dbe86b6a05d88e6","number":"55","street":"MOUNTAINSIDE DR","unit":"","city":"RANDOLPH","district":"","region":"NJ","postcode":"07869","id":""},"geometry":{"type":"Point","coordinates":[-74.5430871,40.8653677]}}
    {"type":"Feature","properties":{"hash":"98b1d1d9634f92c3","number":"7","street":"GREEN HILLS RD","unit":"","city":"MENDHAM","district":"","region":"NJ","postcode":"07945","id":""},"geometry":{"type":"Point","coordinates":[-74.5560017,40.7807695]}}
    {"type":"Feature","properties":{"hash":"01be92cd36fa70be","number":"36","street":"MARGARET RD","unit":"","city":"OAK RIDGE","district":"","region":"NJ","postcode":"07438","id":""},"geometry":{"type":"Point","coordinates":[-74.5220726,41.0303787]}}
    {"type":"Feature","properties":{"hash":"d3036db5131acf04","number":"23","street":"COBBLESTONE TER","unit":"","city":"MONTVILLE","district":"","region":"NJ","postcode":"07045","id":""},"geometry":{"type":"Point","coordinates":[-74.3513245,40.9137137]}}
    {"type":"Feature","properties":{"hash":"859f9c519b5f97b9","number":"10","street":"SMITH RD","unit":"","city":"DENVILLE","district":"","region":"NJ","postcode":"07834","id":""},"geometry":{"type":"Point","coordinates":[-74.515303,40.8658638]}}
    {"type":"Feature","properties":{"hash":"22e27c87c6b69d8c","number":"15","street":"STARLING RD","unit":"","city":"RANDOLPH","district":"","region":"NJ","postcode":"07869","id":""},"geometry":{"type":"Point","coordinates":[-74.5600009,40.8593071]}}
    {"type":"Feature","properties":{"hash":"b40a3f61720af309","number":"11","street":"LUDLOW ST","unit":"","city":"WHARTON","district":"","region":"NJ","postcode":"07885","id":""},"geometry":{"type":"Point","coordinates":[-74.589448,40.9317159]}}
    {"type":"Feature","properties":{"hash":"c513363d43c2cf92","number":"1","street":"GARWOOD TRL","unit":"","city":"DENVILLE","district":"","region":"NJ","postcode":"07834","id":""},"geometry":{"type":"Point","coordinates":[-74.4678182,40.8909779]}}
    {"type":"Feature","properties":{"hash":"a08fd84984066301","number":"68","street":"TAYLORTOWN RD","unit":"","city":"MONTVILLE","district":"","region":"NJ","postcode":"07045","id":""},"geometry":{"type":"Point","coordinates":[-74.3873823,40.9260533]}}
    {"type":"Feature","properties":{"hash":"e24b0547808f8e41","number":"17","street":"WOOD CHASE LN","unit":"","city":"BUTLER","district":"","region":"NJ","postcode":"07405","id":""},"geometry":{"type":"Point","coordinates":[-74.3617744,40.9627613]}}
    {"type":"Feature","properties":{"hash":"2331b22de55fd263","number":"44","street":"BERLIN RD","unit":"","city":"PARSIPPANY","district":"","region":"NJ","postcode":"07054","id":""},"geometry":{"type":"Point","coordinates":[-74.4351279,40.8571771]}}
    {"type":"Feature","properties":{"hash":"a12af36186fa3694","number":"14","street":"STRUBLE AVE","unit":"","city":"BUTLER","district":"","region":"NJ","postcode":"07405","id":""},"geometry":{"type":"Point","coordinates":[-74.3327577,40.9962113]}}
    {"type":"Feature","properties":{"hash":"f7b54ae347b4d3aa","number":"20","street":"PINE ST","unit":"","city":"MORRISTOWN","district":"","region":"NJ","postcode":"07960","id":""},"geometry":{"type":"Point","coordinates":[-74.4781316,40.7953496]}}
    {"type":"Feature","properties":{"hash":"d1ba62e6a7a58f86","number":"31","street":"DARTMOOR RD","unit":"","city":"EAST HANOVER","district":"","region":"NJ","postcode":"07936","id":""},"geometry":{"type":"Point","coordinates":[-74.3377514,40.8195236]}}
    {"type":"Feature","properties":{"hash":"a95a501a596978d5","number":"6","street":"RIVERSIDE DR","unit":"","city":"PEQUANNOCK","district":"","region":"NJ","postcode":"07440","id":""},"geometry":{"type":"Point","coordinates":[-74.2804455,40.9433379]}}
    {"type":"Feature","properties":{"hash":"a109cda2eaa1fba5","number":"1","street":"EAGLE ROCK VLG","unit":"APT 6A","city":"BUDD LAKE","district":"","region":"NJ","postcode":"07828","id":""},"geometry":{"type":"Point","coordinates":[-74.7530068,40.8599496]}}
    {"type":"Feature","properties":{"hash":"d1ec102351b35e18","number":"11","street":"ALEXANDER AVE","unit":"","city":"MADISON","district":"","region":"NJ","postcode":"07940","id":""},"geometry":{"type":"Point","coordinates":[-74.4103848,40.7570735]}}
    {"type":"Feature","properties":{"hash":"207606b88c8ac70a","number":"42","street":"ROSWELL ST","unit":"","city":"DOVER","district":"","region":"NJ","postcode":"07801","id":""},"geometry":{"type":"Point","coordinates":[-74.5589556,40.8931253]}},
    {"type":"Feature","properties":{"id":"","unit":"","number":"611","street":"SUNSET BLVD","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"e0cdb93ecd0d4798"},"geometry":{"type":"Point","coordinates":[-74.9437831,38.9385348]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"137","street":"ELDREDGE AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"6fab874d36b540f1"},"geometry":{"type":"Point","coordinates":[-74.9284121,38.9384896]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"431","street":"2ND AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"32ba5269dbc839f6"},"geometry":{"type":"Point","coordinates":[-74.939216,38.9385614]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"129","street":"ELDREDGE AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"0fcf7cc17dbf4d23"},"geometry":{"type":"Point","coordinates":[-74.9287385,38.938603]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"168","street":"STEVENS ST","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"00f15ced974e4ce2"},"geometry":{"type":"Point","coordinates":[-74.9462597,38.9471048]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"400","street":"STEVENS ST","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"bfa3b7dda3d2498c"},"geometry":{"type":"Point","coordinates":[-74.9430191,38.9473942]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"701","street":"GRAND AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"ae0c6cfb8a6539d2"},"geometry":{"type":"Point","coordinates":[-74.9286726,38.942374]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"290","street":"6TH AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"ac2c9caac04f4e98"},"geometry":{"type":"Point","coordinates":[-74.9354932,38.9422153]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"131","street":"EMERALD AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"4f30706acce64bc8"},"geometry":{"type":"Point","coordinates":[-74.9289234,38.9378302]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"117","street":"EMERALD AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"b5b83e97c83f61f6"},"geometry":{"type":"Point","coordinates":[-74.9293726,38.9378462]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"123","street":"EMERALD AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"b3599337a859da65"},"geometry":{"type":"Point","coordinates":[-74.9292233,38.9378363]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"218","street":"3RD AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"237e2d31f4c3a1e1"},"geometry":{"type":"Point","coordinates":[-74.9339845,38.9378767]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"418","street":"2ND AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"52cda9108aaa369c"},"geometry":{"type":"Point","coordinates":[-74.9384258,38.9377746]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"135","street":"EMERALD AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"43ef129a4c14c1cd"},"geometry":{"type":"Point","coordinates":[-74.9287818,38.9378051]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"409","street":"BROADWAY","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"c18f9a4910c3fa20"},"geometry":{"type":"Point","coordinates":[-74.929816,38.9379353]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"131","street":"3RD AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"1bb951359bc3ce2a"},"geometry":{"type":"Point","coordinates":[-74.9315673,38.937798]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"317","street":"2ND AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"a03d85514418c48e"},"geometry":{"type":"Point","coordinates":[-74.9360043,38.9377554]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"414","street":"PARK BLVD","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"b19e1af95a855a3b"},"geometry":{"type":"Point","coordinates":[-74.9283396,38.9378611]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"137","street":"EMERALD AVE","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"080660a40757ff28"},"geometry":{"type":"Point","coordinates":[-74.9286187,38.937784]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"","street":"BAYSHORE RD","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"6952a2c7d32e78fd"},"geometry":{"type":"Point","coordinates":[-74.9387582,38.9458191]}}
    {"type":"Feature","properties":{"id":"","unit":"","number":"925","street":"FARMDALE DR","city":"WEST CAPE MAY","district":"","region":"","postcode":"","hash":"f02c8cab94cac5f4"},"geometry":{"type":"Point","coordinates":[-74.929215,38.9454159]}}
    {"type":"Feature","properties":{"hash":"10f59cffaa90863a","number":"16","street":"VICKSBURG COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2221752,40.2148701]}}
    {"type":"Feature","properties":{"hash":"4c664f80bbb61e07","number":"5","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2208997,40.2114969]}}
    {"type":"Feature","properties":{"hash":"6cc47c0e530624af","number":"2","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2198844,40.2108065]}}
    {"type":"Feature","properties":{"hash":"424ffdf2fadf9371","number":"4","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2205923,40.2107996]}}
    {"type":"Feature","properties":{"hash":"6519eafe2935a10f","number":"6","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2212249,40.210609]}}
    {"type":"Feature","properties":{"hash":"d3b5f858e9060dfc","number":"8","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2216472,40.2101917]}}
    {"type":"Feature","properties":{"hash":"4e695d38b4f1a818","number":"245","street":"FAIRFIELD ROAD","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2193987,40.2096165]}}
    {"type":"Feature","properties":{"hash":"cca1b1a1bf053674","number":"249","street":"FAIRFIELD ROAD","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2192087,40.210028]}}
    {"type":"Feature","properties":{"hash":"4239d8a7bdba07f4","number":"14","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2238755,40.2105049]}}
    {"type":"Feature","properties":{"hash":"7a32997d4907e563","number":"12","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2230974,40.2103496]}}
    {"type":"Feature","properties":{"hash":"2875ef6c699d7c1c","number":"16","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2244215,40.2106823]}}
    {"type":"Feature","properties":{"hash":"6d1c152be8f93afe","number":"18","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2244089,40.2113377]}}
    {"type":"Feature","properties":{"hash":"b0fa3b0e7da86ae4","number":"20","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2244368,40.2117796]}}
    {"type":"Feature","properties":{"hash":"2218235931c2f7f3","number":"22","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2244616,40.2122154]}}
    {"type":"Feature","properties":{"hash":"96d82dd479915c42","number":"24","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2244835,40.2125992]}}
    {"type":"Feature","properties":{"hash":"2cc1273b4a2a9f32","number":"28","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2245316,40.213588]}}
    {"type":"Feature","properties":{"hash":"de68e4ffab1c80c9","number":"30","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2244678,40.2140548]}}
    {"type":"Feature","properties":{"hash":"c5ea42b1cc01afac","number":"32","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2239972,40.2147345]}}
    {"type":"Feature","properties":{"hash":"e089a93255b348ed","number":"","street":"VICKSBURG COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2234379,40.2159954]}}
    {"type":"Feature","properties":{"hash":"bd83494cc09fba72","number":"31","street":"POTOMAC COURT","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2230204,40.2145097]}}
    {"type":"Feature","properties":{"hash":"75dfb63c15f4231d","number":"2","street":"RALEIGH WAY","unit":"","city":"","district":"","region":"","postcode":"","id":""},"geometry":{"type":"Point","coordinates":[-74.2222719,40.2110168]}}
    {"type":"Feature","properties":{"hash":"8b5432914210af1b","number":"5","street":"TROLL LN","unit":"","city":"ROCKAWAY","district":"","region":"NJ","postcode":"07866","id":""},"geometry":{"type":"Point","coordinates":[-74.495841,40.9569259]}}
    {"type":"Feature","properties":{"hash":"574e56298f46fd12","number":"15","street":"LAFAYETTE PL","unit":"","city":"DENVILLE","district":"","region":"NJ","postcode":"07834","id":""},"geometry":{"type":"Point","coordinates":[-74.4865797,40.9032092]}}
    {"type":"Feature","properties":{"hash":"8ba59d23e782817a","number":"78","street":"WOODLAND RD","unit":"","city":"CHATHAM","district":"","region":"NJ","postcode":"07928","id":""},"geometry":{"type":"Point","coordinates":[-74.3974325,40.7435201]}}
    {"type":"Feature","properties":{"hash":"2dbe86b6a05d88e6","number":"55","street":"MOUNTAINSIDE DR","unit":"","city":"RANDOLPH","district":"","region":"NJ","postcode":"07869","id":""},"geometry":{"type":"Point","coordinates":[-74.5430871,40.8653677]}}
    {"type":"Feature","properties":{"hash":"98b1d1d9634f92c3","number":"7","street":"GREEN HILLS RD","unit":"","city":"MENDHAM","district":"","region":"NJ","postcode":"07945","id":""},"geometry":{"type":"Point","coordinates":[-74.5560017,40.7807695]}}
    {"type":"Feature","properties":{"hash":"01be92cd36fa70be","number":"36","street":"MARGARET RD","unit":"","city":"OAK RIDGE","district":"","region":"NJ","postcode":"07438","id":""},"geometry":{"type":"Point","coordinates":[-74.5220726,41.0303787]}}
    {"type":"Feature","properties":{"hash":"d3036db5131acf04","number":"23","street":"COBBLESTONE TER","unit":"","city":"MONTVILLE","district":"","region":"NJ","postcode":"07045","id":""},"geometry":{"type":"Point","coordinates":[-74.3513245,40.9137137]}}
    {"type":"Feature","properties":{"hash":"859f9c519b5f97b9","number":"10","street":"SMITH RD","unit":"","city":"DENVILLE","district":"","region":"NJ","postcode":"07834","id":""},"geometry":{"type":"Point","coordinates":[-74.515303,40.8658638]}}
    {"type":"Feature","properties":{"hash":"22e27c87c6b69d8c","number":"15","street":"STARLING RD","unit":"","city":"RANDOLPH","district":"","region":"NJ","postcode":"07869","id":""},"geometry":{"type":"Point","coordinates":[-74.5600009,40.8593071]}}
    {"type":"Feature","properties":{"hash":"b40a3f61720af309","number":"11","street":"LUDLOW ST","unit":"","city":"WHARTON","district":"","region":"NJ","postcode":"07885","id":""},"geometry":{"type":"Point","coordinates":[-74.589448,40.9317159]}}
    {"type":"Feature","properties":{"hash":"c513363d43c2cf92","number":"1","street":"GARWOOD TRL","unit":"","city":"DENVILLE","district":"","region":"NJ","postcode":"07834","id":""},"geometry":{"type":"Point","coordinates":[-74.4678182,40.8909779]}}
    {"type":"Feature","properties":{"hash":"a08fd84984066301","number":"68","street":"TAYLORTOWN RD","unit":"","city":"MONTVILLE","district":"","region":"NJ","postcode":"07045","id":""},"geometry":{"type":"Point","coordinates":[-74.3873823,40.9260533]}}
    {"type":"Feature","properties":{"hash":"e24b0547808f8e41","number":"17","street":"WOOD CHASE LN","unit":"","city":"BUTLER","district":"","region":"NJ","postcode":"07405","id":""},"geometry":{"type":"Point","coordinates":[-74.3617744,40.9627613]}}
    {"type":"Feature","properties":{"hash":"2331b22de55fd263","number":"44","street":"BERLIN RD","unit":"","city":"PARSIPPANY","district":"","region":"NJ","postcode":"07054","id":""},"geometry":{"type":"Point","coordinates":[-74.4351279,40.8571771]}}
    {"type":"Feature","properties":{"hash":"a12af36186fa3694","number":"14","street":"STRUBLE AVE","unit":"","city":"BUTLER","district":"","region":"NJ","postcode":"07405","id":""},"geometry":{"type":"Point","coordinates":[-74.3327577,40.9962113]}}
    {"type":"Feature","properties":{"hash":"f7b54ae347b4d3aa","number":"20","street":"PINE ST","unit":"","city":"MORRISTOWN","district":"","region":"NJ","postcode":"07960","id":""},"geometry":{"type":"Point","coordinates":[-74.4781316,40.7953496]}}
    {"type":"Feature","properties":{"hash":"d1ba62e6a7a58f86","number":"31","street":"DARTMOOR RD","unit":"","city":"EAST HANOVER","district":"","region":"NJ","postcode":"07936","id":""},"geometry":{"type":"Point","coordinates":[-74.3377514,40.8195236]}}
    {"type":"Feature","properties":{"hash":"a95a501a596978d5","number":"6","street":"RIVERSIDE DR","unit":"","city":"PEQUANNOCK","district":"","region":"NJ","postcode":"07440","id":""},"geometry":{"type":"Point","coordinates":[-74.2804455,40.9433379]}}
    {"type":"Feature","properties":{"hash":"a109cda2eaa1fba5","number":"1","street":"EAGLE ROCK VLG","unit":"APT 6A","city":"BUDD LAKE","district":"","region":"NJ","postcode":"07828","id":""},"geometry":{"type":"Point","coordinates":[-74.7530068,40.8599496]}}
    {"type":"Feature","properties":{"hash":"d1ec102351b35e18","number":"11","street":"ALEXANDER AVE","unit":"","city":"MADISON","district":"","region":"NJ","postcode":"07940","id":""},"geometry":{"type":"Point","coordinates":[-74.4103848,40.7570735]}}
    {"type":"Feature","properties":{"hash":"207606b88c8ac70a","number":"42","street":"ROSWELL ST","unit":"","city":"DOVER","district":"","region":"NJ","postcode":"07801","id":""},"geometry":{"type":"Point","coordinates":[-74.5589556,40.8931253]}}
    {"type":"Feature","properties":{"hash":"56f9d9a8aeef8d5b","number":"16","street":"Davis Rd","unit":"","city":"Frankford Township","district":"","region":"","postcode":"","id":"1905-35-1.02"},"geometry":{"type":"Point","coordinates":[-74.6786391,41.1696642]}}
    {"type":"Feature","properties":{"h`ash":"2e5b638902fe3345","number":"59","street":"Rt 206","unit":"","city":"Byram Township","district":"","region":"","postcode":"","id":"1904-34-17"},"geometry":{"type":"Point","coordinates":[-74.7189175,40.9297399]}}
    {"type":"Feature","properties":{"hash":"41b57c1d25fa6b47","number":"228","street":"Rt 206","unit":"","city":"Byram Township","district":"","region":"","postcode":"","id":"1904-219-6"},"geometry":{"type":"Point","coordinates":[-74.7326591,40.9495312]}}
    {"type":"Feature","properties":{"hash":"58a107347887db1d","number":"38","street":"File Rd","unit":"","city":"Wantage Township","district":"","region":"","postcode":"","id":"1924-155-3.05"},"geometry":{"type":"Point","coordinates":[-74.6729555,41.2554114]}}
    {"type":"Feature","properties":{"hash":"cfdc6e40c5806742","number":"84","street":"Sparta Ave","unit":"","city":"Sparta Township","district":"","region":"","postcode":"","id":"1918-516-3"},"geometry":{"type":"Point","coordinates":[-74.6442922,41.0391796]}}
    {"type":"Feature","properties":{"hash":"199fb688b26d52e0","number":"34","street":"Main St","unit":"","city":"Stanhope Borough","district":"","region":"","postcode":"","id":"1919-11203-8"},"geometry":{"type":"Point","coordinates":[-74.7081089,40.9023123]}}
    {"type":"Feature","properties":{"hash":"1d6c11272b424c16","number":"352","street":"Maxim Dr","unit":"","city":"Hopatcong Borough","district":"","region":"","postcode":"","id":"1912-41102-4"},"geometry":{"type":"Point","coordinates":[-74.6591113,40.955483]}}
    {"type":"Feature","properties":{"hash":"ad28c526c4760ccf","number":"350","street":"Maxim Dr","unit":"","city":"Hopatcong Borough","district":"","region":"","postcode":"","id":"1912-41102-3"},"geometry":{"type":"Point","coordinates":[-74.6588816,40.9556292]}}
    {"type":"Feature","properties":{"hash":"c7fcdbd49ffbd39a","number":"362","street":"Maxim Dr","unit":"","city":"Hopatcong Borough","district":"","region":"","postcode":"","id":"1912-41102-9"},"geometry":{"type":"Point","coordinates":[-74.6596781,40.9551277]}}
    {"type":"Feature","properties":{"hash":"2267163182d765db","number":"358","street":"Maxim Dr","unit":"","city":"Hopatcong Borough","district":"","region":"","postcode":"","id":"1912-41102-7"},"geometry":{"type":"Point","coordinates":[-74.6595218,40.9552208]}}
    {"type":"Feature","properties":{"hash":"c3831df17b0374ca","number":"44","street":"Main St","unit":"","city":"Stanhope Borough","district":"","region":"","postcode":"","id":"1919-11203-6"},"geometry":{"type":"Point","coordinates":[-74.7083474,40.9023956]}}
    {"type":"Feature","properties":{"hash":"2c766cf5f4ee2e6e","number":"7","street":"First St","unit":"","city":"Sussex Borough","district":"","region":"","postcode":"","id":"1921-505-21.01"},"geometry":{"type":"Point","coordinates":[-74.603975,41.2093964]}}
    {"type":"Feature","properties":{"hash":"9c575a05cb2dd347","number":"348","street":"Maxim Dr","unit":"","city":"Hopatcong Borough","district":"","region":"","postcode":"","id":"1912-41102-28"},"geometry":{"type":"Point","coordinates":[-74.6587955,40.9558766]}}
    {"type":"Feature","properties":{"hash":"79aced25c2e6508f","number":"4","street":"Division Ln","unit":"","city":"Hopatcong Borough","district":"","region":"","postcode":"","id":"1912-41102-2"},"geometry":{"type":"Point","coordinates":[-74.658518,40.9557784]}}
    {"type":"Feature","properties":{"hash":"edf71ad0665d5545","number":"125","street":"Hillside Dr","unit":"","city":"Andover Township","district":"","region":"","postcode":"","id":"1902-87-4"},"geometry":{"type":"Point","coordinates":[-74.7087066,41.0297503]}}
    {"type":"Feature","properties":{"hash":"2c9467270ca82a81","number":"22","street":"The Rotunda","unit":"","city":"Byram Township","district":"","region":"","postcode":"","id":"1904-280-508"},"geometry":{"type":"Point","coordinates":[-74.7209724,40.9756421]}}
    {"type":"Feature","properties":{"hash":"41be950465b1295c","number":"3","street":"Wantage Ave","unit":"","city":"Branchville Borough","district":"","region":"","postcode":"","id":"1903-203-13"},"geometry":{"type":"Point","coordinates":[-74.7519414,41.1469403]}}
    {"type":"Feature","properties":{"hash":"6b1ceffc59ffc415","number":"16","street":"Liberty Trl","unit":"","city":"Andover Township","district":"","region":"","postcode":"","id":"1902-69-4.09"},"geometry":{"type":"Point","coordinates":[-74.7008672,41.0097657]}}
    {"type":"Feature","properties":{"hash":"84c1fef522387548","number":"38","street":"Sharp Rd","unit":"","city":"Frankford Township","district":"","region":"","postcode":"","id":"1905-56-9"},"geometry":{"type":"Point","coordinates":[-74.7660657,41.1429259]}}
    {"type":"Feature","properties":{"hash":"c435361cf4aa1c46","number":"1","street":"Ascot Ln","unit":"","city":"Byram Township","district":"","region":"","postcode":"","id":"1904-337.10-32.02"},"geometry":{"type":"Point","coordinates":[-74.6616698,40.9916069]}}
    {"type":"Feature","properties":{"hash":"9cd70964ffd2f5e0","number":"66","street":"Wantage Ave","unit":"","city":"Frankford Township","district":"","region":"","postcode":"","id":"1905-24-1.01"},"geometry":{"type":"Point","coordinates":[-74.7428656,41.1545887]}}
'''
features = []
for line in data.splitlines():
    line = line.rstrip(", \t")             # trim spaces + trailing comma
    if line:                               # ignore blank lines
        features.append(json.loads(line))

print(f"Loaded {len(features)} features.")

# ---------------------------------------------------------------------------
# 3)  Build nicely formatted address strings
# ---------------------------------------------------------------------------
def pretty_addr(f):
    p = f["properties"]
    unit = (p["unit"] + ", ") if p.get("unit") else ""
    region = f' {p["region"]}' if p["region"] else ""
    postcode = f' {p["postcode"]}' if p["postcode"] else ""
    return f'{p["number"]} {p["street"]}, {unit}{p["city"]}{region}{postcode}'

addresses = [pretty_addr(f) for f in features]
# Generate a random date within the last year
def random_date():
    start_date = datetime.now() - timedelta(days=365)
    while True:
        random_days = random.randint(0, 365)
        date = start_date + timedelta(days=random_days)
        if date.weekday() == 0:  # Monday
            return date.strftime('%Y-%m-%d')

# Insert a single record
def add_card(item_name, amount_spent, location, date):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sales (item_name, amount_spent, location, date)
        VALUES (?, ?, ?, ?)
    """, (item_name, amount_spent, location, date))
    conn.commit()

# Generate many random records
def generate_large_dataset(n=1000):
    for _ in range(n):
        item_name = random.choice(item_names)
        amount_spent = round(random.uniform(5.0, 500.0), 2)
        location = random.choice(addresses)
        date = random_date()
        add_card(item_name, amount_spent, location, date)

# Main
if __name__ == "__main__":
    generate_large_dataset()