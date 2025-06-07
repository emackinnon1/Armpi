import yaml
lab_file_path = '/home/emackinnon1/Projects/Armpi/ArmPi_mini_RPi_5_Version_Source_Code/ArmPi_mini/yaml/lab_config.yaml'
Deviation_file_path = '/home/emackinnon1/Projects/Armpi/ArmPi_mini_RPi_5_Version_Source_Code/ArmPi_mini/yaml/Deviation.yaml'
PickingCoordinates_file_path = '/home/emackinnon1/Projects/Armpi/ArmPi_mini_RPi_5_Version_Source_Code/ArmPi_mini/yaml/PickingCoordinates.yaml'

def get_yaml_data(yaml_file):
    file = open(yaml_file, 'r', encoding='utf-8')
    file_data = file.read()
    file.close()
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    
    return data

def save_yaml_data(data, yaml_file):
    file = open(yaml_file, 'w', encoding='utf-8')
    yaml.dump(data, file)
    file.close()
