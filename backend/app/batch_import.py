#!/usr/bin/env python3

import os
import click
import csv
import requests
import pprint
from app.db.models import Building as BuildingModel
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
ESRI_DATETIME_TO_DATE_FIELDS = (
    'ADR_DATUM',
    'STR_DATUM',
)


def _clean(k, v):
    v = v.strip()
    if v and k in ESRI_DATETIME_TO_DATE_FIELDS:
        v = v.split('T')[0]
    return v or None


@click.command()
@click.option('--url', help="ESRI buildings data csv url.",
              default=ESRI_BUILDINGS_URL)
@click.option('--update', help="Update ESRI buildings data.",
              default=False, is_flag=True)
@click.option('--buffer-size', help="Batch import buffer size.",
              default=10000)
@click.option('--debug', help="Debug mode.",
              default=False, is_flag=True)
def import_buildings_data(url, update, buffer_size, debug) -> None:
    db = SessionLocal()
    if not os.path.exists(ESRI_BUILDINGS_FILE) or update:
        with requests.Session() as s:
            click.echo("Downloading ESRI buildings data...")
            download = s.get(url)
            click.echo("Done!")
            decoded_content = download.content.decode('utf-8')
        with open(ESRI_BUILDINGS_FILE, 'w') as f:
            f.write(decoded_content)

    click.echo('Deleting buildings data...')
    db.query(BuildingModel).delete()
    click.echo('Done!')
    click.echo("Importing buildings data...")
    with open(ESRI_BUILDINGS_FILE, 'r') as csv_file:
        cr = csv.DictReader(csv_file)
        buffer = []
        for row in cr:
            data = {
                key.lower(): _clean(key, value) for (key, value) in row.items() if key in ESRI_BUILDINGS_FIELDS
            }
            if data['adressid'] == '0':
                # Skip invalid records.
                continue
            buffer.append(data)
            if len(buffer) % buffer_size == 0:
                if debug:
                    pprint.pprint(buffer)
                db.execute(BuildingModel.__table__.insert(), buffer)
                buffer = []
                db.commit()
        db.execute(BuildingModel.__table__.insert(), buffer)
        db.commit()
    click.echo("Buildings data imported!")


if __name__ == "__main__":
    import_buildings_data()
