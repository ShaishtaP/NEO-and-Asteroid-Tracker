import requests
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random

API_KEY = "YOUR NASA API KEY"


def fetch_neo_data(start_date, end_date):
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def parse_neo_data(data):
    neo_list = []
    for date, neos in data["near_earth_objects"].items():
        for neo in neos:
            neo_info = {
                "name": neo["name"],
                "is_potentially_hazardous": neo["is_potentially_hazardous_asteroid"],
                "estimated_diameter": neo["estimated_diameter"]["meters"]["estimated_diameter_max"],
                "close_approach_date": neo["close_approach_data"][0]["close_approach_date_full"],
                "miss_distance_km": float(neo["close_approach_data"][0]["miss_distance"]["kilometers"]),
                "relative_velocity_kmh": float(neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
            }
            neo_list.append(neo_info)
    return neo_list


class NEOTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NEO Earth Tracker")
        self.root.geometry("900x700")

        self.custom_font = ("Arial", 20, "bold")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Create Tabs
        self.tab_start_date = ttk.Frame(self.notebook)
        self.tab_end_date = ttk.Frame(self.notebook)
        self.tab_names = ttk.Frame(self.notebook)
        self.tab_hazardous = ttk.Frame(self.notebook)
        self.tab_diameter = ttk.Frame(self.notebook)
        self.tab_velocity = ttk.Frame(self.notebook)
        self.tab_close_distance = ttk.Frame(self.notebook)
        self.tab_miss_distance = ttk.Frame(self.notebook)

        # Add Tabs to Notebook
        self.notebook.add(self.tab_start_date, text="Start Date")
        self.notebook.add(self.tab_end_date, text="End Date")
        self.notebook.add(self.tab_names, text="Asteroid Names")
        self.notebook.add(self.tab_hazardous, text="Hazardous Level")
        self.notebook.add(self.tab_diameter, text="Diameter")
        self.notebook.add(self.tab_velocity, text="Velocity")
        self.notebook.add(self.tab_close_distance, text="Close Approach")
        self.notebook.add(self.tab_miss_distance, text="Miss Distance")

        # Add Background Images
        self.create_background_image(self.tab_start_date, "space_img.jpg")
        self.create_background_image(self.tab_end_date, "space_img.jpg")
        self.create_background_image(self.tab_names, "Asteroid.jpg")
        self.create_background_image(
            self.tab_hazardous, "haz.jpg")
        self.create_background_image(self.tab_diameter, "space.jpg")
        self.create_background_image(self.tab_velocity, "sp.jpg")
        self.create_background_image(
            self.tab_close_distance, "Near-Miss-Day.jpg")
        self.create_background_image(
            self.tab_miss_distance, "Near-Miss-Day.jpg")

        # Add Animated Asteroids
        self.animate_asteroids()

        # Add Widgets to Each Tab
        self.create_tab_start_date()
        self.create_tab_end_date()
        self.create_tab_names()
        self.create_tab_hazardous()  # Ensure this line is present
        self.create_tab_diameter()
        self.create_tab_velocity()
        self.create_tab_close_distance()
        self.create_tab_miss_distance()

        self.neo_data = []
        self.root.bind("<Return>", self.navigate_tabs)

    def create_background_image(self, tab, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((1600, 1200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(tab, image=photo)
            label.image = photo
            # Use pack() instead of place()
            label.pack(fill="both", expand=True)
        except FileNotFoundError:
            tk.Label(tab, text="Background Image Not Found",
                     bg="black", fg="white").pack(fill="both", expand=True)

    def animate_asteroids(self):
        asteroid_image_paths = ["asteroid1.png",
                                "asteroid2.png", "asteroid3.png"]
        self.asteroid_labels = []
        for path in asteroid_image_paths:
            try:
                image = Image.open(path)
                image = image.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                # Place on the Start Date tab
                label = tk.Label(self.tab_start_date, image=photo, bg="black")
                label.image = photo
                label.place(x=random.randint(50, 800),
                            y=random.randint(50, 600))
                self.asteroid_labels.append(label)
            except FileNotFoundError:
                print(f"Asteroid image not found: {path}")

        self.move_asteroids()

    def move_asteroids(self):
        for label in self.asteroid_labels:
            x, y = label.winfo_x(), label.winfo_y()
            dx, dy = random.randint(-5, 5), random.randint(-5, 5)
            label.place(x=x + dx, y=y + dy)
        self.root.after(50, self.move_asteroids)

    def create_tab_start_date(self):
        frame = tk.Frame(self.tab_start_date, bg="#000000", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.lift()
        tk.Label(frame, text="Enter Start Date (YYYY-MM-DD):", font=self.custom_font,
                 bg="#000000", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.start_date_entry = tk.Entry(
            frame, font=self.custom_font, width=15)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=5)

    def create_tab_end_date(self):
        frame = tk.Frame(self.tab_end_date, bg="#000000", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.lift()
        tk.Label(frame, text="Enter End Date (YYYY-MM-DD):", font=self.custom_font,
                 bg="#000000", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.end_date_entry = tk.Entry(frame, font=self.custom_font, width=15)
        self.end_date_entry.grid(row=0, column=1, padx=10, pady=5)
        button = tk.Button(frame, text="Fetch NEO Data", font=self.custom_font,
                           bg="#C0C0C0", command=self.fetch_and_display)
        button.grid(row=1, column=0, columnspan=2, pady=10)
        button.bind("<Enter>", lambda event: button.config(bg="#FFA500"))
        button.bind("<Leave>", lambda event: button.config(bg="#FFD700"))

    def create_tab_names(self):
        frame = tk.Frame(self.tab_names, bg="#000000", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.lift()
        self.tree_names = ttk.Treeview(
            frame, columns=("Name"), show="headings", height=10)
        self.tree_names.heading("Name", text="Asteroid Name")
        self.tree_names.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.tree_names.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_names.configure(yscrollcommand=scrollbar.set)

    def create_tab_hazardous(self):
        frame = tk.Frame(self.tab_hazardous, bg="#000000", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.lift()
        self.tree_hazardous = ttk.Treeview(frame, columns=(
            "Name", "Hazardous"), show="headings", height=10)
        self.tree_hazardous.heading("Name", text="Asteroid Name")
        self.tree_hazardous.heading("Hazardous", text="Hazardous")
        self.tree_hazardous.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.tree_hazardous.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_hazardous.configure(yscrollcommand=scrollbar.set)

    def create_tab_diameter(self):
        frame = tk.Frame(self.tab_diameter, bg="#000000", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.lift()
        self.tree_diameter = ttk.Treeview(frame, columns=(
            "Name", "Diameter (m)"), show="headings", height=10)
        self.tree_diameter.heading("Name", text="Asteroid Name")
        self.tree_diameter.heading("Diameter (m)", text="Diameter (m)")
        self.tree_diameter.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.tree_diameter.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_diameter.configure(yscrollcommand=scrollbar.set)

    def create_tab_velocity(self):
        frame = tk.Frame(self.tab_velocity, bg="#000000", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.lift()
        self.tree_velocity = ttk.Treeview(frame, columns=(
            "Name", "Velocity (km/h)"), show="headings", height=10)
        self.tree_velocity.heading("Name", text="Asteroid Name")
        self.tree_velocity.heading("Velocity (km/h)", text="Velocity (km/h)")
        self.tree_velocity.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.tree_velocity.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_velocity.configure(yscrollcommand=scrollbar.set)

    def create_tab_close_distance(self):
        frame = tk.Frame(self.tab_close_distance, bg="#000000", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.lift()
        self.tree_close_distance = ttk.Treeview(frame, columns=(
            "Name", "Close Approach"), show="headings", height=10)
        self.tree_close_distance.heading("Name", text="Asteroid Name")
        self.tree_close_distance.heading(
            "Close Approach", text="Close Approach Date")
        self.tree_close_distance.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.tree_close_distance.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_close_distance.configure(yscrollcommand=scrollbar.set)

    def create_tab_miss_distance(self):
        frame = tk.Frame(self.tab_miss_distance, bg="#000000", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.lift()
        self.tree_miss_distance = ttk.Treeview(frame, columns=(
            "Name", "Miss Distance (km)"), show="headings", height=10)
        self.tree_miss_distance.heading("Name", text="Asteroid Name")
        self.tree_miss_distance.heading(
            "Miss Distance (km)", text="Miss Distance (km)")
        self.tree_miss_distance.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.tree_miss_distance.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_miss_distance.configure(yscrollcommand=scrollbar.set)

    def navigate_tabs(self, event=None):
        current_tab_index = self.notebook.index(self.notebook.select())
        next_tab_index = (current_tab_index + 1) % self.notebook.index("end")
        self.notebook.select(next_tab_index)

    def fetch_and_display(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date", "Please enter valid dates in YYYY-MM-DD format.")
            return

        data = fetch_neo_data(start_date, end_date)
        if data:
            self.neo_data = parse_neo_data(data)
            self.display_data_in_tabs()

    def display_data_in_tabs(self):
        for tree in [self.tree_names, self.tree_hazardous, self.tree_diameter, self.tree_velocity, self.tree_close_distance, self.tree_miss_distance]:
            for row in tree.get_children():
                tree.delete(row)

        for neo in self.neo_data:
            self.tree_names.insert("", "end", values=(neo["name"],))
            self.tree_hazardous.insert("", "end", values=(
                neo["name"], "Yes" if neo["is_potentially_hazardous"] else "No"))
            self.tree_diameter.insert("", "end", values=(
                neo["name"], f"{neo['estimated_diameter']:.2f}"))
            self.tree_velocity.insert("", "end", values=(
                neo["name"], f"{neo['relative_velocity_kmh']:.2f}"))
            self.tree_close_distance.insert("", "end", values=(
                neo["name"], neo["close_approach_date"]))
            self.tree_miss_distance.insert("", "end", values=(
                neo["name"], f"{neo['miss_distance_km']:.2f}"))


if __name__ == "__main__":
    root = tk.Tk()
    app = NEOTrackerApp(root)
    root.mainloop()
