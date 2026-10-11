#!/usr/bin/env python3

import argparse
import csv
import platform
import subprocess
import time
from datetime import datetime, timezone
from statistics import mean, median, stdev


def ping_once(target: str, timeout_s: float = 1.0) -> bool:
    """Envoie un seul paquet ICMP et retourne True si une réponse est reçue."""
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(int(timeout_s * 1000)), target]
    else:
        cmd = ["ping", "-c", "1", "-W", str(max(1, int(round(timeout_s)))), target]
    try:
        result = subprocess.run(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout_s + 1
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds")


def main():
    parser = argparse.ArgumentParser(description="Mesure du RTO pour le banc d'essai multi-WAN")
    parser.add_argument("--target", default="8.8.8.8", help="IP/hôte à pinger en continu")
    parser.add_argument("--interval", type=float, default=0.5, help="Intervalle entre pings (s)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout par ping (s)")
    parser.add_argument("--output", default="rto_report.csv", help="Fichier CSV de sortie")
    parser.add_argument(
        "--consecutive-fail",
        type=int,
        default=2,
        help="Nombre d'échecs consécutifs avant de déclarer une panne (anti faux-positif)",
    )
    args = parser.parse_args()

    print(f"=== Mesure du RTO — cible: {args.target} — intervalle: {args.interval}s ===")
    print("Ctrl+C pour arrêter et afficher le résumé.\n")

    events = []
    rto_list = []

    state_up = True
    fail_streak = 0
    down_since = None

    csv_file = open(args.output, "w", newline="")
    writer = csv.writer(csv_file)
    writer.writerow(["timestamp", "event", "target", "detail"])
    csv_file.flush()

    try:
        while True:
            t_probe = time.time()
            ok = ping_once(args.target, args.timeout)
            ts = now_iso()

            if ok:
                fail_streak = 0
                if not state_up:
                    rto = t_probe - down_since
                    rto_list.append(rto)
                    state_up = True
                    msg = f"[{ts}]  RECOVERY — RTO = {rto:.2f} s"
                    print(msg)
                    writer.writerow([ts, "RECOVERY", args.target, f"RTO={rto:.2f}s"])
                    csv_file.flush()
            else:
                fail_streak += 1
                if state_up and fail_streak >= args.consecutive_fail:
                   
                    down_since = t_probe - (args.consecutive_fail - 1) * args.interval
                    state_up = False
                    msg = f"[{ts}]  OUTAGE DETECTED"
                    print(msg)
                    writer.writerow([ts, "OUTAGE_START", args.target, ""])
                    csv_file.flush()

            time.sleep(max(0.0, args.interval - (time.time() - t_probe)))

    except KeyboardInterrupt:
        print("\n\n=== Résumé de la session ===")
        if rto_list:
            print(f"Nombre de coupures détectées : {len(rto_list)}")
            print(f"RTO min    : {min(rto_list):.2f} s")
            print(f"RTO max    : {max(rto_list):.2f} s")
            print(f"RTO moyen  : {mean(rto_list):.2f} s")
            print(f"RTO médian : {median(rto_list):.2f} s")
            if len(rto_list) > 1:
                print(f"Écart-type : {stdev(rto_list):.2f} s")
            writer.writerow([])
            writer.writerow(["=== RESUME ==="])
            writer.writerow(["nb_coupures", len(rto_list)])
            writer.writerow(["rto_min_s", f"{min(rto_list):.2f}"])
            writer.writerow(["rto_max_s", f"{max(rto_list):.2f}"])
            writer.writerow(["rto_moyen_s", f"{mean(rto_list):.2f}"])
            writer.writerow(["rto_median_s", f"{median(rto_list):.2f}"])
            if len(rto_list) > 1:
                writer.writerow(["rto_stdev_s", f"{stdev(rto_list):.2f}"])
        else:
            print("Aucune coupure détectée pendant la session.")
        csv_file.close()
        print(f"\nRapport détaillé enregistré dans : {args.output}")


if __name__ == "__main__":
    main()
