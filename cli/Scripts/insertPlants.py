import os
import datetime
import asyncio
import logging
from Data_Objects.dbdo import PlantSpecies, Pests, Hardiness
from Data_Objects.dbdo import Images, ScientificName, Soil, Sunlight, Base, metadata
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy.orm import sessionmaker

# testing one at a time
# PLANTS_By_Page_URL = "https://perenual.com/api/species-list"
# API_Key = "sk-Oezd63f9103a67c4a95"
# count = 1
# PARAMS = {'page': count, 'key': API_Key}
# plant_id = 202
# url = f"https://perenual.com/api/species/details/{plant_id}?key={API_Key}"

# Set up logging
logging.basicConfig(filename='insertPlants.log', level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
load_dotenv()
# Connecting
CONNECTION_PARAMS = {
    'host': os.environ.get('HOST'),
    'port': int(os.environ.get('PORT')),
    'database': os.environ.get('DATABASE'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASSWORD')
}
API_Key = os.environ.get('API_KEY')
ENGINE = create_engine(
    f'postgresql://{CONNECTION_PARAMS["user"]}:{CONNECTION_PARAMS["password"]}@{CONNECTION_PARAMS["host"]}:{CONNECTION_PARAMS["port"]}/{CONNECTION_PARAMS["database"]}')


def min(plant): return 0 if not isinstance(
    plant['hardiness']['min'], int) else plant['hardiness']['min']

def max(plant): return 0 if not isinstance(
    plant['hardiness']['max'], int) else plant['hardiness']['max']

def create_data_object(plant):

    # plants = asyncio.run(fetchPlants.fetch_all_plants())

    logging.info(datetime.datetime.now().strftime("%I:%M %p"))
    logging.info(f"Connection string: {ENGINE}")
    try:
        plantSpecies = PlantSpecies(
            id=plant['id'],
            common_name=plant['common_name'],
            family=plant['family'],
            origin=plant['origin'],
            type=plant['type'],
            dimension=plant['dimension'],
            cycle=plant['cycle'],
            watering=plant['watering'],
            propagation=plant['propagation'],
            growth_rate=plant['growth_rate'],
            maintenance=plant['maintenance'],
            drought_tolerant=plant['drought_tolerant'],
            salt_tolerant=plant['salt_tolerant'],
            thorny=plant['thorny'],
            invasive=plant['invasive'],
            tropical=plant['tropical'],
            indoor=plant['indoor'],
            care_level=plant['care_level'],
            flowers=plant['flowers'],
            cones=plant['cones'],
            fruits=plant['fruits'],
            edible_fruit=plant['edible_fruit'],
            fruit_color=plant['fruit_color'],
            fruiting_season=plant['fruiting_season'],
            harvest_season=plant['harvest_season'],
            harvest_method=plant['harvest_method'],
            leaf=plant['leaf'],
            leaf_color=plant['leaf_color'],
            edible_leaf=plant['edible_leaf'],
            cuisine=plant['cuisine'],
            cuisine_list=plant['cuisine_list'],
            medicinal=plant['medicinal'],
            medicinal_use=plant['medicinal_use'],
            medicinal_method=plant['medicinal_method'],
            poisonous_to_humans=plant['poisonous_to_humans'],
            poison_effects_to_humans=plant['poison_effects_to_humans'],
            poison_to_humans_cure=plant['poison_to_humans_cure'],
            poisonous_to_pets=plant['poisonous_to_pets'],
            poison_effects_to_pets=plant['poison_effects_to_pets'],
            poison_to_pets_cure=plant['poison_to_pets_cure'],
            rare=plant['rare'],
            rare_level=plant['rare_level'],
            endangered=plant['endangered'],
            endangered_level=plant['endangered_level'],
            description=plant['description'],
            problem=plant['problem'])

        sciName = ScientificName(
            id=plant['id'],
            plant_species_id=plant['id'],
            scientific_name=plant['scientific_name']
        )
        sun = Sunlight(
            id=plant['id'],
            plant_species_id=plant['id'],
            sunlight=plant['sunlight']
        )
        soil = Soil(
            id=plant['id'],
            plant_species_id=plant['id'],
            soil=plant['soil']
        )
        pests = Pests(
            id=plant['id'],
            plant_species_id=plant['id'],
            pests=plant['pest_susceptibility']
        )

        hardiness = Hardiness(
            id=plant['id'],
            plant_species_id=plant['id'],
            min_hardiness=min(plant),
            max_hardiness= max(plant) )
        images = Images(
            id=plant['id'],
            plant_species_id=plant['id'],
            license=plant['default_image']['license'],
            license_name=plant['default_image']['license_name'],
            license_url=plant['default_image']['license_url'],
            original_url=plant['default_image']['original_url'],
            regular_url=plant['default_image']['regular_url'],
            medium_url=plant['default_image']['medium_url'],
            small_url=plant['default_image']['small_url'],
            thumbnail=plant['default_image']['thumbnail'])
        # print(plantSpecies.id, sciName.id, sun.id, soil.id, pests.id, hardiness.max_hardiness, images.id)
        insert_plant(plantSpecies, sciName, sun,
                    soil, pests, hardiness, images)

    except Exception as e:
        logging.error(f"Error: {e}")


def insert_plant(plantSpecies, sciName, sun, soil, pests, hardiness, images):

    Session = sessionmaker(bind=ENGINE)
    session = Session()

    try:
        with session.no_autoflush:
            session.merge(plantSpecies)
            session.merge(sciName)
            session.merge(sun)
            session.merge(soil)
            session.merge(pests)
            session.merge(hardiness)
            session.merge(images)
            session.commit()
            logging.debug(f"{plantSpecies.id} added to the database.")

    except (Exception) as e:
        logging.error(f"Error inserting plant {plantSpecies.id}: {e}")
        session.rollback()
    finally:
        session.close()


# if __name__ == "__main__":
    # plantSpecies, sciName, sun, soil, pests, hardiness, images = "", "", "", "", "", "", ""
    # insert_plant(plantSpecies, sciName, sun, soil, pests, hardiness, images)

    # create_data_object()

    # p = requests.get(url=url)
    # p = dict(p.json())
    # plant = plantDO.Plant(plant['id'], p['common_name'], p['scientific_name'], p['other_name'], p['family'], p['origin'], p['type'], p['dimension'], p['cycle'], p['watering'], p['attracts'], p['propagation'], p['hardiness'], p['hardiness_location_image'], p['sunlight'], p['soil'], p['growth_rate'], p['maintenance'], p['drought_tolerant'], p['salt_tolerant'], p['thorny'], p['invasive'], p['tropical'], p['indoor'], p['care_level'], p['pest_susceptibility'], p['pest_susceptibility_api'], p['flowers'], p['flowering_season'], p['flower_color'], p['cones'], p['fruits'], p['edible_fruit'], p['edible_fruit_taste_profile'], p['fruit_nutritional_value'], p['fruit_color'], p['fruiting_season'], p['harvest_season'], p['harvest_method'], p['leaf'], p['leaf_color'], p['edible_leaf'], p['edible_leaf_taste_profile'], p['leaf_nutritional_value'], p['cuisine'], p['cuisine_list'], p['medicinal'], p['medicinal_use'], p['medicinal_method'], p['poisonous_to_humans'], p['poison_effects_to_humans'], p['poison_to_humans_cure'], p['poisonous_to_pets'], p['poison_effects_to_pets'], p['poison_to_pets_cure'], p['rare'], p['rare_level'], p['endangered'], p['endangered_level'], p['description'], p['problem'], p['default_image'])
