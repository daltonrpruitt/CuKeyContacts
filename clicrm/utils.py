import re
from typing import List, Any, Optional
from tabulate import tabulate


def find_by_name_regex(items: List[Any], name_field: str, pattern: str) -> List[Any]:
    regex = re.compile(pattern, re.IGNORECASE)
    return [item for item in items if regex.search(getattr(item, name_field, ""))]


def find_by_id(items: List[Any], target_id: str) -> Optional[Any]:
    for item in items:
        if item.id == target_id:
            return item
    return None


def print_table(items: List[Any], fields: List[str]):
    if not items:
        print("No results found.")
        return
    table = []
    for item in items:
        row = [getattr(item, field, "") for field in fields]
        table.append(row)
    headers = [field.replace("_", " ").title() for field in fields]
    print(tabulate(table, headers=headers, tablefmt="grid"))


def export_csv(items: List[Any], fields: List[str], filename: str):
    import csv
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        for item in items:
            writer.writerow([getattr(item, field, "") for field in fields])
    print(f"Exported {len(items)} records to {filename}")
