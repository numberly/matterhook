from matterhook.attachments import Attachment


class TestAttachmentInit:
    def test_minimal(self):
        att = Attachment(fallback="fallback text")
        assert att.fallback == "fallback text"
        assert att.color is None
        assert att.pretext is None
        assert att.text is None
        assert att.author_name is None
        assert att.author_link is None
        assert att.author_icon is None
        assert att.title is None
        assert att.title_link is None
        assert att.fields is None
        assert att.image_url is None
        assert att.thumb_url is None

    def test_all_params(self):
        fields = [{"short": True, "title": "F", "value": "V"}]
        att = Attachment(
            fallback="fb",
            color="#FF0000",
            pretext="pre",
            text="body",
            author_name="author",
            author_link="https://author.com",
            author_icon="https://author.com/icon.png",
            title="Title",
            title_link="https://title.com",
            fields=fields,
            image_url="https://image.png",
            thumb_url="https://thumb.png",
        )
        assert att.fallback == "fb"
        assert att.color == "#FF0000"
        assert att.pretext == "pre"
        assert att.text == "body"
        assert att.author_name == "author"
        assert att.author_link == "https://author.com"
        assert att.author_icon == "https://author.com/icon.png"
        assert att.title == "Title"
        assert att.title_link == "https://title.com"
        assert att.fields == fields
        assert att.image_url == "https://image.png"
        assert att.thumb_url == "https://thumb.png"


class TestAttachmentPayload:
    def test_minimal_payload(self):
        att = Attachment(fallback="fb")
        assert att.payload == {"fallback": "fb"}

    def test_full_payload(self):
        fields = [{"short": True, "title": "F", "value": "V"}]
        att = Attachment(
            fallback="fb",
            color="#FF0000",
            pretext="pre",
            text="body",
            author_name="author",
            author_link="https://author.com",
            author_icon="https://author.com/icon.png",
            title="Title",
            title_link="https://title.com",
            fields=fields,
            image_url="https://image.png",
            thumb_url="https://thumb.png",
        )
        assert att.payload == {
            "fallback": "fb",
            "color": "#FF0000",
            "pretext": "pre",
            "text": "body",
            "author_name": "author",
            "author_link": "https://author.com",
            "author_icon": "https://author.com/icon.png",
            "title": "Title",
            "title_link": "https://title.com",
            "fields": fields,
            "image_url": "https://image.png",
            "thumb_url": "https://thumb.png",
        }

    def test_partial_payload_only_color(self):
        att = Attachment(fallback="fb", color="#00FF00")
        assert att.payload == {"fallback": "fb", "color": "#00FF00"}

    def test_partial_payload_only_text(self):
        att = Attachment(fallback="fb", text="hello")
        assert att.payload == {"fallback": "fb", "text": "hello"}

    def test_partial_payload_author_fields(self):
        att = Attachment(
            fallback="fb",
            author_name="a",
            author_link="https://a.com",
            author_icon="https://a.com/i.png",
        )
        assert att.payload == {
            "fallback": "fb",
            "author_name": "a",
            "author_link": "https://a.com",
            "author_icon": "https://a.com/i.png",
        }

    def test_partial_payload_title_fields(self):
        att = Attachment(
            fallback="fb", title="T", title_link="https://t.com"
        )
        assert att.payload == {
            "fallback": "fb",
            "title": "T",
            "title_link": "https://t.com",
        }

    def test_partial_payload_image_fields(self):
        att = Attachment(
            fallback="fb",
            image_url="https://img.png",
            thumb_url="https://thumb.png",
        )
        assert att.payload == {
            "fallback": "fb",
            "image_url": "https://img.png",
            "thumb_url": "https://thumb.png",
        }

    def test_partial_payload_pretext(self):
        att = Attachment(fallback="fb", pretext="before")
        assert att.payload == {"fallback": "fb", "pretext": "before"}

    def test_partial_payload_fields(self):
        fields = [{"short": False, "title": "X", "value": "Y"}]
        att = Attachment(fallback="fb", fields=fields)
        assert att.payload == {"fallback": "fb", "fields": fields}
