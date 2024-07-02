import os
from dotenv import load_dotenv


load_dotenv()


class Settings:

    
    # Configuracion de la URL para pedir el Code

    params_authorization = {

        'response_type': os.getenv("RESPONSE_CLIENT_TYPE"),
        'client_id': os.getenv("APP_ID"),
        'redirect_uri': os.getenv("REDIRECT_URI"),
        'state': os.getenv("STATE"),
        'client_secret': os.getenv("CLIENT_SECRET"),
    }    

    params_api = {
        'client_id': os.getenv("APP_ID"),
        'client_secret': os.getenv("CLIENT_SECRET"),
        'response_type': os.getenv("RESPONSE_CLIENT_TYPE"),
        'redirect_uri': os.getenv("REDIRECT_URI"),
        'state': os.getenv("STATE"),
    }


    # Configuracion para pedir el access/refresh token

    url_auth: str = os.getenv("URL_AUTH")
    url_base: str = os.getenv("URL_BASE")
    url_token: str = os.getenv("TOKEN_URL")
    site_id: str = os.getenv("SITE_ID")

    user_agent: str = os.getenv("USER_AGENT")


    # database config

    database_config: dict = {

        "database_address": os.getenv("DATABASE_ADDRESS"),
        "database_port": os.getenv("DATABASE_PORT"),
        "database": os.getenv("DATABASE"),
        "database_user": os.getenv("DATABASE_USER"),
        "database_password": os.getenv("DATABASE_PASSWORD")
    }

    # endponits

    endpoint_categories: str = os.getenv("ENDPOINT_CATEGORIES")
    endpoint_items_by_categories: str = os.getenv("ENDPOINT_ITEMS_BY_CATEGORY")


    categories_dict = {

        'MLU5725': 'vehicle_accessories',
        'MLU1512': 'agriculture',
        'MLU1403': 'food_and_beverages',
        'MLU1071': 'pets_and_animals',
        'MLU1367': 'antiques_and_collectibles',
        'MLU442392': 'art_library_and_merchandise',
        'MLU1743': 'cars_motorcycles_and_others',
        'MLU1384': 'babies',
        'MLU1246': 'beauty_and_personal_care',
        'MLU1039': 'cameras_and_accessories',
        'MLU1051': 'cellphones_telephony',
        'MLU1648': 'computing',
        'MLU1144': 'consoles_and_videogames',
        'MLU1500': 'construction',
        'MLU1276': 'sports_and_fitness',
        'MLU5726': 'home_appliances_and_ac',
        'MLU1000': 'electronics_audio_and_video',
        'MLU208736': 'tools',
        'MLU1574': 'home_furniture_and_garden',
        'MLU1499': 'industrial_and_office',
        'MLU1459': 'real_estate',
        'MLU1182': 'musical_instruments',
        'MLU3937': 'jewelry_and_watches',
        'MLU1132': 'toys_and_games',
        'MLU442458': 'books_magazines_and_comics',
        'MLU1168': 'music_and_movies',
        'MLU1430': 'clothing_shoes_and_accessories',
        'MLU409431': 'health_and_medical_equipment',
        'MLU1540': 'services',
        'MLU111079': 'souvenirs_party_supplies_and_decor',
        'MLU1953': 'other_categories'

    }




if __name__ == '__main__':

    settings = Settings()

    if settings:
        try:
            config = settings.url_base
            print(True)
        except AttributeError as e:
            print(f"Value not found {e}")
