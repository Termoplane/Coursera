from abc import ABC, abstractmethod

class AbstractEffect(Hero, ABC):

    def __init__(self, base):
        self.base = base
    
    @abstractmethod
    def get_positive_effects(self):
        return self.base.positive_effects.copy()
    
    @abstractmethod
    def get_negative_effects(self):
        return self.base.negative_effects.copy()

    @abstractmethod
    def get_stats(self):
        return self.base.stats.copy()

class AbstractPositive(AbstractEffect):

    def get_negative_effects(self):
        return self.base.get_negative_effects()

class AbstractNegative(AbstractEffect):

    def get_positive_effects(self):
        return self.base.get_positive_effects()

class Berserk(AbstractPositive):
    
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Berserk']

    def get_stats(self):
        stats = self.base.get_stats()
        stats['HP'] += 50
        stats['Strength'] += 7
        stats['Endurance'] += 7
        stats['Agility'] += 7
        stats['Luck'] += 7
        stats['Perception'] -= 3
        stats['Charisma'] -= 3
        stats['Intelligence'] -= 3
        return stats

class Blessing(AbstractPositive):
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Blessing']

    def get_stats(self):
        stats = self.base.get_stats()
        stats['Strength'] += 2
        stats['Endurance'] += 2
        stats['Agility'] += 2
        stats['Luck'] += 2
        stats['Perception'] += 2
        stats['Charisma'] += 2
        stats['Intelligence'] += 2
        return stats

class Weakness(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Weakness']

    def get_stats(self):
        stats = self.base.get_stats()
        stats['Strength'] -= 4
        stats['Endurance'] -= 4
        stats['Agility'] -= 4
        return stats

class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['EvilEye']

    def get_stats(self):
        stats = self.base.get_stats()
        stats['Luck'] -= 10
        return stats

class Curse(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Curse']

    def get_stats(self):
        stats = self.base.get_stats()
        stats['Strength'] -= 2
        stats['Endurance'] -= 2
        stats['Agility'] -= 2
        stats['Luck'] -= 2
        stats['Perception'] -= 2
        stats['Charisma'] -= 2
        stats['Intelligence'] -= 2
        return stats
