from matterhook import Webhook, Attachment
from tabulate import tabulate

url = "https://mattermost.MYCOMPANY.com"
api_key = "API_KEY"

mhw = Webhook(url, api_key)

data = [
    {
        "name": "Monty Python and the Holy Grail",
        "relevant thing": ":rabbit:",
        "date": "1975",
    },
    {
        "name": "Monty Python's Life of Brian",
        "relevant thing": ":innocent:",
        "date": "1979",
    },
    {
        "name": "Monty Python's The Meaning of Life",
        "relevant thing": ":tropical_fish:",
        "date": "1983",
    },
]

markdown_table = tabulate(data, headers="keys", tablefmt="github")

author_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Terry_Jones_Monty_Python_O2_Arena_%28cropped%29.jpg/220px-Terry_Jones_Monty_Python_O2_Arena_%28cropped%29.jpg"  # noqa
author_link = "https://en.wikipedia.org/wiki/Terry_Jones"
thumb = "https://en.wikipedia.org/static/images/project-logos/enwiki.png"

text = "#### Movies\n"
text += markdown_table
text += "\n"
text += "#### Other informations\n"
text += "[Search Wikipedia](https://en.wikipedia.org/w/index.php?cirrusUserTesting=glent_m0&search=monty%20python&title=Special%3ASearch&fulltext=1&ns0=1)"  # noqa

attachments = []
attachment = Attachment(
    "Markdown Table Example",
    color="#00FFFF",
    pretext="This appears before the attachement box",
    text=text,
    author_name="Terry Jones",
    author_link=author_link,
    author_icon=author_icon,
    title="Monty Python",
    title_link="https://www.github.com",
    thumb_url=thumb,
)
attachments.append(attachment.payload)

mhw.send(
    username="Flying Circus",
    icon_url=author_icon,
    attachments=attachments
)
