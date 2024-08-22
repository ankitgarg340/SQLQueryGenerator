'''
-make 2 different "n as sensor" strings (1 for 5tms, 1 for mps2)
-make 2 different "n0, n1, ..." strings that are just the sensor ids (1 for 5tm, 1 for mps2)
-save in txt as: a_5tm, a_mps2, a_5tm_ids, a_mps_ids, new line
'''

def get_loc(sensor_str):
    items = sensor_str.split("_")
    return items[0][1:]+"_"+items[1]+"_"+items[2]+"_"+items[3]+"_"+items[4]

def get_header(sensor_loc_str, bay, type):
    return "LEO-" + bay + "_" + sensor_loc_str + "_" + type

def find_bay(src_id, src_group):
    if "center" in src_id and "center" in src_group:
        return "C"
    
    if "east" in src_id and "east" in src_group:
        return "E"
    
    if "west" in src_id and "west" in src_group:
        return "W"
    
    return "Error"

def load_csv_ids(src_csv):
    f = open(src_csv, "r")
    sensor_dict = {}

    for line in f:
        clean_line = line.strip("\n")
        items = clean_line.split(",")

        if items[0] != "sensor":
            sensor_dict[items[0]] = items[1]
    
    return sensor_dict

def load_csv_groups(src_csv, bay):
    f = open(src_csv, "r")
    sensor_dict = {}

    for line in f:
        clean_line = line.strip("\n")
        items = clean_line.split(",")
        if items[0] != "Sensor Code":
            if items[1] not in sensor_dict:
                sensor_dict[items[1]] = []
            sensor_dict[items[1]].append(get_header(items[0], bay, "5TM"))
            sensor_dict[items[1]].append(get_header(items[0], bay, "MPS-2"))
    
    return sensor_dict

def main():
    src_id = "SDI12_id_west.csv"
    src_groups = "SDI12_groups_west.csv"
    bay = find_bay(src_id, src_groups)

    sensor_dict_id = load_csv_ids(src_id)
    sensor_dict_groups = load_csv_groups(src_groups, bay)

    if bay == "W":
        sensor_dict_groups['O'].remove

    f_out = open("query_strings" + "_" + bay + ".txt", "w")
    f_out.write("Sensor Group: Query String\n")

    if bay == "W":
        sensor_dict_groups["O"].remove("LEO-W_26_-3_2_5TM")
        sensor_dict_groups["O"].remove("LEO-W_26_-2_2_5TM")

    sensor_dict_groups_5tm = {}
    sensor_dict_groups_mps2 = {}

    for k,v in sensor_dict_groups.items():
        for sensor in v:
            if "5TM" in sensor:
                if k not in sensor_dict_groups_5tm:
                    sensor_dict_groups_5tm[k] = []
                sensor_dict_groups_5tm[k].append(sensor)
            if "MPS-2" in sensor:
                if k not in sensor_dict_groups_mps2:
                    sensor_dict_groups_mps2[k] = []
                sensor_dict_groups_mps2[k].append(sensor)


    for k,v in sensor_dict_groups_5tm.items():
        line_out_1 = ""
        line_out_1 += (k + "_5TM: '")

        line_out_id = ""
        line_out_id += (k + "_5TM_ids: '")
        for sensor in v:
            sensor_id = sensor_dict_id[sensor]
            line_out_1 += (sensor_id + " as " + sensor + ", ")
            line_out_id += (sensor_id +", ")
        line_out_1 = line_out_1[:-2]
        line_out_1 += "'\n"

        line_out_id = line_out_id[:-2]
        line_out_id += "'\n"

        f_out.write(line_out_1)
        f_out.write(line_out_id)
        f_out.write("\n")
    

    for k,v in sensor_dict_groups_mps2.items():
        line_out_1 = ""
        line_out_1 += (k + "_MPS-2: '")

        line_out_id = ""
        line_out_id += (k + "_MPS-2_ids: '")

        for sensor in v:
            sensor_id = sensor_dict_id[sensor]

            line_out_1 += (sensor_id + " as " + sensor + ", ")
            line_out_id += (sensor_id +", ")
        
        line_out_1 = line_out_1[:-2]
        line_out_1 += "'\n"

        line_out_id = line_out_id[:-2]
        line_out_id += "'\n"

        f_out.write(line_out_1)
        f_out.write(line_out_id)
        f_out.write("\n")



main()