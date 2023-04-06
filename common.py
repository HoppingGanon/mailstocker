import PySimpleGUI as sg

def show_message_box (title: str):
    # メッセージボックスのレイアウト
    layout = [
        [sg.Text(title)],
        [sg.Button('OK'), sg.Button('Cancel')]
    ]

    # ウィンドウを作成
    window = sg.Window('メッセージボックス', layout)

    result = True
    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            # ウィンドウが閉じられた場合やCancelが選択された場合
            result = False
            break
        elif event == 'OK':
            # OKが選択された場合
            result = True

    # ウィンドウを閉じる
    window.close()

    return result
