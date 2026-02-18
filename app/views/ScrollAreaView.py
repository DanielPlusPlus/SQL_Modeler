from PySide6.QtWidgets import QScrollArea


class ScrollAreaView(QScrollArea):
    def __init__(self, ParentWindow):
        super().__init__(ParentWindow)

    def setupUI(self, DrawingAreaView):
        self.setWidget(DrawingAreaView)
        print(DrawingAreaView.styleSheet())
        self.setWidgetResizable(True)
