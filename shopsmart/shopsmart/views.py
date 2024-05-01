from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def index(request):
    return render(request, 'index.html')

def search(request):

    word = request.POST.get('search', 'default')
    # word = word.replace(" ", "+")

    # print(word)
    if word=="":
        return render(request, 'index.html')


    flipcart = f"https://www.flipkart.com/search?q={word}&sort=Relevance"
    # URL = f"https://www.amazon.in/s?k={word}"

    # HEADERS = ({
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    #     'Accept-Language': 'en-US, en;q=0.5'})
    # webpage = requests.get(URL, headers=HEADERS)
    # print(webpage)
    # soup1 = BeautifulSoup(webpage.text, "html.parser")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    d = {}
    r = requests.get(flipcart, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    urls = []
    product_urls = soup.find_all('a', class_='CGtC98')
    i = 0
    for links in product_urls:
        urls.append((links.get("href")))
        if (i == 5): break
        i += 1

    product_titles = soup.find_all('div', class_='KzDlHZ')
    product_prices = soup.find_all('div', class_='Nx9bqj _4b5DiR')
    i = 0
    for title, price in zip(product_titles, product_prices):
        if (i > 5): break
        d[f"title{i}"] = title.text.strip()
        d[f"price{i}"] = price.text.strip()
        d[f"url{i}"] = "https://www.flipkart.com" + urls[i]
        i += 1

    # print(i)
    # --------- ** ebay  ** ---------------
    ebay = f"https://www.ebay.com/sch/i.html?_nkw={word}&"
    headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}
    r2 = requests.get(ebay, headers=headers2)
    soup2 = BeautifulSoup(r2.text, "html.parser")
    product_containers = soup2.find_all('div', class_='s-item__info')

    for container in product_containers:
        if (i == 6):
            i += 1
            continue
        name = container.find('div', class_='s-item__title').text.strip()
        price = container.find('span', class_='s-item__price').text.strip()
        link = container.find('a', class_='s-item__link')['href']
        d[f"title{i}"] = name
        d[f"url{i}"] = link
        if("to" in price ):
            l =price.split("to")
            print(l)
            x = round(( float(l[0][1:]) + float(l[-1][2:]))/2 ,2)
            d[f"price{i}"] = "₹" + str(x)
        else :
            d[f"price{i}"] = "₹" + str(round((float(price[1:])) * 83.43, 2))

        # print(name)
        # print
        # print(link)
        if (i == 10): break
        i += 1



    # print(d)
    # --------- ** amazon  ** ---------------
    # titles = []
    # i = 0
    # product_titles = soup1.find_all('span', class_='a-size-medium a-color-base a-text-normal')
    # for t in product_titles:
    #     titles.append(t.text.strip().split("|")[0])
    #     if i == 2: break
    #     i += 1
    #
    #
    # prise = []
    # i = 0
    # product_prices = soup1.find_all('span', class_='a-price-whole')
    # for p in product_prices:
    #     prise.append(p.text.strip())
    #     if i == 2: break
    #     i += 1
    #
    # links = []
    # i = 0
    # product_links = soup1.find_all("a", attrs={
    #     'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    # for l in product_links:
    #     links.append("https://www.amazon.in" + (l.get("href")))
    #     if i == 2: break
    #     i += 1
    #
    # print(titles)
    # print(prise)
    # print(links)

    # i = 3
    # while i<6 :
    #     d[f"title{i}"] = titles[i-3]
    #     d[f"price{i}"] = prise[i-3]
    #     d[f"url{i}"] = links[i-3]
    #     i+=1

    return render(request, 'search.html', d)


