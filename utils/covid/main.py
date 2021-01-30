import requests 


def country_total(country):
    BASE_URL = "https://api.covid19api.com/total/country/"
    cases = requests.get(f"{BASE_URL}{country}/status/confirmed").json()[-1]
    deaths = requests.get(f"{BASE_URL}{country}/status/deaths").json()[-1] 
    return (cases['Country'], cases['Cases'], deaths['Cases'], cases)


def country_new(country):
    BASE_URL = "https://api.covid19api.com/summary"
    response = requests.get(BASE_URL).json()['Countries']
    data = [i for i in response if country in [str(e).lower() for e in i.values()]][0]
    return (data['NewConfirmed'], data['NewDeaths'])


def world_total():
    BASE_URL = "https://api.covid19api.com/summary"
    data = requests.get(BASE_URL).json()['Global']
    return (data['TotalConfirmed'], data['TotalDeaths'])


def world_new():
    BASE_URL = "https://api.covid19api.com/summary"
    response = requests.get(BASE_URL).json()['Global']
    return (response['NewConfirmed'], response['NewDeaths'])

