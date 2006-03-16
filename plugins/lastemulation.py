#!/usr/bin/python
def lastemulation(self, event):
    """Emulation the fishbot.last variable for older modules."""
    if hasattr(self,"oldlast"):
        self.last = self.oldlast.copy()
        self.oldlast[self.getnick(event.source())] = event.arguments()
    else:
        self.oldlast = {self.getnick(event.source()):event.arguments()}

expression = ("", lastemulation)
