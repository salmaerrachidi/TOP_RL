import os
import pandas as pd

# Fonction pour traiter un fichier et extraire les données
def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Initialisation des variables
        instance_data = {'n': None, 'm': None, 'tmax': None, 'profit_sum': 0}

        for line in lines:
            parts = line.strip().split(';')
            if len(parts) == 2:
                key, value = parts
                if key in instance_data:
                    instance_data[key] = float(value) if '.' in value else int(value)
            elif len(parts) == 3:
                instance_data['profit_sum'] += int(parts[2])  # Ajouter la 3e valeur (profit) à la somme

        return instance_data

# Fonction pour traiter tous les fichiers dans un dossier
def process_directory(directory_path):
    instances = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            instance_name = os.path.splitext(file_name)[0]
            instance_data = process_file(file_path)
            instance_data['instance_name'] = instance_name
            instances.append(instance_data)
    return instances

def main(data_directory):
    directories = ['Chao', 'Newinstances']
    all_instances = []

    for directory in directories:
        directory_path = os.path.join(data_directory, directory)
        if os.path.exists(directory_path):
            all_instances.extend(process_directory(directory_path))


    data = []
    for instance in all_instances:
        data.append([instance['instance_name'], instance['n'], instance['m'], instance['tmax'], instance['profit_sum']])

    df = pd.DataFrame(data, columns=['Instance Name', 'n', 'm', 'tmax', 'Profit Sum'])
    print(df.head())


    output_file = os.path.join(data_directory, 'output.xlsx')
    df.to_excel(output_file, index=False)
    return output_file

#
data_directory = './Data'


output_file = main(data_directory)
print(f"Output file created: {output_file}")
