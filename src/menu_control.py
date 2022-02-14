import pytz
import requests
from datetime import datetime
from bs4 import BeautifulSoup

USP_URL      = 'http://www.puspsc.usp.br/cardapio/'
CLOSED_ALERT = 'Bandeco fechado ...'
CHANGE_ALERT = '(este cardápio poderá ser alterado sem aviso prévio)'

DEFAULT_CONTENT_LEN = 7

DAYS_RELATION = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]
PERIODS_RELATION = {
    'AM': 'Almoço',
    'PM': 'Jantar'
}

def get_index_containing_substring(strings, substring):
    for idx, s in enumerate(strings):
        if substring in s:
            return idx

    return None

class Meal:
    def __init__(self, title, content):
        self.title = title
        self.base  = content[0]

        if self.base != CLOSED_ALERT:
            self.gif_tag = 'food'
            self.salad   = content[1].split(': ')[-1]

            dessert_idx = get_index_containing_substring(
                content, 'Sobremesa:'
            )
            veggie_idx     = 3
            garnish_idx    = dessert_idx - 1
            additional_idx = len(content) - 1

            self.garnish = content[garnish_idx]

            not_veggie = content[2]
            veggie     = content[veggie_idx].split(": ")[-1]
            if garnish_idx - veggie_idx > 1:
                extra_content = ' '.join(content[veggie_idx + 1:garnish_idx])
                veggie += f' {extra_content}'
            self.main    = f'{not_veggie} ou {veggie}'

            self.dessert = content[dessert_idx].split(': ')[-1]
            if additional_idx - dessert_idx > 1:
                extra_content = ' '.join(content[dessert_idx + 1:additional_idx])
                self.dessert += f' {extra_content}'

            self.additional = content[additional_idx]
        else:
            self.gif_tag    = 'no'
            self.garnish    = None
            self.main       = None
            self.salad      = None
            self.dessert    = None
            self.additional = None

    def __str__(self):
        meal_data = [f'{self.title}\n']
        if self:
            meal_data += [
                f'🍚 {self.base}',
                f'🍛 Guarnição: {self.garnish}',
                f'🍳 Principal: {self.main}\n',
                f'🥗 Salada: {self.salad}',
                f'🍫 Sobremesa: {self.dessert}',
                f'🥖 Adicionais: {self.additional}'
            ]
        else:
            meal_data += [self.base]

        return '\n'.join(meal_data)

    def __bool__(self):
        return ( self.base != CLOSED_ALERT )

class Menu:
    def __init__(self):
        self.url          = USP_URL
        self.current_menu = None
        self.current_meal = None

    def __scrape_menu_data(self):
        r    = requests.get(self.url)
        soup = BeautifulSoup(r.text)

        tr_condition = lambda tag : 'odd' in tag if tag else False
        data = filter(None, map(
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

    def update_current_meal(self, date=None):
        self.__scrape_menu_data()

        if date:
            weekday = date[0]
            period  = date[1]
        else:
            curr_date = datetime.now(pytz.timezone('America/Sao_Paulo'))
            weekday   = curr_date.weekday()
            period    = curr_date.strftime('%p')

        day = DAYS_RELATION[weekday]

        content = list()
        if day in self.current_menu:
            content = self.current_menu[day][period]

        if not content or not content[0]:
            content = [CLOSED_ALERT]

        title = f'{PERIODS_RELATION[period]} {day}'

        self.current_meal = Meal(title, content)