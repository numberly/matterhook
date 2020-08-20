class Attachment:
    def __init__(
        self,
        fallback: str,
        color: str = None,
        pretext: str = None,
        text: str = None,
        author_name: str = None,
        author_link: str = None,
        author_icon: str = None,
        title: str = None,
        title_link: str = None,
        fields: list = None,
        image_url: str = None,
        thumb_url: str = None,
    ):
        self.fallback = fallback
        self.color = color
        self.pretext = pretext
        self.text = text
        self.author_name = author_name
        self.author_link = author_link
        self.author_icon = author_icon
        self.title = title
        self.title_link = title_link
        self.fields = fields
        self.image_url = image_url
        self.thumb_url = thumb_url

        payload = {"fallback": self.fallback}
        if self.color:
            payload["color"] = self.color
        if self.pretext:
            payload["pretext"] = self.pretext
        if self.text:
            payload["text"] = self.text
        if self.author_name:
            payload["author_name"] = self.author_name
        if self.author_link:
            payload["author_link"] = self.author_link
        if self.author_icon:
            payload["author_icon"] = self.author_icon
        if self.title:
            payload["title"] = self.title
        if self.title_link:
            payload["title_link"] = self.title_link
        if self.fields:
            payload["fields"] = self.fields
        if self.image_url:
            payload["image_url"] = self.image_url
        if self.thumb_url:
            payload["thumb_url"] = self.thumb_url

        self.payload = payload
