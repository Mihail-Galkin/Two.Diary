import requests
from bs4 import SoupStrainer, BeautifulSoup

from app.decorators import only_ajax
from app.schedule import bp


@bp.route('/schedule')
@only_ajax()
def schedule():
    url = "https://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii"
    response = requests.get(url)

    strainer = SoupStrainer("div", {"class": "page-content"})
    soup = BeautifulSoup(response.text, 'lxml', parse_only=strainer)
    for a in soup.findAll('a'):
        a["href"] = a["href"].replace("/media/storage/file/", "https://kpml.ru/media/storage/file/")
        a["target"] = "_blank"
    div = soup.find("div")

    return f'<div class="border rounded-3 p-2 mt-2 shadow">{div}</div>'
