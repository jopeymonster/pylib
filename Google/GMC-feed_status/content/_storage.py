#!/usr/bin/python

from __future__ import print_function
import json
import os
import sys

from content import _constants
import google.auth
import google.oauth2

class Storage(object):
  def __init__(self, config):
    self._config = config

  def _token_path(self):
    return os.path.join(self._config['path'], _constants.TOKEN_FILE)

  def get(self):
    try:
      with open(self._token_path(), 'r') as infile:
        token = json.load(infile)
      client_info = retrieve_client_config(self._config)['installed']
      credentials = google.oauth2.credentials.Credentials(
          None,
          client_id=client_info['client_id'],
          client_secret=client_info['client_secret'],
          refresh_token=token['refresh_token'],
          token_uri=client_info['token_uri'],
          scopes=[_constants.CONTENT_API_SCOPE])
      try:
        credentials.refresh(google.auth.transport.requests.Request())
        print('Using stored credentials from %s.' % self._token_path())
        return credentials
      except google.auth.exceptions.RefreshError:
        print('The stored credentials in the file %s cannot be refreshed, '
              're-requesting access.' % self._token_path())
        return None
    except (IOError, ValueError, KeyError):
      return None

  def put(self, credentials):
    token = {
        'refresh_token': credentials.refresh_token,
    }
    with open(self._token_path(), 'w') as outfile:
      json.dump(token, outfile, sort_keys=True, indent=2,
                separators=(',', ': '))

def retrieve_client_config(config):
  client_secrets_path = os.path.join(
      config['path'], _constants.CLIENT_SECRETS_FILE)
  with open(client_secrets_path, 'r') as json_file:
    client_config_json = json.load(json_file)
  if 'installed' not in client_config_json:
    print('Please read the note about OAuth2 client IDs in the '
          'top-level README.')
    sys.exit(1)
  return client_config_json
