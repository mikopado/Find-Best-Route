import csv
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox

from source_file.aircrafts_dictionary import AircraftDictionaryParent
from source_file.routes_algorithms import Routes
from source_file.airport_atlas import AirportAtlas
from source_file.custom_exceptions import *
from source_file.currency_rates import CurrencyRatesDictionaryParent
from source_file.country_currencies import CountryCurrenciesDictionaryParent



class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title('Fuel Management Software - Find cheapest route')
        self.master.geometry("%dx%d" %(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg_color = '#DCDCDC'
        self.master.config(bg=self.bg_color)
        self.config(bg=self.bg_color)
        self.grid()
        self.my_font = 'helvetica 12 bold'

        self.select_aircraft()
        self.select_airport_country()
        self.select_airport_code()
        self.create_aircraft_text_box()
        self.create_airports_text_boxes()
        self.create_buttons()
        self.visualize_best_route()

    #-----------------------------------TOP SECTION-----------------------------------------------------------
    # Top section of the window (Comboboxes and labels for selecting airports and aircraft)

    def select_aircraft(self):
        """Combobox for selecting aircraft model and its associated label"""
        self.aircrafts_dictionary = AircraftDictionaryParent('./csv_files/aircraft.csv')
        Label(self, text="Choose Aircraft", bg=self.bg_color).grid(row=0, pady=20)

        # get list of all aircraft models from aircraft.csv file
        self.list_aircrafts = self.aircrafts_dictionary.get_list_aircrafts_model()
        self.list_aircrafts.sort()

        self.aircraft_var = StringVar(self)
        self.aircraft_var.set(self.list_aircrafts[0])
        self.aircraft_cmbox = Combobox(self, textvariable=self.aircraft_var, state='readonly',
                                       values=[*self.list_aircrafts], width=10)
        self.aircraft_cmbox.grid(row=2, padx=20)

        # bind the selected aircraft model to aircraft_model text box
        self.aircraft_cmbox.bind('<<ComboboxSelected>>', self.get_aircraft_model)

    def select_airport_country(self):
        """Combobox for selecting countries and its associated label"""
        self.airport_atlas = AirportAtlas('./csv_files/airport.csv')
        Label(self, text="Choose Airport's Country", bg=self.bg_color).grid(row=0, column=1, pady=20, sticky='n')

        self.list_countries = self.airport_atlas.get_list_countries() #get list of all countries from airport.csv file
        self.list_countries.append('All Airports')
        self.list_countries.sort()

        self.country_var = StringVar(self)
        self.country_var.set(self.list_countries[0])
        self.country_cmbox = Combobox(self, textvariable=self.country_var,
                                      values=[*self.list_countries], state='readonly', width=30)
        self.country_cmbox.grid(row=2, column=1, padx=20)

        # bind the selected countries to Choose airport combobox, updating the list of airports every time the selected country changes
        self.country_cmbox.bind('<<ComboboxSelected>>', self.update_airports_based_on_country)

    def select_airport_code(self):
        """Combobox for selecting airport from airport code."""
        Label(self, text="Choose Airport", bg=self.bg_color).grid(row=0, column=2, pady=20)
        self.list_choosen_airports = self.airport_atlas.get_list_of_airports_from_country(self.country_cmbox.get())
        self.list_choosen_airports.sort()

        self.airport_var = StringVar(self)
        self.airport_var.set(self.list_choosen_airports[0])
        self.airport_cmbox = Combobox(self, state='readonly', values=[*self.list_choosen_airports],
                                      textvariable=self.airport_var, width=10)
        self.airport_cmbox.grid(row=2, column=2, padx=20)

        #bind the choosen airport code to list of selected airports for finding the route
        self.airport_cmbox.bind('<<ComboboxSelected>>', self.get_airports_from_selection)


    #Text Boxes for Aircraft Model, Departure Airport and Selected Airports
    def create_aircraft_text_box(self):

        Label(self, text="Aircraft Model", bg=self.bg_color).grid(row=0, column=3, pady=20)
        self.aircraft_model = StringVar()
        self.aircraft_text_box = Label(self, textvariable=self.aircraft_model, font=self.my_font, height= 1, width=7,
                                       relief=SUNKEN, bg='white')
        self.aircraft_text_box.grid(row=2, column=3,padx=40)

    def create_airports_text_boxes(self):

        Label(self, text="Departure Airport", bg=self.bg_color).grid(row=0, column=5, pady=20)

        Label(self, text="Selected Airports", bg=self.bg_color).grid(row=0, column=6, columnspan=4, pady=20)

        self.airport_1 = StringVar()
        Label(self, textvariable=self.airport_1, font=self.my_font, height=1, width=7,
                                        relief=SUNKEN, bg='white').grid(row=2, column=5, padx=40)

        self.airport_2 = StringVar()
        Label(self, textvariable=self.airport_2, font=self.my_font, height=1, width=7,
                                        relief=SUNKEN, bg='white').grid(row=2, column=6, padx=20)

        self.airport_3 = StringVar()
        Label(self, textvariable=self.airport_3, font=self.my_font, height=1, width=7,
                                        relief=SUNKEN, bg='white').grid(row=2, column=7, padx=20)

        self.airport_4 = StringVar()
        Label(self, textvariable=self.airport_4, font=self.my_font, height=1, width=7,
                                        relief=SUNKEN, bg='white').grid(row=2, column=8, padx=20)

        self.airport_5 = StringVar()
        Label(self, textvariable=self.airport_5, font=self.my_font, height=1, width=7,
                                        relief=SUNKEN, bg='white').grid(row=2, column=9, padx=20)


    def create_buttons(self):
        self.find_best_route_btn = Button(self, text='Find Best Route', font=self.my_font, bg='#FFD700',state='disabled',
                                          command=self.display_best_route)
        self.find_best_route_btn.grid(row=3, column=6, pady=40)
        self.find_best_route_btn.bind('<Return>', self.display_best_route)

        self.reset_btn = Button(self, text='Reset Airports', font=self.my_font, bg='#87CEFA', command=self.reset_route)
        self.reset_btn.grid(row=3, column=7, columnspan=2)
        self.reset_btn.bind('<Return>', self.reset_route)

        self.save_btn = Button(self, text='Save Route', font=self.my_font, bg='#87CEFA',
                                command=self.save_csv_file)
        self.save_btn.grid(row=3, column=9)

    #--------------------------------------------BOTTOM SECTION---------------------------------------------------

    # Bottom section of window. Display results of previous selection
    def visualize_best_route(self):
        # Create a new Frame for better visualization(without it the bottom section would have been affected from the top one)
        self.bottom = Frame()
        self.bottom.grid(row=6, sticky='w', padx=20)
        self.bottom.config(bg=self.bg_color)
        self.width_label = 40
        Label(self.bottom, text='Departure', bg=self.bg_color).grid(row=0, column=1)
        Label(self.bottom, text='Arrival', bg=self.bg_color).grid(row=0, column=3)
        Label(self.bottom, text='Km', bg=self.bg_color).grid(row=0, column=4)
        Label(self.bottom, text='€', bg=self.bg_color).grid(row=0, column=5)
        Label(self.bottom, text='L', bg=self.bg_color).grid(row=0, column=6)

        #Create Label for trips number
        for i in range(1,7):
            self.trip_lbl = Label(self.bottom, text=i, bg=self.bg_color)
            self.trip_lbl.grid(row=i,column=0)

        self.list_text_boxes = []

        # Trip 1 - Departure, Arrival, km, cost, liter
        self.trip1_depar_var = StringVar()
        self.create_labels_for_trips(self.trip1_depar_var, 1, 1, width=self.width_label,anchor='w')
        self.create_arrow_label(1)
        self.trip1_arr_var = StringVar()
        self.create_labels_for_trips(self.trip1_arr_var, 1, 3, width=self.width_label, anchor='w')
        self.km_trip1_var = StringVar()
        self.create_labels_for_trips(self.km_trip1_var, 1, 4)
        self.cost_trip1_var = StringVar()
        self.create_labels_for_trips(self.cost_trip1_var, 1, 5)
        self.fuel_trip1_var = StringVar()
        self.create_labels_for_trips(self.fuel_trip1_var, 1, 6)
        self.list_text_boxes.append((self.trip1_depar_var, self.trip1_arr_var, self.km_trip1_var,
                                     self.cost_trip1_var, self.fuel_trip1_var))
        # Trip 2 - Departure, Arrival, km, cost, liter
        self.trip2_depar_var = StringVar()
        self.create_labels_for_trips(self.trip2_depar_var, 2, 1, self.width_label,anchor='w')
        self.create_arrow_label(2)
        self.trip2_arr_var = StringVar()
        self.create_labels_for_trips(self.trip2_arr_var, 2, 3, self.width_label, anchor='w')
        self.km_trip2_var = StringVar()
        self.create_labels_for_trips(self.km_trip2_var, 2, 4)
        self.cost_trip2_var = StringVar()
        self.create_labels_for_trips(self.cost_trip2_var, 2, 5)
        self.fuel_trip2_var = StringVar()
        self.create_labels_for_trips(self.fuel_trip2_var, 2, 6)
        self.list_text_boxes.append((self.trip2_depar_var, self.trip2_arr_var, self.km_trip2_var,
                                     self.cost_trip2_var, self.fuel_trip2_var))

        # Trip 3 - Departure, Arrival, km, cost, liter
        self.trip3_depar_var = StringVar()
        self.create_labels_for_trips(self.trip3_depar_var, 3, 1, self.width_label, anchor='w')
        self.create_arrow_label(3)
        self.trip3_arr_var = StringVar()
        self.create_labels_for_trips(self.trip3_arr_var, 3, 3, self.width_label, anchor='w')
        self.km_trip3_var = StringVar()
        self.create_labels_for_trips(self.km_trip3_var, 3, 4)
        self.cost_trip3_var = StringVar()
        self.create_labels_for_trips(self.cost_trip3_var, 3, 5)
        self.fuel_trip3_var = StringVar()
        self.create_labels_for_trips(self.fuel_trip3_var, 3, 6)
        self.list_text_boxes.append((self.trip3_depar_var, self.trip3_arr_var, self.km_trip3_var,
                                     self.cost_trip3_var, self.fuel_trip3_var))

        # Trip 4 - Departure, Arrival, km, cost, liter
        self.trip4_depar_var = StringVar()
        self.create_labels_for_trips(self.trip4_depar_var, 4, 1, self.width_label, anchor='w')
        self.create_arrow_label(4)
        self.trip4_arr_var = StringVar()
        self.create_labels_for_trips(self.trip4_arr_var, 4, 3, self.width_label, anchor='w')
        self.km_trip4_var = StringVar()
        self.create_labels_for_trips(self.km_trip4_var, 4, 4)
        self.cost_trip4_var = StringVar()
        self.create_labels_for_trips(self.cost_trip4_var, 4, 5)
        self.fuel_trip4_var = StringVar()
        self.create_labels_for_trips(self.fuel_trip4_var, 4, 6)
        self.list_text_boxes.append((self.trip4_depar_var, self.trip4_arr_var, self.km_trip4_var,
                                     self.cost_trip4_var, self.fuel_trip4_var))

        # Trip 5 - Departure, Arrival, km, cost, liter
        self.trip5_depar_var = StringVar()
        self.create_labels_for_trips(self.trip5_depar_var, 5, 1, self.width_label, anchor='w')
        self.create_arrow_label(5)
        self.trip5_arr_var = StringVar()
        self.create_labels_for_trips(self.trip5_arr_var, 5, 3, self.width_label, anchor='w')
        self.km_trip5_var = StringVar()
        self.create_labels_for_trips(self.km_trip5_var, 5, 4)
        self.cost_trip5_var = StringVar()
        self.create_labels_for_trips(self.cost_trip5_var, 5, 5)
        self.fuel_trip5_var = StringVar()
        self.create_labels_for_trips(self.fuel_trip5_var, 5, 6)
        self.list_text_boxes.append((self.trip5_depar_var, self.trip5_arr_var, self.km_trip5_var,
                                     self.cost_trip5_var, self.fuel_trip5_var))

        # Trip 6 - Departure, Arrival, km, cost, liter
        self.trip6_depar_var = StringVar()
        self.create_labels_for_trips(self.trip6_depar_var, 6, 1, width=self.width_label, anchor='w')
        self.create_arrow_label(6)
        self.trip6_arr_var = StringVar()
        self.create_labels_for_trips(self.trip6_arr_var, 6, 3, width=self.width_label, anchor='w')
        self.km_trip6_var = StringVar()
        self.create_labels_for_trips(self.km_trip6_var, 6, 4)
        self.cost_trip6_var = StringVar()
        self.create_labels_for_trips(self.cost_trip6_var, 6, 5)
        self.fuel_trip6_var = StringVar()
        self.create_labels_for_trips(self.fuel_trip6_var, 6, 6)
        self.list_text_boxes.append((self.trip6_depar_var, self.trip6_arr_var, self.km_trip6_var,
                                     self.cost_trip6_var, self.fuel_trip6_var))

        # Text boxes for total amount of Km, cost, liter
        Label(self.bottom, text='-' * 80, bg=self.bg_color).grid(row=7, column=4, columnspan=3)
        self.total_km_var = StringVar()
        self.create_labels_for_trips(self.total_km_var, 8, 4)
        self.total_euro_var = StringVar()
        self.create_labels_for_trips(self.total_euro_var, 8, 5)
        self.total_liter = StringVar()
        self.create_labels_for_trips(self.total_liter, 8, 6)

        self.list_total = [self.total_km_var, self.total_euro_var, self.total_liter]

    # ---------------------------------------EVENT HANDLERS------------------------------------------------

    def update_airports_based_on_country(self, event):
        """Event which changes the list of airport codes in Choose Airport based on the selected country in
        Choose Airport's country combobox"""
        if self.country_cmbox.get() == 'All Airports':
            self.list_choosen_airports = [*self.airport_atlas.data_dict.keys()]
        else:
            self.list_choosen_airports = self.airport_atlas.get_list_of_airports_from_country(self.country_cmbox.get())
        self.list_choosen_airports.sort()
        self.airport_var.set(self.list_choosen_airports[0])
        self.airport_cmbox['values'] = [*self.list_choosen_airports]

    def get_aircraft_model(self, event):
        """Event that set the Aircraft model, selected in the Choose Aircraft combobox, into Aircraft model text box"""
        self.model = self.aircraft_cmbox.get()
        self.aircraft_model.set(self.model)

        # if user selects all five airports necessary for finding the route let eneable the Find Best Route Button
        if self.airport_5.get():
            self.find_best_route_btn.config(state='normal')

    def get_airports_from_selection(self, event):
        """Event that handles the selection of airport codes in choose airport combobox and adds the selected codes
        to Selected airports text boxes"""
        self.is_airport_in_list = False
        if not self.airport_1.get():
            self.airport_1.set(self.airport_cmbox.get())
        elif not self.airport_2.get() and not self.check_if_user_input_same_airport(self.airport_cmbox.get()):
            self.airport_2.set(self.airport_cmbox.get())
        elif not self.airport_3.get() and not self.check_if_user_input_same_airport(self.airport_cmbox.get()):
            self.airport_3.set(self.airport_cmbox.get())
        elif not self.airport_4.get() and not self.check_if_user_input_same_airport(self.airport_cmbox.get()):
            self.airport_4.set(self.airport_cmbox.get())
        elif not self.airport_5.get() and not self.check_if_user_input_same_airport(self.airport_cmbox.get()):
            self.airport_5.set(self.airport_cmbox.get())
            if self.aircraft_model.get():
                self.find_best_route_btn.config(state='normal')
        else:
            # Two conditions that prevent user selects same airport twice or prevent user keeps selecting
            # airports when list is already full
            if self.is_airport_in_list:
                messagebox.showinfo('Airports Code',
                                    'Cannot select an airport twice. Please select a new airport code!')
            else:
                messagebox.showinfo('Airports Code',
                                    'Airports already selected. Please find best route or reset selection!')

    def check_if_user_input_same_airport(self, value):
        list_choosen_airports = [self.airport_1.get(), self.airport_2.get(), self.airport_3.get(),
                                 self.airport_4.get(), self.airport_5.get()]
        if value in list_choosen_airports:
            self.is_airport_in_list = True
            return self.is_airport_in_list
        return self.is_airport_in_list

    def reset_route(self, event=None):
        self.airport_1.set('')
        self.airport_2.set('')
        self.airport_3.set('')
        self.airport_4.set('')
        self.airport_5.set('')
        self.find_best_route_btn.config(state='disabled')

    def display_best_route(self, event=None):
        """Main event handler that display the best route found after clicking the find best route button."""
        self.routes = Routes(self.aircrafts_dictionary, self.airport_atlas,
                             CurrencyRatesDictionaryParent('./csv_files/currencyrates.csv'),
                             CountryCurrenciesDictionaryParent('./csv_files/countrycurrency.csv'))
        self.list_choosen_airports = [self.airport_1.get(), self.airport_2.get(), self.airport_3.get(),
                                      self.airport_4.get(), self.airport_5.get()]

        try:
            self.best_route = self.routes.find_cheapest_route(self.aircraft_model.get(), self.list_choosen_airports[0],
                                                  self.list_choosen_airports[1:])

        except RouteNotFoundError as exc:
            messagebox.showinfo('Fuel Management Software', exc)
        except InvalidCodeError as ex:
            messagebox.showerror('Fuel Management Software', ex)

        else:
            for trip, route in self.best_route.items():
                for elem in range(len(route)):
                    if elem == 0 or elem == 1:
                        self.list_text_boxes[trip - 1][elem].set(route[elem])
                    else:
                        self.list_text_boxes[trip - 1][elem].set("{:0,.2f}".format(route[elem]))

            for i in range(len(self.list_total)):
                self.list_total[i].set("{:0,.2f}".format(self.routes.calculate_sum_km_or_fuel_in_best_route(self.best_route, i + 2)))


    # Two supporting methods to create labels(textboxes)
    def create_labels_for_trips(self, var, row, col, width=10, height=1, anchor='center'):
        """Methods to gather together all text boxes"""
        trip_lbl = Label(self.bottom, textvariable=var, height=height, width=width,
                         relief=SUNKEN, bg='white', font=self.my_font, anchor=anchor)
        trip_lbl.grid(row=row, column=col, pady=20, padx=15, sticky='w')

        return trip_lbl

    def create_arrow_label(self, row):
        from_to = Label(self.bottom, text='--->', bg=self.bg_color)
        from_to.grid(row=row, column=2)
        return from_to

    def save_csv_file(self):
        """Save the best route found on CSV file"""
        filename = filedialog.asksaveasfilename(confirmoverwrite=True,initialdir="/", title="Save Cheapest Route", filetypes= (("CSV file","*.csv"),("All files","*.*")),defaultextension='.csv')
        if filename:
            with open(filename, "w") as csvFile:
                fieldnames = ['Aircraft Model','Departure', 'Arrival', 'Distance(Km)', 'Cost(Euro)', 'Fuel(L)']
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                writer.writeheader()
                for elem in range(len(self.list_text_boxes)):
                    writer.writerow({fieldnames[0]: self.aircraft_var.get(),
                                     fieldnames[1]: self.list_text_boxes[elem][0].get(),
                                     fieldnames[2]: self.list_text_boxes[elem][1].get(),
                                     fieldnames[3]: self.list_text_boxes[elem][2].get(),
                                     fieldnames[4]: self.list_text_boxes[elem][3].get(),
                                     fieldnames[5]: self.list_text_boxes[elem][4].get()})
                writer.writerow({fieldnames[3]: self.list_total[0].get(),
                                 fieldnames[4]: self.list_total[1].get(),
                                 fieldnames[5]: self.list_total[2].get()})



def main():
    MyFrame().mainloop()

if __name__ == '__main__':
    try:
        main()
    except FileFormatError as ex:
        messagebox.showerror('Fuel Management Software', ex)
    except FileNotExistError as ex:
        messagebox.showerror('Fuel Management Software', ex)


