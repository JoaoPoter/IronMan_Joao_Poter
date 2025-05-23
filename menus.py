menu_buttons = [
    {'text': 'Iniciar Game', 'action': 'start_game', 'icon': spr_start_b},
    {'text': 'Sair do Game', 'action': 'quit', 'icon': spr_quit_b},
]

main_menu = Menu(screen=screen, title='Pause', buttons=menu_buttons, background=spr_iron_bg)
main_menu.run(start=True, pause=True)
