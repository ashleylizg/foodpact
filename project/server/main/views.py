# project/server/main/views.py


from flask import Blueprint, render_template, request
from geopy import distance
from os import path

import geopy as gp
import numpy as np
import pandas as pd


# TODO move all this stuff out of views.py because it really doesn't belong here

def htmlify(string):
    return '<div class="row"><p>' + string + '</p></div>'

def tons_to_gallons(x):
    return(x * 264.17)

def tons_to_liters(x):
    return(x * 1000)

def divider(x):
    return(x/2000)

def get_environmental_prose(food_purchase_city, food_origin_country, food_name):
    """
    Takes a food's origin and purchase locations, plus its name, then outputs
    HTML-formatted words about the environmental impact of this process.
    """
    output_string = ''
    # food_name i.e. 'grapes'
    output_string += htmlify('Food is ' + food_name)
    user_food = water_use[(water_use['food'] == food_name)]
    # food_origin_country i.e. 'Mexico'
    output_string += htmlify('Originated from ' + food_origin_country)
    user_food_origin = country_location[(country_location['country'] == food_origin_country)]
    # food_purchase_city i.e. 'Syracuse, NY'
    output_string += htmlify('Purchased in ' + food_purchase_city)
    user_city = us_city_location[(us_city_location['city'] == food_purchase_city)]
    # FIXME snag lat/lng for city and food origin to calculate
    newport_ri = (41.49008, -71.312796)
    cleveland_oh = (41.499498, -81.695391)
    dist_btw = distance.great_circle(newport_ri, cleveland_oh).miles
    output_string += htmlify('Your food travelled approximately ' + str(dist_btw) + ' miles.')
    # values to multiply by great circle mile calculation
    # ocean transport for refrigerated/temperature sensitive goods. Units = grams of CO2 per TEU kilometer (volume)
    # reefer value multiplied by 0.621371 to get how many grams per mile
    reefer = 941 * (0.621371)
    # rail transport in grams of CO2 per TEU mile
    rail = 292.8
    # truck transport in grams of CO2 per TEU mile
    truck = 597.4
    # carbon emissions estimate for all transportation types
    ghg_reefer = dist_btw * reefer
    ghg_rail = dist_btw * rail
    ghg_truck = dist_btw * truck
    output_string += htmlify('Carbon dioxide emissions are between: ' + str(ghg_rail) \
                                            + ',' + str(ghg_reefer) + ', and ' + str(ghg_truck) + ' grams.')
    # TEU referencing a standard shipping container, meaning twenty-foot equivalent unit
    # convert grams to pounds
    # 1 gram = 0.00220462 lbs.
    g_to_lbs = 0.00220462
    ghg_rf_lbs = ghg_reefer * g_to_lbs
    ghg_rl_lbs = ghg_rail * g_to_lbs
    ghg_tk_lbs = ghg_truck * g_to_lbs
    output_string += htmlify('Carbon dioxide emissions are between: ' + str(ghg_rl_lbs) \
                                        + ', ' + str(ghg_rf_lbs) + ', and ' + str(ghg_tk_lbs) + ' pounds.')
    # water use
    # units = metric tons of water
    for index, row in user_food.iterrows():
        output_string += htmlify('Blue water use in gallons per lb: ' + str(row["blue gal per lb"]))
        output_string += htmlify('Total water use in gallons per lb: ' + str(row["total gal per lb"]))
    return output_string


main_blueprint = Blueprint('main', __name__,)

THIS_DIR = path.dirname(path.abspath(__file__))
CSV_DIR = path.join(THIS_DIR, '..', '..', 'client', 'static', 'csv')
print('Thinks CSV dir = ' + str(CSV_DIR)) # This line is debug

us_cities_csv = path.join(CSV_DIR, 'uscitiesv1.4.csv')
country_centroids_csv = path.join(CSV_DIR, 'country_centroids_az8.csv')
crops_water_csv = path.join(CSV_DIR, 'selected_crops_waterprint.csv')

us_cities = pd.read_csv(us_cities_csv)
us_cities['location'] = us_cities['city'] + ', ' + us_cities['state_id']

country_centroids = pd.read_csv(country_centroids_csv)

crops_water = pd.read_csv(crops_water_csv)

us_city_location = us_cities[['location', 'lat', 'lng']].copy()
us_city_location.rename(columns={'location' : 'city'}, inplace=True)

US_CITIES_LIST = us_city_location['city'].tolist()

us_city_dict = us_city_location.set_index('city').T.to_dict('list')

country_location = country_centroids[['geounit', 'Latitude', 'Longitude']].copy()
country_location.rename(columns = {'geounit' : 'country', 'Latitude' : 'lat', 'Longitude' : 'lng'}, inplace=True)

COUNTRIES_LIST = country_location['country'].tolist()

water_use = crops_water[['product', 'blue_global avg water footprint(m3ton-1)', 'total_global avg water footprint(m3ton-1)']].copy()
water_use.rename(columns = {'product' : 'food', 'blue_global avg water footprint(m3ton-1)' : 'blue water footprint',
                            'total_global avg water footprint(m3ton-1)' : 'total water footprint'}, inplace=True)

FOOD_NAMES_LIST = water_use['food'].tolist()
                            
water_use['blue gal'] = water_use['blue water footprint'].apply(tons_to_gallons)
water_use['total gal'] = water_use['total water footprint'].apply(tons_to_gallons)
water_use['blue liters'] = water_use['blue water footprint'].apply(tons_to_liters)
water_use['total liters'] = water_use['total water footprint'].apply(tons_to_liters)

water_use['blue tons per lb'] = water_use['blue water footprint'].apply(divider)
water_use['total tons per lb'] = water_use['total water footprint'].apply(divider)
water_use['blue gal per lb'] = water_use['blue gal'].apply(divider)
water_use['total gal per lb'] = water_use['total gal'].apply(divider)
water_use['blue liters per lb'] = water_use['blue liters'].apply(divider)
water_use['total liters per lb'] = water_use['total liters'].apply(divider)


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route('/calculator')
def calculator():
    environmental_info_output = None
    food_location = request.args.get('food_location')
    food_name = request.args.get('food_name')
    food_origin = request.args.get('food_origin')
    if food_location is not None and food_name is not None and food_origin is not None:
        food_location_arg = US_CITIES_LIST[int(food_location) - 1]
        food_name_arg = FOOD_NAMES_LIST[int(food_name) - 1]
        food_origin_arg = COUNTRIES_LIST[int(food_origin) - 1]
        environmental_info_output = get_environmental_prose(food_location_arg, food_origin_arg, food_name_arg)
    return render_template('main/calculator.html',
                            food_locations=US_CITIES_LIST,
                            food_names=FOOD_NAMES_LIST,
                            food_origins=COUNTRIES_LIST,
                            environmental_info_output=environmental_info_output)


@main_blueprint.route('/sources')
def sources():
    return render_template('main/sources.html')
