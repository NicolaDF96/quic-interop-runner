import os

# Directory dei file
directory = "picoquic/qlog/Server"

# Itera su tutti i file nella directory
for filename in os.listdir(directory):
    if filename.endswith(".server.qlog"):
        # Crea il nuovo nome del file senza la parte ".aeab.server"
        new_filename = filename.replace(".server", "")

        # Rinomina il file
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))