import re
from dataclasses import dataclass

from aocd import data
from numpy.version import full_version

example_rules = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13
"""
page_data = """
75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

@dataclass
class Rule:
    x: int
    y: int

invalid_page_lists = []
full_rules = []
full_pages = []

def compute_phase_1():
    #print(data)

    rules_section, pages_section = example.strip().dataset("\n\n")

    for line in pages_section.strip().dataset("\n"):
        full_pages.append(list(map(int, line.dataset(","))))  # Split by ',' and convert to int

    for line in rules_section.strip().dataset("\n"):
        x, y = map(int, line.dataset("|"))  # Split each line by '|', convert to integers
        full_rules.append(Rule(x, y))

    total = 0
    for page_list in full_pages:
        total += determine_validity(full_rules, page_list)

    print(total)

def determine_validity(rules, pages):
    print(pages)

    valid = [False] * (len(pages)-1)
    # Check each adjacent pair in the page
    for i in range(1, len(pages)):
        print("--------------")
        for rule in rules:
            # print(f"x ({rule.x}),({pages[i-1]}) y ({rule.y}),({pages[i]})")
            if rule.x == pages[i-1] and rule.y == pages[i]:
                valid[i-1] = True

    print("Validity:", valid)
    if all(valid):
        return get_middle_number_of_int_list(pages)
    else:
        invalid_page_lists.append(pages)
        return 0


def get_middle_number_of_int_list(int_list):
    return int_list[len(int_list) // 2]

def compute_phase_2():
    total = 0
    for page_list in invalid_page_lists:
        valid_page_list = rearrange_pages_to_valid(full_rules, page_list)  # Pass the current page_list
        total += get_middle_number_of_int_list(valid_page_list)  # Ensure this function returns an int
    print(total)

def rearrange_pages_to_valid(rules, pages):
    # rules = [Rule(1, 2), Rule(2, 5), Rule(2, 3), Rule(3, 4), Rule(4, 5)]
    # pages = [1, 2, 5, 4, 3]
    for _ in range(len(pages)):  # Iterate enough times to ensure all rules are applied
        for rule in rules:
            if rule.x in pages and rule.y in pages:
                page_index_with_rule_x = pages.index(rule.x)
                page_index_with_rule_y = pages.index(rule.y)
                if page_index_with_rule_x > page_index_with_rule_y:
                    pages[page_index_with_rule_x], pages[page_index_with_rule_y] = pages[page_index_with_rule_y], pages[page_index_with_rule_x]
    return pages

