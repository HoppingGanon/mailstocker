import PySimpleGUI as sg
import json
import common

# PySimpleGUIのテーマを設定
sg.theme('SystemDefaultForReal')

# JSONファイルのパス
JSON_PATH = './pop3_accounts.json'

# JSONファイルからアカウント情報を読み込む関数
def load_accounts():
    try:
        with open(JSON_PATH, 'r') as f:
            accounts = json.load(f)
    except FileNotFoundError:
        accounts = []
    return accounts

# アカウント情報をJSONファイルに保存する関数
def save_account(account):
    accounts = load_accounts()
    for i, a in enumerate(accounts):
        if a['name'] == account['name']:
            accounts[i] = account
            break
    else:
        accounts.append(account)

    with open(JSON_PATH, 'w') as f:
        json.dump(accounts, f)
        f.close()

def save_accounts(accounts):
    for i, a in enumerate(accounts):
        if a['name'] == account['name']:
            accounts[i] = account
            break
    else:
        accounts.append(account)

    with open(JSON_PATH, 'w') as f:
        json.dump(accounts, f)
        f.close()

# プリセットアカウントを取得
accounts = load_accounts()

# 画面レイアウト
layout_main = [ [sg.Text('アカウント名:'), sg.InputText(key='-EMAIL_ACCOUNT-')],
                [sg.Text('サーバー名　:'), sg.InputText(key='-POP3_SERVER-')],
                [sg.Text('ポート　　　:'), sg.InputText(key='-POP3_PORT-')],
                [sg.Text('ユーザー名　:'), sg.InputText(key='-EMAIL_USER-')],
                [sg.Text('パスワード　:'), sg.InputText(key='-EMAIL_PASSWORD-', password_char='*')],
                [sg.Button('OK'), sg.Button('キャンセル'), sg.Button('設定')] ]

# ウィンドウの生成
window_main = sg.Window('POP3アクセスに必要な情報を入力', layout_main)

# 設定用のウィンドウを格納する変数
window_settings = None

# イベントループ
while True:
    event, values = window_main.read()

    if event == sg.WIN_CLOSED or event == 'キャンセル':
        break
    elif event == '設定':
        # 設定用ウィンドウが存在している場合は、破棄する
        if window_settings is not None:
            window_settings.close()

        # アカウント設定用のウィンドウを表示
        layout_settings = [ [sg.Text('アカウント一覧')],
                            [sg.Listbox(values=[account['name'] for account in accounts], size=(40, 10), key='-ACCOUNT_LIST-')],
                            [sg.Button('ロード'), sg.Button('追加'), sg.Button('削除'), sg.Button('更新')] ]
        window_settings = sg.Window('アカウント設定', layout_settings)

        while True:
            event2, values2 = window_settings.read()

            if event2 == sg.WIN_CLOSED:
                break
            elif event2 == 'ロード':
                # アカウントの削除
                selected_index = window_settings['-ACCOUNT_LIST-'].get_indexes()[0]
                if selected_index is not None:
                    selected_account = accounts[selected_index]
                    window_main['-EMAIL_ACCOUNT-'].update(selected_account['pop3_server'])
                    window_main['-POP3_PORT-'].update(selected_account['pop3_port'])
                    window_main['-POP3_SERVER-'].update(selected_account['email_account'])
                    window_main['-EMAIL_USER-'].update(selected_account['email_user'])
            elif event2 == '追加':
                # アカウントの追加
                name = sg.popup_get_text('アカウント名を入力してください')
                if name:
                    account = {'name': name, 'email_account': '', 'pop3_server': '', 'email_user': '', 'email_password': ''}
                    accounts.append(account)

                    # アカウント情報をJSONファイルに保存
                    selected_index = len(accounts) - 1
                    if selected_index is not None:
                        selected_account = accounts[selected_index]
                        selected_account['pop3_server'] = window_main['-POP3_SERVER-'].get()
                        selected_account['pop3_port'] = window_main['-POP3_PORT-'].get()
                        selected_account['email_account'] = window_main['-EMAIL_ACCOUNT-'].get()
                        selected_account['email_user'] = window_main['-EMAIL_USER-'].get()
                        save_account(selected_account)

                    window_settings['-ACCOUNT_LIST-'].update(values=[account['name'] for account in accounts])
                    save_account(account)
            elif event2 == '削除':
                # アカウントの削除
                selected_index = window_settings['-ACCOUNT_LIST-'].get_indexes()[0]
                if selected_index is not None:
                    del accounts[selected_index]
                    window_settings['-ACCOUNT_LIST-'].update(values=[account['name'] for account in accounts])
                    save_accounts(accounts)
            elif event2 == '更新':
                # アカウント情報をJSONファイルに保存
                if len(window_settings['-ACCOUNT_LIST-'].get_indexes()) != 0:
                    selected_index = window_settings['-ACCOUNT_LIST-'].get_indexes()[0]
                    if selected_index is not None:
                        selected_account = accounts[selected_index]
                        selected_account['pop3_server'] = window_main['-POP3_SERVER-'].get()
                        selected_account['pop3_port'] = window_main['-POP3_PORT-'].get()
                        selected_account['email_account'] = window_main['-EMAIL_ACCOUNT-'].get()
                        selected_account['email_user'] = window_main['-EMAIL_USER-'].get()
                        save_account(selected_account)
                else:
                    sg.popup('プリセットを選択してください')

        # アカウント設定用のウィンドウを閉じる
        window_settings.close()
        window_settings = None

    elif event == '取得':
        # アカウント情報を取得
        pop3_server = values['-POP3_SERVER-']
        pop3_port = values['-POP3_PORT-']
        email_account = values['-EMAIL_ACCOUNT-']
        email_user = values['-EMAIL_USER-']
        email_password = values['-EMAIL_PASSWORD-']

        # TODO: 入力値を使ってPOP3アクセスする処理を実装

    else:
        # リストボックスが選択された場合は、各項目に自動入力する
        if len(values['-ACCOUNT_LIST-']) > 0:
            selected_index = window_main['-ACCOUNT_LIST-'].get_indexes()[0]
            selected_account = accounts[selected_index]
            window_main['-EMAIL_ACCOUNT-'].update(selected_account['email_account'])
            window_main['-POP3_SERVER-'].update(selected_account['pop3_server'])
            window_main['-EMAIL_USER-'].update(selected_account['email_user'])
            window_main['-EMAIL_PASSWORD-'].update(selected_account['email_password'])

# ウィンドウの破棄と終了
if window_settings is not None:
    window_settings.close()

window_main.close()
