def numerate_dict(rules: dict) -> dict:
    rule_dict = rules
    numbered_rule_dict = {}

    for index, items in enumerate(rule_dict.items()):
        rule = items[0]
        action = items[1]

        numbered_rule_dict.update({str(index): {rule: action}})

    return numbered_rule_dict
