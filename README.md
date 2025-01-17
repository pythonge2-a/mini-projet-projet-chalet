[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/oOQR1xPR)
# Nom du projet

## Membres

- Nom 1
- Nom 2
- Nom 3
- ...

## Description

Description du projet en quelques lignes

## Cahier des charges

- Ceci **doit** être fait
- Ceci **doit** être fait
- Ceci **devrait** être fait (si le temps le permet)
- ...

## Installation

```bash
poetry install
```

## (Pour les étudiants, à supprimer une fois fait)

### Comment créer le module

1. Créer un nouveau répertoire avec le nom du module
2. Créer un fichier `__init__.py` vide
3. Créer un fichier `__main__.py` vide
4. Mettre à jour le fichier `README.md`
5. Créer un projet Poetry avec `poetry new`
6. Ajouter les fichiers à Git
7. Commit et push

## Configuration serveur web

1. Installer un os lite sur un raspberry pi depuis pi Imager (32 bits recommandé pour les modèles avant le pi 5)
2. Configurer sur pi Imager l'accès Wi-Fi, un nom d'utilisateur avec mdp et activer le ssh (username: binlin, mdp: tintin)
3. Installer le tout sur la carte SD
4. Allumer le raspberry pi
5. Brancher un dongle Wi-Fi qui sera utilisé comme point d'accès pour les capteurs et actionneur
6. Connection ssh via terminal Windows 
```bash
ssh <username>@raspberrypi.local
```
7. Installation des packets
```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iproute2
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
```
8. Configuration d'une adresse IP statique pour wlan1
Accès au fichier de configuration
```bash
sudo nano /etc/dhcpcd.conf
```
Modifier le fichier en ajoutant ces lignes
```ini
interface wlan1
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```
Redémarrer le service
```bash
sudo systemctl restart dhcpcd
```
9. Configuration de dnsmasq
Accès au fichier de configuration
```bash
sudo nano /etc/dnsmasq.conf
```
Modifier le fichier en ajoutant ces lignes
```ini
interface=wlan1
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
```
Redémarrer le service
```bash
sudo systemctl restart dnsmasq
```
10.   Configuration de hostapd
Accès au fichier de configuration
```bash
sudo nano /etc/hostapd/hostapd.conf
```
Modifier le fichier en ajoutant ces lignes
```ini
interface=wlan1
driver=nl80211
ssid=MonPointAcces
hw_mode=g
channel=7
ieee80211n=1
wmm_enabled=1
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=monmotdepasse
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
```
Ajouter le chemin du fichier de configuration au système
```bash
sudo nano /etc/default/hostapd
```
Ajouter ces lignes
```ini
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```
Redémarrer le service
```bash
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```
11. Vérification
```bash
sudo systemctl status hostapd
sudo systemctl status dnsmasq
```
Si après le redémarrage wlan1 a bien une adresse IP et que vous arrivez à vous connecter au point d'accès avec un autre appareil, alors la configuration est terminée.
12. (Optionel) Configuration d'un script au démarrage pour attribuer une adresse IP à wlan1
Création du script
```bash
sudo nano /usr/local/bin/configure_wlan1.sh
```
Ecrire ces lignes dans le fichier
```bash
ip addr add 192.168.4.1/24 dev wlan1
```
Rendre le script exécutable
```bash
sudo chmod +x /usr/local/bin/configure_wlan1.sh
```
Ajouter le script au fichier de démarrage
```bash 
sudo nano /etc/rc.local
```
Ecrire ces lignes à la fin du fichier et avant le exit 0
```bash
/usr/local/bin/configure_wlan1.sh
```
13. Redémarrer le système
```bash
sudo reboot
```
## Comment utiliser le projet
### 1. Cloner le dépôt
Avant de commencer, vous devez cloner le dépôt sur votre machine locale. Pour ce faire, ouvrez un terminal et exécutez la commande suivante :
```bash
git clone <nom-du-dépôt>
```

### 2. Installer les dépendances
Après avoir cloné le dépôt, vous devez installer les dépendances du projet. Nous utilisons `poetry` donc pour ce faire, exécutez la commande suivante :
```bash
poetry install
```

### 3. Exécuter le programme
Une fois les dépendances installées, vous pouvez exécuter le programme. Pour ce faire, exécutez la commande suivante :
```bash
poetry run chalet
```

### 4. Utiliser l'interface
