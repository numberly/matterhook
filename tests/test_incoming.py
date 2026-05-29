from unittest.mock import patch, MagicMock

import pytest

from matterhook.incoming import Webhook, InvalidPayload, HTTPError


@pytest.fixture
def webhook():
    return Webhook("https://mattermost.example.com", "abc123")


@pytest.fixture
def full_webhook():
    return Webhook(
        "https://mattermost.example.com",
        "abc123",
        channel="town-square",
        icon_url="https://example.com/icon.png",
        username="bot",
        attachments=[{"fallback": "test"}],
    )


class TestWebhookInit:
    def test_minimal(self, webhook):
        assert webhook.url == "https://mattermost.example.com"
        assert webhook.api_key == "abc123"
        assert webhook.channel is None
        assert webhook.icon_url is None
        assert webhook.username is None
        assert webhook.attachments is None

    def test_full(self, full_webhook):
        assert full_webhook.channel == "town-square"
        assert full_webhook.icon_url == "https://example.com/icon.png"
        assert full_webhook.username == "bot"
        assert full_webhook.attachments == [{"fallback": "test"}]


class TestIncomingHookUrl:
    def test_formats_url(self, webhook):
        assert (
            webhook.incoming_hook_url
            == "https://mattermost.example.com/hooks/abc123"
        )


class TestSend:
    @patch("matterhook.incoming.requests.post")
    def test_send_simple_message(self, mock_post, webhook):
        mock_post.return_value = MagicMock(status_code=200)
        webhook.send("hello")
        mock_post.assert_called_once_with(
            "https://mattermost.example.com/hooks/abc123",
            json={"text": "hello"},
        )

    @patch("matterhook.incoming.requests.post")
    def test_send_with_all_params(self, mock_post, webhook):
        mock_post.return_value = MagicMock(status_code=200)
        webhook.send(
            "hello",
            channel="general",
            icon_url="https://icon.png",
            username="mybot",
            attachments=[{"fallback": "fb"}],
        )
        mock_post.assert_called_once_with(
            "https://mattermost.example.com/hooks/abc123",
            json={
                "text": "hello",
                "channel": "general",
                "icon_url": "https://icon.png",
                "username": "mybot",
                "attachments": [{"fallback": "fb"}],
            },
        )

    @patch("matterhook.incoming.requests.post")
    def test_send_uses_defaults(self, mock_post, full_webhook):
        mock_post.return_value = MagicMock(status_code=200)
        full_webhook.send("hello")
        mock_post.assert_called_once_with(
            "https://mattermost.example.com/hooks/abc123",
            json={
                "text": "hello",
                "channel": "town-square",
                "icon_url": "https://example.com/icon.png",
                "username": "bot",
                "attachments": [{"fallback": "test"}],
            },
        )

    @patch("matterhook.incoming.requests.post")
    def test_send_params_override_defaults(self, mock_post, full_webhook):
        mock_post.return_value = MagicMock(status_code=200)
        full_webhook.send(
            "hello",
            channel="off-topic",
            icon_url="https://other.png",
            username="other",
            attachments=[{"fallback": "other"}],
        )
        mock_post.assert_called_once_with(
            "https://mattermost.example.com/hooks/abc123",
            json={
                "text": "hello",
                "channel": "off-topic",
                "icon_url": "https://other.png",
                "username": "other",
                "attachments": [{"fallback": "other"}],
            },
        )

    @patch("matterhook.incoming.requests.post")
    def test_send_no_message(self, mock_post, webhook):
        mock_post.return_value = MagicMock(status_code=200)
        webhook.send()
        mock_post.assert_called_once_with(
            "https://mattermost.example.com/hooks/abc123",
            json={"text": None},
        )

    @patch("matterhook.incoming.requests.post")
    def test_send_raises_http_error(self, mock_post, webhook):
        mock_post.return_value = MagicMock(
            status_code=500, text="Internal Server Error"
        )
        with pytest.raises(HTTPError, match="Internal Server Error"):
            webhook.send("hello")

    @patch("matterhook.incoming.requests.post")
    def test_send_raises_http_error_404(self, mock_post, webhook):
        mock_post.return_value = MagicMock(
            status_code=404, text="Not Found"
        )
        with pytest.raises(HTTPError, match="Not Found"):
            webhook.send("hello")


class TestSetItem:
    @patch("matterhook.incoming.requests.post")
    def test_setitem_string_payload(self, mock_post, webhook):
        mock_post.return_value = MagicMock(status_code=200)
        webhook["general"] = "hello"
        mock_post.assert_called_once_with(
            "https://mattermost.example.com/hooks/abc123",
            json={"text": "hello"},
        )

    @patch("matterhook.incoming.requests.post")
    def test_setitem_dict_payload(self, mock_post, webhook):
        mock_post.return_value = MagicMock(status_code=200)
        webhook["general"] = {"text": "hello", "username": "mybot"}
        mock_post.assert_called_once_with(
            "https://mattermost.example.com/hooks/abc123",
            json={"text": "hello", "username": "mybot"},
        )

    @patch("matterhook.incoming.requests.post")
    def test_setitem_dict_with_icon_url(self, mock_post, webhook):
        mock_post.return_value = MagicMock(status_code=200)
        webhook["general"] = {
            "text": "hello",
            "icon_url": "https://icon.png",
        }
        mock_post.assert_called_once_with(
            "https://mattermost.example.com/hooks/abc123",
            json={"text": "hello", "icon_url": "https://icon.png"},
        )

    def test_setitem_dict_missing_text(self, webhook):
        with pytest.raises(InvalidPayload, match='missing "text" key'):
            webhook["general"] = {"username": "bot"}


class TestExceptions:
    def test_invalid_payload_is_exception(self):
        assert issubclass(InvalidPayload, Exception)

    def test_http_error_is_exception(self):
        assert issubclass(HTTPError, Exception)

    def test_invalid_payload_message(self):
        err = InvalidPayload("test error")
        assert str(err) == "test error"

    def test_http_error_message(self):
        err = HTTPError("server error")
        assert str(err) == "server error"
