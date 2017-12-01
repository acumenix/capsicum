import capsicum


def test_load_rule():
    engine = capsicum.RuleEngine()
    engine.load_rule('./rules/default.py')


def test_load_rule_dir():
    engine = capsicum.RuleEngine()
    engine.load_rule_dir('./rules/')
