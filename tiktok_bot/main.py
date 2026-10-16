from autoinstall import install_if_missing

# Automatisch fehlende Pakete installieren
install_if_missing("undetected_chromedriver")
install_if_missing("selenium")

# GUI starten
import gui
