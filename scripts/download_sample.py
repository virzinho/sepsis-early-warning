from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

BASE = "https://physionet.org/files/challenge-2019/1.0.0/training/training_setA"


def download_one(patient_number: int, destination: Path) -> tuple[int, bool]:
    patient_id = f"p{patient_number:06d}"
    url = f"{BASE}/{patient_id}.psv"
    output = destination / f"{patient_id}.psv"

    response = requests.get(url, timeout=30)
    if response.status_code != 200:
        return patient_number, False

    output.write_bytes(response.content)
    return patient_number, True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=20)
    args = parser.parse_args()

    destination = Path("data/raw/training_setA")
    destination.mkdir(parents=True, exist_ok=True)

    successes = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [
            pool.submit(download_one, i, destination)
            for i in range(1, args.n + 1)
        ]

        for future in as_completed(futures):
            _, ok = future.result()
            successes += int(ok)

    print(f"Downloaded {successes}/{args.n} patient files.")

    if successes == 0:
        raise RuntimeError("No PhysioNet files were downloaded.")


if __name__ == "__main__":
    main()
