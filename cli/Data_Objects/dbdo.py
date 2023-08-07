from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection

Base = declarative_base()
metadata = MetaData(schema='public')


class PlantSpecies(Base):
    __tablename__ = 'plant_species'
    # __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True)
    scientific_name = Column(String)
    common_name = Column(String)
    other_name = Column(String)
    family = Column(String)
    origin = Column(String)
    type = Column(String)
    dimension = Column(String)
    cycle = Column(String)
    watering = Column(String)
    attracts = Column(String)
    propagation = Column(String)
    growth_rate = Column(String)
    maintenance = Column(String)
    drought_tolerant = Column(Boolean)
    salt_tolerant = Column(Boolean)
    thorny = Column(Boolean)
    invasive = Column(Boolean)
    tropical = Column(Boolean)
    indoor = Column(Boolean)
    care_level = Column(String)
    flowers = Column(Boolean)
    cones = Column(Boolean)
    fruits = Column(Boolean)
    edible_fruit = Column(Boolean)
    fruit_color = Column(String)
    fruiting_season = Column(String)
    harvest_season = Column(String)
    harvest_method = Column(String)
    leaf = Column(Boolean)
    leaf_color = Column(String)
    edible_leaf = Column(Boolean)
    cuisine = Column(Boolean)
    cuisine_list = Column(String)
    medicinal = Column(Boolean)
    medicinal_use = Column(String)
    medicinal_method = Column(String)
    poisonous_to_humans = Column(Integer)
    poison_effects_to_humans = Column(String)
    poison_to_humans_cure = Column(String)
    poisonous_to_pets = Column(Integer)
    poison_effects_to_pets = Column(String)
    poison_to_pets_cure = Column(String)
    rare = Column(String)
    rare_level = Column(String)
    endangered = Column(String)
    endangered_level = Column(String)
    description = Column(Text)
    problem = Column(Text)

    sunlight = relationship('Sunlight', back_populates='plant_species')
    soil = relationship('Soil', back_populates='plant_species')
    pests = relationship('Pests', back_populates='plant_species')
    hardiness = relationship('Hardiness', back_populates='plant_species')
    images = relationship('Images', back_populates='plant_species')

class Sunlight(Base):
    __tablename__ = 'sunlight'
    # __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True)
    plant_species_id = Column(Integer, ForeignKey('plant_species.id'))
    sunlight = Column(String)
    plant_species = relationship('PlantSpecies', back_populates='sunlight')


class Soil(Base):
    __tablename__ = 'soil'
    id = Column(Integer, primary_key=True)
    plant_species_id = Column(Integer, ForeignKey('plant_species.id'))
    soil = Column(String)
    plant_species = relationship('PlantSpecies', back_populates='soil')


class Pests(Base):
    __tablename__ = 'pests'
    # __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True)
    plant_species_id = Column(Integer, ForeignKey('plant_species.id'))
    pests = Column(String)
    plant_species = relationship('PlantSpecies', back_populates='pests')


class Hardiness(Base):
    __tablename__ = 'hardiness'
    # __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True)
    plant_species_id = Column(Integer, ForeignKey('plant_species.id'))
    min_hardiness = Column(Integer)
    max_hardiness = Column(Integer)
    plant_species = relationship('PlantSpecies', back_populates='hardiness')


class Images(Base):
    __tablename__ = 'images'
    # __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True)
    plant_species_id = Column(Integer, ForeignKey('plant_species.id'))
    license = Column(String)
    license_name = Column(String)
    license_url = Column(String)
    original_url = Column(String)
    regular_url = Column(String)
    medium_url = Column(String)
    small_url = Column(String)
    thumbnail = Column(String)
    plant_species = relationship('PlantSpecies', back_populates='images')

