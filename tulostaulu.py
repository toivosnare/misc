import obspython as obs
import serial

ser = None
portti = "COM1"
viestit = {
    "33" : {
        "_K" : [[5, 9], []],
        "_PA" : [[9, 12], []],
        "_PB" : [[12, 15], []],
        "_J" : [[15, 16], []],
        "_JVA" : [[16, 17], []],
        "_JVB" : [[17, 18], []],
        "_AA" : [[18, 19], []],
        "_AB" : [[19, 20], []],
        "_A" : [[22, 49], []],
        "_H" : [[49, 51], []]
    },
    "37" : {
        "_K" : [[5, 9], []],
        "_H" : [[49, 51], []]
    },
    "38" : {
        "_K" : [[5, 9], []],
        "_H" : [[49, 51], []]
    }
}
merkit = {
    "@" : "0",
    "A" : "1",
    "B" : "2",
    "C" : "3",
    "D" : "4",
    "E" : "5",
    "F" : "6",
    "G" : "7",
    "H" : "8",
    "I" : "9"
}
grafiikat = [[], [], []]

def script_load(settings):
    global ser
    print("load")
    ser = serial.Serial()
    ser.baudrate = 19200

def script_unload():
    global ser
    print("unload")
    ser.close()

def script_description():
    return "Versio 1.1"

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "portti", "Sarjaportti", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_button(props, "yhdistä", "yhdistä", nappi)
    return props

def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "portti", "COM1")

def script_update(settings):
    global portti
    portti = obs.obs_data_get_string(settings, "portti")

def lue():
    global ser
    global viestit

    if not ser.is_open:
        print("remove_current_callback")
        obs.remove_current_callback()
        return

    while True:
        if ser.read(1).hex() == "f8":
            break
    viesti = ser.read(53)
    #viesti = b'3004242064128E123200100000000000000000000000021040000'
    #viesti = b'30010000000001550000100000000000000000000000000240000'
    #viesti = b'300001 22211144615001000000000000000000000000210D0000'

    koodi = viesti[0:1].hex()

    if not koodi in viestit:
        print("tuntematon viesti")
        return

    if not viesti[52:53].hex() == "0d":
        print("virheellinen viesti")
        return
    
    for liite in viestit[koodi]:
        tavut = viestit[koodi][liite][0]
        sourcet = viestit[koodi][liite][1]

        if liite == "_K":
            if str(viesti)[tavut[1]-1:tavut[1]] == " ":
                tieto = str(int(str(viesti)[tavut[0]:tavut[0]+2])) + "." + str(viesti)[tavut[0]+2:tavut[1]-1]
            else:
                tieto = (str(viesti)[tavut[0]:tavut[0]+2] + ":" + str(viesti)[tavut[0]+2:tavut[1]]).lstrip("0")

        elif liite == "_A":
            tieto = str(viesti)[tavut[0]:tavut[0]+1] + ":" + str(viesti)[tavut[1]-2:tavut[1]]
            for source in grafiikat[2]:
                if not tieto == " :  ":
                    obs.obs_source_set_enabled(source, True)
                else:
                    obs.obs_source_set_enabled(source, False)

        elif liite == "_PA" or liite == "_PB":
            tieto = str(viesti)[tavut[0]:tavut[1]].lstrip("0")
            if tieto == "":
                tieto = "0"

        elif liite == "_H":
            if str(viesti)[tavut[0]+1:tavut[1]] in "@ABCDEFGHI":
                tieto = str(viesti)[tavut[0]:tavut[1]-1] + "." + merkit[str(viesti)[tavut[0]+1:tavut[1]]]
            else:
                tieto = str(viesti)[tavut[0]:tavut[1]].lstrip("0")
            if tieto == "" or tieto == "0.0":
                tieto = "0"

        elif liite == "_JVA":
            tieto = str(viesti)[tavut[0]:tavut[1]]
            for i in range(len(grafiikat[0])):
                if i < int(tieto):
                    obs.obs_source_set_enabled(grafiikat[0][i], True)
                else:
                    obs.obs_source_set_enabled(grafiikat[0][i], False)

        elif liite == "_JVB":
            tieto = str(viesti)[tavut[0]:tavut[1]]
            for i in range(len(grafiikat[1])):
                if i < int(tieto):
                    obs.obs_source_set_enabled(grafiikat[1][i], True)
                else:
                    obs.obs_source_set_enabled(grafiikat[1][i], False)

        else:
            tieto = str(viesti)[tavut[0]:tavut[1]]

        for source in sourcet:
            data = obs.obs_data_create()
            obs.obs_data_set_string(data, "text", tieto)
            obs.obs_source_update(source, data)
            obs.obs_data_release(data)

def nappi(props, p):
    global ser
    global portti
    global grafiikat

    muotti = [["_1JVA", "_2JVA", "_3JVA", "_4JVA", "_5JVA"], ["_1JVB", "_2JVB", "_3JVB", "_4JVB", "_5JVB"], ["AIKALISÄ"]]

    if ser.is_open:
        print("Aloitettu jo")
        return
    sources = obs.obs_enum_sources()
    for source in sources:
        nimi = obs.obs_source_get_name(source)
        for viesti in viestit:
            for liite in viestit[viesti]:
                if nimi.endswith(liite) and source not in viestit[viesti][liite][1]:
                    viestit[viesti][liite][1].append(source)
                    break
    for i in muotti:
        for liite in i:
            for source in sources:
                nimi = obs.obs_source_get_name(source)
                if liite == "AIKALISÄ":
                    if liite in nimi:
                        grafiikat[muotti.index(i)].append(source)
                else:
                    if nimi.endswith(liite):
                        grafiikat[muotti.index(i)].append(source)
    print(grafiikat)
    ser.port = portti
    try:
        ser.open()
        print("yhdistetty")
    except serial.serialutil.SerialException as e:
        print(e)
    obs.timer_add(lue, 50)