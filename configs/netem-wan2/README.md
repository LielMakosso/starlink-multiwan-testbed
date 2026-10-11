# Configuration de netem-wan2

Cette machine simule un lien WAN dégradé (Netem) sur l'interface `ens37`.

## Configuration réseau
Le fichier `interfaces` contient la configuration IP de la machine.

## Configuration Netem (QoS)
La configuration est appliquée manuellement via la commande `tc`.

### Profil Normal (par défaut)
```bash
tc qdisc replace dev ens37 root netem delay 40ms 10ms distribution normal loss 1%

### Profil Dégradé (test 2)
tc qdisc replace dev ens37 root netem delay 80ms 25ms distribution normal loss 5%

## Scripts de test
./periodic_outage.sh ens37 2 15 5

## Suppression de la configuration
tc qdisc del dev ens37 root
