from statements import Statement
from const import logger
from util import find_all_player_indices, get_random_center, get_random_player, swap_characters
import const
import random

class Player():
    def __init__(self, player_index):
        self.player_index = player_index

    def get_statement(self, stated_roles=None, previous=None):
        return random.choice(tuple(self.statements))

    def json_repr(self):
        return {'type': self.role, 'player_index': self.player_index, 'statements': self.statements}

    def __repr__(self):
        return '<' + self.role + '>'


class Seer(Player):
    def __init__(self, player_index, game_roles):
        super().__init__(player_index)
        seer_peek_index, seer_peek_character, seer_peek_index2, seer_peek_character2 = self.seer_init(game_roles)
        self.role = 'Seer'
        self.new_role = ''
        self.statements = self.get_seer_statements(player_index, seer_peek_index, seer_peek_character,
                                                    seer_peek_index2, seer_peek_character2)

    def seer_init(self, game_roles):
        ''' Initializes Seer - either sees 2 center cards or 1 player card. '''
        # Picks two center cards more often, because that generally yields higher win rates.
        choose_center = random.choices([True, False], [0.9, 0.1])
        if choose_center and const.NUM_CENTER > 1:
            seer_peek_index = get_random_center()
            seer_peek_character = game_roles[seer_peek_index]
            seer_peek_index2 = get_random_center()
            while seer_peek_index2 == seer_peek_index:
                seer_peek_index2 = get_random_center()
            seer_peek_character2 = game_roles[seer_peek_index2]
            logger.debug('[Hidden] Seer sees that Center ' + str(seer_peek_index - const.NUM_PLAYERS) +
                    ' is a ' + str(seer_peek_character) + ' and Center ' + str(seer_peek_index2 - const.NUM_PLAYERS) +
                    ' is a ' + str(seer_peek_character2))
            return seer_peek_index, seer_peek_character, seer_peek_index2, seer_peek_character2
        else:
            seer_peek_index = get_random_player()
            while seer_peek_index == self.player_index:
                seer_peek_index = get_random_player()
            seer_peek_character = game_roles[seer_peek_index]
            logger.debug('[Hidden] Seer sees that Player ' + str(seer_peek_index) +
                    ' is a ' + str(seer_peek_character))
            return seer_peek_index, seer_peek_character, None, None

    @staticmethod
    def get_seer_statements(player_index, seen_index, seen_role, seen_index2=None, seen_role2=None):
        sentence = 'I am a Seer and I saw that Player ' + str(seen_index) + ' was a ' + str(seen_role) + '.'
        knowledge = [(player_index, {'Seer'}), (seen_index, {seen_role})]
        if seen_index2 != None:
            sentence = 'I am a Seer and I saw that Center ' + str(seen_index - const.NUM_PLAYERS) \
                        + ' was a ' + str(seen_role) + ' and that Center ' \
                        + str(seen_index2 - const.NUM_PLAYERS) + ' was a ' + str(seen_role2) + '.'
            knowledge += [(seen_index2, {seen_role2})]
        return [Statement(sentence, knowledge)]


class Villager(Player):
    def __init__(self, player_index):
        super().__init__(player_index)
        self.role = 'Villager'
        self.new_role = ''
        self.statements = self.get_villager_statements(player_index)

    @staticmethod
    def get_villager_statements(player_index):
        return [Statement('I am a Villager.' , [(player_index, {'Villager'})])]


class Mason(Player):
    def __init__(self, player_index, game_roles, ORIGINAL_ROLES):
        super().__init__(player_index)
        mason_indices = self.mason_init(game_roles, ORIGINAL_ROLES)
        self.role = 'Mason'
        self.new_role = ''
        self.statements = self.get_mason_statements(player_index, mason_indices)

    def mason_init(self, game_roles, ORIGINAL_ROLES):
        ''' Initializes Mason - sees all other Masons. '''
        mason_indices = find_all_player_indices(ORIGINAL_ROLES, 'Mason')
        logger.debug('[Hidden] Masons are at indices: ' + str(mason_indices))
        return mason_indices

    @staticmethod
    def get_mason_statements(player_index, mason_indices):
        if len(mason_indices) == 1:
            sentence = 'I am a Mason. The other Mason is not present.'
            knowledge = [(player_index, {'Mason'})]
            for ind in range(const.NUM_PLAYERS):
                if ind != player_index:
                    knowledge.append((ind, set(const.ROLE_SET) - {'Mason'}))
        else:
            other_mason = mason_indices[0] if mason_indices[0] != player_index else mason_indices[1]
            sentence = 'I am a Mason. The other Mason is Player ' + str(other_mason) + '.'
            knowledge = [(player_index, {'Mason'}), (other_mason, {'Mason'})]
        return [Statement(sentence, knowledge)]


class Robber(Player):
    def __init__(self, player_index, game_roles):
        super().__init__(player_index)
        robber_choice_index, robber_choice_character = self.robber_init(game_roles)
        self.role = 'Robber'
        self.new_role = robber_choice_character
        self.statements = self.get_robber_statements(player_index, robber_choice_index, robber_choice_character)

    def robber_init(self, game_roles):
        ''' Initializes Robber - switches roles with another player. '''
        robber_choice_index = get_random_player()
        while robber_choice_index == self.player_index:
            robber_choice_index = get_random_player()
        robber_choice_character = game_roles[robber_choice_index]
        logger.debug('[Hidden] Robber switches with Player ' + str(robber_choice_index) +
                    ' and becomes a ' + str(robber_choice_character))
        swap_characters(game_roles, self.player_index, robber_choice_index)
        return robber_choice_index, robber_choice_character

    @staticmethod
    def get_robber_statements(player_index, robber_choice_index, robber_choice_character):
        sentence = 'I am a Robber and I swapped with Player ' + str(robber_choice_index) + \
                    '. I am now a ' + robber_choice_character + '.'
        knowledge = [(player_index, {'Robber'}), (robber_choice_index, {robber_choice_character})]
        switches = [(const.ROBBER_PRIORITY, robber_choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]

    def get_statement(self, stated_roles, previous):
        if self.new_role == 'Wolf':
            from wolf import Wolf
            logger.warning('Robber is a Wolf now!')
            robber_wolf = Wolf(self.player_index)
            return robber_wolf.get_statement(stated_roles, previous)
        else:
            return random.choice(tuple(self.statements))


class Troublemaker(Player):
    def __init__(self, player_index, game_roles):
        super().__init__(player_index)
        trblmkr_index1, trblmkr_index2 = self.troublemaker_init(game_roles)
        self.role = 'Troublemaker'
        self.new_role = ''
        self.statements = self.get_troublemaker_statements(player_index, trblmkr_index1, trblmkr_index2)

    def troublemaker_init(self, game_roles):
        ''' Initializes Troublemaker - switches one player with another player. '''
        troublemaker_choice_index1 = get_random_player()
        troublemaker_choice_index2 = get_random_player()
        while troublemaker_choice_index1 == self.player_index:
            troublemaker_choice_index1 = get_random_player()
        while troublemaker_choice_index2 == self.player_index or troublemaker_choice_index2 == troublemaker_choice_index1:
            troublemaker_choice_index2 = get_random_player()
        swap_characters(game_roles, troublemaker_choice_index1, troublemaker_choice_index2)
        logger.debug('[Hidden] Troublemaker switches Player ' + str(troublemaker_choice_index1)
            + ' with Player ' + str(troublemaker_choice_index2))
        return troublemaker_choice_index1, troublemaker_choice_index2

    @staticmethod
    def get_troublemaker_statements(player_index, trblmkr_index1, trblmkr_index2):
        sentence = 'I am a Troublemaker and I swapped Player ' + str(trblmkr_index1) + \
                    ' and Player ' + str(trblmkr_index2) + '.'
        knowledge = [(player_index, {'Troublemaker'})]
        switches = [(const.TROUBLEMAKER_PRIORITY, trblmkr_index1, trblmkr_index2)]
        return [Statement(sentence, knowledge, switches)]


class Drunk(Player):
    def __init__(self, player_index, game_roles):
        super().__init__(player_index)
        drunk_choice_index = self.drunk_init(game_roles)
        self.role = 'Drunk'
        self.new_role = ''
        self.statements = self.get_drunk_statements(player_index, drunk_choice_index)

    def drunk_init(self, game_roles):
        ''' Initializes Drunk - switches with a card in the center. '''
        assert(const.NUM_CENTER != 0)
        drunk_choice_index = get_random_center()
        logger.debug('[Hidden] Drunk switches with Center Card ' + str(drunk_choice_index - const.NUM_PLAYERS) +
                    ' and unknowingly becomes a ' + str(game_roles[drunk_choice_index]))
        swap_characters(game_roles, self.player_index, drunk_choice_index)
        return drunk_choice_index

    @staticmethod
    def get_drunk_statements(player_index, drunk_choice_index):
        sentence = 'I am a Drunk and I swapped with Center ' + \
                    str(drunk_choice_index - const.NUM_PLAYERS) + '.'
        knowledge = [(player_index, {'Drunk'})]
        switches = [(const.DRUNK_PRIORITY, drunk_choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]


class Insomniac(Player):
    def __init__(self, player_index, game_roles):
        super().__init__(player_index)
        insomniac_new_role = self.insomniac_init(game_roles)
        self.role = 'Insomniac'
        self.new_role = insomniac_new_role
        self.statements = self.get_insomniac_statements(player_index, insomniac_new_role)

    def insomniac_init(self, game_roles):
        ''' Initializes Insomniac - learns new role. '''
        insomniac_new_role = game_roles[self.player_index]
        logger.debug('[Hidden] Insomniac wakes up as a ' + insomniac_new_role)
        return insomniac_new_role

    @staticmethod
    def get_insomniac_statements(player_index, insomniac_new_role, new_insomniac_index=None):
        knowledge = [(player_index, {'Insomniac'})]
        sentence = 'I am a Insomniac and when I woke up I was a ' + str(insomniac_new_role) + '.'
        if new_insomniac_index == None:
            if insomniac_new_role != 'Insomniac':
                sentence += ' I don\'t know who I switched with.'
        else:
            sentence += ' I switched with Player ' + str(new_insomniac_index) + '.'
        # switches = [(player_index, new_insomniac_index)]  # TODO
        return [Statement(sentence, knowledge)]

    def get_statement(self, stated_roles, previous):
        if self.new_role == 'Wolf':
            from wolf import Wolf
            logger.warning('Insomniac is a Wolf now!')
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
