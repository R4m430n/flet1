import flet as ft

def main(page: ft.Page):
    page.title = "Flet Calc"
    page.window_width = 360
    page.window_height = 640
    page.theme_mode = ft.ThemeMode.LIGHT

    display = ft.TextField(
        value="0",
        text_size=36,
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor=ft.colors.WHITE,
    )

    def clear_all(_=None):
        display.value = "0"
        page.update()

    def backspace(_=None):
        s = display.value
        display.value = s[:-1] if len(s) > 1 else "0"
        page.update()

    def append(txt: str):
        if display.value == "0" and txt not in (".", "÷", "×", "+", "-", "%"):
            display.value = txt
        else:
            display.value += txt
        page.update()

    def calc(_=None):
        expr = display.value.replace("×", "*").replace("÷", "/")
        try:
            # %-ni foiz operatori sifatida ishlatamiz: “a%b” emas, “a*(b/100)”
            # oddiy qoida: ... % raqam -> * (raqam/100)
            # juda soddalashtirilgan: faqat oxirida % bo'lsa
            if expr.endswith("%"):
                expr = expr[:-1]
                result = float(eval(expr)) / 100.0
            else:
                result = eval(expr)
            # int ko‘rinishida bo‘lsa kasrni yashiramiz
            display.value = str(int(result)) if float(result).is_integer() else str(result)
        except Exception:
            display.value = "Error"
        page.update()

    # Tugma yaratish yordamchisi
    def key(text, on_click=None, expand=1, color=ft.colors.BLUE_GREY_50):
        return ft.Container(
            content=ft.TextButton(
                text,
                on_click=on_click or (lambda e, t=text: append(t)),
                style=ft.ButtonStyle(padding=20),
            ),
            bgcolor=color,
            border_radius=16,
            padding=2,
            expand=expand,
        )

    grid = ft.Column(
        [
            ft.Container(display, padding=10, bgcolor=ft.colors.BLUE_GREY_50, border_radius=16),
            ft.Row(
                [
                    key("C", clear_all, color=ft.colors.AMBER_100),
                    key("⌫", backspace, color=ft.colors.AMBER_100),
                    key("%", color=ft.colors.AMBER_100),
                    key("÷", color=ft.colors.AMBER_100),
                ],
                expand=True,
            ),
            ft.Row([key("7"), key("8"), key("9"), key("×", color=ft.colors.AMBER_100)], expand=True),
            ft.Row([key("4"), key("5"), key("6"), key("-", color=ft.colors.AMBER_100)], expand=True),
            ft.Row([key("1"), key("2"), key("3"), key("+", color=ft.colors.AMBER_100)], expand=True),
            ft.Row(
                [
                    key("0", expand=2),
                    key("."),
                    ft.Container(
                        content=ft.ElevatedButton("=", on_click=calc),
                        bgcolor=ft.colors.BLUE_200,
                        border_radius=16,
                        padding=2,
                        expand=1,
                    ),
                ],
                expand=True,
            ),
        ],
        spacing=8,
        expand=True,
    )

    page.add(grid)

if __name__ == "__main__":
    ft.app(target=main)
