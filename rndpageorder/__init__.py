from collections import Counter
from otree.api import *
from random import Random
from re import findall


doc = """
oTree page randomization example
"""


class C(BaseConstants):
    NAME_IN_URL = "rndpageorder"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5  # equal to the number of pages


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # this field is required
    shown_in_this_round = models.IntegerField()

    # example field on pages Q1, Q4
    age = models.IntegerField()
    siblings = models.IntegerField()


def creating_session(subsession):
    if subsession.round_number != 1:
        return

    r = (
        Random(subsession.session.config["seed"])
        if "seed" in subsession.session.config
        and subsession.session.config["seed"] != -1
        else Random()
    )

    rounds = range(1, C.NUM_ROUNDS + 1)
    orders = Counter()

    for player in subsession.get_players():
        pages = list(rounds)

        r.shuffle(pages)
        orders[tuple(pages)] += 1

        for round_, page in zip(rounds, pages):
            player.in_round(round_).shown_in_this_round = page

    print(f"{__name__}: {len(orders)} orders, frequencies:")

    for o, c in orders.items():
        print(o, c)


# PAGES
def page_id(page):
    try:
        return int("".join(findall(r"\d", page.__name__)))
    except Exception as e:
        return None


def randomized_order(page):
    current_page_id = page_id(page)

    assert current_page_id is not None

    assert (
        current_page_id >= 1 and current_page_id <= C.NUM_ROUNDS
    ), f"Page {page.__name__} has invalid number(s)"

    assert (
        page.is_displayed == Page.is_displayed
    ), f"Page {page.__name__} has is_displayed - you cannot use @randomized_order directly"

    @staticmethod
    def is_displayed(player):
        i_am = current_page_id

        return i_am == player.shown_in_this_round

    page.is_displayed = is_displayed

    return page


class Start(Page):
    # non-randomized page, shown at beginning

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


@randomized_order
class Q1(Page):
    form_model = "player"
    form_fields = ["siblings"]


@randomized_order
class Q2(Page):
    pass


@randomized_order
class Q3(Page):
    pass


class Q4Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.shown_in_this_round == 4


@randomized_order
class Q4(Page):
    form_model = "player"
    form_fields = ["age"]


@randomized_order
class Q5(Page):
    pass


class End(Page):
    # non-randomized page, shown at the end

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [Start, Q1, Q2, Q3, Q4Instructions, Q4, Q5, End]

assert all(
    any((page_id(p) == i) for p in page_sequence) for i in range(1, C.NUM_ROUNDS + 1)
), "Some page that ought to be randomized is missing in the page_sequence"
