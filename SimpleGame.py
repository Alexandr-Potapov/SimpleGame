import random


class Player(object):
    def __init__(self, name):
        self._health = 100
        self.name = name
        self.haveExtraHealBonus = False

    def get_attacked(self, damage):
        self._health -= damage

        if self._health <= 0:
            self._health = 0

        return self._health == 0

    @staticmethod
    def fight(attacker, defender, damage):
        return defender.get_attacked(damage)

    @staticmethod
    def heal(current_player, other_player, health_point):
        current_player._health += health_point

        if current_player._health > 100:
            current_player._health = 100

    def get_health(self):
        return self._health

    def get_info(self, end_of_printing='\n'):
        print('%s: %s' % (self.name, self._health), end=end_of_printing)


human, computer = Player('Human'), Player('AI')
choices = [1, 2, 3]
choicesWithExtraHeal = [1, 2, 3, 3]
steps = {
    1: {'message': 'Нанести умеренный урон (%s единиц урона)',
        'rangeHP': [15, 25],
        'action': Player.fight},
    2: {'message': 'Нанести урон в увеличеном диапазоне (%s единиц урона)',
        'rangeHP': [10, 35],
        'action': Player.fight},
    3: {'message': 'Исцелить себя (%s единиц здоровья)',
        'rangeHP': [15, 25],
        'action': Player.heal}
    }

print('НАЧИНАЕМ ИГРУ!')
print('Рандомно выбираем стартующего...')
currentPlayer = random.choice((human, computer))
otherPlayer = human if currentPlayer == computer else computer

print('СТАРТУЕТ ИГРОК %s\n' % currentPlayer.name)

while True:
    print('---Ход игрока %s' % currentPlayer.name)

    # Определям нужно ли игроку "computer"
    # дать увеличеный шанс получения шага "Вылечиться".
    if not currentPlayer.haveExtraHealBonus and currentPlayer == computer\
            and currentPlayer.get_health() <= 35:
        print('У игрока %s осталось мало здоровья, повышен шанс получить лечение!' % computer.name)
        currentPlayer.haveExtraHealBonus = True

    # рандомно выбираем ход
    if currentPlayer.haveExtraHealBonus:
        currentStep = random.choice(choicesWithExtraHeal)
    else:
        currentStep = random.choice(choices)

    print('Рандомно выпал ход под номером %s:' % currentStep, end=' ')

    # Выполняем выбранное действие (с соотв. настройками), получая данные из словаря steps.
    start = steps[currentStep]['rangeHP'][0]
    end = steps[currentStep]['rangeHP'][1]
    randomHP = random.randint(start, end)

    print(steps[currentStep]['message'] % randomHP)

    isPlayerDead = steps[currentStep]['action'](currentPlayer, otherPlayer, randomHP)

    human.get_info()
    computer.get_info('\n\n')

    if isPlayerDead:
        print('У игрока %s закончилось здоровье, игра окончена!' % otherPlayer.name)
        break

    currentPlayer, otherPlayer = otherPlayer, currentPlayer
