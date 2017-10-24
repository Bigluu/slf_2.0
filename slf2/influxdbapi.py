""" slf2 influxdb module"""

# stdlib

import logging

# 3rd-party

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from requests.exceptions import RequestException


LOG = logging.getLogger(__name__)


class InfluxDbError(Exception):
    """exception raised when a slf api connection/parse error occurs."""


class InfluxDbApi:
    """ influxdb module"""

    def __init__(self, hostname='localhost', port='8086', username='slf', password='slf', database='slf'):
        """ initialize module api"""
        self._client = InfluxDBClient(hostname, port, username, password, database)

    def store_point(self, station_name, station_id, measurements):
        for measurement in measurements:
            timestamp = int(measurement[0])
            hs = float_or_zero(measurement[1] * 10)
            hn6h = float_or_zero(measurement[8] * 10)
            ta = float_or_zero(measurement[3])
            tss = float_or_zero(measurement[4])
            vw = float_or_zero(measurement[5])
            vw_max = float_or_zero(measurement[6])
            dw = float_or_zero(measurement[7])

            json_body = [
                {
                    "measurement": "snow",
                    "tags": {
                        "station_name": station_name,
                        "station_id": station_id
                    },
                    "time": timestamp,
                    "fields": {
                        'snow_depth': hs,
                        'snow_depth_6h': hn6h
                    }
                },
                {
                    "measurement": "temperature",
                    "tags": {
                        "station_name": station_name,
                        "station_id": station_id
                    },
                    "time": timestamp,
                    "fields": {
                        'air_temperature': ta,
                        'snow_surface_temperature': tss
                    }
                },
                {
                    "measurement": "wind",
                    "tags": {
                        "station_name": station_name,
                        "station_id": station_id
                    },
                    "time": timestamp,
                    "fields": {
                        'wind speed': vw,
                        'wind_direction': dw,
                        'wind_gusts': vw_max
                    }
                }
            ]
            try:
                self._client.write_points(json_body, 's')
            except (InfluxDBClientError, RequestException) as exc:
                LOG.debug('could not write to InfluxDB: %s', exc)
                raise InfluxDbError('could not write to InfluxDB: %s' % exc) from None


def float_or_zero(value):
    try:
        return float(value)
    except ValueError:
        return 0.0
