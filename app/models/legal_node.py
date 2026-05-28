from typing import List, Optional
import uuid
class LegalNode:
    def __init__(
        self,
        node_type: str,
        title: str,
        text: str,
        parent=None,
        children: Optional[List] = None,
        metadata: Optional[dict] = None,
        node_id: Optional[str] = None

    ):
            # unique node id
            self.node_id = node_id or str(uuid.uuid4())

            # type of node
            self.node_type = node_type

            # title of the node 
            # (e.g., "Section 1", "Clause 2.3")
            self.title = title

            # actual legal text
            self.text = text

            # parent node reference
            self.parent = parent

            # list of child nodes
            self.children = children or []

            # metadata dictionary for additional info 
            # (e.g., source, annotations)
            self.metadata = metadata or {}
        
    # here attach child node to current node
    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)
    
    # here leaf node means no children below it
    def is_leaf(self):
        return len(self.children) == 0
