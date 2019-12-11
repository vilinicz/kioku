from datetime import datetime
from collections import deque

import numpy as np


class Buffer:
    def __init__(self, size: int = 8, lifetime: int = 3,
                 tolerance: float = 0.6):
        self.groups = []
        self.size = size
        self.lifetime = lifetime
        self.tolerance = tolerance

    # face is a tuple of (encoding, location, frame)
    def add(self, face):
        # Clear old groups before
        self.clean()

        # Collect list of distances between new face and each group
        # Add face for existing nearest group if present
        # Otherwise, create new group for face
        d = [g.distance(face[0]) for g in self.groups]
        if any(self.groups) and min(d) < self.tolerance:
            self.groups[d.index(min(d))].add(face)
        else:
            # Increase size for potentially unknown face
            # size = self.size * 2 if any(self.groups) else self.size
            self.groups.append(Group(face, self.size))

    # Return full groups
    def get_active_groups(self):
        return [
            g.faces for g in
            filter(lambda g: len(g.faces) >= g.size, self.groups)
        ]

    # Delete old groups
    def clean(self):
        self.groups = \
            list(filter(lambda g:
                        (datetime.now() - g.timestamp).seconds < self.lifetime,
                        self.groups))


class Group:
    def __init__(self, face, size: int = 8):
        self.size = size
        self.faces = deque(maxlen=size)
        self.timestamp = datetime.now()
        self.add(face)

    def add(self, face):
        self.timestamp = datetime.now()
        self.faces.append(face)

    def distance(self, face):
        encodings = np.array([f[0] for f in self.faces])
        return np.mean(np.linalg.norm(encodings - face, axis=1))
