import tkinter as tk
import threading
import brain


def get_geometry(width, height):
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    return f"{width}x{height}+{x}+{y}"


def is_numeric(char):
    return char.isdigit()


def get_number_from_brain():
    selected_number = None
    thinking_numbers = []
    for i in range(10):
        thinking_numbers.append(brain.thinking_number())
    selected_number = brain.select_number(thinking_numbers)
    return selected_number


def on_brain_think():
    global brain_selected_number
    brain_selected_number = get_number_from_brain()
    if brain_selected_number != None:
        app.after(0, lambda: on_user_guess(brain_selected_number))
    else:
        failed_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        app.after(2000, lambda: on_reset())


def on_user_guess(brain_selected_number):
    think_lbl.place_forget()
    guess_lbl.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    number_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    submit_btn.place(relx=0.5, rely=0.7, anchor=tk.CENTER)


def on_check_result(brain_selected_number):
    guess_lbl.place_forget()
    number_entry.place_forget()
    submit_btn.place_forget()
    user_guess = number_entry.get()
    if user_guess == "" or int(user_guess) != brain_selected_number:
        incorrect_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    elif int(user_guess) == brain_selected_number:
        correct_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    app.after(2000, lambda: on_reset())


def on_reset():
    incorrect_lbl.place_forget()
    failed_lbl.place_forget()
    correct_lbl.place_forget()
    guess_lbl.place_forget()
    number_entry.delete(0, "end")
    number_entry.place_forget()
    submit_btn.place_forget()
    think_lbl.place_forget()
    start_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def on_start():
    start_btn.place_forget()
    think_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    threading.Thread(target=on_brain_think).start()


brain_selected_number = None

app = tk.Tk()
app.title("Guess what number i'm thinking of")
app.geometry(get_geometry(380, 150))
app.resizable(False, False)
app.attributes("-topmost", True)
app.lift()

start_btn = tk.Button(text="Start", width=20, bg="yellow", command=on_start)
start_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

think_lbl = tk.Label(text="Wait I'm thinking...")
guess_lbl = tk.Label(text="Guess the number!")

validate_digit = (app.register(is_numeric), "%S")
number_entry = tk.Entry(width=20, validate="key", validatecommand=validate_digit)

submit_btn = tk.Button(
    text="Submit",
    width=20,
    bg="yellow",
    command=lambda: on_check_result(brain_selected_number),
)

failed_lbl = tk.Label(text="What!, my brain is failed of thinking number.")
correct_lbl = tk.Label(text="Correct!, you so good.")
incorrect_lbl = tk.Label(text="Incorrect!, try again...")

app.mainloop()
