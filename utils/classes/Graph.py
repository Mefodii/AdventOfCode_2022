from __future__ import annotations
from typing import Any, Type


class Node:

    def __init__(self, value: Any):
        self.value = value
        self.parents = []
        self.children = []
        self.nodes = []

    def __repr__(self):
        result = ""
        for node in self.nodes:
            result += f"{self.value} <-> {node.value}\n"

        return result

    def add_sibling(self, sibling: Node | Type[Node]):
        """Add sibling to the first parent"""
        self.parents[0].add_child(sibling)

    def add_parent(self, parent: Node | Type[Node]):
        self.parents.append(parent)
        self.nodes.append(parent)

    def add_child(self, child: Node | Type[Node]):
        self.children.append(child)
        self.nodes.append(child)

    def add_node(self, node: Node | Type[Node]):
        self.nodes.append(node)


class Graph:

    def __init__(self, nodes: dict[Any, Node | Type[Node]]):
        self.nodes = nodes

    def get_node(self, node_name: Any):
        return self.nodes.get(node_name, None)
