import requests
from datetime import datetime
from bs4 import BeautifulSoup

DAYS_RELATION = [
    'Domingo',
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-feira',
    'Sexta-feira',
    'Sábado'
]

PERIODS_RELATION = {
    'lunch'  : 'Almoço',
    'dinner' : 'Jantar'
}

class Scraper:
    def __init__(self, url):
        self.url = url
        self.current_menu = None
        self.current_week = None

    def __upadate_menu_data(self):
        r    = requests.get(self.url)
        soup = BeautifulSoup(r.text)

        tr_condition = lambda tag : 'odd' in tag if tag else False
        data = filter(len, map(
            lambda el: el.findAll('td'),
            soup.findAll('tr', {'class': tr_condition})
        ))

        menu_data = dict()
        for element in data:
            week_day   = element[0].get_text().strip()
            day_lunch  = element[1].get_text().split('\n')
            day_dinner = element[2].get_text().split('\n')

            menu_data[week_day] = {
                'lunch': day_lunch,
                'dinner': day_dinner
            }

        self.current_menu = menu_data

    def get_meal_data(self, day, period):
        self.__upadate_menu_data()

        day = DAYS_RELATION[day]

        content = self.current_menu[day][period]
        title = f'{PERIODS_RELATION[period]} {day}'

        return title, content

class Meal:
    def __init__(self, title, content):
        self.title   = title

        self.base    = content[0]
        self.garnish = content[4]

        not_veggie   = content[2]
        veggie       = content[3].split(": ")[-1]
        self.main    = f'{not_veggie} ou {veggie}'

        self.salad   = content[1].split(': ')[-1]
        self.dessert = content[5].split(': ')[-1]

    def __str__(self):
        meal_data = [
            f'{self.title}\n',
            self.base,
            f'Guarnição: {self.garnish}',
            f'Prato principal: {self.main}',
            f'Salada: {self.salad}',
            f'Sobremesa: {self.dessert}'
        ]

        return '\n'.join(meal_data)

URL = 'http://www.puspsc.usp.br/cardapio/'

scraper = Scraper(URL)
title, content = scraper.get_meal_data(0, 'lunch')
today = Meal(title, content)

print(today)