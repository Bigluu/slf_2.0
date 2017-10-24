""" SLF 2.0 data aggregator"""

# stdlib

import logging
import os

# 3rd-party
from slf2.slfapi import SlfApi, SlfError
from slf2.influxdbapi import InfluxDbApi

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    """ main entrypoint"""

    slf_api = SlfApi('http://odb.slf.ch/odb/api/v1/stations', 'http://odb.slf.ch/odb/api/v1/measurement')

    hostname = os.getenv('INFLUXDB_HOST', 'localhost')
    port = os.getenv('INFLUXDB_PORT', '8086')
    username = os.getenv('INFLUXDB_USER', 'slf')
    password = os.getenv('INFLUXDB_PASSWORD', 'slf')
    database = os.getenv('INFLUXDB_DATABASE', 'slf')
    influxdb_api = InfluxDbApi(hostname, port, username, password, database)
    stations = slf_api.stations()
    measurements = {}
    for station in stations:
        print('Get measurements for station {0}'.format( stations[station]))
        measurement = slf_api.station_measurement(station)
        measurements[station] = measurement
        print('Save measurements for station {0}'.format(stations[station]))
        influxdb_api.store_point(stations[station],station,measurement)

    return "All done"
