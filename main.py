import flet as ft
import webbrowser
from sources import (
    news_bbc_en,
    news_ntv_tr,
    news_karar_tr,
    news_independent_en
)

def main(page: ft.Page):
    page.title = "MixNews Global v5"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.padding = 20
    page.window_center()

    saved_favs = page.client_storage.get("user_favorites")
    favorites = saved_favs if saved_favs is not None else []

    def save_favorites():
        page.client_storage.set("user_favorites", favorites)

    all_sites = [
        {"ad": "BBC English", "renk": "red600", "sub": "Global news source", "module": news_bbc_en},
        {"ad": "NTV News", "renk": "amber800", "sub": "Breaking news from Turkey", "module": news_ntv_tr},
        {"ad": "Karar", "renk": "blue700", "sub": "Fast and objective reporting", "module": news_karar_tr},
        {"ad": "Independent", "renk": "blue900", "sub": "World reporting", "module": news_independent_en},
    ]


    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()

    def go_to_main(e):
        page.controls.clear()
        page.add(main_menu_view())
        page.update()

    def go_to_favorites(e):
        page.controls.clear()
        page.add(favorites_view())
        page.update()

    def go_to_news(site_name):
        page.controls.clear()
        page.add(news_list_view(site_name))
        page.update()

    def show_summary(url, module):
        summary_container = ft.Column([
            ft.Text("Quick Summary", size=20, weight="bold"),
            ft.ProgressBar(color="blue"),
            ft.Text("Fetching content...", italic=True)
        ], tight=True)
        
        bs = ft.BottomSheet(ft.Container(summary_container, padding=20))
        page.open(bs)
        
        content = module.get_content(url)
        summary_container.controls[1].visible = False 
        summary_container.controls[2].value = content
        summary_container.controls[2].italic = False
        page.update()

    def add_remove_favorite(site_ad):
        if site_ad in favorites:
            favorites.remove(site_ad)
        else:
            favorites.append(site_ad)
        save_favorites() 
        if "Favorites" in page.title:
            go_to_favorites(None)
        else:
            go_to_main(None)


    def main_menu_view():
        page.title = "MixNews - Main Menu"
        header = ft.Column([
            ft.Row([
                ft.Text("MIXNEWS", size=40, weight="bold", color="primary", expand=True),
                ft.IconButton(icon="favorite", icon_color="red", on_click=go_to_favorites),
                ft.IconButton(icon="settings", on_click=lambda _: page.open(settings_dialog))
            ]),
            ft.Divider(height=10, thickness=2),
        ])
        cards = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True, spacing=15)
        for s in all_sites:
            is_fav = s["ad"] in favorites
            cards.controls.append(create_site_card(s, is_fav))
        return ft.Column([header, cards], expand=True)

    def favorites_view():
        page.title = "MixNews - Favorites"
        header = ft.Column([
            ft.Row([
                ft.IconButton(icon="arrow_back", on_click=go_to_main),
                ft.Text("MY FAVORITES", size=30, weight="bold", color="red", expand=True),
            ]),
            ft.Divider(height=10, thickness=2),
        ])
        cards = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True, spacing=15)
        fav_sites = [s for s in all_sites if s["ad"] in favorites]
        if not fav_sites:
            cards.controls.append(ft.Container(content=ft.Text("No favorites added yet.", size=16), padding=20))
        else:
            for s in fav_sites:
                cards.controls.append(create_site_card(s, True))
        return ft.Column([header, cards], expand=True)

    def create_site_card(s, is_fav):
        return ft.Card(content=ft.Container(padding=15, content=ft.Column([
            ft.ListTile(
                leading=ft.Icon(name="newspaper", color=s["renk"]),
                title=ft.Text(s["ad"], weight="bold", size=18),
                subtitle=ft.Text(s["sub"]),
                trailing=ft.IconButton(
                    icon="favorite" if is_fav else "favorite_border",
                    icon_color="red" if is_fav else None,
                    on_click=lambda e: add_remove_favorite(s["ad"])
                )
            ),
            ft.Row([ft.ElevatedButton("VIEW FEED", on_click=lambda _, x=s["ad"]: go_to_news(x))], alignment=ft.MainAxisAlignment.END)
        ])))

    settings_dialog = ft.AlertDialog(
        title=ft.Text("Settings"),
        content=ft.Column([
            ft.Switch(label="Light / Dark Mode", value=True, on_change=toggle_theme),
            ft.TextButton("Back to Main Menu", icon="home", on_click=lambda e: [page.close(settings_dialog), go_to_main(None)]),
        ], height=150, tight=True),
    )


    
    def news_list_view(site_name):
        news_container = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=10)
        site_module = next((s["module"] for s in all_sites if s["ad"] == site_name), None)
        
        def load_category(cat):
            news_container.controls.clear()
            news_container.controls.append(ft.ProgressBar())
            page.update()
            
            articles = site_module.get_news(cat) 
            news_container.controls.clear()
            
            for a in articles:
                news_container.controls.append(
                    ft.Container(
                        padding=10, border=ft.border.all(1, "outlinevariant"), border_radius=10,
                        content=ft.Column([
                            ft.Text(a["title"], size=14, weight="bold"),
                            ft.Row([
                                ft.TextButton("Summary", icon=ft.icons.SHORT_TEXT, 
                                              on_click=lambda _, u=a["url"]: show_summary(u, site_module)),
                                ft.IconButton(icon="open_in_new", on_click=lambda _, u=a["url"]: webbrowser.open(u))
                            ], alignment=ft.MainAxisAlignment.END)
                        ])
                    )
                )
            page.update()

        tabs = ft.Tabs(
            on_change=lambda e: load_category(e.control.tabs[e.control.selected_index].text),
            tabs=[ft.Tab(text="Top Stories"), ft.Tab(text="Economy"), ft.Tab(text="Sport")]
        )
        
        top_bar = ft.Row([
            ft.IconButton(icon="arrow_back", on_click=go_to_main),
            ft.Text(site_name, size=20, weight="bold", expand=True),
            ft.IconButton(icon=ft.icons.REFRESH, 
                          on_click=lambda _: load_category(tabs.tabs[tabs.selected_index].text))
        ])

        load_category("Top Stories")
        return ft.Column([top_bar, tabs, news_container], expand=True)     


   
    page.add(main_menu_view())

ft.app(target=main)
