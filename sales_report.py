#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

@dataclass
class Sale:
    product: str
    quantity: int
    unit_price: float


def read_sales(csv_path: Path) -> List[Sale]:
    sales: List[Sale] = []
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        next(reader, None)
        for line_no, row in enumerate(reader, start=2):
            product, qty, price = row
            sales.append(Sale(product.strip(), int(qty), float(price.replace(",", "."))))
    return sales


Totals = Dict[str, Dict[str, float]]
Report = Tuple[Totals, str | None, float]


def build_report(sales: List[Sale]) -> Report:
    totals: Totals = {}
    for s in sales:
        if s.product not in totals:
            totals[s.product] = {"quantity": 0, "value": 0.0}
        totals[s.product]["quantity"] += s.quantity
        totals[s.product]["value"] += s.quantity * s.unit_price
    most_sold = max(totals, key=lambda p: totals[p]["quantity"]) if totals else None
    grand_total = sum(item["value"] for item in totals.values())
    return totals, most_sold, grand_total


def print_report(report: Report) -> None:
    totals, most_sold, grand_total = report
    header = f"{'Produto':<20} {'Quantidade':>12} {'Valor Total':>15}"
    rule = "-" * len(header)
    print("Relatório de Vendas")
    print(header)
    print(rule)
    for product, data in sorted(totals.items()):
        print(f"{product:<20} {data['quantity']:>12} R$ {data['value']:>12.2f}")
    print(rule)
    print(f"Produto mais vendido : {most_sold if most_sold else 'N/A'}")
    print(f"Total geral          : R$ {grand_total:.2f}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera um relatório de vendas a partir de um arquivo CSV.")
    parser.add_argument("csv_file", type=Path, help="Caminho para o CSV de vendas")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    report = build_report(read_sales(args.csv_file))
    print_report(report)


if __name__ == "__main__":
    main()
