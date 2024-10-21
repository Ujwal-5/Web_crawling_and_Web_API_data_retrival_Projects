import tkinter as tk

def manual_captcha_popup():
    global captcha
    captcha = ''

    def enter_captcha():
        global captcha
        captcha = captcha_entry.get()
        print("Entered CAPTCHA:", captcha)
        popup.destroy()

    popup = tk.Tk()
    popup.title("CAPTCHA")
    label = tk.Label(popup, text="Please enter the CAPTCHA:")
    label.pack()
    captcha_entry = tk.Entry(popup)
    captcha_entry.pack()
    submit_button = tk.Button(popup, text="Submit", command=enter_captcha)
    submit_button.pack()
    popup.mainloop()

    return captcha
