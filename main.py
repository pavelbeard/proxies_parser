import base64
import requests
import lxml
from bs4 import BeautifulSoup


def get_free_proxies():
    cookies = {
        '_ga_FS4ESHM7K5': 'GS1.1.1705677959.1.0.1705677962.0.0.0',
        '__gads': 'ID=91f23da8c048a814:T=1705677960:RT=1705677960:S=ALNI_MYj6nCcz6LcAft5A-0RxprLgWxu4w',
        '__gpi': 'UID=00000cfb631bc968:T=1705677960:RT=1705677960:S=ALNI_MYpUefy3jbB-_vi64YmFt7hQwaRnQ',
        '_ga': 'GA1.1.1104839935.1705677960',
        'fp': '8866c7f0496ac107f521d76daade4053',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Cookie': '_ga_FS4ESHM7K5=GS1.1.1705677959.1.0.1705677962.0.0.0; __gads=ID=91f23da8c048a814:T=1705677960:RT=1705677960:S=ALNI_MYj6nCcz6LcAft5A-0RxprLgWxu4w; __gpi=UID=00000cfb631bc968:T=1705677960:RT=1705677960:S=ALNI_MYpUefy3jbB-_vi64YmFt7hQwaRnQ; _ga=GA1.1.1104839935.1705677960; fp=8866c7f0496ac107f521d76daade4053',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'free-proxy.cz',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
        'Referer': 'http://free-proxy.cz/en/',
        # 'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }

    session = requests.Session()
    src = session.get('http://free-proxy.cz/en/proxylist/country/US/http/ping/all', cookies=cookies,
                      headers=headers)

    soup = BeautifulSoup(src.text, "lxml")

    options = soup.find("select", id="frmsearchFilter-country").find_all("option")

    print("[INFO] Available countries:")

    for option in options[1:]:
        short_name = option.get('value')
        full_name = option.text.split(' (')[0]
        print(f"Country: {short_name}/{full_name}")

    select_country = input("Select country: ")
    url = f"http://free-proxy.cz/en/proxylist/country/{select_country}/http/ping/all"

    print(url)
    print("[INFO]: Please, wait for data...")

    proxy_list = requests.get(url=url, cookies=cookies, headers=headers)

    if proxy_list.ok:

        table_trs = soup.find("table", id="proxy_list").find("tbody").find_all("tr")

        ip_list = []

        for tr in table_trs:
            try:
                ip = tr.find("td").find("script").text
            except Exception as ex:
                print(ex)
                continue

            if ip:
                ip = base64.b64decode(ip.split('"')[1]).decode("utf-8")
                port = tr.find("span", class_="fport").text
                ip_list.append(f"{ip}:{port}")
            else:
                continue

        with open("ip_list.txt", "w") as writer:
            print(f"We have {len(ip_list)} proxies.")
            writer.writelines(f"[+] {ip}\n" for ip in ip_list)
    else:
        print("Something went wrong...")


def main():
    get_free_proxies()


if __name__ == "__main__":
    main()
