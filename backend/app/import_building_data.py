#!/usr/bin/env python3

import os
import click
import csv
import requests
import pprint
from app.db.session import get_db
from app.db.crud import create_building
from app.db.schemas import Building
from app.db.session import SessionLocal

ESRI_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data'
)
ESRI_BUILDINGS_FILE = os.path.join(ESRI_DATA_PATH, 'buildings.csv')
ESRI_BUILDINGS_URL = "https://opendata.arcgis.com/datasets/273bf4ae7f6a460fbf3000d73f7b2f76_0.csv" + \
                     "?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
ESRI_BUILDINGS_FIELDS = (
    'ADRESSID',
    'OBJECTID',
    'BEZ_NAME',
    'ORT_NAME',
    'PLR_NAME',
    'STR_NAME',
    'HNR',
    'PLZ',
    'BLK',
    'ADR_DATUM',
    'STR_DATUM',
    'QUALITAET',
    'TYP',
)


@click.command()
@click.option('--url', help="ESRI buildings data csv url.",
              default=ESRI_BUILDINGS_URL)
@click.option('--update', help="Update ESRI buildings data.",
              default=False, is_flag=True)
@click.option('--debug', help="Debug mode.",
              default=False, is_flag=True)
def import_buildings_data(url, update, debug) -> None:
    db = SessionLocal()
    decoded_content = None
    if os.path.exists(ESRI_BUILDINGS_FILE) and not update:
        click.echo("Using downloaded ESRI buildings data.")
        decoded_content = open(ESRI_BUILDINGS_FILE, 'r').read()
    else:
        with requests.Session() as s:
            click.echo("Downloading ESRI buildings data...")
            download = s.get(url)
            click.echo("Done!")
            decoded_content = download.content.decode('utf-8')
        with open(ESRI_BUILDINGS_FILE, 'w') as f:
            f.write(decoded_content)
    
    if not update:
        click.echo("Importing buildings data...")
    else:
        click.echo("Updating buildings data...")

    cr = csv.DictReader(decoded_content.splitlines())
    for row in list(cr):
        data = {key.lower(): value.strip() or None for (key, value) in row.items() if key in ESRI_BUILDINGS_FIELDS}
        if debug:
            pprint.pprint(data)
        create_building(db, Building(**data), update)
    click.echo("Buildings data imported!")


if __name__ == "__main__":
    import_buildings_data()
