import tkinter as tk

class StretchableSlider(tk.Canvas):
    def __init__(self, parent, min_val=0, max_val=100, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.min_val = min_val
        self.max_val = max_val
        self.rect_width = 50  # Initial width of the rectangle
        self.rect_height = 20
        self.rect_id = None
        self.start_x = None
        self.slider_value = tk.DoubleVar(value=min_val)
        self.resizing = False

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

        self.draw_slider()

    def draw_slider(self):
        # Draw a line to represent the track of the slider
        self.create_line(10, self.rect_height // 2, self.winfo_reqwidth() - 10, self.rect_height // 2, fill="gray", width=2)
        # Draw the initial rectangle (cursor)
        self.rect_id = self.create_rectangle(10, 0, 10 + self.rect_width, self.rect_height, fill="blue", outline="black")

    def on_click(self, event):
        self.start_x = event.x
        self.rect_coords = self.coords(self.rect_id)
        if self.rect_coords[0] <= event.x <= self.rect_coords[0] + 5 :
            self.resizing = -1
            print("Resize-L")
        elif self.rect_coords[2] - 5 <= event.x <= self.rect_coords[2]:
            self.resizing = 1
            print("Resize-R")
        else:
            self.resizing = False
            print("Resize-OFF")

    def on_drag(self, event):
        if self.resizing:
            self.resize_rect(event)
            
        else:
            self.move_rect(event)
            print("Move")

    def move_rect(self, event):
        dx = event.x - self.start_x
        new_x1 = self.rect_coords[0] + dx
        new_x2 = self.rect_coords[2] + dx

        if 10 <= new_x1 and new_x2 <= self.winfo_reqwidth() - 10:
            self.move(self.rect_id, dx, 0)
            self.start_x = event.x
            self.rect_coords = self.coords(self.rect_id)
            self.update_slider_value()

    def resize_rect(self, event):
        if self.rect_coords[0] <= self.start_x: # <= self.rect_coords[0] + 1025:
            new_x1 = event.x
            print(f"Resize:{new_x1}")
            if new_x1 < 10:
                new_x1 = 10
            if new_x1 >= self.rect_coords[2] - 10:
                new_x1 = self.rect_coords[2] - 10
            self.coords(self.rect_id, new_x1, self.rect_coords[1], self.rect_coords[2], self.rect_coords[3])
        elif self.start_x <= self.rect_coords[2]:  #self.rect_coords[2] - 5 <= 
            new_x2 = event.x
            if new_x2 > self.winfo_reqwidth() - 10:
                new_x2 = self.winfo_reqwidth() - 10
            if new_x2 <= self.rect_coords[0] + 10:
                new_x2 = self.rect_coords[0] + 10
            self.coords(self.rect_id, self.rect_coords[0], self.rect_coords[1], new_x2, self.rect_coords[3])
        self.rect_coords = self.coords(self.rect_id)
        self.update_slider_value()

    def on_release(self, event):
        self.resizing = False

    def update_slider_value(self):
        track_length = self.winfo_reqwidth() - 20
        rect_midpoint = (self.rect_coords[0] + self.rect_coords[2]) / 2
        normalized_value = (rect_midpoint - 10) / track_length
        self.slider_value.set(self.min_val + normalized_value * (self.max_val - self.min_val))
        #print(f"Slider value: {self.slider_value.get():.2f}")

# Crear la ventana principal
root = tk.Tk()
root.title("Slider con cursor estirable")
root.geometry("400x100")

# Crear e insertar el slider
slider = StretchableSlider(root, min_val=0, max_val=100, width=400, height=50)
slider.pack(pady=20)

root.mainloop()
