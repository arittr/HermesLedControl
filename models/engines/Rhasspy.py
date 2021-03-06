import os
import json
import logging
from pathlib import Path
from typing import Optional

import toml


class Rhasspy:

	def __init__(self):
		self._logger = logging.getLogger('HermesLedControl')
		self._logger.info('Initializing Rhasspy settings')


	def loadConfig(self, params) -> Optional[dict]:

		"""
		Load assistant configuration
		:return: configs are returned as a dict:
		{
		  'mqttServer': ip
		  'mqttPort': port
		  'mqttUsername': username, optional
		  'mqttPassword': password, optional
		  'mqttTLSCAFile': path to cacert TLS file, optional
		  'deviceName': name
		}
		"""

		self._logger.info('Loading configurations')

		userHomePath = os.path.expanduser('~')
		configPath = userHomePath + '/.config/rhasspy/profiles/en/profile.json'
		path = Path(params.pathToConfig or configPath)

		configs = dict()

		if path.exists():
			with path.open() as confFile:
				conf = json.load(confFile)

				try:
					configs['mqttServer'] = conf['mqtt']['host']
					configs['mqttPort'] = conf['mqtt'].get('port', 1883)
					configs['mqttUsername'] = conf['mqtt'].get('username', '')
					configs['mqttPassword'] = conf['mqtt'].get('password', '')
					configs['mqttTLSCAFile'] = ''
					configs['deviceName'] = conf['mqtt'].get('site_id', 'default')

					return configs
				except:
					self._logger.info('Error loading configurations')
					return None
		else:
			if params.debug:
				self._logger.info('No Rhasspy config found but debug mode, allow to continue')
				return dict()
			else:
				self._logger.fatal('Error loading configurations, file does not exist')
				return None
