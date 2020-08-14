import queue
import threading
import PySimpleGUI as sg
from spider import scrape
import pandas as pd

class Gui:
    def __init__(self):
        sg.theme("DarkAmber")
        sg.SetOptions(font="opensans 11")
        self.layout = [
            [sg.Text("Instagram Crawler", font="sfprodisplay 25 bold")],
            [
                sg.Text("Input CSV File", pad=((10, 25), (10, 10))),
                sg.InputText(key="_FILE_"),
                sg.FileBrowse(),
            ],
            [
                sg.Button("Scrape", pad=((200, 50), (10, 10)), key="_SCRAPE_"),
                sg.Button("Quit", pad=((50, 0), (10, 10)), key="_QUIT_"),
            ],
            [sg.Output(size=(200, 400), pad=(0, (10, 10)))],
        ]
        self.window = sg.Window("Spider", size=(650, 400), layout=self.layout)


if __name__ == "__main__":

    # queue used to communicate between the gui and the threads
    gui_queue = queue.Queue()

    gui = Gui()

    # --------------------- EVENT LOOP ---------------------
    while True:
        # wait for up to 100 ms for a GUI event
        event, values = gui.window.Read(timeout=100)
        if event is None or event == "_QUIT_":
            break

        if event == "_SCRAPE_":
            filepath = values.get("_FILE_")

            if filepath:
                try:
                    df = pd.read_csv(filepath)
                    profiles = list(df.profiles)
                    print("Starting to crawl")
                    threading.Thread(
                        target=scrape, args=(profiles, gui_queue,), daemon=True
                    ).start()
                except Exception as e:
                    print(f"Error occured {str(e)}")
            else:
                print("Please provide input csv file")

        # --------------- Check for incoming messages from threads  ---------------
        try:
            # get_nowait() will get exception when Queue is empty
            message = gui_queue.get_nowait()
        except queue.Empty:
            # break from the loop if no more messages are queued up
            message = None

        # if message received from queue, display the message in the Window
        if message:
            print(message)

    # if user exits the window, then close the window and exit the GUI func
    gui.window.Close()
