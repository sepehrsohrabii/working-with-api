from bs4 import BeautifulSoup

soup = BeautifulSoup(open('origin.html'), "html.parser")
values = soup.findAll('option')

with open("origin-output.html", "w") as file:
    for text in soup:
        result = text.get_text().strip()
        print(result)
        file.write('\n'+str(result))
