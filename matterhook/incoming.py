import requests

__all__ = ["Webhook"]


class InvalidPayload(Exception):
    pass


class HTTPError(Exception):
    pass


class Webhook:
    """
    Interacts with a Mattermost incoming webhook.
    """

    def __init__(
        self,
        url: str,
        api_key: str,
        channel: str = None,
        icon_url: str = None,
        username: str = None,
        attachments: list = None,
    ):
        """Init Webhook object

        :param url: Mattermost base URL
        :type url: str
        :param api_key: Webhook API key
        :type api_key: str
        :param channel: Channel name, defaults to None
        :type channel: str, optional
        :param icon_url: Icon URL for message, defaults to None
        :type icon_url: str, optional
        :param username: Overrides user name, defaults to None
        :type username: str, optional
        :param attachments: Attachments, defaults to None
        :type attachments: list, optional
        """
        # Store values in Webhook object
        self.api_key = api_key
        self.channel = channel
        self.icon_url = icon_url
        self.username = username
        self.url = url
        self.attachments = attachments

    def __setitem__(self, channel: str, payload: str or dict):
        """Sets and checs item

        :param channel: Channel name
        :type channel: str
        :param payload: Message data
        :type payload: str or dict
        :raises InvalidPayload: Raises when the payload is invalid
        """
        if isinstance(payload, dict):
            try:
                message = payload.pop("text")
            except KeyError:
                raise InvalidPayload('missing "text" key')
        else:
            message = payload
            payload = {}
        self.send(message, **payload)

    @property
    def incoming_hook_url(self):
        """Formats webhook URL

        :return: webhook URL
        :rtype: str
        """
        return "{}/hooks/{}".format(self.url, self.api_key)

    def send(
        self,
        message: str = None,
        channel: str = None,
        icon_url: str = None,
        username: str = None,
        attachments: list = None,
    ):
        """Sends a message to a mattermost webhook

        :param message: Text message, defaults to None
        :type message: str, optional
        :param channel: Channel name, defaults to None
        :type channel: str, optional
        :param icon_url: Icon URL, defaults to None
        :type icon_url: str, optional
        :param username: Override username, defaults to None
        :type username: str, optional
        :param attachments: Attachments, defaults to None
        :type attachments: list, optional
        :raises HTTPError: Raises when request return code is not 200
        """
        payload = {"text": message}

        if channel or self.channel:
            payload["channel"] = channel or self.channel
        if icon_url or self.icon_url:
            payload["icon_url"] = icon_url or self.icon_url
        if username or self.username:
            payload["username"] = username or self.username
        if attachments or self.attachments:
            payload["attachments"] = attachments or self.attachments

        r = requests.post(self.incoming_hook_url, json=payload)
        if r.status_code != 200:
            raise HTTPError(r.text)
