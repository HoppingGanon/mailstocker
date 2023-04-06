import poplib
import json
import common

def get_pop3_emails(pop3_server, pop3_port, email_account, email_password):
    # POP3サーバーに接続
    mail_server = poplib.POP3_SSL(pop3_server, pop3_port)

    # メールアカウントにログイン
    mail_server.user(email_account)
    mail_server.pass_(email_password)

    # 取得できるメールの件数を取得
    num_messages = len(mail_server.list()[1])

    if not common.show_message_box('メールの総数は' + str(num_messages) + '件です\nテキストファイルにダンプしますか？'):
        return

    # 全てのメールを保存するリスト
    messages = []

    # 全てのメールを１通ずつ取得し、辞書型に変換しリストに追加
    print('メールの取得中...')
    for i in range(num_messages):
        message = {}
        raw_message = b"\n".join(mail_server.retr(i + 1)[1]).decode("utf-8", errors="replace")

        # メールヘッダとボディに分割
        header, body = raw_message.split("\n\n", 1)

        # メールヘッダを辞書型に変換
        header_dict = {}
        for line in header.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                header_dict[key.strip()] = value.strip()
        message["header"] = header_dict

        # メールボディをUnicode文字列に変換して追加
        message["body"] = body.encode("utf-8", errors="replace").decode("utf-8", errors="replace")

        # リストに追加
        messages.append(message)

    # 取得したメールのリストをJSON形式で保存
    with open("emails.json", "w") as f:
        json.dump(messages, f, ensure_ascii=False)

    # メールサーバーからログアウト
    mail_server.quit()
