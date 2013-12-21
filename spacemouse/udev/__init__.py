import pyudev

udev_context = pyudev.Context()


def _3dconnexion_match(device):
    devnode = device.device_node
    if not devnode or not "event" in devnode:
        return

    dev_parent = device.find_parent("usb", "usb_device")
    if not dev_parent:
        return

    if dev_parent.get('ID_VENDOR') == "3Dconnexion":
        return (devnode, "3Dconnexion", dev_parent.get('ID_MODEL'))
