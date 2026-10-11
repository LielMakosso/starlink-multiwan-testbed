# Banc d'essai Starlink MultiWAN

## Description du projet

Ce projet vise à valider la mise en place d'une architecture MultiWAN avec bascule automatique entre deux liens Internet (Starlink et un lien dégradé simulé via Netem). L'objectif est de mesurer le **RTO (Recovery Time Objective)**, de valider la **QoS (priorisation VoIP)** et d'observer le comportement du réseau en cas de coupure.

## Architecture

![Topologie](Topologie/topologie_gns3.png)

### Plan d'adressage

| Équipement | Interface | Adresse IP | Rôle |
| :--- | :--- | :--- | :--- |
| pfSense | LAN | 192.168.10.1/24 | Pare-feu / Routeur principal |
| pfSense | WAN1 | DHCP | Lien Starlink |
| pfSense | OPT1 | DHCP | Lien Netem (WAN2) |
| VyOS-R2 | eth0 | 10.0.1.1/24 | Routeur FAI simulé |
| VyOS-R2 | lo | 172.16.99.1/32 | Loopback OSPF |
| netem-wan2 | ens33 | 10.0.2.1/24 | Simulation réseau dégradé |
| netem-wan2 | ens37 | DHCP | Lien vers pfSense |
| zabbix-supervision | ens33 | 192.168.10.50/24 | Supervision |

### Caractéristiques techniques des machines

| Machine | OS | CPU | RAM | Disque |
| :--- | :--- | :--- | :--- | :--- |
| pfSense | pfSense CE | 2 vCPU | 2 Go | 20 Go |
| VyOS-R2 | VyOS 1.4 | 1 vCPU | 1 Go | 10 Go |
| netem-wan2 | Debian 12 | 1 vCPU | 1 Go | 10 Go |
| zabbix-supervision | Ubuntu 22.04 | 2 vCPU | 4 Go | 40 Go |

## Prérequis

- GNS3 (pour la topologie réseau)
- VMware ou VirtualBox (pour les VMs)
- pfSense CE
- VyOS
- Debian (pour Netem) 
- Ubuntu (pour Zabbix)

## Installation et Reproductibilité

1. Cloner ce dépôt :
   ```bash
   git clone https://github.com/LielMakosso/starlink-multiwan-testbed.git

2. Configurer chaque équipement en se référant au dossier configs/

3. Lancer les scripts de test depuis le dossier Scripts/

##  Commandes de lancement des tests

### Mesure du RTO (depuis zabbix-supervision)
```bash
python3 scripts/rto_monitor.py --target 8.8.8.8 --interval 0.5 --output results/rto_demo_live.csv

