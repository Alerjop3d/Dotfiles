#!/bin/bash
sudo pacman -S --noconfirm archlinux-wallpaper python-setuptools

Run_lightdm() {
    sudo systemctl restart lightdm
    echo "LightDM reiniciado correctamente."
}

Run_xorg() {
    startx
    echo "Xorg reiniciado correctamente."
}
mv 
sudo python ./setup.py build && setup.py install

if systemctl is-active --quiet lightdm; then
    Run_lightdm
elif command -v startx &> /dev/null; then
    Run_xorg
else
    echo "Ni LightDM ni Xorg están instalados en este sistema."
fi

echo "Paquetes instalados y lightdm reiniciado correctamente."


