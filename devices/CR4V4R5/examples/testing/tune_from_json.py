def tune_from_json(band, cr4):
    # Set the attenuation for all channels
    cr4.set_attenuation_db([1, 2, 3, 4], band["attenuation_db"])

    # Tune the RF Filters
    filters = band["filter_settings"]
    cr4.tune_filters([1,2,3,4], filters[0], filters[1], filters[2], filters[3])

    # Tune the PLLs
    cr4.tune_pll("D", band["lo_freq_mhz_downconvert"])
    cr4.tune_pll("B", band["lo_freq_mhz_downconvert"])

    cr4.tune_pll("A", band["lo_freq_mhz_upconvert"])
    cr4.tune_pll("C", band["lo_freq_mhz_upconvert"])

    # Set the switch state
    cr4.set_switch("AB", band["switch_mode"])
    cr4.set_switch("CD", band["switch_mode"])