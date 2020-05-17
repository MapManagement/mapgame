import arcade
import os

# constants for the screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "MapGame"

SPRITE_SCALING_PLAYER = 0.1


class MenuView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.AZURE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Menu", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, 50, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.player_list = None
        self.hit_list = None

        self.score = 0
        self.player_sprite = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.hit_list = arcade.SpriteList()

        self.score = 0

        self.player_sprite = arcade.Sprite("sprites/character_octa.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
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
        game_view.setup()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "MapGame")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
