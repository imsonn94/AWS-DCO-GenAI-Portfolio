import os

# 1. 파일 경로 설정
# 교육용 샘플 폴더 구조에 맞춰 경로를 지정합니다.
input_file_path = './sample_dco_log.txt'
output_file_path = './incident_summary-02.md'

def analyze_dco_log():
    # 결과를 담을 변수들을 준비합니다.
    total_lines = 0
    severity_counts = {}
    event_counts = {}
    high_severity_logs = []
    key_events_summary = []

    # 파일이 있는지 먼저 확인합니다.
    if not os.path.exists(input_file_path):
        print(f"오류: {input_file_path} 파일을 찾을 수 없습니다.")
        return

    # 2. 파일 읽기 및 분석
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line: continue  # 빈 줄은 건너뜁니다.
            
            total_lines += 1
            
            # 로그 형식: 날짜 | 장비 | 심각도 | 이벤트 | 메시지
            # '|' 기호를 기준으로 데이터를 나눕니다.
            parts = [p.strip() for p in line.split('|')]
            
            if len(parts) < 5: continue # 형식이 맞지 않는 줄은 건너뜁니다.
            
            timestamp, device, severity, event, message = parts

            # [심각도별 개수 세기]
            # dictionary를 사용하여 각 심각도가 몇 번 나오는지 계산합니다.
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

            # [이벤트별 개수 세기]
            event_counts[event] = event_counts.get(event, 0) + 1

            # [WARNING 또는 ERROR(CRITICAL) 로그 따로 모으기]
            if severity in ['WARNING', 'ERROR', 'CRITICAL']:
                high_severity_logs.append(f"- [{timestamp}] {device}: {event} - {message}")

            # [주요 키워드 이벤트 요약]
            # CRC error, Link Down, Ticket escalated 키워드가 포함되어 있는지 확인합니다.
            upper_event = event.upper()
            if "CRC ERROR" in upper_event or "LINK DOWN" in upper_event or "TICKET ESCALATED" in upper_event:
                key_events_summary.append(f"| {timestamp} | {device} | {event} | {message} |")

    # 3. 결과 리포트 작성 (마크다운 형식)
    markdown_content = []
    markdown_content.append("# 📋 DCO 로그 분석 보고서\n")
    
    markdown_content.append("## 1. 전체 현황")
    markdown_content.append(f"- **총 로그 수:** {total_lines} 줄\n")

    markdown_content.append("## 2. 심각도별 통계")
    for sev, count in severity_counts.items():
        markdown_content.append(f"- **{sev}:** {count}건")
    markdown_content.append("")

    markdown_content.append("## 3. 이벤트별 통계 (상위 5개)")
    # 이벤트 개수가 많은 순서대로 정렬하여 상위 5개만 보여줍니다.
    sorted_events = sorted(event_counts.items(), key=lambda x: x[1], reverse=True)
    for evt, count in sorted_events[:5]:
        markdown_content.append(f"- {evt}: {count}건")
    markdown_content.append("")

    markdown_content.append("## 4. 주의 필요 로그 (WARNING/ERROR)")
    if high_severity_logs:
        markdown_content.extend(high_severity_logs)
    else:
        markdown_content.append("- 특이 사항 없음")
    markdown_content.append("")

    markdown_content.append("## 5. 주요 인시던트 요약 (Network/Ticket)")
    markdown_content.append("| 시간 | 장비명 | 이벤트 | 상세 메시지 |")
    markdown_content.append("| :--- | :--- | :--- | :--- |")
    if key_events_summary:
        markdown_content.extend(key_events_summary)
    else:
        markdown_content.append("| - | - | - | 데이터 없음 |")

    # 4. 파일 저장
    # 폴더가 없다면 생성합니다.
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        out_file.write("\n".join(markdown_content))

    print(f"분석이 완료되었습니다! 결과 파일: {output_file_path}")

if __name__ == "__main__":
    analyze_dco_log()