def TextButton(label, payload='', color='secondary'):
    button = dict(
        action=dict(
            type='text',
            label=label,
            payload=payload
        ),
        color=color
    )
    return button


def MainKeyboard():
    buttons = [
        [
            TextButton('📖 Помощь'),
            TextButton('⭐ Баланс')
        ],
        [
            TextButton('🏆 Награды'),
            TextButton('📊 Очки')
        ],
        [
            TextButton('💬 Комментарии'),
        ],
    ]
    return dict(one_time=False, inline=False, buttons=buttons)
