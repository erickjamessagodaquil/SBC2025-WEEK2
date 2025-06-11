import flet as ft
import os # Import os module for file system operations
import json # Import json module for reading/writing JSON files

def main(page: ft.Page):
    """
    Main function for the Flet application.
    Sets up the page, app bar, alternative navigation row, and content views.
    Integrates local data storage for settings, and implements dynamic dark mode.
    All colors are now hardcoded as hex strings to bypass 'flet.colors' issues.
    Adds chat functionality with message sending and clearing.
    """
    page.title = "Welcome to Erich James Sagodaquil website!"
    page.vertical_alignment = ft.CrossAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 375  # Simulate a typical mobile width for initial preview
    page.window_height = 812 # Simulate a typical mobile height for initial preview
    page.window_resizable = True
    page.padding = 0 # Remove default page padding

    # --- Constants for Data Storage ---
    APP_BASE_DIR = "storage"
    DATA_FILE = os.path.join(APP_BASE_DIR, "data", "app_data.json")
    TEMP_DIR = os.path.join(APP_BASE_DIR, "temp")

    # --- Hardcoded Color Definitions ---
    COLOR_WHITE = "#FFFFFF"
    COLOR_BLACK = "#000000"
    COLOR_BLUE_GREY_600 = "#546E7A"
    COLOR_GREEN_700 = "#388E3C"
    COLOR_ORANGE_700 = "#F57C00"
    COLOR_BLUE_ACCENT_700 = "#2962FF"
    COLOR_BLUE_GREY_900 = "#263238" # Darker grey for dark mode app bar
    COLOR_BLUE_GREY_800 = "#37474F" # Darker grey for dark mode nav bar background
    COLOR_BLUE_GREY_700 = "#455A64" # Darker grey for selected button (dark mode)
    COLOR_BLUE_GREY_50 = "#ECEFF1" # Light grey for light mode nav bar background
    COLOR_BLUE_100 = "#BBDEFB" # Light blue for selected button (light mode)
    COLOR_BLUE_700 = "#1976D2" # Darker blue for selected button text (light mode)
    COLOR_LIGHT_BLUE_200 = "#81D4FA" # Light blue for selected button text (dark mode)
    COLOR_WHITE70 = "#B3FFFFFF" # 70% opacity white for unselected button text (dark mode)
    COLOR_RED_ACCENT_700 = "#D32F2F" # Red for clear chat button
    COLOR_GREY_300 = "#E0E0E0" # Light grey for TextField filled background (light mode)
    COLOR_GREY_700 = "#616161" # Dark grey for TextField filled background (dark mode)

    # --- Data Storage Functions ---
    def load_data():
        """Loads data from the local JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {DATA_FILE} is empty or corrupted. Starting with default data.")
                return {
                    "settings": {"enable_notifications": False, "dark_mode": False},
                    "chat_messages": []
                }
        return {
            "settings": {"enable_notifications": False, "dark_mode": False},
            "chat_messages": []
        }

    def save_data():
        """Saves current data_store to the local JSON file."""
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump(data_store, f, indent=4)

    # --- Initialize Data Store from file or with defaults ---
    data_store = load_data()

    # --- Add dummy messages to ensure scrolling is visible for testing ---
    if not data_store["chat_messages"]: # Only add if chat is empty
        for i in range(1, 15): # Add 14 dummy messages
            data_store["chat_messages"].append(f"Dummy Message {i}: This is a test message to fill up the chat area.")
        save_data() # Save dummy data so it persists across runs for testing

    # --- Apply initial theme mode from loaded data ---
    page.theme_mode = ft.ThemeMode.DARK if data_store["settings"]["dark_mode"] else ft.ThemeMode.LIGHT

    # --- Create the 'storage/temp' directory ---
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True) # Creates 'storage/data'
    os.makedirs(TEMP_DIR, exist_ok=True) # Creates 'storage/temp'

    # --- Track current selected content index ---
    current_selected_index = ft.Ref[int]() # Use a Ref to store and update the index

    # --- Define theme-dependent colors using hardcoded hex values ---
    def get_app_bar_colors(is_dark_mode):
        """Returns app bar colors based on theme mode."""
        if is_dark_mode:
            return {"bgcolor": COLOR_BLUE_GREY_900, "content_color": COLOR_WHITE}
        else:
            return {"bgcolor": COLOR_BLUE_ACCENT_700, "content_color": COLOR_WHITE}

    def get_general_text_color(is_dark_mode):
        """Returns general text color for content views based on theme mode."""
        return COLOR_WHITE if is_dark_mode else COLOR_BLACK

    def get_nav_bar_container_bgcolor(is_dark_mode):
        """Returns navigation bar container background color based on theme mode."""
        return COLOR_BLUE_GREY_800 if is_dark_mode else COLOR_BLUE_GREY_50

    def get_nav_button_colors(is_dark_mode, is_selected):
        """Returns navigation button colors based on theme mode and selection state."""
        if is_selected:
            if is_dark_mode:
                return {"bg": COLOR_BLUE_GREY_700, "text": COLOR_LIGHT_BLUE_200}
            else:
                return {"bg": COLOR_BLUE_100, "text": COLOR_BLUE_700}
        else:
            if is_dark_mode:
                return {"bg": COLOR_BLUE_GREY_800, "text": COLOR_WHITE70}
            else:
                return {"bg": COLOR_WHITE, "text": COLOR_BLUE_GREY_600}

    def get_text_field_colors(is_dark_mode):
        """Returns text field colors based on theme mode."""
        if is_dark_mode:
            return {"bgcolor": COLOR_GREY_700, "text_color": COLOR_WHITE, "hint_color": COLOR_WHITE70}
        else:
            return {"bgcolor": COLOR_GREY_300, "text_color": COLOR_BLACK, "hint_color": COLOR_BLUE_GREY_600}

    # --- Chat UI elements ---
    chat_messages_list = ft.ListView(
        expand=True, # ListView itself expands within its parent Container
        auto_scroll=True,
        spacing=10,
        padding=10,
    )

    initial_tf_colors = get_text_field_colors(page.theme_mode == ft.ThemeMode.DARK)
    new_message_field = ft.TextField(
        hint_text="Type your message...",
        expand=True,
        border_radius=ft.border_radius.all(10),
        filled=True,
        bgcolor=initial_tf_colors["bgcolor"],
        text_style=ft.TextStyle(color=initial_tf_colors["text_color"]),
        hint_style=ft.TextStyle(color=initial_tf_colors["hint_color"]),
    )

    def add_message(message):
        """Adds a message to the chat list and data store."""
        chat_messages_list.controls.append(ft.Text(message, color=get_general_text_color(page.theme_mode == ft.ThemeMode.DARK)))
        data_store["chat_messages"].append(message)
        save_data()
        page.update()
        chat_messages_list.scroll_to(offset=-1, duration=300)

    def send_message(e):
        """Handles sending a new chat message."""
        if new_message_field.value:
            add_message(new_message_field.value)
            new_message_field.value = ""
            page.update()

    def clear_chat(e):
        """Clears all messages from the chat and data store."""
        chat_messages_list.controls.clear()
        data_store["chat_messages"].clear()
        save_data()
        page.update()


    # Populate chat messages from loaded data
    for msg in data_store["chat_messages"]:
        chat_messages_list.controls.append(ft.Text(msg, color=get_general_text_color(page.theme_mode == ft.ThemeMode.DARK)))


    # --- Content Views ---
    home_view = ft.Column(
        [
            ft.Text("🏠", size=80, color=get_general_text_color(page.theme_mode == ft.ThemeMode.DARK)),
            ft.Text("Welcome to Home!", size=30, weight=ft.FontWeight.BOLD, color=get_general_text_color(page.theme_mode == ft.ThemeMode.DARK)),
            ft.Text("This is your personalized dashboard.", size=16, color=get_general_text_color(page.theme_mode == ft.ThemeMode.DARK)),
            ft.ElevatedButton("Go to Chat", on_click=lambda e: update_content(1))
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # Re-build chat_view so that when the dark mode is changed, the colors apply for all objects.
    def build_chat_view(is_dark_mode):
        return ft.Column(
            [
                ft.Text("💬", size=80, color=get_general_text_color(is_dark_mode)),
                ft.Text("Chat with your friends!", size=30, weight=ft.FontWeight.BOLD, color=get_general_text_color(is_dark_mode)),
                ft.Text("Start a new conversation or continue an existing one.", size=16, color=get_general_text_color(is_dark_mode)),
                ft.Container( # Container for chat messages list to give it a visible box and handle scrolling
                    content=chat_messages_list,
                    height=200, # Explicit height to ensure visibility and provide scrollable area
                    width=page.window_width * 0.9, # Added explicit width
                    bgcolor=COLOR_GREY_300 if not is_dark_mode else COLOR_GREY_700, # Background for the chat box
                    border_radius=ft.border_radius.all(10),
                    padding=ft.padding.all(5),
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Row( # Input field and send button
                    [
                        new_message_field,
                        ft.IconButton(
                            icon="send",
                            on_click=send_message,
                            tooltip="Send Message",
                            icon_color=COLOR_BLUE_ACCENT_700 if not is_dark_mode else COLOR_LIGHT_BLUE_200
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=10,
                    width=page.window_width * 0.9, # Added explicit width
                ),
                ft.ElevatedButton("Clear Chat", on_click=clear_chat, style=ft.ButtonStyle(bgcolor=COLOR_RED_ACCENT_700, color=COLOR_WHITE)),
                ft.ElevatedButton("Go to Settings", on_click=lambda e: update_content(2))
            ],
            alignment=ft.MainAxisAlignment.START, # Align to start for chat flow
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True, # This overall Column expands to fill available space
            spacing=10, # Add spacing for chat elements
            scroll=ft.ScrollMode.ADAPTIVE, # Make the entire chat view scrollable
        )
    
    # Initialize chat_view using the builder function
    chat_view = build_chat_view(page.theme_mode == ft.ThemeMode.DARK)

    def on_dark_mode_switch_change(e):
        """Handles the dark mode switch change and saves the setting."""
        is_dark = e.control.value
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        data_store["settings"]["dark_mode"] = is_dark
        save_data()

        # Update app bar colors
        app_bar_colors = get_app_bar_colors(is_dark)
        page.appbar.bgcolor = app_bar_colors["bgcolor"]
        page.appbar.title.color = app_bar_colors["content_color"]
        page.appbar.leading.color = app_bar_colors["content_color"]
        for action in page.appbar.actions:
            if isinstance(action, ft.IconButton) and isinstance(action.content, ft.Text):
                action.content.color = app_bar_colors["content_color"]

        # Update TextField colors
        tf_colors = get_text_field_colors(is_dark)
        new_message_field.bgcolor = tf_colors["bgcolor"]
        new_message_field.text_style.color = tf_colors["text_color"]
        new_message_field.hint_style.color = tf_colors["hint_color"]
        # new_message_field.border_color = tf_colors["hint_color"] # border_color is not a direct property

        # Re-initialize content views to apply new general text colors
        nonlocal home_view, chat_view, settings_view
        home_view = ft.Column(
            [
                ft.Text("🏠", size=80, color=get_general_text_color(is_dark)),
                ft.Text("Welcome to Home!", size=30, weight=ft.FontWeight.BOLD, color=get_general_text_color(is_dark)),
                ft.Text("This is your personalized dashboard.", size=16, color=get_general_text_color(is_dark)),
                ft.ElevatedButton("Go to Chat", on_click=lambda e: update_content(1))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        # Re-build chat_view to apply new colors to static text and chat box
        chat_view = build_chat_view(is_dark) # Re-build chat_view with updated theme
        
        settings_view = ft.Column(
            [
                ft.Text("⚙️", size=80, color=get_general_text_color(is_dark)),
                ft.Text("Adjust your settings!", size=30, weight=ft.FontWeight.BOLD, color=get_general_text_color(is_dark)),
                ft.Text("Customize your app experience.", size=16, color=get_general_text_color(is_dark)),
                e.control # Keep the switch control itself (e.control is the switch)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        # Re-assign views dictionary with new view instances
        nonlocal views
        views = {
            0: home_view,
            1: chat_view,
            2: settings_view,
        }

        # Update chat message colors if chat is active
        for msg_control in chat_messages_list.controls:
            msg_control.color = get_general_text_color(is_dark)

        page_content_area.content = views[current_selected_index.current]
        
        # Update navigation bar container background
        nav_container.bgcolor = get_nav_bar_container_bgcolor(is_dark)

        # Update navigation button colors based on new theme
        update_content(current_selected_index.current) # Re-run update_content to refresh button colors
        page.update()

    # Initial definition of settings_view (needed for page initialization)
    settings_view = ft.Column(
        [
            ft.Text("⚙️", size=80, color=get_general_text_color(page.theme_mode == ft.ThemeMode.DARK)),
            ft.Text("Adjust your settings!", size=30, weight=ft.FontWeight.BOLD, color=get_general_text_color(page.theme_mode == ft.ThemeMode.DARK)),
            ft.Text("Customize your app experience.", size=16, color=get_general_text_color(page.theme_mode == ft.ThemeMode.DARK)),
            ft.Switch(
                label="Dark Mode",
                value=data_store["settings"]["dark_mode"],
                on_change=on_dark_mode_switch_change
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # Initial views dictionary (before on_dark_mode_switch_change might re-assign it)
    views = {
        0: home_view,
        1: chat_view, # Initialized with build_chat_view
        2: settings_view,
    }

    # --- App Bar (Title Bar) ---
    initial_app_bar_colors = get_app_bar_colors(page.theme_mode == ft.ThemeMode.DARK)
    page.appbar = ft.AppBar(
        leading=ft.Text("🔷", size=24, color=initial_app_bar_colors["content_color"]),
        leading_width=40,
        title=ft.Text("My Flet App", color=initial_app_bar_colors["content_color"], weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=initial_app_bar_colors["bgcolor"],
        actions=[
            ft.IconButton(content=ft.Text("🔍", size=24, color=initial_app_bar_colors["content_color"])),
            ft.IconButton(content=ft.Text("⋮", size=24, color=initial_app_bar_colors["content_color"])),
        ],
    )

    # --- Page Content (initially Home View) ---
    page_content_area = ft.Container(
        content=views[0],
        expand=True,
        alignment=ft.alignment.center,
    )

    # --- Forward declaration for nav_buttons_row for use in update_content lambda ---
    nav_buttons_row = ft.Row([])

    # --- Alternative Navigation Row (Bottom) ---
    def update_content(index):
        """
        Updates the content area based on the selected index from the navigation buttons,
        and updates the visual style of the buttons based on the current theme.
        """
        current_selected_index.current = index # Update the Ref
        page_content_area.content = views[index] # Set the content

        is_dark_mode = page.theme_mode == ft.ThemeMode.DARK

        for i, btn in enumerate(nav_buttons_row.controls):
            button_colors = get_nav_button_colors(is_dark_mode, i == index)
            # Apply color changes directly to the Text controls inside the button's content
            btn.content.bgcolor = button_colors["bg"]
            # Accessing the children of the Column within the button's Container content
            btn.content.content.controls[0].color = button_colors["text"]  # Emoji
            btn.content.content.controls[1].color = button_colors["text"]  # Label

        page.update()

    # Define the actual nav_buttons_row with its TextButtons
    nav_buttons_row.controls.extend([
        ft.TextButton(
            content=ft.Container( # Wrap content in a Container to set background
                content=ft.Column([ft.Text("🏠", size=20), ft.Text("Home", size=8)], # Adjusted sizes
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center, # Center content within this container
                expand=True, # Make container fill the button area
            ),
            on_click=lambda e: update_content(0),
            expand=True, # Make button expand to fill width
        ),
        ft.TextButton(
            content=ft.Container( # Wrap content in a Container to set background
                content=ft.Column([ft.Text("💬", size=20), ft.Text("Chat", size=8)], # Adjusted sizes
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True,
            ),
            on_click=lambda e: update_content(1),
            expand=True,
        ),
        ft.TextButton(
            content=ft.Container( # Wrap content in a Container to set background
                content=ft.Column([ft.Text("⚙️", size=20), ft.Text("Settings", size=8)], # Adjusted sizes
                                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True,
            ),
            on_click=lambda e: update_content(2),
            expand=True,
        ),
    ])

    nav_buttons_row.alignment = ft.MainAxisAlignment.SPACE_AROUND
    nav_buttons_row.height = 45 # Adjusted navigation bar height to be much smaller
    nav_buttons_row.spacing = 0
    nav_buttons_row.run_spacing = 0
    nav_buttons_row.vertical_alignment = ft.CrossAxisAlignment.CENTER
    nav_buttons_row.expand = True # Allow the row to expand horizontally within its container

    initial_nav_container_bgcolor = get_nav_bar_container_bgcolor(page.theme_mode == ft.ThemeMode.DARK)
    nav_container = ft.Container( # Container to provide background for the custom nav row
        content=nav_buttons_row,
        bgcolor=initial_nav_container_bgcolor,
        padding=ft.padding.only(top=2, bottom=2), # Reduced padding
        border_radius=ft.border_radius.all(10),
        expand=True,
    )

    page.add(
        ft.Column(
            [
                page_content_area,
                nav_container,
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
    )

    # Set initial selection and apply initial colors
    update_content(0)


# To run the app:
# For desktop/mobile emulation (default):
# if __name__ == "__main__":
#     ft.app(target=main)

# For web (uncomment to test in browser):
if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
