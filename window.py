import PySimpleGUI as sg
import preset

DEFAULT_FONT = 'Arial'

# 参考:
# 【永久保存版】PySimpleGUIの基本操作すべてお伝えします
# https://arika-blog.com/pysimplegui/
def main():
    sg.theme("Material1")

    presets = preset.getPresets()
    print(presets)

    # 表示する画面の設定をします。
    layout=[
        [text("名前を入力してください", 15)],
        inputTextLabel("名前", key="text", label="初期値"),
        [button("OK",key="ok")]
    ]

    window=sg.Window("test",layout)

    # 無限ループで画面を表示します。×ボタンかOKボタンで無限ループを抜けます。OKボタンの場合はテキストボックスの値も取得します。
    while True:
        event,values=window.read()
        if event==sg.WIN_CLOSED:
            break
        elif event=="ok":
            name=values["text"]
            print(name)
            break

    # 画面を閉じます。
    window.close()

def text(str: str, size: int | None = None):
    if size is None:
        return sg.Text(str, font=(DEFAULT_FONT))
    else:
        return sg.Text(str, font=(DEFAULT_FONT, size))

def button(str: str, key: str, size: int | None = None):
    if size is None:
        return sg.Button(str, font=(DEFAULT_FONT), key=key)
    else:
        return sg.Button(str, font=(DEFAULT_FONT, size), key=key)

def inputText(str: str, key: str, size: int | None = None):
    if size is None:
        return sg.InputText(str, font=(DEFAULT_FONT), key=key)
    else:
        return sg.InputText(str, font=(DEFAULT_FONT, size), key=key)
    
def inputTextLabel (str: str, key: str, size: int | None = None, label: str = "", label_size: int | None = None):
    return [text(str, size),inputText(label, key=key, size=label_size)]

main()
