def process_data(jsondata):
    if "put" in jsondata:
        if "/vessels/self/environment/inside/lights/1" == jsondata["put"]["path"]:
            print(jsondata["put"]["value"])
            
            ledvalue = (int(jsondata["put"]["value"]))
            boatman = {"light": {"1" : ledvalue}}
            return boatman

        print("No recognised object to put")
        return 0

    else:
        print("Unrecognised command")
        print("JSON data: {}".format(jsondata))
        return -1