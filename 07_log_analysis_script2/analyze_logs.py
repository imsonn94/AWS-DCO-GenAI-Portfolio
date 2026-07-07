#!/usr/bin/env python3
"""
server*.log 파일에서 서버별 CRC Error / Link Down 발생 횟수를 집계합니다.

판별 규칙:
  - CRC Error  : 레벨이 ERROR이고, 메시지에 'crc error' 포함
                 단, 'crc error recovered' / 'no crc error found' 제외
  - Link Down  : 레벨이 ERROR이고, 메시지에 'link down' 포함
                 단, 'linkdown_timer' 제외
"""

import glob
import re
from pathlib import Path
from collections import defaultdict

# ── 패턴 정의 ──────────────────────────────────────────────────────────────────
# 지원하는 타임스탬프 형식 (서버마다 다름):
#   server01: 2026-07-06 00:26:20        → ISO datetime
#   server02: Jul 06 01:59:04            → syslog (월 일 시각)
#   server03: [06/Jul/2026:01:36:20]     → Apache Combined Log
#   server04: 03:27:06.628               → 시각만 (HH:MM:SS.mmm)
TS_PATTERNS = [
    r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}",        # ISO
    r"[A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}",    # syslog
    r"\[\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}\]", # Apache
    r"\d{2}:\d{2}:\d{2}\.\d+",                          # HH:MM:SS.mmm
]
TS_RE = "(?:" + "|".join(TS_PATTERNS) + ")"

LOG_LINE_RE = re.compile(
    r"^" + TS_RE + r"\s+"  # timestamp (형식 무관)
    r"(\S+)\s+"             # (1) server name
    r"(\S+)\s+"             # (2) level
    r"(.+)$"                # (3) message
)

def is_crc_error(level: str, msg: str) -> bool:
    """ERROR 레벨 + 'crc error' 포함 + 복구/정상 메시지 제외"""
    if level.upper() != "ERROR":
        return False
    m = msg.lower()
    if "crc error" not in m:
        return False
    # 제외 패턴
    if "crc error recovered" in m:
        return False
    if "no crc error" in m:
        return False
    return True

def is_link_down(level: str, msg: str) -> bool:
    """ERROR 레벨 + 'link down' 포함 + linkdown_timer 제외"""
    if level.upper() != "ERROR":
        return False
    m = msg.lower()
    if "link down" not in m:
        return False
    if "linkdown_timer" in m:
        return False
    return True

# ── 집계 ───────────────────────────────────────────────────────────────────────
def analyze(log_dir: str = ".") -> dict:
    results = defaultdict(lambda: {"CRC Error": 0, "Link Down": 0})

    pattern = str(Path(log_dir) / "server*.log")
    log_files = sorted(glob.glob(pattern))

    if not log_files:
        print(f"[!] '{pattern}' 패턴에 해당하는 파일을 찾을 수 없습니다.")
        return results

    for filepath in log_files:
        fname = Path(filepath).name
        print(f"[읽는 중] {fname}")
        with open(filepath, encoding="utf-8", errors="replace") as f:
            for line in f:
                m = LOG_LINE_RE.match(line.rstrip())
                if not m:
                    continue
                server, level, msg = m.group(1), m.group(2), m.group(3)
                if is_crc_error(level, msg):
                    results[server]["CRC Error"] += 1
                if is_link_down(level, msg):
                    results[server]["Link Down"] += 1

    return results

# ── 출력 ───────────────────────────────────────────────────────────────────────
def print_results(results: dict) -> None:
    if not results:
        print("집계 결과가 없습니다.")
        return

    col_w = max(len(s) for s in results) + 2
    header = f"{'서버':<{col_w}} {'CRC Error':>12} {'Link Down':>12}"
    sep    = "-" * len(header)

    print()
    print("=" * len(header))
    print("  서버별 CRC Error / Link Down 집계 결과")
    print("=" * len(header))
    print(header)
    print(sep)

    total_crc = total_ld = 0
    for server in sorted(results):
        crc = results[server]["CRC Error"]
        ld  = results[server]["Link Down"]
        total_crc += crc
        total_ld  += ld
        print(f"{server:<{col_w}} {crc:>12} {ld:>12}")

    print(sep)
    print(f"{'합계':<{col_w}} {total_crc:>12} {total_ld:>12}")
    print("=" * len(header))

if __name__ == "__main__":
    import sys
    log_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    results = analyze(log_dir)
    print_results(results)
