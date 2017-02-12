KHL teams data interface
========================
This package is the interface to the KHL teams data. Data are parsed from the resource `championat.com <https://www.championat.com/>`_.

Available data:

- information about players and stats

- information about matches

- team statistics

- meta data

There is possibility to generate ics file from specific events. The title of teams
and parameters statistics are displayed in Russian language only.

Usage
~~~~~

.. code-block:: python

    import datetime

    from khl_team import KHLTeam, KHLEvent

    team = KHLTeam('Локомотив')

    """
    The title of the teams:

    Авангард, Автомобилист, Адмирал, Ак Барс, Амур, Барыс, Витязь,
    Динамо М, Динамо Мн, Динамо Р, Йокерит, Куньлунь Ред Стар, Лада,
    Локомотив, Медвешчак, Металлург Мг, Металлург Нк, Нефтехимик,
    Салават Юлаев, Северсталь, Сибирь, СКА, Слован, Спартак, Торпедо,
    Трактор, ХК Сочи, ЦСКА, Югра.
    """

    # Printing all data:
    for attr in team.__dict__:
        print('%s : %s\n' % (attr, team.__dict__[attr]))

    """
    sponsor :  ОАО "РЖД"

    matches : [
        KHLEvent(Амур - Локомотив, 2016-08-24 12:30:00), KHLEvent(Адмирал - Локомотив, 2016-08-26 11:30:00),
        KHLEvent(Локомотив - Динамо М, 2016-08-29 19:00:00), KHLEvent(Локомотив - Авангард, 2016-08-31 19:00:00),
        KHLEvent(Локомотив - Металлург Нк, 2016-09-02 19:00:00), KHLEvent(Локомотив - Сибирь, 2016-09-05 19:00:00),
        KHLEvent(Лада - Локомотив, 2016-09-08 18:00:00), KHLEvent(Ак Барс - Локомотив, 2016-09-12 17:00:00),
        KHLEvent(Нефтехимик - Локомотив, 2016-09-14 19:30:00), KHLEvent(Локомотив - Торпедо, 2016-09-16 19:30:00),
        KHLEvent(Локомотив - Торпедо, 2016-09-18 17:30:00), KHLEvent(Локомотив - Спартак, 2016-09-20 19:00:00),
        KHLEvent(ХК Сочи - Локомотив, 2016-09-23 19:30:00), KHLEvent(Динамо М - Локомотив, 2016-09-26 19:30:00),
        ...
    ]

    players : [
        KHLPlayer(Павел Евгеньевич Кудрявцев, 84), KHLPlayer(Павел Дмитриевич Красковский, 63),
        KHLPlayer(Денис Андреевич Осипов, 66), KHLPlayer(Роман Сергеевич Манухов, 26),
        KHLPlayer(Егор Алексеевич Коршков, 96), KHLPlayer(Станислав Михайлович Чистов, 41),
        KHLPlayer(Рушан Русланович Рафиков, 87), KHLPlayer(Даниил Юрьевич Апальков, 40),
        KHLPlayer(Егор Валерьевич Аверин, 29), KHLPlayer(Максим  Тальбо, 25),
        KHLPlayer(Дмитрий Евгеньевич Лугин, 19), KHLPlayer(Артём Сергеевич Ильенко, 34),
        KHLPlayer(Патрик  Херсли, 6), KHLPlayer(Андрей Вячеславович Локтионов, 90),
        KHLPlayer(Якуб  Накладал, 22), KHLPlayer(Денис Александрович Мосалёв, 54), KHLPlayer(Брэндон  Козун, 15),
        KHLPlayer(Егор Андреевич Фатеев, 8), KHLPlayer(Владислав Андреевич Гавриков, 4),
        KHLPlayer(Михаил Валерьевич Пашнин, 33),
         ...
    ]

    # Team stats is divided into three parts: the first tuple is total stats, second - home, a third - guest.
    # Percentage values are the average stat value.
    stats : {
        'Выигранные вбрасывания (соперник) (% от возможных)': ('48.3%', '46.3%', '50.1%'),
        'Сыгранные матчи': ('57', '27', '30'),
        'Вбрасывания': ('3236', '1491', '1745'),
        'Разность шайб': [('28', '0.49'), ('20', '0.74'), ('8', '0.27')],
        'Штрафное время': [('626', '10.98'), ('276', '10.22'), ('350', '11.67')],
        'Пропущенные шайбы': [('122', '2.14'), ('55', '2.04'), ('67', '2.23')],
        'Поражения': [('17', '30%'), ('6', '22%'), ('11', '37%')],
        'Буллиты (назначенные / забитые)': [('1 / 1', '100%'), ('1 / 1', '100%'), ('0 / 0', '0%')],
        'Победы по буллитам': [('3', '5%'), ('0', '0%'), ('3', '10%')],
        'Реализация бросков (соперник)': ('8.4%', '8.3%', '8.5%'),
        'Реализация бросков': ('8.3%', '8.7%', '8%'),
        'Броски по воротам': [('1809', '31.74'), ('866', '32.07'), ('943', '31.43')],
        'Буллиты (соперник) (назначенные / забитые)': [('1 / 0', '0%'), ('1 / 0', '0%'), ('0 / 0', '0%')],
        'Заброшенные шайбы': [('150', '2.63'), ('75', '2.78'), ('75', '2.5')],
        'Победы': [('30', '53%'), ('18', '67%'), ('12', '40%')],
        'Поражения в овертайме': [('3', '5%'), ('2', '7%'), ('1', '3%')],
        'Победы в овертайме': [('1', '2%'), ('1', '4%'), ('0', '0%')],
        'Ничьи': [('0', '0%'), ('0', '0%'), ('0', '0%')],
        'Выигранные вбрасывания (% от возможных)': ('51.7%', '53.7%', '49.9%'),
        'Поражения по буллитам': [('3', '5%'), ('0', '0%'), ('3', '10%')],
        'Набранные очки': [('104', '61%'), ('58', '72%'), ('46', '51%')],
        'Броски по воротам (соперник)': [('1449', '25.42'), ('662', '24.52'), ('787', '26.23')],
        'Зрители': [('413365', '7252'), ('225834', '8364'), ('187531', '6251')]}

    president :  Юрий Николаевич Яковлев

    arena : Арена-2000-Локомотив

    location : Ярославль

    head_coach : Алексей Николаевич Кудашов

    team : Локомотив

    site : http://hclokomotiv.ru
    """

    # Match filter.

    # By opponent:
    matches = team.get_match(opponent='СКА', played=True)
    print(matches)

    # Output:
    # [KHLEvent(Локомотив - СКА, 2016-11-13 17:00:00), KHLEvent(СКА - Локомотив, 2016-12-29 19:30:00)]

    # By result (won/lose):
    matches = team.get_match(result='won', played=True)

    # played parameter specifies whether to include games played.

    # Player filter.

    # By number:
    player = team.get_player(number='27')
    print(player)

    # Output:
    # [KHLPlayer(Стаффан  Кронвалль, 27)]

    # By last name:
    player = team.get_player(l_name='Кронвалль')

    # By role:
    players = team.get_player(role='вратарь')

    # Generation of the ics file:
    matches = team.get_match(played=False)
    duration = datetime.timedelta(hours=3)
    remind = datetime.timedelta(minutes=15)

    ics_data = KHLEvent.gen_ics(
        matches,
        title="HockeyEvent: %s - %s",  # Will be inserted title teams.
        duration=duration,
        remind=remind
    )

    with open('hockey_events.ics', 'wb') as ics_file:
        ics_file.write(ics_data)
