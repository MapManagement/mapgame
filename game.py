import arcade
import os

# constants for the screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "MapGame"

SPRITE_SCALING_PLAYER = 0.3


# buttons that will be used to open views
class MenuButton(arcade.TextButton):

    def __init__(self, view, text, x, y, open_view, font_color=arcade.color.WHITE, theme=None):
        super().__init__(text=text, center_x=x, center_y=y, width=250, height=75, theme=theme)
        self.view = view
        self.font_color = font_color
        self.open_view = open_view

    def on_press(self):
        self.open_view.setup()
        self.view.window.show_view(self.open_view)


class ExitButton(arcade.TextButton):
    def __init__(self, view, text, x=0, y=0, width=250, height=75, color=arcade.color.ROYAL_AZURE,
                 font_color=arcade.color.BLACK, secondary_color=arcade.color.BLACK, theme=None):
        super().__init__(text=text, center_x=x, center_y=y, width=width, height=height, face_color=color,
                         font_color=font_color, highlight_color=secondary_color, theme=theme)
        self.view = view
        self.font_color = font_color

    def on_press(self):
        self.view.window.close()


# some text inputs
class CustomizeButton(arcade.TextButton):
    def __init__(self, text, x, y, font_color=arcade.color.WHITE, theme=None):
        super().__init__(text=text, center_x=x, center_y=y, width=200, height=50, theme=theme)
        self.font_color = font_color


class TextLabel(arcade.TextLabel):
    def __init__(self, text, x=0, y=0, font_size=15, font_name="Calibri", color=arcade.color.WHITE):
        super().__init__(text=text, x=x, y=y, font_size=font_size, font_name=font_name, color=color)


# different views
class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.player_sprite = arcade.Sprite("sprites/crossh_cross_circle.png", SPRITE_SCALING_PLAYER)
        self.theme = None

    def set_button_textures(self):
        default = "sprites/button_default.png"
        hover = "sprites/button_hover.png"
        clicked = "sprites/button_locked.png"
        self.theme.add_button_textures(default, hover, clicked)

    def setup_theme(self):
        self.theme = arcade.Theme()
        self.set_button_textures()

    def setup(self):
        self.setup_theme()
        self.set_buttons()

    def set_buttons(self):
        start_button = MenuButton(self, "Start Game", 640, 430, GameView(), arcade.color.WHITE, self.theme)
        customize_button = MenuButton(self, "Customize", 640, 340, CustomizeView(), arcade.color.WHITE, self.theme)
        exit_button = ExitButton(self, "Exit Game", 640, 250, font_color=arcade.color.WHITE, theme=self.theme)
        self.button_list.append(start_button)
        self.button_list.append(customize_button)
        self.button_list.append(exit_button)

    def on_show(self):
        arcade.set_background_color(arcade.color.AZURE)

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        self.player_sprite.draw()

        arcade.draw_text("Game Menu", SCREEN_WIDTH/2, SCREEN_HEIGHT/1.5,
                         arcade.color.WHITE, 50, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.player_list = arcade.SpriteList()
        self.hit_list = arcade.SpriteList()

        self.score = 0
        self.player_sprite = None

        self.player_sprite = arcade.Sprite("sprites/crossh_cross_circle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 640
        self.player_sprite.center_y = 360
        self.player_list.append(self.player_sprite)

    def on_show(self):
        arcade.set_background_color(arcade.color.AZURE)

    def on_draw(self):
        arcade.start_render()
        self.hit_list.draw()
        self.player_list.draw()

        score_text = f"Hits: {self.score}"
        arcade.draw_text(score_text, 20, 680, arcade.color.BLACK, 25)

    def on_key_press(self, symbol: int, _modifiers):
        if symbol == arcade.key.ESCAPE:
            pause_view = PauseView()
            self.window.show_view(pause_view)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


class PauseView(arcade.View):

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game paused", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, 40, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class CustomizeView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = arcade.Sprite("sprites/crossh_cross_circle.png", SPRITE_SCALING_PLAYER)
        self.theme = None

    def set_button_textures(self):
        default = "sprites/button_default.png"
        hover = "sprites/button_hover.png"
        clicked = "sprites/button_locked.png"
        self.theme.add_button_textures(default, hover, clicked)

    def setup_theme(self):
        self.theme = arcade.Theme()
        self.set_button_textures()

    def setup(self):
        self.setup_theme()
        self.set_targets()
        self.set_crosshairs()
        self.set_backgrounds()
        self.set_speed()

    def set_targets(self):
        target_text = TextLabel(text="Targets", x=175, y=625, font_size=25)
        self.text_list.append(target_text)

        target_moehre = CustomizeButton(text="Moehre", x=175, y=575, theme=self.theme)
        self.button_list.append(target_moehre)

        target_default = CustomizeButton(text="Default", x=175, y=500, theme=self.theme)
        self.button_list.append(target_default)

    def set_crosshairs(self):
        crosshair_text = TextLabel(text="Crosshairs", x=425, y=625, font_size=25)
        self.text_list.append(crosshair_text)

        crossh_cross = CustomizeButton(text="Cross", x=425, y=575, theme=self.theme)
        self.button_list.append(crossh_cross)

        crossh_dot = CustomizeButton(text="Dot", x=425, y=500, theme=self.theme)
        self.button_list.append(crossh_dot)

        crossh_circle = CustomizeButton(text="Circle", x=425, y=425, theme=self.theme)
        self.button_list.append(crossh_circle)

        crossh_cross_circle = CustomizeButton(text="Cross & Circle", x=425, y=350, theme=self.theme)
        self.button_list.append(crossh_cross_circle)

    def set_backgrounds(self):
        background_text = TextLabel(text="Backgrounds", x=675, y=625, font_size=25)
        self.text_list.append(background_text)

        background_clean = CustomizeButton(text="Clean", x=675, y=575, theme=self.theme)
        self.button_list.append(background_clean)

        background_forest = CustomizeButton(text="Forest", x=675, y=500, theme=self.theme)
        self.button_list.append(background_forest)

        background_mountains = CustomizeButton(text="Mountains", x=675, y=425, theme=self.theme)
        self.button_list.append(background_mountains)

        background_sea = CustomizeButton(text="Sea", x=675, y=350, theme=self.theme)
        self.button_list.append(background_sea)

    def set_speed(self):
        background_text = TextLabel(text="Speed", x=925, y=625, font_size=25)
        self.text_list.append(background_text)

        speed_beginner = CustomizeButton(text="Beginner", x=925, y=575, theme=self.theme)
        self.button_list.append(speed_beginner)

        speed_slow = CustomizeButton(text="Slow", x=925, y=500, theme=self.theme)
        self.button_list.append(speed_slow)

        speed_medium = CustomizeButton(text="Medium", x=925, y=425, theme=self.theme)
        self.button_list.append(speed_medium)

        speed_fast = CustomizeButton(text="Fast", x=925, y=350, theme=self.theme)
        self.button_list.append(speed_fast)

        speed_ultra = CustomizeButton(text="Ultra", x=925, y=275, theme=self.theme)
        self.button_list.append(speed_ultra)

    def on_show(self):
        arcade.set_background_color(arcade.color.AZURE)

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        self.player_sprite.draw()

        arcade.draw_text("Customizations", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1,
                         arcade.color.WHITE, 50, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_key_press(self, symbol: int, _modifiers):
        if symbol == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "MapGame")
    window.set_mouse_visible(False)
    menu_view = MenuView()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
