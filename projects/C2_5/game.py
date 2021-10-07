from primitive_bot import PrimitiveBot
from user import User


class Game:
    def __init__(self):
        self.user = User()
        self.bot = PrimitiveBot()
        self._user_name = 'user'

    def play(self):
        while not self.user.all_ships_sunken() and not self.bot.all_ships_sunken():
            self.bot.print_board_repr_with_no_ships()
            self._shot(self.user, self.bot)
            self._shot(self.bot, self.user)
            self.user.print_board_repr_with_ships()

        print('Game Over')
        print('*********')
        if self.user.all_ships_sunken():
            print("Bot's victory!")
        if self.bot.all_ships_sunken():
            print("User's victory!")

    def _shot(self, shooter, victim):
        while True:
            try:
                if victim.all_ships_sunken() or shooter.all_ships_sunken():
                    return
                print(f'{shooter.get_name()} shots now!')
                shot = shooter.get_next_own_shot()
                message = victim.foreign_shot_is_invalid(shot)
                if message:
                    print(message)
                    continue
                victim.set_foreign_shot(shot)
                if (shooter.get_name().lower() == self._user_name):
                    self.bot.print_board_repr_with_no_ships()
                if victim.foreign_shot_is_hit(shot):
                    shooter.set_own_shot_hit()
                    print(f"{shooter.get_name()}'s shot {shot} hits on target, service goes on")
                else:
                    shooter.set_own_shot_miss()
                    print(f"{shooter.get_name()}'s shot {shot} missed, service finished")
                    return
            except Exception as e:
                print(str(e))


if __name__=='__main__':
    Game().play()