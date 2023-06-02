RESOURCE_SCORE_BOARD = {
    'grain': {
        0: -1,
        1: 1,
        2: 1,
        3: 1,
        4: 2,
        5: 2,
        6: 3,
        7: 3,
        8: 4,
    },
    'vegetable': {
        0: -1,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 4,
        6: 4,
        7: 4,
        8: 4,
    },
    'sheep': {
        0: -1,
        1: 1,
        2: 1,
        3: 1,
        4: 2,
        5: 2,
        6: 3,
        7: 3,
        8: 4,
    },
    'boar': {
        0: -1,
        1: 1,
        2: 1,
        3: 2,
        4: 2,
        5: 3,
        6: 3,
        7: 4,
        8: 4,
    },
    'cattle': {
        0: -1,
        1: 1,
        2: 2,
        3: 2,
        4: 3,
        5: 3,
        6: 4,
        7: 4,
        8: 4,
    },
}

INITIAL_COMMON_RESOURCE = {
    'wood': 30,
    'clay': 24,
    'reed': 14,
    'stone': 16,
    'grain': 24,
    'vegetable': 16,
    'sheep': 18,
    'boar': 15,
    'cattle': 13,
    'food': 76,
}

INITIAL_PLAYER_RESOURCE = {
    "family": 2,
    "room": 2,
}

LAST_TURN = 3
LAST_ROUND = 3
LAST_PHASE = 13
FIRST_CHANGE_CARD_NUMBER = "CARD_01"

# TODO: 베이스 카드 시작 정보 값
INITIAL_BASE_CARDS = [
    {
        'card_number': "BASE_01",
        'is_stacked': True,
        'count': 1,
        'resource': {
            'wood': 0,
        }
    },
    {
        'card_number': "BASE_02",
        'is_stacked': True,
        'count': 2,
        'resource': {
            'wood': 0,
        }
    },
    {
        'card_number': "BASE_03",
        'is_stacked': False,
        'count': 0,
        'resource': {
            'reed': 1,
            'food': 1,
            'stone': 1,
        }
    },
    {
        'card_number': "BASE_04",
        'is_stacked': True,
        'count': 2,
        'resource': {
            'clay': 0,
        }
    },
    {
        'card_number': "BASE_05",
        'is_stacked': False,
        'count': 0,
        'resource': None,
    },
    {
        'card_number': "BASE_06",
        'is_stacked': True,
        'count': 1,
        'resource': {
            'food': 0,
        }
    },
    {
        'card_number': "BASE_07",
        'is_stacked': False,
        'count': 0,
        'resource': None,
    },
    {
        'card_number': "BASE_08",
        'is_stacked': False,
        'count': 0,
        'resource': None,
    },
    {
        'card_number': "BASE_09",
        'is_stacked': False,
        'count': 0,
        'resource': {
            'grain': 1,
        }
    },
    {
        'card_number': "BASE_10",
        'is_stacked': False,
        'count': 0,
        'resource': None,
    },
    {
        'card_number': "BASE_11",
        'is_stacked': False,
        'count': 0,
        'resource': None,
    },
    {
        'card_number': "BASE_12",
        'is_stacked': False,
        'count': 0,
        'resource': {
            'food': 2,
        }
    },
    {
        'card_number': "BASE_13",
        'is_stacked': True,
        'count': 3,
        'resource': {
            'wood': 0,
        }
    },
    {
        'card_number': "BASE_14",
        'is_stacked': True,
        'count': 1,
        'resource': {
            'clay': 0,
        }
    },
    {
        'card_number': "BASE_15",
        'is_stacked': True,
        'count': 1,
        'resource': {
            'reed': 0,
        }
    },
    {
        'card_number': "BASE_16",
        'is_stacked': True,
        'count': 1,
        'resource': {
            'food': 0,
        }
    },
]

# TODO: 라운드 카드 시작 정보 값
INITIAL_ROUND_CARDS = {
    1: [

    ],
    2: [

    ],
    3: [

    ],
    4: [

    ],
    5: [

    ],
    6: [

    ],
}
