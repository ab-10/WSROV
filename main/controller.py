class controller:
    pDirection = 'none'

    # Xbox controller button IDs
    a_but = 0
    b_but = 1
    x_but = 2
    y_but = 3
    l_but = 4
    r_but = 5
    back_but = 6
    start_but = 7

    # ls_but = 8 uncomment if on Windows
    # rs_but = 9 uncomment if on Windows
    ls_but = 9   # comment out if on Windows
    rs_but = 10  # comment out if on Windows

    # Xbox controller axis IDs
    lsx = 0
    lsy = 1
    # trig = 2 uncomment if on Windows
    ltrig = 2  # comment out if on Windows
    rtrig = 5  # comment out if on Windows
    rsx = 3
    rsy = 4

    # Xbox controller button values (states)
    a_butVal = 0
    b_butVal = 0
    x_butVal = 0
    y_butVal = 0
    l_butVal = 0
    r_butVal = 0
    back_butVal = 0
    start_butVal = 0
    ls_butVal = 0
    rs_butVal = 0

    # Xbox controller axis values
    lsx_val = 0
    lsy_val = 0
    # trig_val = 0 uncomment if on Windows
    ltrig_val = 50  # comment out if on Windows
    rtrig_val = 50  # comment out if on Windows
    rsx_val = 0
    rsy_val = 0

