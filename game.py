import arcade
import os

# constants for the screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "MapGame"

SPRITE_SCALING_PLAYER = 0.1


# buttons that will be used to open views
class MenuButton(arcade.TextButton):

    def __init__(self, view, text, x, y, open_view, font_color=arcade.color.WHITE, theme=None):
        super().__init__(text=text, center_x=x, center_y=y, width=250, height=75, theme=theme)
        self.view = view
        self.font_color = font_color
        self.open_view = open_view

    def on_press(self):
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


# different views
class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.player_sprite = arcade.Sprite("sprites/character_octa.png", SPRITE_SCALING_PLAYER)
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
        options_button = MenuButton(self, "Options", 640, 340, OptionsView(), arcade.color.WHITE, self.theme)
        customize_button = MenuButton(self, "Customize", 640, 250, CustomizeView(), arcade.color.WHITE, self.theme)
        exit_button = ExitButton(self, "Exit Game", 640, 160, font_color=arcade.color.WHITE, theme=self.theme)
        self.button_list.append(start_button)
        self.button_list.append(options_button)
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

        self.player_sprite = arcade.Sprite("sprites/character_octa.png", SPRITE_SCALING_PLAYER)
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
        # game_view.setup()
        self.window.show_view(game_view)


class OptionsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = arcade.Sprite("sprites/character_octa.png", SPRITE_SCALING_PLAYER)
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
        start_button = StartButton(self, "Start Game", 640, 430, font_color=arcade.color.WHITE, theme=self.theme)
        options_button = OptionButton(self, "Options", 640, 340, font_color=arcade.color.WHITE, theme=self.theme)
        customize_button = CustomizeButton(self, "Customize", 640, 250, font_color=arcade.color.WHITE, theme=self.theme)
        exit_button = ExitButton(self, "Exit Game", 640, 160, font_color=arcade.color.WHITE, theme=self.theme)
        self.button_list.append(start_button)
        self.button_list.append(options_button)
        self.button_list.append(customize_button)
        self.button_list.append(exit_button)

    def on_show(self):
        arcade.set_background_color(arcade.color.AZURE)

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        self.player_sprite.draw()

        arcade.draw_text("Game Menu", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5,
                         arcade.color.WHITE, 50, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_key_press(self, symbol: int, _modifiers):
        if symbol == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


class CustomizeView(arcade.View):
    pass


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "MapGame")
    window.set_mouse_visible(False)
    menu_view = MenuView()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
