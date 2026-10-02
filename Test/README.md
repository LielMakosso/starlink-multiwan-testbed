Sur zabbix-supervision (Console)
Pour créer de la congestion (QoS) :
curl -o /dev/null http://speedtest.tele2.net/100MB.zip

Pour lancer les scripts de mesure du RTO :
python3 rto_monitor.py --target 8.8.8.8 --interval 0.5 --output rto_demo_live.csv
python3 rto_monitor.py --target 8.8.8.8 --interval 0.5 --output rto_profil2.csv
Pour arrêter les scripts (à la fin des tests) :
Ctrl+C
Sur PC2 et PC1 (Consoles GNS3)
Pour simuler le flux VoIP (PC2) :
ping 1.1.1.1
Pour la preuve visuelle de la coupure (PC1) :
ping 8.8.8.8 -t
Sur netem-WAN2 (Console)
Pour simuler un réseau très dégradé (Profil 2) :
tc qdisc replace dev ens37 root netem delay 80ms 25ms distribution normal loss 5%
Pour lancer les coupures périodiques :
./periodic_outage.sh ens37 2 15 5
Pour restaurer le profil réseau normal (Nettoyage final) :
tc qdisc replace dev ens37 root netem delay 40ms 10ms distribution normal loss 1%
