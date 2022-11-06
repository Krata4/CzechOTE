import asyncio
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

async def get_price():
    url="https://www.ote-cr.cz/services/PublicDataService"
    headers = {'content-type': 'application/soap+xml'}
    #headers = {'content-type': 'text/xml'}
    today = datetime.today().strftime('%Y-%m-%d')
    body = """<?xml version="1.0" encoding="UTF-8" ?>
            <soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:pub="http://www.ote-cr.cz/schema/service/public">
            <soapenv:Header/>
            <soapenv:Body>
            <pub:GetDamPriceE>
            <pub:StartDate>"""+today+"""</pub:StartDate>
            <pub:EndDate>"""+today+"""</pub:EndDate>
            <!--Optional:-->
            <pub:StartHour>1</pub:StartHour>
            <!--Optional:-->
            <pub:EndHour>24</pub:EndHour>
            <!--Optional:-->
            <pub:InEur>false</pub:InEur>
            </pub:GetDamPriceE>
            </soapenv:Body>
            </soapenv:Envelope>
            """
    
    response = requests.post(url,data=body,headers=headers)

    #response = """<?xml version="1.0" ?><SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Body><GetDamPriceEResponse xmlns="http://www.ote-cr.cz/schema/service/public"><Result><Item><Date>2022-06-28</Date><Hour>1</Hour><Price>6718.03</Price><Volume>3831.4</Volume></Item><Item><Date>2022-06-28</Date><Hour>2</Hour><Price>6791.71</Price><Volume>3851.2</Volume></Item><Item><Date>2022-06-28</Date><Hour>3</Hour><Price>6138.23</Price><Volume>3920.6</Volume></Item><Item><Date>2022-06-28</Date><Hour>4</Hour><Price>6304.13</Price><Volume>4105.9</Volume></Item><Item><Date>2022-06-28</Date><Hour>5</Hour><Price>6524.93</Price><Volume>4078.4</Volume></Item><Item><Date>2022-06-28</Date><Hour>6</Hour><Price>6982.59</Price><Volume>3943.0</Volume></Item><Item><Date>2022-06-28</Date><Hour>7</Hour><Price>8841.91</Price><Volume>3625.3</Volume></Item><Item><Date>2022-06-28</Date><Hour>8</Hour><Price>9437.53</Price><Volume>3679.2</Volume></Item><Item><Date>2022-06-28</Date><Hour>9</Hour><Price>9890.00</Price><Volume>3641.6</Volume></Item><Item><Date>2022-06-28</Date><Hour>10</Hour><Price>9191.52</Price><Volume>3330.8</Volume></Item><Item><Date>2022-06-28</Date><Hour>11</Hour><Price>8468.81</Price><Volume>3211.5</Volume></Item><Item><Date>2022-06-28</Date><Hour>12</Hour><Price>7549.78</Price><Volume>3231.8</Volume></Item><Item><Date>2022-06-28</Date><Hour>13</Hour><Price>6852.29</Price><Volume>2924.4</Volume></Item><Item><Date>2022-06-28</Date><Hour>14</Hour><Price>7275.83</Price><Volume>3285.6</Volume></Item><Item><Date>2022-06-28</Date><Hour>15</Hour><Price>7583.16</Price><Volume>3337.3</Volume></Item><Item><Date>2022-06-28</Date><Hour>16</Hour><Price>8102.63</Price><Volume>3367.2</Volume></Item><Item><Date>2022-06-28</Date><Hour>17</Hour><Price>8693.31</Price><Volume>3249.5</Volume></Item><Item><Date>2022-06-28</Date><Hour>18</Hour><Price>9457.56</Price><Volume>3408.1</Volume></Item><Item><Date>2022-06-28</Date><Hour>19</Hour><Price>10666.12</Price><Volume>3613.8</Volume></Item><Item><Date>2022-06-28</Date><Hour>20</Hour><Price>11643.00</Price><Volume>3677.0</Volume></Item><Item><Date>2022-06-28</Date><Hour>21</Hour><Price>11203.89</Price><Volume>3882.8</Volume></Item><Item><Date>2022-06-28</Date><Hour>22</Hour><Price>10160.00</Price><Volume>3894.4</Volume></Item><Item><Date>2022-06-28</Date><Hour>23</Hour><Price>9800.50</Price><Volume>3905.5</Volume></Item><Item><Date>2022-06-28</Date><Hour>24</Hour><Price>8430.98</Price><Volume>3736.6</Volume></Item></Result></GetDamPriceEResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>"""
    root = ET.fromstring(response.content)
    lower_price = 30000
    lower_hour = 0
    average = 0
    SUM_price = 0
    highest_price = 0
    highest_hour = 0
    print(f'{{')
    for item in root.findall('.//{http://www.ote-cr.cz/schema/service/public}Item'):
        Price = item.find('{http://www.ote-cr.cz/schema/service/public}Price').text
        Hour = item.find('{http://www.ote-cr.cz/schema/service/public}Hour').text
        
        SUM_price = SUM_price + float(Price)
        print(f'"{"Hour_"+Hour+""}": {Price},')
        if lower_price > float(Price): 
            lower_price = float(Price)
            lower_hour = int(Hour)
        if highest_price < float(Price):
            highest_price = float(Price)
            highest_hour = int(Hour)

    average = SUM_price / 24
    print(f'"{"Lower_hour"}": {lower_hour},')
    print(f'"{"Lower_price"}": {lower_price},')
    print(f'"{"highest_price"}": {highest_price},')
    print(f'"{"highest_hour"}": {highest_hour},')
    print(f'"{"average_price"}": {average},')
    print(f"}}")

asyncio.run(get_price())