from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from genetic import GA01Knapsack
from genetic import GAUnboundedKnapsack
from differential import DE01Knapsack
from differential import DEUnboundedKnapsack
import tkinter as tk


class Window:
    @staticmethod
    def show():
        win = tk.Tk()  # creating window
        win.title("Knapsack problem")  # window title
        win.minsize(600, 440)
        margin0 = tk.Label(win, text="    ").grid(column=0, row=0)  # just margin
        w_lbl = tk.Label(win, text="Enter the weights: ").grid(column=2, row=1, pady=15)
        v_lbl = tk.Label(win, text="Enter the values: ").grid(column=2, row=2, pady=15)
        capacity_lbl = tk.Label(win, text="knapsack capacity: ").grid(column=2, row=3, pady=15)

        # can put the random intialization here
        weights = tk.StringVar(value='23, 2, 4, 18, 5, 18, 5, 8, 6, 12, 11, 1, 7, 7, 15, 22, 23, 14, 1, 16')
        # weights = '23, 2, 4, 18, 5, 18, 5, 8, 6, 12, 11, 1, 7, 7, 15, 22, 23, 14, 1, 16'
        values = tk.StringVar(value='9, 10, 8, 10, 1, 8, 4, 6, 7, 7, 7, 7, 7, 5, 10, 10, 2, 6, 5, 5')
        # values = '9, 10, 8, 10, 1, 8, 4, 6, 7, 7, 7, 7, 7, 5, 10, 10, 2, 6, 5, 5'
        capacity = tk.StringVar(value='50')
        # capacity = '100'

        weightsEntered = tk.Entry(win, width=60, textvariable=weights).grid(column=3, row=1)
        valuesEntered = tk.Entry(win, width=60, textvariable=values).grid(column=3, row=2)
        capacityEntered = tk.Entry(win, width=60, textvariable=capacity).grid(column=3, row=3)

        # Dropdown menu options
        options = [
            "0-1 knapsack using Genetic Algorithm",
            "Unbounded knapsack using Genetic Algorithm",
            "0-1 knapsack using Differential Evolution",
            "Unbounded knapsack using Differential Evolution",
        ]

        clicked = tk.StringVar()  # datatype of menu text
        clicked.set("0-1 knapsack using Genetic Algorithm")  # initial menu text

        # Create Dropdown menu
        drop = tk.OptionMenu(win, clicked, *options).grid(column=3, row=5, pady=15)

        def click():
            # Create empty Labels
            sol_lbl = tk.Label(win, text="\t\t\t\t\t\t\t").grid(column=3, row=7)
            val_lbl = tk.Label(win, text="\t\t\t\t\t\t\t").grid(column=3, row=8)
            sol_w_lbl = tk.Label(win, text="\t\t\t\t\t\t\t").grid(column=3, row=9)

            try:
                # can put the random values here
                WEIGHTS = [int(w.strip()) for w in str(weights.get()).split(",")]
                VALUES = [int(v.strip()) for v in str(values.get()).split(",")]
            except:
                # Create error Label
                sol_lbl = tk.Label(win, text="Invalid input").grid(column=3, row=7)
            else:
                if (len(WEIGHTS) != len(VALUES)) or (not capacity.get().isnumeric()):
                    # Create error Label
                    sol_lbl = tk.Label(win, text="Invalid input").grid(column=3, row=7)

                else:
                    choice = clicked.get()
                    sol = ()
                    if choice == "0-1 knapsack using Genetic Algorithm":
                        genetic_01 = GA01Knapsack(WEIGHTS, VALUES, len(WEIGHTS), int(capacity.get()))
                        sol, avg = genetic_01.execute()
                    elif choice == "Unbounded knapsack using Genetic Algorithm":
                        genetic_unbounded = GAUnboundedKnapsack(WEIGHTS, VALUES, len(WEIGHTS), int(capacity.get()))
                        sol, avg = genetic_unbounded.execute()
                    elif choice == "0-1 knapsack using Differential Evolution":
                        diff_01 = DE01Knapsack(WEIGHTS, VALUES, len(WEIGHTS), int(capacity.get()))
                        sol, avg = diff_01.execute()
                    elif choice == "Unbounded knapsack using Differential Evolution":
                        diff_unbounded = DEUnboundedKnapsack(WEIGHTS, VALUES, len(WEIGHTS), int(capacity.get()))
                        sol, avg = diff_unbounded.execute()


                    # Create Solution Label
                    sol_lbl = tk.Label(win, text="Solution: " + str(sol[2])).grid(column=3, row=7, pady=15)

                    # Create Value for Solution Label
                    val_lbl = tk.Label(win, text="Solution value: " + str(sol[0])).grid(column=3, row=8, pady=5)

                    # Create Value for Solution Label
                    sol_w_lbl = tk.Label(win, text="Solution weight: " + str(sol[1])).grid(column=3, row=9)

                    figure3 = plt.Figure(figsize=(4, 4), dpi=80)
                    ax3 = figure3.add_subplot(111)
                    ax3.plot(range(len(avg)), avg)
                    scatter3 = FigureCanvasTkAgg(figure3, win)
                    scatter3.get_tk_widget().grid(column=4, row=4)

                    ax3.legend(['Average Fitness'])
                    ax3.set_xlabel('Generations')
                    ax3.set_title('Convergence Graph')



        button = tk.Button(win, text="submit", command=click).grid(column=3, row=6, pady=5)
        warning_lbl = tk.Label(win,
                               text="Please enter the Values and Weights separated by comma ','. (e.g. Values: 1,2,3,4)",
                               fg="red").grid(column=3, row=4)

        win.mainloop()  # showing the window


