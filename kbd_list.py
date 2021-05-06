def get_kbd(value):
    return globals()[value]


main = {
    'one_time': False,
    'inline': False,
    'buttons':
        [
            [
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Settings', 'payload': '{"type": "page", "value": "settings"}'}},
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Statistics', 'payload': '{"type": "page", "value": "stats"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Control Panel', 'payload': '{"type": "page", "value": "control"}'}}
            ]
        ]
}


settings = {
    'one_time': False,
    'inline': False,
    'buttons':
        [
            [
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Show Report', 'payload': '{"type": "toggle", "value": "report"}'}},
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Show Profile', 'payload': '{"type": "toggle", "value": "profile"}'}},
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Subscribe', 'payload': '{"type": "toggle", "value": "subscribe"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Pushes fo battle', 'payload': '{"type": "page", "value": "battle_push"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Home', 'payload': '{"type": "page", "value": "main"}'}}
            ]
        ]
}

control = {
    'one_time': False,
    'inline': False,
    'buttons':
        [
            [
                {'color': 'positive', 'action': {'type': 'text', 'label': 'Set target', 'payload': '{"type": "page", "value": "target"}'}}
            ],
            [
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Manage associates', 'payload': '{"type": "list", "value": "associates"}'}},
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Notes', 'payload': '{"type": "list", "value": "notes"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Reports List', 'payload': '{"type": "list", "value": "reports"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Home', 'payload': '{"type": "page", "value": "main"}'}}
            ]
        ]
}

stats = {
    'one_time': False,
    'inline': False,
    'buttons':
        [
            [
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Personal', 'payload': '{"type": "stats", "value": "person"}'}},
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Overall', 'payload': '{"type": "stats", "value": "fraction"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Squad', 'payload': '{"type": "stats", "value": "squad"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Home', 'payload': '{"type": "page", "value": "main"}'}}
            ]
        ]
}

battle_push = {
    'one_time': False,
    'inline': False,
    'buttons':
        [
            [
                {'color': 'primary', 'action': {'type': 'text', 'label': 'Enable push', 'payload': '{"type": "toggle", "value": "push"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Text', 'payload': '{"type": "input", "value": "push"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Back', 'payload': '{"type": "page", "value": "settings"}'}},
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Home', 'payload': '{"type": "page", "value": "main"}'}}
            ]
        ]
}

target = {
    'one_time': False,
    'inline': False,
    'buttons':
        [
            [
                {'color': 'primary', 'action': {'type': 'text', 'label': '&#128160; Aegis', 'payload': '{"type": "target", "value": 1}'}},
                {'color': 'primary', 'action': {'type': 'text', 'label': '&#128679; V-Hack', 'payload': '{"type": "target", "value": 2}'}},
                {'color': 'primary', 'action': {'type': 'text', 'label': '&#127541; Hu&#466;qi&#225;ng', 'payload': '{"type": "target", "value": 4}'}}
            ],
            [
                {'color': 'primary', 'action': {'type': 'text', 'label': '&#128305; NetKings', 'payload': '{"type": "target", "value": 5}'}},
                {'color': 'primary', 'action': {'type': 'text', 'label': '&#127482;&#127480; NHS', 'payload': '{"type": "target", "value": 6}'}},
                {'color': 'primary', 'action': {'type': 'text', 'label': '&#128272; Защита', 'payload': '{"type": "target", "value": 7}'}}
            ],
            [
                {'color': 'negative', 'action': {'type': 'text', 'label': '&#10060; Удалить клавиатуру', 'payload': '{"type": "target", "value": 0}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Back', 'payload': '{"type": "page", "value": "control"}'}},
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Home', 'payload': '{"type": "page", "value": "main"}'}}
            ]
        ]
}

lists = {
    'one_time': False,
    'inline': False,
    'buttons':
        [
            [
                {'color': 'positive', 'action': {'type': 'text', 'label': 'Example', 'payload': '{"type": "item", "value": "example"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Back', 'payload': '{"type": "page", "value": "back"}'}},
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Home', 'payload': '{"type": "page", "value": "main"}'}}
            ]
        ]
}

inputs = {
    'one_time': False,
    'inline': False,
    'buttons':
        [
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Home', 'payload': '{"type": "page", "value": "main"}'}}
            ],
            [
                {'color': 'secondary', 'action': {'type': 'text', 'label': 'Back', 'payload': '{"type": "page", "value": "back"}'}}
            ]
        ]
}
