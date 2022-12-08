def get_tests():
    result = [
        {
            'title': 'Кабачки.',  # название теста
            'questions': [
                {
                    'text': 'В строение кабачка входит...',
                    'variants': [
                        'Огурец',
                        'Люля-кебаб',
                        'Мармелад',
                        'Батон'
                    ],
                    'ans': 2
                },
                {
                    'text': 'Кабачок на вкус как...',
                    'variants': [
                        'Кирпич',
                        'Подводная лодка',
                        'Танк Т-34',
                        'Кабачок'
                    ],
                    'ans': 2
                },
                {
                    'text': 'Где произрастают кабачки?',
                    'variants': [
                        'Земля',
                        'Наушники',
                        'Звонок',
                        'Интенсив'
                    ],
                    'ans': 3
                }
            ]
        }
    ]

    return result
