"""
calc.py

derived from ../calc.ipynb
"""

from geopy import distance
from os import path

import geopy as gp
import numpy as np
import pandas as pd


def tons_to_gallons(x):
    return(x * 264.17)

def tons_to_liters(x):
    return(x * 1000)

def divider(x):
    return(x/2000)


THIS_DIR = path.dirname(path.abspath(__file__))
CSV_DIR = path.join(THIS_DIR, '..', '..', 'project', 'client', 'static', 'csv')

us_cities_csv = path.join(CSV_DIR, 'uscitiesv1.4.csv')
country_centroids_csv = path.join(CSV_DIR, 'country_centroids_az8.csv')
crops_water_csv = path.join(CSV_DIR, 'selected_crops_waterprint.csv')

us_cities = pd.read_csv(us_cities_csv)
us_cities['location'] = us_cities['city'] + ', ' + us_cities['state_id']

country_centroids = pd.read_csv(country_centroids_csv)

crops_water = pd.read_csv(crops_water_csv)

us_city_location = us_cities[['location', 'lat', 'lng']].copy()
us_city_location.rename(columns={'location' : 'city'}, inplace=True)

us_city_dict = us_city_location.set_index('city').T.to_dict('list')

country_location = country_centroids[['geounit', 'Latitude', 'Longitude']].copy()
country_location.rename(columns = {'geounit' : 'country', 'Latitude' : 'lat', 'Longitude' : 'lng'}, inplace=True)

country_dict = country_location.set_index('country').T.to_dict('list')

water_use = crops_water[['product', 'blue_global avg water footprint(m3ton-1)', 'total_global avg water footprint(m3ton-1)']].copy()
water_use.rename(columns = {'product' : 'food', 'blue_global avg water footprint(m3ton-1)' : 'blue water footprint',
                            'total_global avg water footprint(m3ton-1)' : 'total water footprint'}, inplace=True)
                            
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


if __name__ == '__main__':
    
    input_city = 'Syracuse, NY'
    user_city = us_city_location[(us_city_location['city'] == input_city)]

    input_food_origin = 'Mexico'
    user_food_origin = country_location[(country_location['country'] == input_food_origin)]

    input_food = 'grapes'
    user_food = water_use[(water_use['food'] == input_food)]

    # example from geopy documentation: eventually want to snag lat/lng for city and food origin to calculate
    newport_ri = (41.49008, -71.312796)
    cleveland_oh = (41.499498, -81.695391)
    dist_btw = distance.great_circle(newport_ri, cleveland_oh).miles
    print(f'Your food travelled approximately {dist_btw:.0f} miles')

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

    # {variable:.0f} for no decimal places
    print(f'Carbon dioxide emissions are between: {ghg_rail:.0f}, {ghg_reefer:.0f}, and {ghg_truck:.0f} grams')

    # TEU referencing a standard shipping container, meaning twenty-foot equivalent unit
    # convert grams to pounds
    # 1 gram = 0.00220462 lbs.
    g_to_lbs = 0.00220462
    ghg_rf_lbs = ghg_reefer * g_to_lbs
    ghg_rl_lbs = ghg_rail * g_to_lbs
    ghg_tk_lbs = ghg_truck * g_to_lbs

    print(f'Carbon dioxide emissions are between: {ghg_rl_lbs:.0f}, {ghg_rf_lbs:.0f}, and {ghg_tk_lbs:.0f} pounds')

    # water use
    # units = metric tons of water

    # standard deviation for each numerical column
    print(water_use.std())

    for index, row in user_food.iterrows():
        print(f'Blue water use in gallons per lb: {row["blue gal per lb"]:.0f} \nTotal water use in gallons per lb: {row["total gal per lb"]:.0f}')
