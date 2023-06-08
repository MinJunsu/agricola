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

# FIXME: 테스트 환경을 위해 임시로 자원 수정
# INITIAL_PLAYER_RESOURCE = {
#     'wood': 30,
#     'clay': 24,
#     'reed': 14,
#     'stone': 16,
#     'grain': 24,
#     'vegetable': 16,
#     'sheep': 18,
#     'boar': 15,
#     'cattle': 13,
#     'food': 76,
# }

INITIAL_PLAYER_RESOURCE = {
    "family": 2,
    "room": 2,
}

LAST_TURN = 3
LAST_ROUND = 14
LAST_PHASE = 13
FIRST_CHANGE_CARD_NUMBER = "BASE_08"

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
        {
            'card_number': "ACTION_01",
            'is_stacked': False,
            'count': 0,
            'resource': None
        },
        {
            'card_number': "ACTION_02",
            'is_stacked': False,
            'count': 0,
            'resource': None
        },
        {
            'card_number': "ACTION_03",
            'is_stacked': False,
            'count': 0,
            'resource': None
        },
        {
            'card_number': "ACTION_04",
            'is_stacked': True,
            'count': 1,
            'resource': {
                'sheep': 0,
            }
        }
    ],
    2: [
        {
            'card_number': "ACTION_05",
            'is_stacked': True,
            'count': 1,
            'resource': {
                'stone': 0,
            }
        },
        {
            'card_number': "ACTION_06",
            'is_stacked': False,
            'count': 0,
            'resource': None
        },
        {
            'card_number': "ACTION_07",
            'is_stacked': False,
            'count': 0,
            'resource': None
        }
    ],
    3: [
        {
            'card_number': "ACTION_08",
            'is_stacked': True,
            'count': 1,
            'resource': {
                'boar': 0,
            }
        },
        {
            'card_number': "ACTION_09",
            'is_stacked': False,
            'count': 0,
            'resource': {
                'vegetable': 1,
            }
        }
    ],
    4: [
        {
            'card_number': "ACTION_10",
            'is_stacked': True,
            'count': 1,
            'resource': {
                'stone': 0,
            }
        },
        {
            'card_number': "ACTION_11",
            'is_stacked': True,
            'count': 1,
            'resource': {
                'cattle': 0,
            }
        }
    ],
    5: [
        {
            'card_number': "ACTION_12",
            'is_stacked': False,
            'count': 0,
            'resource': None
        },
        {
            'card_number': "ACTION_13",
            'is_stacked': False,
            'count': 0,
            'resource': None
        }
    ],
    6: [
        {
            'card_number': "ACTION_14",
            'is_stacked': False,
            'count': 0,
            'resource': None
        }
    ],
}

INITIAL_PRI_CARDS = [
    {
        'card_number': "PRI_FAC_01",
        'owner': None,
    },
    {
        'card_number': "PRI_FAC_02",
        'owner': None,
    },
    {
        'card_number': "PRI_FAC_03",
        'owner': None,
    },
    {
        'card_number': "PRI_FAC_04",
        'owner': None,
    },
    {
        'card_number': "PRI_FAC_05",
        'owner': None,
    },
    {
        'card_number': "PRI_FAC_06",
        'owner': None,
    },
    {
        'card_number': "PRI_FAC_07",
        'owner': None,
    },
    {
        'card_number': "PRI_FAC_08",
        'owner': None,
    }
]

NO_USER = -1

RESOURCE_CONVERT_FUNCTION = {
    "PRI_FAC_02": {
        "additional": {
            "reed": 3,
        }
    },
    "PRI_FAC_03": {
        "additional": {
            "clay": 2,
        }
    },
    "PRI_FAC_04": {
        "additional": {
            "wood": 2,
        }
    },
    "PRI_FAC_05": {
        "additional": {
            "grain": 3,
        },
        "always": {
            "vegetable": 3,
            "sheep": 2,
            "boar": 3,
            "cattle": 4,
        }
    },
    "PRI_FAC_06": {
        "additional": {
            "grain": 2,
        },
        "always": {
            "vegetable": 2,
            "sheep": 2,
            "boar": 2,
            "cattle": 3,
        }
    },
    "PRI_FAC_07": {
        "additional": {
            "grain": 3,
        },
        "always": {
            "vegetable": 3,
            "sheep": 2,
            "boar": 3,
            "cattle": 4,
        }
    },
    "PRI_FAC_08": {
        "additional": {
            "grain": 2,
        },
        "always": {
            "vegetable": 2,
            "sheep": 2,
            "boar": 2,
            "cattle": 3,
        }
    },
    "PRI_FAC_09": {
        "additional": {
            "grain": 4,
        }
    },
    "PRI_FAC_10": {
        "additional": {
            "grain": 5,
        }
    },
}

MOVE_ANIMAL_FUNCTION = {
    "move_animal_card": {
        "always": {
            'to': {
                'position': 'index',
                'count': 2,
            },
            'from': {
                'position': 'index',
                'count': 2,
            }
        }
    }
}

INSTALL_FENCE_FUNCTION = {
    "card_number": {
        "aditional": {
            'to': {
                'position': 'index',
                'count': 2,
            }
        }
    }
}

UPGRADE_FIELD_FUNCTION = {
    "room_card_number": {
        "aditional": {
            'to': {
                'position': 'index',
                'count': 2,
            }
        }
    },
    "farm_card_number": {
        "aditional": {
            'to': {
                'position': 'index',
                'count': 2,
            }
        }
    },
    "barn_card_number": {
        "aditional": {
            'to': {
                'position': 'index',
                'count': 2,
            }
        }
    }
}

DUMP_FIELD_FUNCTION = {
    "seed": {
        "aditional": {
            'to': {
                'position': 'index',
                'count': 2,
            }
        }
    },
    "animal": {
        "aditional": {
            'to': {
                'position': 'index',
                'count': 2,
            }
        }
    },
}
