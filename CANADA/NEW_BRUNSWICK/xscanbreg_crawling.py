from urllib.parse import quote
# print(response.status_code)
import requests
# from IPython.display import HTML
from bs4 import BeautifulSoup
from lxml import html
from MySQLdb import _mysql
from datetime import datetime
import random
import time
import subprocess
import cloudscraper
import os
import traceback
from urllib.parse import urlencode

scraper = cloudscraper.create_scraper()
try:
    db = _mysql.connect("localhost","root", "", "crawler_db")      

    flag = True
    print('before flag')
    while flag:
        try:
            db.query('CALL `PROCEDURE_KEYWORDS_2_CANBREG`(@p0, @p1); ')
            db.query("SELECT @p0 AS `id`, @p1 AS `keyword`;")
            flag = False
        except Exception as e: 
            print(e)
            continue
    r=db.store_result()
    results=r.fetch_row()

    print(results)
    keyword = results[0][1].decode()
    print(keyword)
    # payload = input("Please add your payload here :")

    # vpn_ips = ["1.2.3.4", "5.6.7.8", "9.10.11.12"]  # Add your VPN IP addresses here

    # def rotate_vpn_ip():
    #     # Choose a random IP address from the list
    #     vpn_ip = random.choice(vpn_ips)
    #     # Set the VPN IP address
    #     os.system(f"netsh interface ip set address \"Local Area Connection\" static {vpn_ip} 255.255.255.0")

    url = "https://www.pxw2.snb.ca/card_online/Search/search.aspx"

    payload = f'CARDScriptManager_HiddenField=%3B%3BAjaxControlToolkit%2C+Version%3D1.0.20229.20821%2C+Culture%3Dneutral%2C+PublicKeyToken%3D28f01b0e84b6d53e%3Aen-US%3Ac5c982cc-4942-4683-9b48-c2c58277700f%3A865923e8%3A91bd373d%3A8e72a662&__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=KPwffYEWrTFW%2BAA0ekdG3M%2BpABwymbtxylq35hGN55F6sjjjFP68xWyYNyqQ5qtBTNTiSx4OwrkWEREK0FY9n504lTKC2Rg6cO4qBbYHXry8xWI0pyYeX5tr5vDMDF8tfKAaMtF%2BtuqXeojOJgHIjzbyax5NFjJlDxGjN5V1hAr7abvJk1t4q8phzijmewCg%2FyMEudI6C04sLTSAzbyyQrPq1HaotTfDdRAniYy5yqrYAmv%2BY9yD9t%2BkPiYSXksoCyedxv23nQvd8lzG75T7a2HJocUbJDfPlvACnLWuLEfwtsaUqVZx2tXnhzYityRNbOTaueQ1vQdsTqAv4CvTLvLoTcD1S0TbAv4FFzgY2kBmBns7QpWzsirlOF4Mxa6ZEev9j5niKQQk5xR3rt%2F4xgGD7RPp1GSJMU%2BFDUatqJApvyILUD9vE5HVk9dvh9PNmScZoteOeAzzMgwD2qHSj12%2FBNOBnc3d7rRmN42j5kYg83uNO3xFrQ%2B4n%2BKop%2FRenjf2JZA0mFE9iYjLX4YOPaBLFTJEDToasZrNgcjH9pUV2KJ6s%2BgkX9Gfak1KZSWj43GlOrdBB9q4hsyNM97aJkUqZFtZ86DHeZo3bfn5eKdU%2Bb1rFt2NeiYk7nEcqsi8Y8yZB%2Bn%2BIDJ55v%2FDstdXU%2BeQg1wJ%2BdoP7k9KXddgE%2Fqm61ZXh8ja2JOEEOP3sDMGgZ9Er0MrDpc6GM7oEHnsH0j88plRWk%2FVmao2GykaPsAcgeDouRf%2FdVdIcVbZIfPhcTtOWEafF%2Fdbm4dEOp%2FBQhLpk%2F2Ug%2BSBW%2FndahxHn7vpkbDBFs5aJI%2Fqe%2FFJ%2FxzlxhsSSeCuleRTv58%2Fz2iO6WqCy%2Fs2At%2FDVZfTvGrdPrQjDNNA7xgSqV5szIsZmATXtq0Kfmb2W8jRp5HxT4LPq4XUboI7ir591zxJBLo2o4%2BiYFcBQ2ysxVyPjQGXFPg0KrxbCKT%2FyR%2FsfcAncNpfGWYzduo4lnQhk4D8VpbmRSRXFOyA4O969z9s4TadwwJJ%2BJiWTy9hKUrkcTfu6%2BX60f5xpbJSF7mAp7nlJNJIzscUvgHc6Q9upwoNQRPjOcwzo3UeSoNaXkZUFu1gAnP6a2YUaqwnGBR834aHiFLva0Xhd6M1S0xheJORNzlkC4G5W9vbSTL4c6XPWI2uThvRcZuQxXrOVHCqLqafNtskzcmae3gXZQ8PiCp9apWnCXfQ2gkv4xrhddgzmCeBMtyEVMWBW8R%2FV8Y2yCceG%2FpXNj6MB6drdBlzYlAIB0kKGb6ppUGOjBI9VIBA36Z2TreaGQ9K7Hvjsz88%2FVR7%2BoaoVyasPmhbg7Y07OKVB%2FWTSQmWhyqJJCIBBJpB7jY3FL8pBheea%2BnpfpuO9vrKrkiCn6frGGwN16hsf9uv2wagLkQb0BNn1RHgwg%2B837s%2BAiieqebFeyR24UiVyQUgauUACJ3cM2OH%2FFJg6VIvlzzAh6ie8am5pAJTtWq%2FVcHnoopZvTLYeJyJGqWgoJP2P4VzN0iF8UHRF29TyTINedZmeYlW%2F96P9XHxbASOWX%2FLjX5zJbejk74CmBqECBpCpwptbuTeDJdR8jvmlVO%2FEkadD4Hr4CTaVlKvJw3KAyQYzUjYYQGtQsL7qGi2ka6Jm%2FON7IezgjxYEyN9PJeBIMkkGStyMX7hQ5C2P8a0wZ2fp0naXNFY7jNvU0dvGUK%2Fzcl%2FPKhONB%2Fsk9NSU95Btpl78H%2BgE3E5slQvVcl6zG2b7dF3B6UP%2BIbyMyN9zLEhPsZ3kfDz%2F6KUd8ZRhyJJZKONBeBlCriWlcXpCsGuU1nYQpBN1AAiLGpSOyw5K0jzYe3bu77eehexI2z1tOgfOrE4hXR8FqDK2XNafr%2FkHt8W9w28AOt%2FRFEIAVLm5G%2ByzVL6f7PJXBtmzsS5B2k%2B3qOpH1%2BrKI3RsMZaXN2InfDm0PTga1mj0PYOLPnD9bEoJZzeMCM1s5GsRzqxD7hz7w4mnKXKUbe2v6ED1zbtoQ%2BfklUwJDfBbiMYzWkTKhHHl98%2FQhQXfi8ZplVxysw3F%2B%2BOXG4BTZpoyNNwvDdF2MAvo9Ad9OgXrIYVRhrF66CmUhpup1y9XUQuWwQa2AZeGcqQKXD4fwqV2arjovimOsbZOV1VdsIP93n09KeJc7HoGVv6RlWTiOpSdgzFGyBFWs0XzxLgdVff86VcO2g1TlgXxN6v09eLh9ceuD%2B44fhpedMEPTlpon5caVrKNQ%2BkBB4zb8kzoZf7mka30lp7JoyFUXVBAwbbjbFZa64VJ5RjGoOjw255zuGbRe7vcPbaLR55FMkMd6q43u9b%2FvV6CIYF7WEfUQqmYH7CbXOYB3cKGJ1GI2HpEHkm%2BgYWGZYnqJXEYKk55F7savsDikcyCjSVlDG9DQFI8NV7cM3qYSwfbufsMxUIyE0HKmS5OBe%2B%2BkCPaYRE140IcAMTQjKUHR%2Bu9ReYQ%2BQUw%2FVUOlK7QYtVf2Pj7pECZCoUOEN5ftmm4zbJ99DNjQYLlPGDOEysjeVsimBGlx1kF8baJCYvz9gcy3%2FCOvUmBbB%2Bl5%2BLH7xn0Qn%2Bfbp5F9NozHi%2BZVhXrEHU6HUfyEKbPrJnbN4GbK%2FpvLkoNrAm27wsw%2BqdWo4ZVq2UAs8MqUx1FVHE8OZi1cZTKdu0YVPtNfOCX1f%2BVkQGWdPtfrEXw5wFktlh%2BYGKP0FmcCWhdoPSx%2By8Ul%2B2NBeq1PWwqFysd%2By%2FxKylcniiWQgkHjFuZn5lSFa%2FHf%2B%2BHmBiCBq9cn5wGj0T3LEEofEp%2BFsI0%2BhMRsCEaq0Bu7UGMozH%2Fw8GZpaJkEzrF7aoOGimHkx5Q5yQsSdJlq7k6fJHgbG%2F%2BsZiPwM88n2m4bpWX%2BtwrG%2F9KUGFscUmS7Nsj%2F%2FYEmWXn%2Bke6Z4iwY28791ujKYGNuUkz46IJnVS2GmEQhbmf7JxloD2HW0BFK6kDlmkxzzO5A%2FXtlavrRCbzqt9ieDf2qiGp1nLwX4wGd6tLW7939fJtbJtCjAkZddvsovONyekL7xr3xHZfpOSdcLhlzk7TsXR3Wq%2BfhJn%2B5FgBMFLTgO0alLSflIiKavBH0QpNV4Zcb2CS21QjJKMbFh5yg4z%2BJ4WHcMUem%2BcgtAd4NI55WDH0gic%2FexQjDBoKqUw5WRNS%2FK9UzwJzGBvfr9Z4PSiLH7sfrZo88bhgHBsnCxCkFuDERYkQGktd9sjOr2w1S%2BXVzovxTD1NmikzfNtNQF9i1gvzY9awU43Xzgfu%2BOXDClbY4M2CLTGaI1tDyRswBLCbMPxrkxNpHQbYEJX6QU%2FhOe9wYREVWjYzw1hEduO6e30ySStX4d74kmYTJtQDkvbZhakkVy7kH0X1EHgQnANgkGSbaUHMGRfSb3PhM12V5tGpoDVRtDEw%2F4cdH3ELSQ1ohFZkW7IHv%2BYj2%2Bop2arpKSLpt93K1YjJz6PWl02WA89L1DCLetCNvk2MelRfWnIgNtZLtYzkkuE%2BCHSuyiTmwm6sF05EM6zO7ITC%2BU9Qa8ws%2BQ0iDWgHwp9Nhy3Vd%2FMO7gGhu9W6dEua8HrY3KBt43c2oJo220ZCDeoEhadM2zUenxOJIhe36b0gCowXoB8ZQOtJWDlc9zjKnv7WaWiE%2FnvQCKA8qUhgVa4AumZQq5i0pCYvvq3v8vlAXTwnSpaL2ztWwvSAftfuF1tV6xlW8vtCMAfyx6C3H88fV6yl2r1GFqXUtLorylELByeLz%2BeVPk7XZT5UY0q%2FNVMOs6wxiIMQRbBI2JbXLmi3Sp1O9a1NOeMKe8FjAjHBgIZr6b5PzD1BdbfIxrYA0ckHD7zbHRJFo2uQ9xCO4jV7oKJ%2BlSTtQRaJi2d%2F76Isf3KgFsy%2B7SDkeD%2FQ7GIhsD%2B2YmIvZIsMVxZ84q%2FPfLWiuzFv3waUwD8BU8JdulXR4358oxNRG9CENlt2FV9rDPnbtxPBjfX4k%2B3ifMezmHnlsmhC%2BwWCYLBuKjqg4%2BVLRC6QkK%2BXQ8GprqHlvzHE%2FJQhkn7mLKqUiB9QwZUzpkVM8QQ%2B%2Fo0L%2BQJHR7k5LJht8QVLckfA6rQKa29U9%2B96GjQCC2vfut0tEK54u2YRaJM7L7sI7TXHT4hDvnCWoVTMCPn8nIPlzYzJIQIVGhASkWondp5Nj3%2F88V8huzNotSCCFFtTKsR7JswgfpiGD%2Bp%2BpVVhzHX2v2Zjqc3tewsSKSsqJCNc2KXVaucQsTe9H9ellyF3Ns4TOSpaxaJyc5coNNje6O3n98cVh0jo7dnN9noBZudZtwnNzBeIbg6wRubB%2FkPtqbL4Okd1lF115xICQW0VzQeO0NUAJeR%2BWFZu0tiT6B3bxC4V%2BR5xpRiMB7AAAK5s1edS3FEcTumHw5hA3gHrU6Jvx9b0XR3d0%2FXJwS3zstvlxr3Xmp1B8egE3BHhlfbY0MQgJTqSztuUVTfJIEIDi3JiA73h8f2jqUh4a3prrl6X5U5tQI4X1A%2B9BjRADOQy1T1DayJK2apEd1%2FqD8uABfmNQQq6YH33EvKr38DoW%2BXvJ5bowVQSsBGZWqXkXDf7y4sfQe4rKs70juinA6nevOZu%2Fp5F8rIPBWZkRgrwWbBePvCLnHEmqugl4a3SzmCVjYrBCOa5MrbuUUgEqrgjgkjvIKWx6VxIniJUG72iQG5MN98yznMdInbJ1IMxx%2BhT0TNcyMTSUt8OP4DJKLT9VJQS2pP%2Fq0mAL%2FnWBLN70OSU%2FwuxYkfem%2BoKJ6d%2BxKxe9C%2BPY1f7Vkl1mDMGSqEEM7drknFFTa0nYj4ujHPcGyvZwievHkL9UQPBgzPVgLPZ8Ykhl7%2BdPJdgcfPrBqvie105iGWmiKmG47R6DWWi6qLaG9bLqzHfqB%2BqfE%2B3ID9DL3ajc35yLRWDy53TcR%2FAvv5TPVPWYLBrwJN18lKB6XLKvmPGF4HlbuoH1NnCUsdF3SBu6aIXm8rrWPmaAFXzJ6D1IWdzz4GmmaW%2FanJawg3T04yqLbayHTmPvVUy37wW8M0yBRDX7H1Gi%2FcamMgKlQXt7qYOZLTL5j75JnIXGkQ%2F%2BsKc49gBBgQw%2Fn0D3qK10fDqwU79PerCVeqtbu6Km0kfEt75LbQj3mi0Nj71XkSy%2BWIbp0sfAk9nhSogr%2BTuMgyzWYL6NGP2ErQDO%2BN8jbisMZU%2F2S%2Fid4Dokc32eYKbvMtMD%2B2sZId2NHgphxi0QJNgBHg%2B%2BwWz6QliUBpFflVnhZd5fsoRpNYA6LH3xLLS0AXUUooO%2FuP2nCHJAQPXUDoFQAw47sAY9rLznBuZSqOKGfuLR%2B%2BcUkzVQ%2FHPOU1L8kc%2Fgwc2ULVEehJ023t1NdhXkk4B46hOg2bG%2FPRBrXpe%2FQHIz71gMt0czTfbnDD8eP3VtujHehW7XPmqzvR189CkQaVAFrCT4y5cu7ynxwl2M%2FDDm7KPL%2Fjm%2BLu8%2FCQCiilsjF1NjdWGEYwQ8thILsBN%2BZeOv1cehu58lvfLRLZimXQoiKRD46%2FyXkrwjc%2Fy31lXwprHcsClHK%2FLcgX06kXCHXlod1lQBB6CxVEf%2FqflDseY2%2Faf%2BC46SpBI%2BblCxdOtBqlYFv54ooJidts3uSH%2BXDuwkW%2BtUM9qn68ioeuxw%2FskOGghJC33k8Y%2FfhGYZz7bPCL5YpX3duW6Kv1h20AxiuYA7m5lLWxCmlJwlsK1hrLgvz9CVrp0Cajep9V5OsG8q3b9Ed%2FGZ55fE99R3ViNiyS&__VIEWSTATEGENERATOR=7CB58EAD&__EVENTVALIDATION=AEug19G44ZPWq7NLN%2BDmmOv2KFPCOE7cb6Ex8s7v1rzFCICAEVln4vQ0TvESyP9Vt77FOgwZ2uOf%2FfW2on5fA%2FJmRgmfakyKWV31vvDyXEvfiXHHsIMfFT0JHQCGTdbR2rzO2bJ8c6x1sXWVltvJ2mKnweJDUUaBu%2Bz6rXNSiAzlKQPT%2FN5jd2%2BK0gNqNuEeYMoNzVX0LnOI%2B%2F7d9TJEWp9zRAKVKXJ2Rh9Xg75KxEhJHcULvnTtCeb1OZkMmeeakwP3Hndq%2BCjUYdePfXVRuIkwekj0x80aGd%2FmUy1WvEE5DvcbYHd72STcoCki4CpDrAL7L%2FUq8dEnpx2n4Kovbg%3D%3D&ctl00%24cphMain%24txtBusinessNumber=&ctl00%24cphMain%24txtReferenceNumber=&ctl00%24cphMain%24txtKeyWordSingle={keyword}&ctl00%24cphMain%24btnKeyWordSingle=Search&ctl00%24cphMain%24txtKeyWordCombined=&ctl00%24cphMain%24txtKeyWordCombined2='

    # payload = f'CARDScriptManager_HiddenField=%3B%3BAjaxControlToolkit%2C%20Version%3D1.0.20229.20821%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D28f01b0e84b6d53e%3Aen-US%3Ac5c982cc-4942-4683-9b48-c2c58277700f%3A865923e8%3A91bd373d%3A8e72a662&__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=fYN%2FpGne1cjTuEWXRcUsDEtGbn2OQAJ0bAwkjdTUuqpr5Xnto%2B4AWRoXEmGZaPt27eGRwBEnVbp9t6cktulUktpfUbuhRJnk2UyuSbkTV6DKfxFnZ3dp8mszL63pQSHzmOZ5bnqDRcmjSRkVY8oVouVBkOUeZuLibjAruhT%2F57lRwTbI9b0zv9G5H385pQQoFlEO9wQdaLbf1XjC8WBvuYD%2BHxkEVfl7K1mWyyFD%2Bo8AiubRfIw7mS%2FJcCXEb8xOqg1FEtt8mHczurxlHN0XbUNocjojUcNI7XuOzNT72UO2Kv9U9dIg4XHdZFsADo%2FESLujVK6NnnPhMBN9tJwU4XNnEeGauSA4cdKmh9YAWKU8B%2BOWwDne9YLJy8qZqKEPqzlnFY0cG7xnK1M2oSQdkReyQTjCcGVtjPd3uO0UuMwD5pPgyZhNZy8bpmHhXeZk47dgurhf1ukBxva94W6tZbhTpebfw9JS7bJZXTaJLbE%2Fdau0ZbJI%2FW5VCYvg3ozJ6YHtZIkmD%2BrduJUGIHBVb%2BhuSalA%2FZB%2BmSSZOPvDOy08cDd3mGBs2QZq5owJVJrGCkNCnfkux5Yhl%2FIkYrkb%2B0b9uRblDXe%2BJuhpVUqr82y7DQEWk8%2FbHK6y58029lRz12KFZM7FzhXxy8fIw%2FKM92uE25Gjy3rH%2F0HB1RZMgV21xgu3ts5V9mFAMjg7%2BfWohwVn5XMDhz2ZJMRguoxGmLS5R3NiQK6F4viOXYTcfS3kVC5hVwg69if2UFlbkTqAm8b4%2FXVdsrsqhwLEtigkw%2FLEVI5hBSigCabAOFbLOAgiM5bFGpU0vIhnf7JyQR4RPah8slTL%2FVg3tGVZcsX7J5Mx3PqgEhjQ7jC%2Fzrr52LeDuNyM2wrGvOshlHWTT%2BFFebIkVQNrUmryyA%2ByhGPy8jn2wx4kQejXfBF5FUFGhdB%2BRqQ29MUTnMENF9KzoNlX77VD%2B4f9nsfs%2B2Ibq7Uyk5ay6OVpNT8Lzz0lQjyxRA5wbiBcFLYB7lEDjOKuompcknFmfuy2aarsbI%2FjC8gPYh5D7NQxdGqWZ1LWfnRpQwZG2%2FSI3WcMM5t962Jhyjk%2B5TmGTrTUa7IsboxYGVAbiwWKo1ZnwgB1ZPDeE198bbAMuTII%2BBDLNCBysg7HABvEHMzeKVADTU6P%2Fm6C%2FWf4%2Fv%2BOWxA%2B5boWrDrq%2F3eFYEI07S8i%2F6RjA8syt0dJpElIXXbwZ6H8OMTivlr0qwI4I4AVNEmELC9I%2BYX2nu9eEQhaAwcpMqU79kjlC2pPJFu120zsGEP5qxKSYoK3ZB8AC%2FdI213F2xtxr3iqiN96Xg4Hpyii0lBu6M76ELCLpNKWRQhodGoZPphIu3m3plo21KPZJLH5cQe1Z6ZSpvRPjlxDRxl1GO5ZtIqwZuCot9ODqsxd0tW3coJyQJayELww6cl%2BLbicfsJaFHU6llH3B4Co328sgkN0NRd80Hv5LLRsRcDmO7%2BW%2F%2BRSX4u4Amx0mgXbcYLtX0E5Vo0IbZeofqvjVdpGRniB6c8qZXzGLxdnQ1UgmK9WYxe8nYRyAYZWG6uaNwQqu0dkXryaJS4D3c95JzJIX17UhJbb4lUmHHXPuoc5pTuRZ%2F2Q1H8qgyFOTLkuUc2sN8agcnZmsVsV37Yj55FrXJt%2Fg3pWCr4VP%2BGAsPDZBriZQ4geXUUiMA%2FX2o7GoFJ34W4rQvwozQdcqdoZzE9%2FnQJJD6ux1ZgaHV2CDLnD3PqDdkEJhCNmkRpQQKC%2BOZylGjjJ9wHUTZnwTeTwol%2BaqBoltRC6Bl7pGI7IFNjLUQ6%2FRKOBr0Qwpo3cLwopwceHJXzc1rXQ8FhEjS9EHvInrhXiTHGFA7Mcwftx3WkijFuN2G%2FMUAltvpr047kZyt%2F%2BAx3QLQ1Nqlw0kxG1uy5sxBfD%2FZFqTKe4siCjgEvJGuuJmGd2QelAKMHMn0beDLahP2lCaTcCbMLrmk%2F2l8HHSRhsWrfdT1DysOICgJnJ%2BDqcUIK2Jp7OYZy0zap8k9aaHIfAIS2ob%2F9WH8x9wC42DNF2C4a0SJ%2FT1q6PPmBF3rzvoRxFbci3th9X7dHjgBFTeIHULnfrApR%2BAUGJWFhiMNceb1KUKfB6%2Fp2pefLGVK%2FlMpsiG95h9OFhpg07A8c7%2B3VMqQ4r3t7IjrNSWaQYmf5tGR64uEJ75R3mkDAr%2B4IjBXxlNuGDnGKI2G8piYe3pwoVvC%2FW2SDjYYIXUHsqRHfkToaVzCMMwiCLs%2FfnPT%2Fw%2BLT1uNSk4se7H%2Fu%2BlBGu41Cb%2BHVJqjotv3R%2FabwWh0q2hZbWqT00Cb0hjJdmqPdzWDpzmrgfjXlfsf0YKxlg6NF%2FNs9pwi01c1Oj1KGER6TYQ5%2Fsii5AiUnMG61wT0kVqnhLG43RAGHIRXXbXQ04Zu3x51%2BeTxantGbgrWSq3n2p4f%2FYnM2ngoucMcyMQTRo6aWDrxt904wM5%2BFatxyxCz7E2hF0PVapEvJAw96mya86dW6VeP4Zb67rX2pPECmt1XdyBY%2FFzlHnxPIb7SuY27w4CKqdRo86Yx1OF%2FiUAGKvYpUUYQn5Y9Utmo8Bmxjd5PUhEiAdPo8VUTdy9IrfW0eP5fTCUBzfs%2F3r3njkJvIYA%2BL7QONAb0AhHsI1SwkSYU73%2BdMCFF08K3P2aR8NV3S3xXtv%2BWoyccIroVkhGo6kt%2FGTBIax%2FaCoJbPW7VZfyP8wdte9i83nSL5ZgjRmoAkebrOpK4SOVLbW%2BhmUe4ak%2BKw8s5uLZVwN1cazfySNddskhTFR5Kxy9XLeYC6jjDxzZ6XxoktFcPjL4rW11WI4pL%2BEPaC6IN8wvqwkWjltMsfpiHgmaexknz%2Fz8xANKSLQgArheW8%2BXFe%2FEjxvpjcM6rpy9r5FoRp2EkmfPNXUrIKxIBzgj26Ru2Wk8Zu4jTwrDLig0SLWG4oFUkhcKjfO%2Bfp3Mx5tmDrVWuM%2FMU1f4c%2FhzqELZIway4eCQF92CjZABiRz1mPEr06WAErVGt%2BHXGXHdzMtxFtDHvdlm%2BaJ3hFkBQ2bRK0LkwnHSlDSzvhTeT%2FP%2BvVl20bPIEddtdUN57hWUU5B6Kms7xCqJuYPSb1TNvcmpcCnlCk1nDjleMnZSewyZDMoMEio9dsSgPP5UK0RuJ87qhTVLWYwZbHHc%2FVMMfshdFJBLLsohP1Q0JffG%2BH7TcQx4ru80wMpKjltgVBstiMmnECl0igWkiS3vCDUKu8cW6mJY9zD%2FT%2BY01gll2%2FjFBny30QHDP8EPFkUTBTdbKMu%2F%2BWLZBF5n8E72eeYRaepuFWAvQQ5Ous5cCnmzCWaAuqGycWCU%2BkHSewpPN%2BOKHDtbKsCVC123epzIaAo4Nu6wZ48tje6EfHRSpaCQMFieh%2BpBJvTB%2BYPfSKdgC1WZ%2F8Qt3800uU9hDMdUY90TYlL3MNYDdT3uHzjIfp9u5M6bUWJuI0KwYb7L7OVgNYR9wXhu8E2pppDy6jZ1XZUpYAm%2F%2B8p63y5AmWWe1o1%2FVtxEMv8cy5jVd4jHk4qMh0ZhQe1TwN83rI33J1cklER%2F7u3EEkp74Qt6QUShy28MwHXFwI5rxrKyAEbeHxRvO5R3W8l17vNUOBpWXwKtJe%2FtFEfEjI2g0i%2Bx6YDZh0KN5F9wE%2B2hGmdlXj88DR6N%2FLK103K%2BW0mF2Wnw4cmqZXGHtlDIlN7J4wTmHHpd3WovkcF%2FTKWv%2F3yukCoftdTd%2B26sue9xFQ%2BAJnSIKmEYBTQZMNCadflctG103gbKajhMzBj7CeARbf%2B1F1QcVgftMeM6sWaF6E2muaH4P21T4EOxTtg7wx0%2B2vCSdvRRQUJx8UHqLTV5Mg8EnGTXByrN3YyRrawywCH8VDrY0NJ0VtchArNH%2BIiewcxih%2BMh7MYYh8ARtATWa9xyJrvncqNlfgLeteCDLQBxGe%2B7qt2XRRL05WRjAVQAq6FkZuhA5JjjCgr%2FcPPww7mvtjgzakkO3SAKKoA%2FinfKMmitt6M%2BWqBkTfetd4Kjs0U76RN192Khj0CCgcQcRMw%2B5QjEShNhy2DmR0H4doahQuRTmWhDaRpssExED25pL8NsGev0K5hPWW1WXmSTI2K0P3eJBdctD%2BORf9IQ5R1gCXM4pHvh51Q1uzSVNdWh5Ac91OxWQtRR0OxANbpFHXpadpBB5Pqji8senTF5wGO4jP856Rch5Nv%2BM3r1AtOIq6aFAbQZ8ifTUID5Srd1915VwD%2FC%2B7%2FCYSu4a%2BMVIj6ae%2F3JjeaIAp5MV0bzCnF0rlSJ919CQuMI0zQZXZ3areDDqzH0AMzLuXk%2FJZ312afanqjKPHNqv520XFDblgSg5OIdF1AICefENv9R6TTWmpTKTXOlntYz7hKuWBFCp0%2Fh9oqrPI4QDdY9g73XyHMTuLBQDXLIB4LiBROTP4yi1uwiBH4%2FbEF0jzcnVCv7U3P1%2Bh1tMJpGAPYSj00lktzRKTY7KArLRGiRYEvQISfuH3HsVjxNcO8O4827%2FxRgz2i1t64qHVhEzkUwzgrPu86d%2FvN47hP7k3UZntfUVpxbRiubNFXahgPxhEP%2F48pQbGCa33J9hhvvMUQHfoU9uLJDzUzPXEfA48MV5rSYs5WOi%2FIqRd7akveIun7uwEoy42vcuDfsPGCFlSgINVbzhw8YpZUrQJMSW1pAqScn%2F9AH32YJjUIppbawt2aiFmTad%2BRBUbSPIcfhZkrVpgT1GePlnzucTUkYDphmR5iPMqCc2xwMKoyDlD%2BBw931X4kcnpAr0DSVykgp701UyofWDzrEyjt18mBfC%2Bn3Tl%2FDmCZYD58vxaPZfVxD1hioYl%2FvMQnA9XORUjctQr84mreBvhZJKb1mYqiDdzZUiVNgs4fxkxwrrFWm%2BMvCqLmYV2M3C3wM3OnQSxd1AUPaeQma75RhWKROi8ARUeHtFb6J2uZ9byaoyIGnnh7r%2BTGELC7F8WuofZCgpHMSmqlQJIqSTa9%2FS8DcxOENBeqYa4JxyPIF3rWXnIp%2BvE260n1%2FTSVOAaXWmXXdFQCNTA3YxUJj3PpiYtXtGZDKLCqVPWaS3OVxwcqVGPXxi102IRszRDSznA4cmVdbFuI%2FjsCbl1XGNy1LXoaxZ%2FwilOzA1vKMUNQOv4Aj%2BHBwQnF7hkKlsVhjfcSuA39toEa7i%2BPEz6TmBnD0dUBdYr2g33rONLU2CpTShXgEhvPpvj5rAxa1Vq0lpatADqPHtft7AW%2BelikkQU2rcKWDVMbplnHyCNqs0JDjkzDfcPgks2mr7DX18KfsLWVvJJQZqdX9XcE%2FdsZdrnI6xkuhOeCYUyZOuwrEKOtM%2BMWfxglF52qryXTKWtIawPil%2BWZNMp3iXF0qiJVoevsumbQVe%2BtG4Fj2671Rul2lPLmBG05yYptI5Qs0hYtiPdeG1YdmIjuRTuiN5OC2rv0WStFi8IGBApIhOVzgBvDYxkdigUT2bgXVb8N64LOMvnN03urCamrZEqVyCJQIjKyvzpEMjNdxNZapTGwVBEOabbdr5beURShrc3ihm3gJ0dNO2oWKHFRctKQ%2BAZmBxm3qLKFeF9xlKYxtfHj6lu9w1uFYKQJDu%2FG7pxgKdTz5X1lqty05dE%2BszfmIjngFgAoYv%2FuIDB8s%2FxlaA4epcb4p7x5p%2BqV4hUPNz69eO6yvFjDb5AVLQzxNDHgyUp%2BfwEyDkh2m%2Bj%2BJKgFkFbE%2F2rPmxc19EMge9&__VIEWSTATEGENERATOR=7CB58EAD&__EVENTVALIDATION=tUq%2F%2FlrlbjiVCacn3LzQ66DfTqh7S9US%2BW%2BuHP3sHkmh4VgRbp14xHY9su2DR%2BC9w0xZnKN2tSU33JEVxH1Vct%2BranGjUNsrHrW4mO30cJSS1BJATmBh9GfUMeMQ9IoyJLvv%2FBn61HZQGF6ttW1uMbZNf6nPNeW1IdFittlI6EsGbXB8ZFoChxijyJnvhgSB1M66EwxZqU3JrtZG%2FHdrrLelKDX5oKY8Jn8QGYc1fgDfH3Hh7UqhGUOpnMqGWIYFT8ZEG4FbolNqjQUTOD3e%2BpMGtsvKyHZpWPpxWYSVlgLqsjGOZmhiwuegnSdgOjtpymRN7SFkwq0I%2Bu8g%3D%3D&ctl00%24cphMain%24txtBusinessNumber=&ctl00%24cphMain%24txtReferenceNumber=&ctl00%24cphMain%24txtKeyWordSingle={keyword}&ctl00%24cphMain%24btnKeyWordSingle=Search&ctl00%24cphMain%24txtKeyWordCombined=&ctl00%24cphMain%24txtKeyWordCombined2='
    headers = {
    'authority': 'www.pxw2.snb.ca',
    'method': 'POST',
    'path': '/card_online/Search/search.aspx',
    'scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Content-Length': '6986',
    'Content-Type': 'application/x-www-form-urlencoded',
    #   'Cookie': 'cf_chl_3=1f3379fcaf2a120; cf_clearance=Vx.KrQKtueZRsz_sSdtidpw9qFwqP3bwjZrSmOq5KVY-1706596188-1-AZvHCvN6//GXLiPVDNXm/ce9LMS5AS34nOjUr0aCx/DKN2OLPOr9vBCxIBUVEcQvuJ4IW9bA4EJ7olWSGEYT2qM=; ASP.NET_SessionId=00q0k1pcqgdqfkgikg2azgkl; CVVFKCLZ=02c0d65ab7-d230-43RK-eGp1CuyIwM3gCiCCnwt4iSHnnkUhKcR6RARBYqGXc9fI1GZi3jYMTTcekShh0vsM; __cf_bm=RaHU_3rMql3kZy3dyMPnC.VmXf4KDiIEGZlDgtQEdKU-1706596192-1-AY6AT8PX+16Z1SI1mkqKp10I3kbBQOn/RujGdq6sJ7gLATMqXKaqS1/BHwTZ7rgMuGVl8dGnKpQGIM+q2Hv0o=; _cfuvid=BFzjexpegoddKJ8FfhXBoLTgW7OEw2m3h2vKyZAZmwM-1706596192446-0-604800000; __cf_bm=6nzs8ZPungjBeAeB3Gp6eke9Q31CoXcC57f5mRL3VEg-1706597459-1-AbgmSSqx2I2sAfOjKXp9NalgKrPQ/tXvMzQqA5O0bpRxEfyPPvuFtpn8MJnK/q7o2V6IrnzdOxhraQjfpfOurkE=; _cfuvid=YOEL52OUGtZp1Yqr8hYbkBngHukCwESvqsjLIB4zSg0-1706597459192-0-604800000',
    'Origin': 'https://www.pxw2.snb.ca',
    'Referer': 'https://www.pxw2.snb.ca/card_online/Search/search.aspx',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Arch': '"x86"',
    'Sec-Ch-Ua-Bitness': '"64"',
    'Sec-Ch-Ua-Full-Version': '"121.0.6167.85"',
    'Sec-Ch-Ua-Full-Version-List': '"Not A(Brand";v="99.0.0.0", "Google Chrome";v="121.0.6167.85", "Chromium";v="121.0.6167.85"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Model': '""',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    proxy_params = {
        'api_key': 'your_scrapops_key',
        'url': url,
    }


    for _ in range(10):
        # rotate_vpn_ip()
        response = scraper.post(url, headers=headers, data=payload)
        # try:
        #     response = requests.get(
        #         url='https://proxy.scrapeops.io/v1/',
        #         headers=headers, 
        #         data=payload,
        #         params=urlencode(proxy_params),
        #         timeout=20,
        #     )
        if response.status_code == 200:
            break
        # except: 
        #     continue


    if response.status_code == 200:
        pageno = 1
        last_pageno = '1'
        with open(f"{keyword}_{pageno}.html", "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"HTML response saved to '{keyword}_{pageno}.html'")

        # Parse the HTML content using BeautifulSoup
        while True:
            # rotate_vpn_ip()
            # time.sleep(random.uniform(3,8))
            try:
                if last_pageno == "<<":
                    try:
                        print('Hello')
                        current_time = datetime.now()
                        query = f"UPDATE KEYWORDS_2_CANBREG SET FLAG = 5, updatedAt = '{current_time}', PAGE = {pageno} WHERE KEYWORD = '{keyword}'"
                        print(query)
                        db.query(query)
                    except:
                        pass
                else:
                    print('Hi')
                    current_time = datetime.now()
                    query = f"UPDATE KEYWORDS_2_CANBREG SET FLAG = 5, updatedAt = '{current_time}', PAGE = {pageno}, LAST_PAGE ={last_pageno}  WHERE KEYWORD = '{keyword}'"
                    print(query)
                    db.query(query)

            except:
                pass
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find the input tag with name="__VIEWSTATE"
            viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
            viewgen_input = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})
            eventval_input = soup.find('input', {'name': '__EVENTVALIDATION'})
            cardscript_input = soup.find('input', {'name': 'CARDScriptManager_HiddenField'})

            # Extract the value attribute of the input tag
            if viewstate_input:
                viewstate_value = viewstate_input.get('value')
                print(f"__VIEWSTATE value: {viewstate_value}")
            else:
                print("__VIEWSTATE input not found on the page.")

            if viewgen_input:
                viewgen_value = viewgen_input.get('value')
                print(f"__VIEWSTATEGENERATOR value: {viewgen_value}")
            else:
                print("__VIEWSTATEGENERATOR input not found on the page.")

            if eventval_input:
                eventval_value = eventval_input.get('value')
                print(f"__EVENTVALIDATION value: {eventval_value}")
            else:
                print("__EVENTVALIDATION input not found on the page.")

            if cardscript_input:
                cardscript_value = cardscript_input.get('value')
                print(f"CARDScriptManager_HiddenField value: {cardscript_value}")
            else:
                print("CARDScriptManager_HiddenField input not found on the page.")
                

            url1 = "https://www.pxw2.snb.ca/card_online/Search/results.aspx"

            q_viewstate = quote(viewstate_value, safe='')
            q_viewgen = quote(viewgen_value, safe='')
            q_eventval = quote(eventval_value, safe='')
            q_cardscript = quote(cardscript_value, safe='')
            page_number = int(pageno)+1
            print("page_number :", page_number)
            payload1 = f'CARDScriptManager_HiddenField={q_cardscript}&__EVENTTARGET=ctl00%24cphMain%24gvResults&__EVENTARGUMENT=Page%24{page_number}&__VIEWSTATE={q_viewstate}&__VIEWSTATEGENERATOR={q_viewgen}&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION={q_eventval}'


            # print(payload)

            headers1 = {
            'authority': 'www.pxw2.snb.ca',
            'method': 'POST',
            'path': '/card_online/Search/results.aspx',
            'scheme': 'https',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Content-Length': '21462',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.pxw2.snb.ca',
            'Referer': 'https://www.pxw2.snb.ca/card_online/Search/results.aspx',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Arch': '"x86"',
            'Sec-Ch-Ua-Bitness': '"64"',
            'Sec-Ch-Ua-Full-Version': '"120.0.6099.225"',
            'Sec-Ch-Ua-Full-Version-List': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.225", "Google Chrome";v="120.0.6099.225"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Model': '""',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            proxy_params1 = {
                'api_key': 'your_scrapops_key',
                'url': url1,
            }

            # response = scraper.post(url1, headers=headers, data=payload1)
                # rotate_vpn_ip()
            response = scraper.post(url1, headers=headers1, data=payload1)
            # try:
            #     response = requests.post(
            #         url='https://proxy.scrapeops.io/v1/',
            #         headers=headers1, 
            #         data=payload1,
            #         params=urlencode(proxy_params1),
            #         timeout=20,
            #     )
            # except: 
            #     response.status_code = 400
            #     print(traceback.print_exc())
            #     continue
            # print(response.text)

            if response.status_code == 200:
                # Parse the HTML content using lxml
                tree = html.fromstring(response.content)
                pageno = tree.xpath('//tr[@class="gvPager"]//span/text()')
                pageno=pageno[0]
                try:
                    last_pageno_arr = tree.xpath('//tr[@class="gvPager"]/td//td[last()]//text()')
                    print('last_pageno:', last_pageno_arr[0])
                    last_pageno=last_pageno_arr[0]
                except:
                    pass

                with open(f"{keyword}_{pageno}.html", "w", encoding="utf-8") as file:
                    file.write(response.text)
                print(F"HTML response saved to '{keyword}_{pageno}.html'")

                if last_pageno == "<<":
                    continue
                elif last_pageno == pageno:
                    current_time = datetime.now()
                    for _ in range(5):
                        try:
                            query = f"UPDATE KEYWORDS_2_CANBREG SET FLAG = 10, updatedAt = '{current_time}', PAGE = {pageno}, LAST_PAGE ={last_pageno}  WHERE KEYWORD = '{keyword}'"
                            db.query(query)
                            break
                        except:
                            continue
                    break
            else:
                print(f"Error: {response.status_code}")

        # print(display(HTML(response.text)))
    else:
        print(f"Error: {response.status_code}")
except:
    print(traceback.print_exc())
finally:
    try:
        db.close()
    except:
        pass

try:
    subprocess.run(["aws", "s3", "mv", "./", "s3://dev_buk/DATA/CANBREG/BULK/TODO_2/", "--recursive", "--exclude", "*", "--include", "*.html"], check=True)
except: pass