import requests
from bs4 import BeautifulSoup

URL = "https://news.ycombinator.com/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

title_elements = soup.find_all("tr", class_="athing")
subtext_elements = soup.find_all("td", class_="subtext")

final_result = []

for i in range(30):
    res = {}
    rank = title_elements[i].find('span', class_="rank").text
    title = title_elements[i].find('span', class_="titleline").text

    res['rank'] = int(rank[:-1])
    res['title'] = title

    try:
        score = subtext_elements[i].find('span', class_="score").text
        comments = subtext_elements[i].find_all('a', href=True)[-1].text

        res['score'] = int(score.split()[0])

        if comments == 'discuss':
            res['comments'] = 0
        elif 'comment' in comments:
            res['comments'] = int(comments.split()[0])
        else:
            res['comments'] = 0

    except AttributeError:
        res['score'] = 0
        res['comments'] = 0

    final_result.append(res)

print(final_result)