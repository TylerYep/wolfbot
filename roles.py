from statements import Statement
import random
import const

class Player():
    def __init__(self, player_index):
        self.player = player_index

    def getNextStatement(self):
        return random.choice(tuple(self.statements))

    def __repr__(self):
        return "<" + self.role + ">"


class Wolf(Player):
    def __init__(self, player_index, wolf_indices):
        super().__init__(player_index)
        self.role = 'Wolf'
        # self.wolf_indices = wolf_indices
        self.statements = self.get_wolf_statements(player_index, wolf_indices)

    @staticmethod
    def get_wolf_statements(player_index, wolf_indices):
        statements = Villager.get_villager_statements(player_index)
        for i in range(const.NUM_PLAYERS):
            statements += Mason.get_mason_statements(player_index, [player_index, i])

            # Wolf-seer more likely to declare they saw a villager
            # Wolf should not give away other wolves or themselves
            for role in const.ROLES:
                if i not in wolf_indices and role != 'Seer':
                    statements += Seer.get_seer_statements(player_index, i, role)
        return statements


class Seer(Player):
    def __init__(self, player_index, seer_peek_index, seer_peek_character):
        super().__init__(player_index)
        self.role = 'Seer'
        self.statements = self.get_seer_statements(player_index, seer_peek_index, seer_peek_character)

    @staticmethod
    def get_seer_statements(player_index, seen_index, seen_role):
        sentence = "I am a Seer and I saw that Player " + str(seen_index) + " was a " + str(seen_role) + "."
        knowledge = [(player_index, {'Seer'}), (seen_index, {seen_role})]
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
        # self.mason_indices = mason_indices
        self.statements = self.get_mason_statements(player_index, mason_indices)

    @staticmethod
    def get_mason_statements(player_index, mason_indices):
        if len(mason_indices) == 1:
            # TODO saving this knowledge
            sentence = "I am a Mason. The other Mason is not present."
            knowledge = [(player_index, {'Mason'})]
        else:
            otherMason = mason_indices[0] if mason_indices[0] != player_index else mason_indices[1]
            sentence = "I am a Mason. The other Mason is Player " + str(otherMason)
            knowledge = [(player_index, {'Mason'}), (otherMason, {'Mason'})]
        return [Statement(sentence, knowledge)]


class Robber(Player):
    def __init__(self, player_index, robber_choice_index, robber_choice_character):
        super().__init__(player_index)
        self.role = 'Robber'
        self.statements = self.get_robber_statements(player_index, robber_choice_index, robber_choice_character)

    # TODO Finish
    @staticmethod
    def get_robber_statements(player_index, robber_choice_index, robber_choice_character):
        # if robber_choice_character != 'Wolf':
        sentence = "I am a Robber and I swapped with Player " + str(robber_choice_index)
        sentence += ". I am now a " + robber_choice_character
        knowledge = [(robber_choice_index, {robber_choice_character}), (player_index, {'Robber'})]
        return [Statement(sentence, knowledge)]


class Troublemaker(Player):
    def __init__(self, player_index):
        super().__init__(player_index)
        self.role = 'Troublemaker'
        self.statements = self.get_troublemaker_statements(player_index)


class Drunk(Player):
    def __init__(self, player_index):
        super().__init__(player_index)
        self.role = 'Drunk'
        self.statements = self.get_drunk_statements(player_index)
