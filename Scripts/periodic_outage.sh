#!/bin/bash
set -u

IFACE="${1:-ens37}"
OUTAGE_DURATION="${2:-2}"
INTERVAL="${3:-15}"
CYCLES="${4:-0}"

NORMAL_DELAY="40ms 10ms distribution normal"
NORMAL_LOSS="1%"

LOG_FILE="periodic_outage.log"

log() {
    local ts
    ts=$(date -Iseconds)
    echo "[$ts] $1" | tee -a "$LOG_FILE"
}

apply_normal() {
    tc qdisc replace dev "$IFACE" root netem delay $NORMAL_DELAY loss $NORMAL_LOSS >/dev/null 2>&1
}

apply_outage() {
    tc qdisc replace dev "$IFACE" root netem loss 100% >/dev/null 2>&1
}

restore_and_exit() {
    log "Arrêt demandé — restauration de l'état normal sur $IFACE"
    apply_normal
    log "=== Fin de la simulation ==="
    exit 0
}

trap restore_and_exit SIGINT SIGTERM

if ! ip link show "$IFACE" >/dev/null 2>&1; then
    echo "Erreur : l'interface $IFACE n'existe pas."
    exit 1
fi

log "=== Démarrage simulation coupures périodiques ==="
log "Interface: $IFACE | Durée coupure: ${OUTAGE_DURATION}s | Intervalle: ${INTERVAL}s | Cycles: $([ "$CYCLES" -eq 0 ] && echo illimité || echo $CYCLES)"

apply_normal
log "État initial: lien normal appliqué (delay=$NORMAL_DELAY loss=$NORMAL_LOSS)"

count=0
while true; do
    if [ "$CYCLES" -ne 0 ] && [ "$count" -ge "$CYCLES" ]; then
        break
    fi

    sleep "$INTERVAL"

    apply_outage
    log "🔴 COUPURE #$((count+1)) — début (durée ${OUTAGE_DURATION}s)"

    sleep "$OUTAGE_DURATION"

    apply_normal
    log "🟢 COUPURE #$((count+1)) — fin, lien normal restauré"

    count=$((count+1))
done

restore_and_exit
