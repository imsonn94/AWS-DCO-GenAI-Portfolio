# 📋 DCO Incident & Log Analysis Summary

이 보고서는 교육용 샘플 DCO 로그 파일을 바탕으로 Python 분석 스크립트를 실행하여 자동 생성된 결과물입니다.
*(본 결과는 실제 인프라 및 장비와 무관한 시뮬레이션 데이터입니다.)*

## 📊 1. 전체 로그 요약 통계
- **전체 분석 대상 로그 수:** 140 줄

## 🛡️ 2. 심각도(Severity)별 집계
| 심각도 (Severity) | 로그 수 (Count) |
| :--- | :--- |
| `INFO` | 135개 |
| `WARNING` | 3개 |
| `ERROR` | 2개 |

## 🔍 3. 이벤트(Event) 유형별 집계 (상위 10개)
| 이벤트명 (Event Name) | 발생 횟수 (Count) |
| :--- | :--- |
| Normal heartbeat | 125개 |
| Ticket opened | 3개 |
| Ticket escalated | 3개 |
| Maintenance completed | 3개 |
| Fan Alert | 1개 |
| Temperature warning | 1개 |
| SSD failure warning | 1개 |
| CRC error 증가 | 1개 |
| Link Down | 1개 |
| Link Up | 1개 |

## ⚠️ 4. WARNING 및 CRITICAL 로그 목록
| 시간 (Timestamp) | 장비 (Device) | 심각도 | 이벤트명 | 세부 메시지 |
| :--- | :--- | :--- | :--- | :--- |
| 2026-07-03 01:05:00 | `DEMO_CORE_SW_02` | **WARNING** | Fan Alert | Fan module 2 RPM dropped to 15% (Below threshold 20%). IP: 198.51.100.2 |
| 2026-07-03 02:05:00 | `EDU_SRV_R04_N12` | **WARNING** | Temperature warning | Chassis temperature reached 42C (Threshold: 40C). IP: 192.0.2.12 |
| 2026-07-03 03:05:00 | `SAMPLE_TOR_SW_01` | **WARNING** | CRC error 증가 | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1 |

## 🚀 5. 주요 이슈 유형별 특별 요약
네트워크 장애 탐지 및 작업 프로세스 확인에 필수적인 주요 이벤트 필터링 결과입니다.

### 🔹 A. CRC_ERROR (물리 선로/감쇄 의심 요약)
- **시간:** 2026-07-03 03:05:00 | **장비:** `SAMPLE_TOR_SW_01` | **이벤트:** CRC error 증가
  - *메시지:* Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1
- **시간:** 2026-07-03 03:30:00 | **장비:** `SAMPLE_TOR_SW_01` | **이벤트:** Normal heartbeat
  - *메시지:* System status is healthy. Interface Gi0/1 running with 0 CRC errors. IP: 192.0.2.1

### 🔹 B. LINK_DOWN (포트/링크 오프라인 장애 요약)
- **시간:** 2026-07-03 03:06:00 | **장비:** `SAMPLE_TOR_SW_01` | **이벤트:** Link Down
  - *메시지:* Interface Gi0/1 status changed to DOWN. Connection to server lost.

### 🔹 C. TICKET_ESCALATED (티켓 이관 및 에스컬레이션 흐름)
- **시간:** 2026-07-03 01:10:00 | **장비:** `DEMO_CORE_SW_02` | **이벤트:** Ticket escalated
  - *메시지:* Ticket EDU-TKT-2026-0001 escalated to Local Infrastructure Team.
- **시간:** 2026-07-03 02:15:00 | **장비:** `EDU_SRV_R04_N12` | **이벤트:** Ticket escalated
  - *메시지:* Ticket EDU-TKT-2026-0002 escalated to DCO Hardware Support.
- **시간:** 2026-07-03 03:12:00 | **장비:** `SAMPLE_TOR_SW_01` | **이벤트:** Ticket escalated
  - *메시지:* Ticket EDU-TKT-2026-0003 escalated to Onsite Cabling Team.

