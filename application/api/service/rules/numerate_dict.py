def numerate_dict(rules: dict) -> dict:
    rule_dict = rules["rules"]
    numbered_rule_dict = {}

    for index, items in enumerate(rule_dict.items()):
        rule = items[0]
        action = items[1]

        numbered_rule_dict.update({index: {rule: action}})

    return {"rules_numbered": numbered_rule_dict}
