class Rule:
    def __init__(self, poss):
        self.poss = poss

    def __repr__(self):
        if self.poss:
            return "<Rule:{}>".format(",".join(self.poss))
        return "None"

    def __eq__(self, other):
        return self.poss == other.poss

    def __hash__(self):
        if self.poss is None:
            return hash(0)
        return hash(','.join(self.poss))

    def is_match(self, morpheme):
        """
        :type morpheme: 
        :rtype: bool
        """
        # TODO: もっと効率的な持ち方する
        if self.poss is None:
            return True

        for rule_pos, target_pos in zip(self.poss, morpheme.poss):
            if rule_pos == 'nan':
                continue
            elif rule_pos.startswith('~'):
                if target_pos in rule_pos[1:].split('|'):
                    return False
            elif target_pos not in rule_pos.split('|'):
                return False
        return True
