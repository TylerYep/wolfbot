from statements import Statement
from const import logger
import const
import random

class Player():
    def __init__(self, player_index):
        self.player_index = player_index

    def get_statement(self, stated_roles=None, previous=None):
        return random.choice(tuple(self.statements))

    def __repr__(self):
        return "<" + self.role + ">"


class Seer(Player):
    def __init__(self, player_index, seer_peek_index, seer_peek_character, seer_peek_index2, seer_peek_character2):
        super().__init__(player_index)
        self.role = 'Seer'
        self.statements = self.get_seer_statements(player_index, seer_peek_index, seer_peek_character,
                                                    seer_peek_index2, seer_peek_character2)

    @staticmethod
    def get_seer_statements(player_index, seen_index, seen_role, seen_index2=None, seen_role2=None):
        sentence = "I am a Seer and I saw that Player " + str(seen_index) + " was a " + str(seen_role) + "."
        knowledge = [(player_index, {'Seer'}), (seen_index, {seen_role})]
        if seen_index2 != None:
            sentence = "I am a Seer and I saw that Center " + str(seen_index - const.NUM_PLAYERS) + " was a " + str(seen_role) \
                        + " and that Center " + str(seen_index2 - const.NUM_PLAYERS) + " was a " + str(seen_role2) + "."
            knowledge += [(seen_index2, {seen_role2})]
        return [Statement(sentence, knowledge)]


class Villager(Player):
    def __init__(self, player_index):
        super().__init__(player_index)
        self.role = 'Villager'
        self.statements = self.get_villager_statements(player_index)

    @staticmethod
    def get_villager_statements(player_index):
        return [Statement("I am a Villager." , [(player_index, {'Villager'})])]


class Mason(Player):
    def __init__(self, player_index, mason_indices):
        super().__init__(player_index)
        self.role = 'Mason'
        self.statements = self.get_mason_statements(player_index, mason_indices)

    @staticmethod
    def get_mason_statements(player_index, mason_indices):
        if len(mason_indices) == 1:
            sentence = "I am a Mason. The other Mason is not present."
            knowledge = [(player_index, {'Mason'})]
            for ind in range(const.NUM_PLAYERS):
                if ind != player_index:
                    knowledge.append((ind, set(const.ROLE_SET) - {'Mason'}))
        else:
            otherMason = mason_indices[0] if mason_indices[0] != player_index else mason_indices[1]
            sentence = "I am a Mason. The other Mason is Player " + str(otherMason) + '.'
            knowledge = [(player_index, {'Mason'}), (otherMason, {'Mason'})]
        return [Statement(sentence, knowledge)]


class Robber(Player):
    def __init__(self, player_index, robber_choice_index, robber_choice_character):
        super().__init__(player_index)
        self.role = 'Robber'
        self.new_role = robber_choice_character
        self.statements = self.get_robber_statements(player_index, robber_choice_index, robber_choice_character)

    @staticmethod
    def get_robber_statements(player_index, robber_choice_index, robber_choice_character):
        sentence = "I am a Robber and I swapped with Player " + str(robber_choice_index) + \
                    ". I am now a " + robber_choice_character + "."
        knowledge = [(player_index, {'Robber'}), (robber_choice_index, {robber_choice_character})]
        switches = [(const.ROBBER_PRIORITY, robber_choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]

    def get_statement(self, stated_roles, previous):
        if self.new_role == 'Wolf':
            from wolf import Wolf
            logger.warning("Robber is a Wolf now!")
            robber_wolf = Wolf(self.player_index)
            return robber_wolf.get_statement(stated_roles, previous)
        else:
            return random.choice(tuple(self.statements))


class Troublemaker(Player):
    def __init__(self, player_index, trblmkr_index1, trblmkr_index2):
        super().__init__(player_index)
        self.role = 'Troublemaker'
        self.statements = self.get_troublemaker_statements(player_index, trblmkr_index1, trblmkr_index2)

    @staticmethod
    def get_troublemaker_statements(player_index, trblmkr_index1, trblmkr_index2):
        sentence = "I am a Troublemaker and I swapped Player " + str(trblmkr_index1) + \
                    " and Player " + str(trblmkr_index2) + "."
        knowledge = [(player_index, {'Troublemaker'})]
        switches = [(const.TROUBLEMAKER_PRIORITY, trblmkr_index1, trblmkr_index2)]
        return [Statement(sentence, knowledge, switches)]


class Drunk(Player):
    def __init__(self, player_index, drunk_choice_index):
        super().__init__(player_index)
        self.role = 'Drunk'
        self.statements = self.get_drunk_statements(player_index, drunk_choice_index)

    @staticmethod
    def get_drunk_statements(player_index, drunk_choice_index):
        sentence = "I am a Drunk and I swapped with Center " + \
                    str(drunk_choice_index - const.NUM_PLAYERS) + "."
        knowledge = [(player_index, {'Drunk'})]
        switches = [(const.DRUNK_PRIORITY, drunk_choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]


class Insomniac(Player):
    def __init__(self, player_index, insomniac_new_role):
        super().__init__(player_index)
        self.role = 'Insomniac'
        self.new_role = insomniac_new_role
        self.statements = self.get_insomniac_statements(player_index, insomniac_new_role)

    @staticmethod
    def get_insomniac_statements(player_index, insomniac_new_role, new_insomniac_index=None):
        knowledge = [(player_index, {'Insomniac'})]
        sentence = "I am a Insomniac and when I woke up I was a " + str(insomniac_new_role) + "."
        if new_insomniac_index == None:
            if insomniac_new_role != 'Insomniac':
                sentence += " I don't know who I switched with."
        else:
            sentence += " I switched with Player " + str(new_insomniac_index) + '.'
        # switches = [(player_index, new_insomniac_index)]  # TODO put this into known_switches
        return [Statement(sentence, knowledge)]

    def get_statement(self, stated_roles, previous):
        if self.new_role == 'Wolf':
            from wolf import Wolf
            logger.warning("Insomniac is a Wolf now!")
            insomniac_wolf = Wolf(self.player_index)
            return insomniac_wolf.get_statement(stated_roles, previous)
        else:
            possible_switches = []
            for i in range(len(stated_roles)):
                if stated_roles[i] == self.new_role:
                    possible_switches.append(i)
            if len(possible_switches) == 1: # TODO how to handle multiple possible switches
                self.statements = self.get_insomniac_statements(self.player_index, self.new_role, possible_switches[0])
            return random.choice(tuple(self.statements))
