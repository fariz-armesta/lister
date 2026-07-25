import ctypes
from gui import App


myappid = "lister.app"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()