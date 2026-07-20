# -*- coding: utf-8 -*-
"""
교육용 DCO 로그 분석기 (DCO Log Analyzer)
작성 목적: Python 초보자 및 비전공자 학생들을 위한 로그 분석 기초 스크립트입니다.
외부 라이브러리 없이 Python 표준 라이브러리(Standard Library)만 사용하여 로그를 읽고 요약 보고서를 작성합니다.
"""
 
import os
 
# -------------------------------------------------------------
# 1. 파일 경로 설정
# -------------------------------------------------------------
# 분석할 샘플 로그 파일명과 분석 결과를 저장할 보고서 파일명입니다.
INPUT_FILE_NAME = "sample_dco_log.txt"
OUTPUT_FILE_NAME = "incident_summary.md"
 
 
def analyze_logs():
    # 로그 파일이 있는지 먼저 확인합니다.
    if not os.path.exists(INPUT_FILE_NAME):
        print(f"오류: '{INPUT_FILE_NAME}' 파일이 존재하지 않습니다.")
        print("먼저 분석할 로그 파일을 준비해 주세요.")
        return
 
    # -------------------------------------------------------------
    # 2. 데이터 분석을 위한 변수(저장소) 초기화
    # -------------------------------------------------------------
    total_lines = 0               # 1) 전체 로그 줄 수를 셀 변수
    severity_counts = {}          # 2) 심각도별(INFO, WARNING, ERROR 등) 개수를 저장할 딕셔너리
    event_counts = {}             # 3) 이벤트 종류별 개수를 저장할 딕셔너리
    warning_or_critical_logs = [] # 4) WARNING 또는 CRITICAL 로그를 모아둘 리스트
    
    # 5) 주요 이슈 요약을 위한 리스트
    major_events = {
        "CRC_ERROR": [],          # CRC 에러 관련 로그 리스트
        "LINK_DOWN": [],          # 링크 다운(오프라인) 관련 로그 리스트
        "TICKET_ESCALATED": []    # 티켓 에스컬레이션(팀 이관) 관련 로그 리스트
    }
 
    print(f"진행 중: '{INPUT_FILE_NAME}' 파일을 한 줄씩 읽으며 분석하고 있습니다...")
 
    # -------------------------------------------------------------
    # 3. 파일 읽기 및 분석 시작
    # -------------------------------------------------------------
    # utf-8 인코딩을 명시하여 한글 로그 메시지도 깨지지 않도록 안전하게 읽습니다.
    with open(INPUT_FILE_NAME, "r", encoding="utf-8") as file:
        for line in file:
            # 줄바꿈 문자(\n) 및 양쪽 공백을 제거합니다.
            cleaned_line = line.strip()
            
            # 빈 줄은 무시하고 넘어갑니다.
            if not cleaned_line:
                continue
 
            total_lines += 1  # 전체 줄 수 증가
 
            # 로그 형식: YYYY-MM-DD HH:MM:SS | DEVICE | SEVERITY | EVENT | MESSAGE
            # 파이프(|) 기호를 기준으로 각 열을 나눕니다.
            parts = cleaned_line.split("|")
            
            # 올바른 형식인지 확인합니다 (열이 5개 이상이어야 함).
            if len(parts) >= 5:
                # 각 요소의 앞뒤 공백을 깨끗하게 제거합니다.
                timestamp = parts[0].strip()
                device = parts[1].strip()
                severity = parts[2].strip()
                event = parts[3].strip()
                message = parts[4].strip()
 
                # A) 심각도별 개수 집계
                # dict.get(key, 0)은 해당 key가 없으면 0을 반환하고, 있으면 원래 값을 가져오는 똑똑한 파이썬 함수입니다.
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
 
                # B) 이벤트별 개수 집계
                event_counts[event] = event_counts.get(event, 0) + 1
 
                # C) WARNING 또는 CRITICAL 로그 분류
                # 대소문자 차이로 인한 오류를 방지하기 위해 upper()를 사용하여 대문자로 맞춰 확인합니다.
                if severity.upper() in ["WARNING", "CRITICAL"]:
                    # 분석하기 좋게 딕셔너리 형태로 묶어 저장합니다.
                    warning_or_critical_logs.append({
                        "timestamp": timestamp,
                        "device": device,
                        "severity": severity,
                        "event": event,
                        "message": message
                    })
 
                # D) 주요 키워드 매칭을 통한 이벤트 요약 (CRC_ERROR, LINK_DOWN, TICKET_ESCALATED)
                # event 내용이나 message 내용 안에 특정 단어가 포함되어 있는지 확인합니다.
                
                # 1. CRC_ERROR 감지 (예: 'CRC error 증가' 또는 메시지에 'CRC error')
                if "CRC" in event.upper() or "CRC" in message.upper():
                    major_events["CRC_ERROR"].append({
                        "timestamp": timestamp,
                        "device": device,
                        "event": event,
                        "message": message
                    })
 
                # 2. LINK_DOWN 감지 (예: 'Link Down' 또는 메시지에 'changed to DOWN')
                if "LINK DOWN" in event.upper() or "DOWN" in message.upper():
                    major_events["LINK_DOWN"].append({
                        "timestamp": timestamp,
                        "device": device,
                        "event": event,
                        "message": message
                    })
 
                # 3. TICKET_ESCALATED 감지 (예: 'Ticket escalated' 또는 메시지에 'escalated')
                if "ESCALATED" in event.upper() or "ESCALATED" in message.upper():
                    major_events["TICKET_ESCALATED"].append({
                        "timestamp": timestamp,
                        "device": device,
                        "event": event,
                        "message": message
                    })
 
    # -------------------------------------------------------------
    # 4. 분석 결과를 Markdown(인시던트 요약) 파일로 저장
    # -------------------------------------------------------------
    print(f"진행 중: 분석 결과를 '{OUTPUT_FILE_NAME}'에 작성하고 있습니다...")
 
    with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as out:
        # Markdown 보고서 헤더 작성
        out.write("# 📋 DCO Incident & Log Analysis Summary\n\n")
        out.write("이 보고서는 교육용 샘플 DCO 로그 파일을 바탕으로 Python 분석 스크립트를 실행하여 자동 생성된 결과물입니다.\n")
        out.write("*(본 결과는 실제 인프라 및 장비와 무관한 시뮬레이션 데이터입니다.)*\n\n")
 
        # 1. 전체 로그 요약 통계
        out.write("## 📊 1. 전체 로그 요약 통계\n")
        out.write(f"- **전체 분석 대상 로그 수:** {total_lines} 줄\n\n")
 
        # 2. 심각도별 개수 (표 형태로 출력)
        out.write("## 🛡️ 2. 심각도(Severity)별 집계\n")
        out.write("| 심각도 (Severity) | 로그 수 (Count) |\n")
        out.write("| :--- | :--- |\n")
        # 개수가 많은 순서대로 정렬하여 출력합니다.
        for sev, count in sorted(severity_counts.items(), key=lambda x: x[1], reverse=True):
            out.write(f"| `{sev}` | {count}개 |\n")
        out.write("\n")
 
        # 3. 이벤트별 개수 (표 형태로 출력)
        out.write("## 🔍 3. 이벤트(Event) 유형별 집계 (상위 10개)\n")
        out.write("| 이벤트명 (Event Name) | 발생 횟수 (Count) |\n")
        out.write("| :--- | :--- |\n")
        # 발생 빈도가 높은 순으로 정렬하여 상위 10개만 먼저 노출합니다.
        sorted_events = sorted(event_counts.items(), key=lambda x: x[1], reverse=True)
        for evt, count in sorted_events[:10]:
            out.write(f"| {evt} | {count}개 |\n")
        out.write("\n")
 
        # 4. WARNING 또는 CRITICAL 로그 목록
        out.write("## ⚠️ 4. WARNING 및 CRITICAL 로그 목록\n")
        if not warning_or_critical_logs:
            out.write("- 발생한 WARNING 또는 CRITICAL 로그가 없습니다.\n\n")
        else:
            out.write("| 시간 (Timestamp) | 장비 (Device) | 심각도 | 이벤트명 | 세부 메시지 |\n")
            out.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for log in warning_or_critical_logs:
                out.write(f"| {log['timestamp']} | `{log['device']}` | **{log['severity']}** | {log['event']} | {log['message']} |\n")
            out.write("\n")
 
        # 5. 주요 이슈 유형별 요약 (CRC_ERROR, LINK_DOWN, TICKET_ESCALATED)
        out.write("## 🚀 5. 주요 이슈 유형별 특별 요약\n")
        out.write("네트워크 장애 탐지 및 작업 프로세스 확인에 필수적인 주요 이벤트 필터링 결과입니다.\n\n")
 
        # A) CRC_ERROR 요약
        out.write("### 🔹 A. CRC_ERROR (물리 선로/감쇄 의심 요약)\n")
        if not major_events["CRC_ERROR"]:
            out.write("- 감지된 CRC 에러가 없습니다.\n\n")
        else:
            for item in major_events["CRC_ERROR"]:
                out.write(f"- **시간:** {item['timestamp']} | **장비:** `{item['device']}` | **이벤트:** {item['event']}\n")
                out.write(f"  - *메시지:* {item['message']}\n")
            out.write("\n")
 
        # B) LINK_DOWN 요약
        out.write("### 🔹 B. LINK_DOWN (포트/링크 오프라인 장애 요약)\n")
        if not major_events["LINK_DOWN"]:
            out.write("- 감지된 링크 다운 이벤트가 없습니다.\n\n")
        else:
            for item in major_events["LINK_DOWN"]:
                out.write(f"- **시간:** {item['timestamp']} | **장비:** `{item['device']}` | **이벤트:** {item['event']}\n")
                out.write(f"  - *메시지:* {item['message']}\n")
            out.write("\n")
 
        # C) TICKET_ESCALATED 요약
        out.write("### 🔹 C. TICKET_ESCALATED (티켓 이관 및 에스컬레이션 흐름)\n")
        if not major_events["TICKET_ESCALATED"]:
            out.write("- 이관된 티켓 이벤트가 없습니다.\n\n")
        else:
            for item in major_events["TICKET_ESCALATED"]:
                out.write(f"- **시간:** {item['timestamp']} | **장비:** `{item['device']}` | **이벤트:** {item['event']}\n")
                out.write(f"  - *메시지:* {item['message']}\n")
            out.write("\n")
 
    print(f"성공: '{OUTPUT_FILE_NAME}' 보고서 작성이 완벽하게 완료되었습니다!")
 
 
# 이 파일이 독립적인 스크립트로 실행될 때 분석 함수를 가동합니다.
if __name__ == "__main__":
    analyze_logs()