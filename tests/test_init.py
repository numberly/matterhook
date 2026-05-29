import matterhook
from matterhook import Webhook, Attachment
from matterhook.incoming import Webhook as IncomingWebhook
from matterhook.attachments import Attachment as AttachmentsAttachment


class TestModuleExports:
    def test_webhook_exported(self):
        assert Webhook is IncomingWebhook

    def test_attachment_exported(self):
        assert Attachment is AttachmentsAttachment

    def test_all_contains_webhook(self):
        assert "Webhook" in matterhook.__all__

    def test_all_contains_attachment(self):
        assert "Attachment" in matterhook.__all__

    def test_all_length(self):
        assert len(matterhook.__all__) == 2
