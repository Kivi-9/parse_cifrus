import requests
import xlsxwriter

from bs4 import BeautifulSoup


def checkRating(stars):
    countStars = len(stars)
    if countStars == 0:
        return "Нет отзывов"
    else:
        return countStars

def writing(nameList,imageList,linkList,priceList,ratingList,codeList):
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    my_dict = {
        "№": range(1, len(nameList) + 1),
        "Модель": nameList,
        "Изображение": imageList,
        "Ссылка": linkList,
        "Стоимость": priceList,
        "Оценка": ratingList,
        "Артикул на сайте": codeList
    }

    alignCenterBold = workbook.add_format()
    alignCenterBold.set_align('center')
    alignCenterBold.set_bold()

    alignCenter = workbook.add_format()
    alignCenter.set_align('center')

    col_num = 0
    for key, value in my_dict.items():
        worksheet.write(0, col_num, key, alignCenterBold)
        if (col_num > 3 or col_num == 0):
            worksheet.write_column(1, col_num, value, alignCenter)
        else:
            worksheet.write_column(1, col_num, value)
        col_num += 1
    worksheet.autofit()
    workbook.close()
    print('Данные записаны в output.xlsx')
def parse(url):
    # url = 'https://www.cifrus.ru/catalog/smartfony'
    nameList, imageList, linkList, priceList, ratingList, codeList = [], [], [], [], [], []
    payloads = {
        'id_r': '1',
        'id_r3': '25',
        'csol': 'price desc',
        'id_rs': '',
        'start': '0',
        'limit': '120'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"
    }
    rq = requests.get(url,
                      headers=headers, params=payloads)

    if rq.status_code!=200:
        print("Ошибка доступа к сайту")
        return

    soup = BeautifulSoup(rq.text, 'lxml')
    # print(soup)
    cards = soup.find_all('div', class_='product-layout product-list col-xs-12')
    for card in cards:
        name = card.find('div', class_='name').text
        image = "https://www.cifrus.ru" + card.find('img').get('src')
        link = "https://www.cifrus.ru" + card.find('div', class_='image').find('a').get('href')
        price = card.find('span', class_='price-new').text[6:]
        rating = checkRating(card.find_all('i', class_='stary'))
        code = card.find('div', class_='cod_tovar_m').find('span').text
        nameList.append(name)
        imageList.append(image)
        linkList.append(link)
        priceList.append(price)
        ratingList.append(rating)
        codeList.append(code)
        #print(count, name, image, link, price, rating, code)
    print("Данные получены")
    writing(nameList, imageList, linkList, priceList, ratingList, codeList)
def main():
    parse('https://www.cifrus.ru/ajax/sorting.php?id_r=1&id_r3=25&csol=price+asc&id_rs=&start=0&limit=120')



if __name__ == '__main__':
    main()

