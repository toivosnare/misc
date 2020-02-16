import obspython as obs

liitteet = ["_NA", "_VA", "_NB", "_VB"]
settings = None

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "_NA", "Joukkue A", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "_VA", "Väri A", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "_NB", "Joukkue B", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "_VB", "Väri B", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_button(props, "aseta", "Aseta", aseta)
    p = obs.obs_properties_add_list(props, "valinta", "Valinta", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "color_source":
                name = obs.obs_source_get_name(source)
                if name.endswith("_VA") or name.endswith("_VB"):
                    obs.obs_property_list_add_string(p, name, name)
    obs.source_list_release(sources)
    obs.obs_properties_add_button(props, "tulosta", "Tulosta", tulosta)
    return props

def script_update(s):
    global settings
    settings = s

def aseta(props, p):
    global liitteet
    global settings
    sources = obs.obs_enum_sources()

    for liite in liitteet:
        for source in sources:
            nimi = obs.obs_source_get_name(source)
            if nimi.endswith(liite):
                data = obs.obs_data_create()
                if "N" in liite:
                    tieto = obs.obs_data_get_string(settings, liite)
                    obs.obs_data_set_string(data, "text", tieto)
                elif "V" in liite:
                    tieto = obs.obs_data_get_string(settings, liite)
                    obs.obs_data_set_int(data, "color", int(tieto))
                obs.obs_source_update(source, data)
                obs.obs_data_release(data)
                obs.obs_source_release(source)

def tulosta(props, p):
    global settings

    nimi = obs.obs_data_get_string(settings, "valinta")
    source = obs.obs_get_source_by_name(nimi)
    data = obs.obs_source_get_settings(source)
    color = obs.obs_data_get_int(data, "color")
    print(color)