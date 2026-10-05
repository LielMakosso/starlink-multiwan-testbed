🌐 Starlink Multi-WAN 

# Intégration de Starlink dans une architecture multi-WAN : bascule automatique, QoS VoIP et supervision

[![pfSense](https://img.shields.io/badge/pfSense-2.9.0-blue)](https://www.pfsense.org/)
[![VyOS](https://img.shields.io/badge/VyOS-rolling-green)](https://vyos.io/)
[![Zabbix](https://img.shields.io/badge/Zabbix-7.4-red)](https://www.zabbix.com/)
[![GNS3](https://img.shields.io/badge/GNS3-3.1.0-orange)](https://www.gns3.com/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey)]()

📖 Présentation

Ce projet a été réalisé dans le cadre d'un **Projet de Fin d'Études (PPP)** à l'**École Centrale des Logiciels Libres et de Télécommunications (EC2LT).

Il consiste à étudier l'intégration de **Starlink** (constellation satellite en orbite basse LEO) comme lien WAN parmi d'autres, au sein d'une architecture réseau hétérogène. L'objectif est de démontrer qu'il est possible de :

- Basculer automatiquement entre un lien terrestre (fibre/LTE) et un lien satellite Starlink en cas de panne.
- Mesurer objectivement la performance et la fiabilité de cette bascule (RTO).
- Préserver la qualité de service (QoS) pour les flux critiques comme la VoIP.
- Superviser l'ensemble de l'architecture avec des métriques en temps réel.

Message clé : La question n'est plus de savoir si le LEO a sa place, mais comment l'intégrer de façon fiable et mesurable.


❓ Problématique

Comment intégrer Starlink comme lien WAN parmi d'autres, au sein d'une architecture réseau hétérogène, avec une bascule automatique dont la performance et la fiabilité soient mesurables ?

# Sous-questions

1. Critères : Quelles métriques (latence, gigue, perte, disponibilité) déclenchent la bascule ?
2. Mécanismes : Quels outils (SD-WAN, routage dynamique, sondes) l'automatisent sans intervention humaine ?
3. Évaluation : Quels indicateurs mesurables prouvent l'efficacité de l'intégration ?


🏗️ Architecture

# Schéma de la topologie

┌─────────────────────────────────────────────────────────────┐
│                    ZONE DE SUPERVISION                       │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │   Zabbix    │  │   Grafana   │                          │
│  └─────────────┘  └─────────────┘                          │
│         │                                                   │
│         │ (Collecte : Latence, RTO, Gigue)                  │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ZONE LAN (Utilisateur)                  │   │
│  │  ┌─────────────┐  ┌─────────────────────────────┐   │   │
│  │  │   Client    │  │   Téléphonie VOIP           │   │   │
│  │  │ (Générateur │  │   (Flux critique)           │   │   │
│  │  │  de trafic) │  │                             │   │   │
│  │  └─────────────┘  └─────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                    Interface LAN                            │
│                           │                                 │
│                           ▼                                 │
│              ┌─────────────────────────┐                    │
│              │   ROUTEUR DUAL-WAN      │                    │
│              │   (pfSense)             │                    │
│              └─────────────────────────┘                    │
│                    │              │                         │
│         WAN 1      │              │      WAN 2              │
│    (Fibre/LTE)     │              │   (Starlink)            │
│         │          │              │      │                  │
│         ▼          │              │      ▼                  │
│  ┌─────────────┐   │              │  ┌─────────────────┐    │
│  │  Émulateur  │   │              │  │  Émulateur      │    │
│  │  Fibre      │   │              │  │  Starlink       │    │
│  │  (VyOS R2)  │   │              │  │  (tc netem)     │    │
│  │  Latence:   │   │              │  │  Latence:       │    │
│  │  10ms       │   │              │  │  25-60ms        │    │
│  │  Perte: 0%  │   │              │  │  Gigue, Coupures│    │
│  └─────────────┘   │              │  └─────────────────┘    │
│         │          │              │      │                  │
│         └──────────┼──────────────┼──────┘                  │
│                    │              │                         │
│                    ▼              ▼                         │
│              ┌─────────────────────────┐                    │
│              │   INTERNET / CLOUD      │                    │
│              │   (Serveur de test RTO) │                    │
│              └─────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘

# Composants

| Composant | Rôle | Technologie |
|-----------|------|-------------|
| pfSense CE | Routeur dual-WAN, failover, QoS, pare-feu | FreeBSD |
| VyOS R2 | Routeur WAN1 (fibre/LTE), OSPF, NAT | Linux/Debian |
| netem-WAN2 | Émulation du lien Starlink | Debian + tc netem |
| Zabbix | Supervision, métriques, alertes | Ubuntu |
| PC1/PC2/PC3 | Clients de test (trafic, VoIP, load balancing) | VPCS |


🛠️ Technologies utilisées

| Technologie | Version | Usage |
|-------------|---------|-------|
| GNS3 | 3.1.0 | Émulation de la topologie réseau |
| VMware Workstation | 17 | Hébergement des VMs |
| pfSense CE | 2.9.0 | Routeur dual-WAN, failover, QoS |
| VyOS | Rolling | Routeur WAN1, OSPF, NAT |
| Debian | 13 | Émulation Starlink (tc netem) |
| Zabbix | 7.4 | Supervision réseau |
| MySQL | 8.0 | Base de données Zabbix |
| FRR | - | Routage OSPF sur pfSense |
| tc netem | - | Émulation latence/gigue/pertes |
| Python | 3.x | Script de mesure du RTO |
| Bash | - | Script de coupures périodiques |


📁 Structure du dépôt

starlink-multiwan-testbed/
│
├── README.md                          # Ce fichier
│
├── docs/                              # Documentation
│   ├── rapport_ppp.pdf                # Rapport complet du PPP
│   ├── presentation.pptx              # Présentation de soutenance
│   └── schemas/                       # Schémas et diagrammes
│       ├── topologie_gns3.png
│       ├── architecture_cible.png
│       └── flux_supervision.png
│
├── configs/                           # Fichiers de configuration
│   ├── pfsense/
│   │   ├── gateway_groups.xml         # Configuration Gateway Groups
│   │   ├── firewall_rules.xml         # Règles de firewall
│   │   └── limiters_qos.xml           # Configuration QoS
│   ├── vyos/
│   │   ├── config.boot                # Configuration VyOS
│   │   └── ospf.conf                  # Configuration OSPF
│   └── netem/
│       ├── netem_setup.sh             # Script de configuration tc netem
│       └── periodic_outage.sh         # Script de coupures périodiques
│
├── scripts/                           # Scripts de test
│   ├── rto_monitor.py                 # Mesure du RTO
│   ├── ping_test.sh                   # Test de connectivité
│   └── qos_test.sh                    # Test de QoS
│
├── results/                           # Résultats des tests
│   ├── rto_test_final.csv             # Résultats du RTO
│   ├── qos_latency.csv                # Résultats QoS
│   └── graphs/                        # Graphiques
│       ├── rto_bar_chart.png
│       └── qos_latency_chart.png
│
└── gns3/                              # Projet GNS3
    ├── topology.gns3                  # Fichier de topologie
    └── images/                        # Images des VMs


⚙️ Prérequis

# Matériel
- CPU : 4 cœurs minimum (8 recommandés)
- RAM : 16 Go minimum (32 Go recommandés)
- Stockage : 100 Go d'espace libre
- Réseau : Connexion Internet stable

# Logiciel
- GNS3 3.x
- VMware Workstation 17+
- pfSense CE 2.9.0 (ISO)
- VyOS rolling release (ISO)
- Debian 13 netinst (ISO)
- Ubuntu 22.04 (pour Zabbix)
- Python 3.x
- Git


🚀 Installation

#  1. Cloner le dépôt

git clone https://github.com/LielMakosso/starlink-multiwan-testbed.git
cd starlink-multiwan-testbed


# 2. Importer la topologie GNS3

1. Ouvrir GNS3
2. `File` → `Import portable project`
3. Sélectionner `gns3/topology.gns3`

# 3. Configurer les VMs

# pfSense

# Configuration des interfaces
WAN   : 10.0.1.2/24 (vers VyOS-R2)
LAN   : 192.168.10.1/24
OPT1  : 10.0.2.2/24 (vers netem-WAN2)


# VyOS-R2

configure
set interfaces ethernet eth0 address 10.0.1.1/24
set interfaces ethernet eth1 address dhcp
set protocols static route 0.0.0.0/0 next-hop 192.168.140.2
set nat source rule 100 outbound-interface name eth1
set nat source rule 100 source address 0.0.0.0/0
set nat source rule 100 translation address masquerade
commit
save


# netem-WAN2

# Configuration des interfaces
sudo ip addr add 10.0.2.1/24 dev ens33
sudo ip link set ens33 up
sudo ip link set ens37 up

# Activation du forwarding IP
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf

# Configuration du NAT
sudo iptables -t nat -A POSTROUTING -o ens37 -j MASQUERADE

# Application de tc netem sur ens37
sudo tc qdisc add dev ens37 root netem delay 40ms 10ms distribution normal loss 1%

# 4. Configurer Zabbix

# Installation de Zabbix
wget https://repo.zabbix.com/zabbix/7.4/release/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest_7.4+ubuntu22.04_all.deb
sudo dpkg -i zabbix-release_latest_7.4+ubuntu22.04_all.deb
sudo apt update
sudo apt install zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent

# Création de la base de données
mysql -uroot -p
CREATE DATABASE zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE USER 'zabbix'@'localhost' IDENTIFIED BY 'MonM0tDeP@sseS3curise!2026';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';
SET GLOBAL log_bin_trust_function_creators = 1;
QUIT;

# Import du schéma
zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql --default-character-set=utf8mb4 -uzabbix -p zabbix

# Redémarrage des services
sudo systemctl restart zabbix-server zabbix-agent apache2
sudo systemctl enable zabbix-server zabbix-agent apache2

🔧 Configuration

# pfSense : Gateway Groups

1. `System` → `Routing` → `Gateways`
   - Vérifier WANGW (10.0.1.1) et OPT1GW (10.0.2.1)
   - Configurer Monitor IP : 8.8.8.8 (WANGW) et 1.1.1.1 (OPT1GW)

2. `System` → `Routing` → `Gateway Groups`
   - Créer `WAN_FAILOVER` : WANGW (Tier 1), OPT1GW (Tier 2)
   - Trigger Level : Member Down

3. `Firewall` → `Rules` → `LAN`
   - Modifier la règle par défaut pour utiliser `WAN_FAILOVER`

# pfSense : QoS

1. `Firewall` → `Traffic Shaper` → `Limiters`
   - Créer `OPT1_Bandwidth` (3 Mbit/s)
   - Créer `VoIP_Priority_Down` (poids 90)
   - Créer `Default_Traffic_Down` (poids 10)

2. `Firewall` → `Rules` → `LAN`
   - Règle VoIP (PC2) → `VoIP_Priority_Down`
   - Règle par défaut → `Default_Traffic_Down`

# pfSense : OSPF (FRR)

1. `System` → `Package Manager` → Installer `FRR`
2. `Services` → `FRR` → `Global Settings` → Activer
3. `Services` → `FRR` → `OSPF` → `Interfaces` → Ajouter WAN (Area 0.0.0.0)
4. `Firewall` → `Rules` → `WAN` → Autoriser OSPF

# VyOS : OSPF

configure
set protocols ospf area 0 network 10.0.1.0/24
set protocols ospf area 0 network 172.16.99.1/32
set interfaces loopback lo address 172.16.99.1/32
commit
save


🧪 Scénarios de test

| # | Scénario | Méthode | Mesure |
|---|----------|---------|--------|
| 1 | Émulation Starlink | `tc netem delay 40ms 10ms loss 1%` | Latence et gigue WAN2 vs WAN1 |
| 2 | Failover réel | Arrêt de VyOS-R2 + ping continu | Pertes, bascule Tier 2 |
| 3 | RTO | `rto_monitor.py` (pas de 0,5 s), 4 coupures | RTO min / moyen / max |
| 4 | Micro-coupures | `periodic_outage.sh` : 2 s toutes les 15 s | Absence de flapping |
| 5 | QoS VoIP | WAN2 limité à 3 Mbit/s + téléchargement 100 Mo | Latence de PC2 |
| 6 | OSPF et load balancing | FRR ; Gateway Group au même Tier | Full/DR ; répartition WAN/OPT1 |

# Exécution des tests


# Test de RTO
python3 scripts/rto_monitor.py --target 8.8.8.8 --interval 0.5 --output results/rto_test.csv

# Test de coupures périodiques (sur netem-WAN2)
./configs/netem/periodic_outage.sh ens37 2 15 10

# Test de QoS
curl -o /dev/null http://speedtest.tele2.net/100MB.zip


 📊 Résultats

# RTO (Recovery Time Objective)

| Métrique | Valeur |
|----------|--------|
| Nombre de coupures testées | 4 |
| RTO minimum | 15,85 s |
| RTO maximum | 17,05 s |
| **RTO moyen** | **16,28 s** |
| RTO médian | 16,11 s |
| Écart-type | 0,53 s |

# QoS VoIP

| Métrique | Valeur |
|----------|--------|
| Bande passante WAN2 | 3 Mbit/s |
| Charge (téléchargement) | 2,8 Mbit/s |
| Latence VoIP | 13-28 ms |
| Poids VoIP | 90 |
| Poids Default | 10 |

# Load Balancing

| Destination | Paquet 1 | Paquet 2 | Paquet 3 | Paquet 4 |
|-------------|----------|----------|----------|----------|
| 1.1.1.1 | WAN | OPT1 | WAN | OPT1 |
| 8.8.8.8 | OPT1 | WAN | OPT1 | WAN |
| 9.9.9.9 | WAN | OPT1 | WAN | OPT1 |
| 4.2.2.1 | OPT1 | WAN | OPT1 | WAN |

Répartition : 50/50 entre WAN et OPT1

# OSPF

| Métrique | Valeur |
|----------|--------|
| État du voisinage | Full/DR |
| Route apprise | 172.16.99.1/32 |
| Gateway | 10.0.1.1 (VyOS-R2) |
| Interface | em0 (WAN) |


⚠️ Limites et perspectives

# Limites

- Émulation tc netem : Ne modélise pas les effets radio (Doppler, météo, handoffs satellite réels).
- RTO perfectible : 16,28 s est trop long pour la VoIP en cours d'appel.
- Peu de mesures : Seulement 4 mesures de RTO.
- WAN1 : Connexion Internet réelle du lab (55-146 ms), pas un lien fibre dédié.
- Complexité : Gestion accrue à grande échelle.
- MPTCP et bonding : Étudiés mais non implémentés (support des extrémités, hétérogénéité des liens).



📚 Références

- [pfSense Documentation](https://docs.netgate.com/pfsense/en/latest/)
- [VyOS Documentation](https://docs.vyos.io/)
- [Zabbix Documentation](https://www.zabbix.com/documentation/current/)
- [GNS3 Documentation](https://docs.gns3.com/)
- [tc netem Manual](https://man7.org/linux/man-pages/man8/tc-netem.8.html)
- [3GPP NTN Specifications](https://www.3gpp.org/technologies/ntn)
- [Starlink Official](https://www.starlink.com/)
- [MPTCP RFC 8684](https://datatracker.ietf.org/doc/html/rfc8684)


