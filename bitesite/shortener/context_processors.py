menu = [{'title': "About", 'url_name': 'about'},
        {'title': "Create short link", 'url_name': 'create_short_link'},
        {'title': "Feedback", 'url_name': 'feedback'},
        ]


def get_menu(request):
    return {
        'menu': menu
    }
