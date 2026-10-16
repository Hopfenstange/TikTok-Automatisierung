from autoinstall import install_if_missing

install_if_missing("undetected_chromedriver")
install_if_missing("selenium")

import gui

if __name__ == "__main__":
    gui.start_gui()
