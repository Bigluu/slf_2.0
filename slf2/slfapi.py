""" slf2 slfapi module"""

# stdlib

import logging
# 3rd-party

import requests
from requests.exceptions import RequestException

LOG = logging.getLogger(__name__)


class SlfError(Exception):
    """exception raised when a slf api connection/parse error occurs."""


class SlfApi:
    """ slf api module"""

    def __init__(self, stations_url, measurement_url):
        """ initialize module api"""
        self._stations_url = stations_url
        self._measurement_url = measurement_url

    def stations(self):
        """get all available stations"""
        try:
            stations_api = requests.get(self._stations_url)
            stations = {}
            for station in stations_api.json():
                station_id = station['id']
                station_name = station['name']
                stations[station_id] = station_name

            return stations
        except (RequestException, KeyError) as exc:
            LOG.debug('could not read from api: %s', exc)
            raise SlfError('could not read from api: %s' % exc) from None

    def station_measurement(self, station_id):
        """ get measurements of a station """
        try:
            params = {
                'id': station_id
            }
            measurements_api = requests.get(url=self._measurement_url, params=params)
            measurements = []
            for measurement in measurements_api.json():
                measurement_array = measurement.split(';')
                measurements.append(measurement_array)

            return measurements

        except (RequestException, KeyError) as exc:
            LOG.debug('could not read from api: {0}'.format(exc))
            raise SlfError('could not read from api: {0}'.format(exc)) from None
