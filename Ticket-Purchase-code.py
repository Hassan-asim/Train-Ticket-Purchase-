import tkinter as tk
from tkinter import messagebox

class ElectricMountainRailwayGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Electric Mountain Railway System")
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))

        self.railway = ElectricMountainRailway()
        self.create_widgets()

    def create_widgets(self):
        self.display_label_departure = tk.Label(self.master, text="Current Ticket Availability (Departure):")
        self.display_label_departure.grid(row=0, column=0, columnspan=2, pady=10)

        self.display_text_departure = tk.Text(self.master, height=10, width=40)
        self.display_text_departure.grid(row=1, column=0, columnspan=2, pady=10)

        self.display_label_return = tk.Label(self.master, text="Current Ticket Availability (Return):")
        self.display_label_return.grid(row=0, column=2, columnspan=2, pady=10)

        self.display_text_return = tk.Text(self.master, height=10, width=40)
        self.display_text_return.grid(row=1, column=2, columnspan=2, pady=10)

        self.update_display()

        self.purchase_label = tk.Label(self.master, text="Purchase Tickets:")
        self.purchase_label.grid(row=2, column=0, columnspan=4, pady=10)

        self.departure_label = tk.Label(self.master, text="Departure Time:")
        self.departure_label.grid(row=3, column=0, pady=5)

        self.departure_var = tk.StringVar(self.master)
        self.departure_var.set(self.railway.train_schedule[0]["departure"])
        self.departure_menu = tk.OptionMenu(self.master, self.departure_var, *self.railway.get_departure_times())
        self.departure_menu.grid(row=3, column=1, pady=5)

        self.return_label = tk.Label(self.master, text="Return Time:")
        self.return_label.grid(row=4, column=0, pady=5)

        self.return_var = tk.StringVar(self.master)
        self.return_var.set(self.railway.train_schedule[0]["return"])
        self.return_menu = tk.OptionMenu(self.master, self.return_var, *self.railway.get_return_times())
        self.return_menu.grid(row=4, column=1, pady=5)

        self.passengers_label = tk.Label(self.master, text="Number of Passengers:")
        self.passengers_label.grid(row=5, column=0, pady=5)

        self.passengers_entry = tk.Entry(self.master)
        self.passengers_entry.grid(row=5, column=1, pady=5)

        self.purchase_button = tk.Button(self.master, text="Purchase Tickets", command=self.purchase_tickets)
        self.purchase_button.grid(row=6, column=0, columnspan=4, pady=10)

        self.end_of_day_button = tk.Button(self.master, text="End of Day Report", command=self.end_of_day_report)
        self.end_of_day_button.grid(row=7, column=0, columnspan=4, pady=10)

    def update_display(self):
        display_text_departure = ""
        for time, tickets in self.railway.available_tickets_departure.items():
            if tickets == 0:
                display_text_departure += f"{time} - Closed\n"
            else:
                display_text_departure += f"{time} - Tickets available: {tickets}\n"

        self.display_text_departure.delete(1.0, tk.END)
        self.display_text_departure.insert(tk.END, display_text_departure)

        display_text_return = ""
        for time, tickets in self.railway.available_tickets_return.items():
            if tickets == 0:
                display_text_return += f"{time} - Closed\n"
            else:
                display_text_return += f"{time} - Tickets available: {tickets}\n"

        self.display_text_return.delete(1.0, tk.END)
        self.display_text_return.insert(tk.END, display_text_return)

    def purchase_tickets(self):
        departure_time = self.departure_var.get()
        return_time = self.return_var.get()
        num_passengers = self.passengers_entry.get().strip()

        if not num_passengers:
            messagebox.showerror("Error", "Number of passengers must be filled.")
            return

        try:
            num_passengers = int(num_passengers)
        except ValueError:
            messagebox.showerror("Error", "Number of passengers must be an integer.")
            return

        if not self.railway.is_valid_time_combination(departure_time, return_time):
            messagebox.showerror("Error", "Invalid time combination. Return time must be greater than or equal to departure time.")
            return

        result = self.railway.purchase_tickets(departure_time, return_time, num_passengers)
        if result:
            messagebox.showinfo("Success", result)
            self.update_display()

    def end_of_day_report(self):
        report_text = self.railway.generate_end_of_day_report()
        messagebox.showinfo("End of Day Report", report_text)

class ElectricMountainRailway:
    def __init__(self):
        self.coaches_per_train = 6
        self.seats_per_coach = 80
        self.ticket_price_up = 25
        self.ticket_price_down = 25

        self.train_schedule = [
            {"departure": "09:00", "return": "10:00", "coaches": 6},
            {"departure": "11:00", "return": "12:00", "coaches": 6},
            {"departure": "13:00", "return": "14:00", "coaches": 6},
            {"departure": "15:00", "return": "16:00", "coaches": 8},
        ]

        self.available_tickets_departure = {
            "09:00": self.coaches_per_train * self.seats_per_coach,
            "11:00": self.coaches_per_train * self.seats_per_coach,
            "13:00": self.coaches_per_train * self.seats_per_coach,
            "15:00": (self.coaches_per_train + 2) * self.seats_per_coach,
        }

        self.available_tickets_return = {
            "10:00": self.coaches_per_train * self.seats_per_coach,
            "12:00": self.coaches_per_train * self.seats_per_coach,
            "14:00": self.coaches_per_train * self.seats_per_coach,
            "16:00": (self.coaches_per_train + 2) * self.seats_per_coach,
        }

        self.total_passengers = {time: 0 for time in ["09:00", "11:00", "13:00", "15:00", "10:00", "12:00", "14:00", "16:00"]}
        self.total_money_collected = {time: 0 for time in ["09:00", "11:00", "13:00", "15:00", "10:00", "12:00", "14:00", "16:00"]}
        self.total_free_tickets = {time: 0 for time in ["09:00", "11:00", "13:00", "15:00", "10:00", "12:00", "14:00", "16:00"]}

    def get_departure_times(self):
        return [schedule["departure"] for schedule in self.train_schedule]

    def get_return_times(self):
        return [schedule["return"] for schedule in self.train_schedule]

    def is_valid_time_combination(self, departure_time, return_time):
        departure_index = self.get_departure_times().index(departure_time)
        return_index = self.get_return_times().index(return_time)
        return return_index >= departure_index

    def purchase_tickets(self, departure_time, return_time, num_passengers):
        if departure_time not in self.get_departure_times() or return_time not in self.get_return_times():
            return "Error: Invalid departure or return time."

        if not self.is_valid_time_combination(departure_time, return_time):
            messagebox.showerror("Error", "Invalid time combination. Return time must be greater than or equal to departure time.")
            return

        if self.available_tickets_departure[departure_time] < num_passengers:
            return "Error: Not enough tickets available for the departure train."

        if self.available_tickets_return[return_time] < num_passengers:
            return "Error: Not enough tickets available for the return train."

        total_cost = num_passengers * (self.ticket_price_up + self.ticket_price_down)

        if num_passengers >= 10:
            free_tickets = num_passengers // 10
            total_cost -= free_tickets * (self.ticket_price_up + self.ticket_price_down)
            self.total_free_tickets[departure_time] += free_tickets

        self.available_tickets_departure[departure_time] -= num_passengers
        self.available_tickets_return[return_time] -= num_passengers
        self.total_passengers[departure_time] += num_passengers
        self.total_passengers[return_time] += num_passengers
        self.total_money_collected[departure_time] += total_cost

        return f"Tickets purchased successfully for {departure_time} - {return_time}. Total cost: ${total_cost}" \
               f"\nGroup Discount: {free_tickets} free tickets awarded."

    def generate_end_of_day_report(self):
        report_text = "End of Day Report:\n\n"
        for time in ["09:00", "11:00", "13:00", "15:00", "10:00", "12:00", "14:00", "16:00"]:
            report_text += f"{time} - Passengers: {self.total_passengers[time]}, " \
                           f"Money Collected: ${self.total_money_collected[time]}, " \
                           f"Free Tickets Awarded: {self.total_free_tickets[time]}\n"

        total_passengers = sum(self.total_passengers.values())
        total_money_collected = sum(self.total_money_collected.values())
        total_free_tickets_awarded = sum(self.total_free_tickets.values())

        report_text += f"\nTotal Passengers for the Day: {total_passengers}\n"
        report_text += f"Total Money Collected for the Day: ${total_money_collected}\n"
        report_text += f"Total Free Tickets Awarded for the Day: {total_free_tickets_awarded}\n"

        max_passengers_time = max(self.total_passengers, key=self.total_passengers.get)
        report_text += f"Train with the most passengers today: {max_passengers_time} " \
                       f"({self.total_passengers[max_passengers_time]} passengers)"

        return report_text

def main():
    root = tk.Tk()
    app = ElectricMountainRailwayGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
