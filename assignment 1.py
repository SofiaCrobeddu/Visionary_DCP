#NELLA INTERFACCIA METTO IL LOGO DI UPEC, IL NOME DEL PROF, IL NOME DEL GRUPPO E NOSTRI
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSizePolicy
from PyQt5 import uic
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """Matplotlib canvas for embedding plots."""
    def __init__(self, parent=None):
        fig = Figure(tight_layout=True)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()


class SimulationApp(QMainWindow):
    def __init__(self):
        super(SimulationApp, self).__init__()
        # Load the user interface from the .ui file
        uic.loadUi('C:\\Users\\sofyc\\OneDrive\\Desktop\\UPEC\\Data capture and processing\\2 module projects\\assignment_Simulation.ui', self)
        
        # Set the window size
        self.setMinimumSize(1200, 800)

        # Ensure layouts are present
        self.ensure_layout(self.SystemSimulation_box)
        self.ensure_layout(self.NoiseSimulation_box)

        # Connect buttons for selecting the system type
        self.LinearBottom.clicked.connect(lambda: self.run_simulation("linear"))
        self.ExponentialBottom.clicked.connect(lambda: self.run_simulation("exponential"))
        self.LogarithmicBottom.clicked.connect(lambda: self.run_simulation("logarithmic"))

        
        # Connect buttons for selecting the noise type
        self.GaussianNoise.clicked.connect(lambda: self.update_noise_type("gaussian"))
        self.UniformNoise.clicked.connect(lambda: self.update_noise_type("uniform"))
        
        # Connect the button to execute the simulation
        self.RunSimulationBottom.clicked.connect(self.run_current_simulation)

        # Connect sliders to update parameters
        self.a.valueChanged.connect(self.update_a)
        self.b.valueChanged.connect(self.update_b)
        self.lambda_exp.valueChanged.connect(self.update_lambda_exp)
        self.mu_exp.valueChanged.connect(self.update_mu_exp)
        self.a_log.valueChanged.connect(self.update_a_log)
        self.b_log.valueChanged.connect(self.update_b_log)

        self.mu_noise.valueChanged.connect(self.update_mu_noise)
        self.sigma_noise.valueChanged.connect(self.update_sigma_noise)
        self.a_noise.valueChanged.connect(self.update_a_noise)
        self.b_noise.valueChanged.connect(self.update_b_noise)

        # Initial parameters
        self.N = 50  # Number of points
        self.X_min = 5
        self.X_max = 40

        # System parameters
        self.a_val = 1 #Linear
        self.b_val = 1
        self.lambda_exp_val = 1 #Exponential
        self.mu_exp_val = 1
        self.a_log_val = 1 #Logarithmic
        self.b_log_val = 1

        # Noise parameters
        self.noise_type = "gaussian"  # Initial noise type
        self.mu_noise_val = 0
        self.sigma_noise_val = 0.1
        self.a_noise_val = 0.1
        self.b_noise_val = 0.1

    def ensure_layout(self, widget):
        """Ensures that the widget has a vertical layout."""
        if not widget.layout():
            layout = QVBoxLayout(widget)
            widget.setLayout(layout)

    #Update of Linear system parameters
    def update_a(self, value):
        self.a_val = value

    def update_b(self, value):
        self.b_val = value

    #Update of Exponential system parameters
    def update_lambda_exp(self, value):
        self.lambda_exp_val = value

    def update_mu_exp(self, value):
        self.mu_exp_val = value
    
    #Update of Logarithmic system parameters
    def update_a_log(self, value):
        self.a_log_val = value

    def update_b_log(self, value):
        self.b_log_val = value

    #Update of Gaussian noise parameters
    def update_mu_noise(self, value):
        self.mu_noise_val = value

    def update_sigma_noise(self, value):
        self.sigma_noise_val = value

    #Update of Uniform noise parameters
    def update_a_noise(self, value):
        self.a_noise_val = value

    def update_b_noise(self, value):
        self.b_noise_val = value

    #Update noise type
    def update_noise_type(self, noise_type):
        self.noise_type = noise_type

    #Functions to add noise
    def add_gaussian_noise(self, size):
        """Generate Gaussian noise with defined parameters."""
        return np.random.normal(self.mu_noise_val, self.sigma_noise_val, size)

    def add_uniform_noise(self, size):
        """Generate uniform noise with defined parameters."""
        return np.random.uniform(self.a_noise_val, self.b_noise_val, size)

    def plot_simulation_in_system_box(self, x, y, noisy_y):
        """Displays the system simulation graph in SystemSimulation_box."""
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(x, y, label="Original Signal", color="blue")
        ax.plot(x, noisy_y, label="Noisy Signal", color="orange")
        ax.set_title("System Simulation")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()

        canvas = FigureCanvas(figure)
        layout = self.SystemSimulation_box.layout()
        layout.addWidget(canvas)
        canvas.draw()

    def plot_noise_in_noise_box(self, noise):
        """Displays the noise graph in NoiseSimulation_box."""
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(noise, label="Noise", color="green")
        ax.set_title("Noise Simulation")
        ax.set_xlabel("X")
        ax.set_ylabel("Noise Value")
        ax.legend()

        canvas = FigureCanvas(figure)
        layout = self.NoiseSimulation_box.layout()
        layout.addWidget(canvas)
        canvas.draw()

        # Noise distribution histogram
        figure_hist = plt.Figure(figsize=(5, 4), dpi=100)
        ax_hist = figure_hist.add_subplot(111)
        ax_hist.hist(noise, bins=20, color="red", alpha=0.7)
        ax_hist.set_title("Noise Distribution")
        ax_hist.set_xlabel("Noise Value")
        ax_hist.set_ylabel("Frequency")

        canvas_hist = FigureCanvas(figure_hist)
        layout.addWidget(canvas_hist)
        canvas_hist.draw()

    def run_simulation(self, system_type):
        """Set the current system type for simulation."""
        self.current_system = system_type
        print(f"Selected system: {system_type}")
    
    def run_current_simulation(self):
        """Runs the simulation with the selected system and noise."""
        x = np.linspace(self.X_min, self.X_max, self.N)

        # Generate noise
        if self.noise_type == "gaussian":
            noise = self.add_gaussian_noise(len(x))
        elif self.noise_type == "uniform":
            noise = self.add_uniform_noise(len(x))

        # Simulation based on the selected type
        if self.current_system == "linear":
            y = self.a_val * x + self.b_val
        elif self.current_system == "exponential":
            y = self.lambda_exp_val * np.exp(self.mu_exp_val * x)
        elif self.current_system == "logarithmic":
            y = self.a_log_val * np.log(x + self.b_log_val)
        else:
            print("No system type selected!")
            return

        noisy_y = y + noise
        self.plot_simulation_in_system_box(x, y, noisy_y)
        self.plot_noise_in_noise_box(noise)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SimulationApp()
    window.show()
    sys.exit(app.exec_())