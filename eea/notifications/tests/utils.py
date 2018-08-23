def log(test_name, test_info, status="success"):
    class Color:
        OK = '\033[92m'
        ERR = '\033[91m'
        END = '\033[0m'

    text = "\n    TESTING {:>40}: {}".format(test_name, test_info)
    if status == "success":
        text = "{0}{1}{2}".format(Color.OK, text, Color.END)
    else:
        text = "{0}{1}{2}".format(Color.ERR, text, Color.END)

    print(text)
