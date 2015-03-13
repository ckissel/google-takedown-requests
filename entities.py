"""
Entity and DisplayEntity (i.e. basically model and view) classes for the Google Takedown Requests visualization.
"""


class Entity:
    """
    Represents a requester or domain.

    name: copyright owner name or domain name
    category: requester or target
    size: how large the circle should be
    x, y, width, alpha: line properties
    """
    def __init__(self, name, category, size):
        self.name = name
        self.category = category
        self.size = size
        self.x = None
        self.y = None
        self.width = 1
        self.alpha = 1


class DisplayEntity:
    """
    View class. (Or viewmodel I guess?)
    center: center Entity
    outer: list of Entity objects connected to center
    """
    def __init__(self, center, outer):
        self.center = center
        self.outer = outer
