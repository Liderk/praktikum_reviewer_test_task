# лучше импортировать не весь модуль, а конкретный класс -
# from datetime import datetime...
import datetime as dt


class Record:
    # Лучше всегда использовать докстринги с описанием что делает класс/функция
    # что ожидается на вход, что будет на выходе.
    # Это касается всех мест объявления классов и их методов ниже

    # 1. Не понятно что ожидается на вход. Лучше использовать аннотацию типов.
    # 2. В качестве дефолтного значения лучше использовать None
    def __init__(self, amount, comment, date=''):
        self.amount = amount

        # 1. Следует избегать использование условий if с отрицанием:
        # они крайне тяжелы в понимании и рано или поздно сам запутаешься.
        # 2. Вместо тапла лучше использовать переносы строк кода через \
        # если получается длинная строка кода.
        # 3. Для простоты понимания лучше просто указать
        # if date:
        #     self.date = dt.datetime.strptime(date, '%d.%m.%Y').date())
        # else:
        #     self.date = dt.datetime.now().date()
        # 4. Вспоминая дзен питона, лучше писать код который проще к пониманию
        # Простое лучше сложного:
        # можно разбить строку dt.datetime.strptime(date, '%d.%m.%Y').date())
        # на более простые действия и не перегружать код. Как пример:
        # self.full_date = dt.datetime.strptime(date, '%d.%m.%Y')
        # self.date = self.full_date.date()
        self.date = dt.datetime.now().date() \
            if not date else \
            dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:
    # Докстринги и аннотация типов
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # 1. переменная не может начинаться с заглавной буквы.
        # Для нейминга переменных следует использовать snake_case.
        # https://ru.wikipedia.org/wiki/Snake_case
        # 2. У тебя существует класс Record и ты объявляешь переменную Record.
        # Не следует давать одинаковый нейминг переменным/классам/функциям
        # иначе однажды код превратиться в магию.
        for Record in self.records:
            # так как вычисляем в сравнении с конкретной датой, то лучше дату
            # получить один раз, и поместить в переменную до цикла, а не
            # вычислять на каждой итерации цикла for.
            # date = dt.datetime.now().date()
            if Record.date == dt.datetime.now().date():
                # лаконичней и проще использовать оператор +=
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Если какое-то вычисление повторяется 2 и более раза в пределах
            # одного пространства имен, то следует задуматься о том,
            # чтоб провести вычисления один раз,
            # результат поместить в переменную,
            # а переменную уже использовать многократно.
            # today - record.date - можно вывести в переменную

            # очень сложная запись условия сравнения.
            # Можно и нужно сделать проще ( вспоминаем дзен питона -
            # Красивое лучше уродливого.
            # Явное лучше неявного.
            # Простое лучше сложного.
            # Сложное лучше запутанного.).
            # Подумай как упростить условие до вида "x < some_value < y"
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Комментарий лучше перевести в докстринг

        # Переменные из одной буквы не запрещены,
        # но ими надо пользоваться очень аккуратно. В данном случае лучше
        # назвать переменную х как то осмысленно,
        # это облегчит чтение кода как тебе, так и тому,
        # кто будет поддерживать код после тебя
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Данный else избыточен. Его можно убрать, так как уже есть return
        # в случае выполнения условия
        else:
            # Скобки не нужны
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Наименование аргументов в объявлении методов/функци должны быть в нижнем
    # регистре usd_rate=USD_RATE..
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Совершенно бессмысленно переопределять переменную хранящую тип валюты
        # Если использовать в методе напрямую currency вместо currency_type,
        # то ничего не измениться.
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Для улучшения визуального восприятия кода, следует вставлять
        # пустые строки между логическими блоками внутри функций:
        # объявил переменные - пустая строка,
        # сделал логические вычисления - пустая строка,
        # сформировал ответ и возвращаешь результат - пустая строка
        # перед этим блоком.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Использован оператор сравнения, вместо оператора
            # присваивания/деления.
            # Эта строчка не делает ничего в коде.
            # Возвращает булевое значение сравнения и не используется нигде.
            cash_remained == 1.00
            currency_type = 'руб'  # Переопределение наименование валюты лучше
            # делать в пределах одного языка. В предыдущих случаях используется
            # английский, в текущем - русский.
        if cash_remained > 0:
            # Форматирование возвращаемых данных лучше привести к единообразию.
            # Следует выбрать что-то одно - использовать для округления только
            # функцию round, или только через  `:.2f`. Так же в первом случае
            # ответ формируется в виде f строки, в третьем случае
            # в виде функции format - так же нужно выбрать один метод.

            # Правильнее будет избегать использование математических и
            # логических вычислений в f-строках и format.
            # Порой это может привести к неправильным результатам.
            # Лучше значения посчитать отдельно в переменной,
            # а переменную использовать в выбранном методе формирования строки.
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Правильнее все блоки if..elif.. заканчивать блоком else.
        # А условия ставить так, чтоб охватывались все варианты.
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # Нет необходимости перегружать родительский метода,
    # если при этом в него не вносятся изменения,
    # а вызывается этот же метод родительского класса.
    # Если убрать тут get_week_stats, то ничего не поменяется.
    def get_week_stats(self):
        super().get_week_stats()

# Бонус совет/замечание))
# В методе get_today_cash_remained по сути много переиспользуемого кода,
# что нарушает принцип DRY. Делается одинаковые сравнения,
# а затем одинаковые действия со всеми валютами.
# Отличие только в наименовании валюты и ее курсе.
# Можно создать словарь с валютой и ее курсом
# currencies = {
        #     'usd': {
        #         'currency_type': 'USD',
        #         'currency_rate': usd_rate,
        #     },
        #     'eur': {
        #         'currency_type': 'Euro',
        #         'currency_rate': euro_rate,
        #     },
        #     'rub': {
        #         'currency_type': 'руб',
        #         'currency_rate': 1.00,
        #     },
        # }
# А затем упростить код до трех строк:
# currency_rate = currencies[currency]['currency_rate']
# currency_type = currencies[currency]['currency_type']
# cash_remained /= currency_rate
