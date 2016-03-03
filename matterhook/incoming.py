# -*- coding: utf-8 -*-

import requests

__all__ = ['Webhook']


class InvalidPayload(Exception):
    pass


class HTTPError(Exception):
    pass


class Webhook(object):
    """
    Interacts with a Mattermost incoming webhook.
    """

    def __init__(self,
                 url,
                 api_key,
                 channel=None,
                 icon_url=None,
                 username=None):
        self.api_key = api_key
        self.channel = channel
        self.icon_url = icon_url
        self.username = username
        self.url = url

    def __setitem__(self, channel, payload):
        if isinstance(payload, dict):
            try:
                message = payload.pop('text')
            except KeyError:
                raise InvalidPayload('missing "text" key')
        else:
            message = payload
            payload = {}
        self.send(message, **payload)

    @property
    def incoming_hook_url(self):
        return '{}/hooks/{}'.format(self.url, self.api_key)

    def send(self, message, channel=None, icon_url=None, username=None):
        payload = {'text': message}

        if channel or self.channel:
            payload['channel'] = channel or self.channel
        if icon_url or self.icon_url:
            payload['icon_url'] = icon_url or self.icon_url
        if username or self.username:
            payload['username'] = username or self.username

        r = requests.post(self.incoming_hook_url, json=payload)
        if r.status_code != 200:
            raise HTTPError(r.text)
