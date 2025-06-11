import flet as ft

def main(page: ft.Page):
    """
    The main function for the Flet application.
    This function sets up the page, adds controls, and handles events.
    """
    page.title = "Flet Mobile Link Demo" 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 

    txt_number = ft.Text(value="0", size=30)

    def increment_number(e):
        """
        Event handler for the increment button.
        Increments the number and updates the text control.
        """
        txt_number.value = str(int(txt_number.value) + 1)
        page.update() 

    def decrement_number(e):
        """
        Event handler for the decrement button.
        Decrements the number and updates the text control.
        """
        txt_number.value = str(int(txt_number.value) - 1)
        page.update() 

    page.add(
        ft.Column(
            [
                ft.Text("Welcome to your Flet App!", size=20, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.IconButton(ft.Icons.REMOVE, on_click=decrement_number), 
                        txt_number, 
                        ft.IconButton(ft.Icons.ADD, on_click=increment_number), 
                    ],
                    alignment=ft.MainAxisAlignment.CENTER 
                ),
                ft.Text("This app is accessible on mobile when run as a web app!"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER 
        )
    )
ft.app(target=main, view=ft.WEB_BROWSER, port=8550)
