# pylint: skip-file


from abc import ABC


class Agent(ABC):
    """
    Wordle agent.
    """

    def __init__(self) -> None:
        ...


class ManualAgent(Agent):
    ...
