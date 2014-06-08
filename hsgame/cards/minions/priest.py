import hsgame.targeting
from hsgame.constants import CHARACTER_CLASS, CARD_RARITY
from hsgame.game_objects import MinionCard, Minion
from hsgame.cards.battlecries import take_control_of_minion

__author__ = 'Daniel'


class CabalShadowPriest(MinionCard):
    def __init__(self):
        super().__init__("Cabal Shadow Priest", 6, CHARACTER_CLASS.PRIEST, CARD_RARITY.EPIC, hsgame.targeting.find_enemy_minion_battlecry_target, lambda target: target.attack_power <= 2 and target.spell_targetable())

    def create_minion(self, player):
        return Minion(4, 5, battlecry=take_control_of_minion)
    
    
class Lightwell(MinionCard):
    def __init__(self):
        super().__init__("Lightwell", 2, CHARACTER_CLASS.PRIEST, CARD_RARITY.RARE)

    def create_minion(self, player):
        def heal_damaged_friendly_character():
            targets = hsgame.targeting.find_friendly_spell_target(player.game, lambda character: character.health != character.max_health)
            if len(targets) != 0:
                targets[player.game.random(0, len(targets) - 1)].heal(3)
        
        minion = Minion(0, 5)
        player.bind("turn_started", heal_damaged_friendly_character)
        minion.bind_once("silenced", lambda: player.unbind("turn_started", heal_damaged_friendly_character))
        return minion