from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):    # FigureCanvas sınıfından miras alır
    def __init__(self, parent=None): 
        self.fig = Figure(figsize=(5, 4), dpi=100) # Yeni bir Figure nesnesi oluşturur
        self.ax = self.fig.add_subplot(111) # Figure üzerine bir subplot ekler
        super().__init__(self.fig) # Üst sınıfın yapıcı metodunu çağırır
