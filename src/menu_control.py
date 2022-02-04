import pytz
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup

LOGGER = logging.getLogger()

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
    'AM': 'Almoço',
    'PM': 'Jantar'
}

class Meal:
    def __init__(self, title, content):
        self.title   = title

        self.base    = content[0]
        self.garnish = content[-2]

        not_veggie   = content[2]
        veggie       = content[3].split(": ")[-1]
        if len(content) > 6:
            veggie += f' {content[4]}'

        self.main    = f'{not_veggie} ou {veggie}'
        self.salad   = content[1].split(': ')[-1]
        self.dessert = content[-1].split(': ')[-1]

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

class MenuScraper:
    menu_url = 'http://www.puspsc.usp.br/cardapio/'

    def __init__(self):
        # self.current_week = None
        self.current_menu = None
        self.current_meal = None

    def __upadate_menu_data(self):
        r    = requests.get(self.menu_url)
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
                'AM': day_lunch,
                'PM': day_dinner
            }

        self.current_menu = menu_data

    def update_current_meal(self, date=None, period=None):
        self.__upadate_menu_data()

        if date:
            weekday = date[0]
            period  = date[1]
        else:
            curr_date = datetime.now(pytz.timezone('America/Sao_Paulo'))
            weekday = curr_date.weekday()
            period  = curr_date.strftime('%p')

        day = DAYS_RELATION[weekday]

        content = self.current_menu[day][period]
        title = f'{PERIODS_RELATION[period]} {day}'

        self.current_meal = Meal(title, content)