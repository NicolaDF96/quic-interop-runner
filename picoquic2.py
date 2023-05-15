import json
import csv
import os

client_path = "picoquic/qlog/Client/"
server_path = "picoquic/qlog/Server/"
output_filename = "RisultatiPicoquic.csv"  # Nome del file CSV di output su cui memorizzare i risultati

# Apertura del file CSV di output una volta all'esterno del ciclo for
with open(output_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['File', 'Packet Loss', 'RTT Medio'])

    for filename in os.listdir(client_path):
        # consideriamo solo i file con estensione .qlog
        if filename.endswith(".qlog"):
            # Caricamento dei dati dal file
            with open(os.path.join(client_path, filename), "r") as file_client, \
                 open(os.path.join(server_path, filename), "r") as file_server:

                # Inizializzazione dei contatori
                sent_count = 0
                recv_count = 0
                num_rtt = 0
                sum_rtt = 0

                # Lettura dei file qlog e aggiornamento i contatori sent_count e recv_count
                data = json.load(file_client)
                events = data["traces"][0]["events"]
                for event in events:
                    if "packet_received" in event:
                        recv_count += 1
                    if isinstance(event, list) and len(event) >= 4 and isinstance(event[3], dict):
                        if "latest_rtt" in event[3]:
                              rtt_value = event[3]["latest_rtt"]
                              sum_rtt += rtt_value
                              num_rtt += 1
                        
            
                data = json.load(file_server)
                events = data["traces"][0]["events"]
                for event in events:
                    if "packet_sent" in event:
                        sent_count+=1
                    

                # Calcolo Packet loss
                packet_loss = round ((sent_count - recv_count) / sent_count * 100,3)

                # Calcolo RTT 
                rtt_medio = round (sum_rtt / num_rtt,3)

                # Scrittura deii risultati nel file CSV di output
                writer.writerow([filename, packet_loss, rtt_medio])

print(f"Risultati salvati correttamente nel file {output_filename}")