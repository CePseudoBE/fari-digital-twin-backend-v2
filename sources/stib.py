import json
import dotenv
from collections import defaultdict
from itertools import chain, product
from typing import Dict, List

import geopandas as gpd
import pandas as pd
import requests
import shapely
from bs4 import BeautifulSoup

dotenv.load_dotenv()

from digitaltwin_dataspace import run_components, Collector, ComponentConfiguration


class STIBGTFSCollector(Collector):
    def get_schedule(self) -> str:
        return "1s"

    def get_configuration(self) -> ComponentConfiguration:
        return ComponentConfiguration(
            name="stib_gtfs_collector",
            tags=["STIB", "GTFS", "Transport"],
            description="Collecte les données GTFS statiques de la STIB pour Bruxelles",
            content_type="application/zip"
        )

    def collect(self) -> bytes:
        endpoint = "https://stibmivb.opendatasoft.com/api/explore/v2.1/catalog/datasets/gtfs-files-production/alternative_exports/gtfszip/"
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        return response.content


class STIBShapeFilesCollector(Collector):
    def get_schedule(self) -> str:
        return "10s"

    def get_configuration(self) -> ComponentConfiguration:
        return ComponentConfiguration(
            name="stib_shapefiles_collector",
            tags=["STIB", "GeoJSON", "Shapefiles"],
            description="Collecte les shapefiles du réseau STIB en format GeoJSON",
            content_type="application/geo+json"
        )

    def collect(self) -> bytes:
        endpoint = "https://stibmivb.opendatasoft.com/api/explore/v2.1/catalog/datasets/shapefiles-production/exports/geojson"
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        return response.content


class STIBVehiclePositionsCollector(Collector):
    def get_schedule(self) -> str:
        return "10s"

    def get_configuration(self) -> ComponentConfiguration:
        return ComponentConfiguration(
            name="stib_vehicle_positions_collector",
            tags=["STIB", "Vehicle", "Positions", "Real-time"],
            description="Collecte les positions des véhicules STIB en temps réel",
            content_type="application/json"
        )

    def collect(self) -> bytes:
        endpoint = "https://stibmivb.opendatasoft.com/api/explore/v2.1/catalog/datasets/vehicle-position-rt-production/records"

        try:
            response = requests.get(endpoint, params={"limit": 100}, timeout=10)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Erreur lors de la récupération des positions de véhicules : {e}")
            return json.dumps([]).encode('utf-8')

        raw_results = data.get("results", [])
        results = []

        for raw_result in raw_results:
            try:
                vehicle_positions = json.loads(raw_result.get("vehiclepositions", "[]"))
                line_id = str(raw_result.get("lineid", ""))
                for vp in vehicle_positions:
                    results.append({**vp, "lineId": line_id})
            except json.JSONDecodeError:
                continue

        return json.dumps(results).encode('utf-8')


class STIBStopsCollector(Collector):
    def get_schedule(self) -> str:
        return "10s"

    def get_configuration(self) -> ComponentConfiguration:
        return ComponentConfiguration(
            name="stib_stops_collector",
            tags=["STIB", "Arrêts", "GeoJSON"],
            description="Collecte les arrêts STIB avec coordonnées géographiques",
            content_type="application/geo+json"
        )

    def collect(self) -> bytes:
        try:
            stops_per_line = pd.read_csv(
                "https://stibmivb.opendatasoft.com/explore/dataset/gtfs-files-production/files"
                "/7068c8d492df76c5125fac081b5e09e9/download/"
            )
        except Exception as e:
            print(f"Erreur lors du chargement des arrêts officiels : {e}")
            stops_per_line = pd.DataFrame(columns=["stop_id", "stop_lat", "stop_lon"])

        stops_per_line["stop_id"] = self._convert_stop_ids_to_generic(stops_per_line["stop_id"])
        stops_per_line = stops_per_line[["stop_id", "stop_lat", "stop_lon"]]

        merged = stops_per_line.drop_duplicates(subset=["stop_id"], keep="first")
        with_coords = merged[merged["stop_lat"].notnull() & merged["stop_lon"].notnull()]

        if with_coords.empty:
            return json.dumps({
                "type": "FeatureCollection",
                "features": []
            }).encode('utf-8')

        gdf = gpd.GeoDataFrame(
            with_coords,
            crs="epsg:4326",
            geometry=[shapely.geometry.Point(lon, lat) for lon, lat in zip(with_coords["stop_lon"], with_coords["stop_lat"])]
        )

        return gdf.to_json().encode('utf-8')

    def _convert_stop_ids_to_generic(self, stop_ids):
        return stop_ids.astype(str).str.replace(r'[^0-9]', '', regex=True)