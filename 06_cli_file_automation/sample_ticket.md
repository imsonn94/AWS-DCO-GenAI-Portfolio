# [교육용 샘플 데이터 사용]

## 1. 티켓 정보 (Ticket Information)
- **티켓 ID**: EDU-TICKET-SAMPLE-0001
- **발생 시간 (Event Time)**: 2026-07-07 15:10:00 KST (EDU_TIME)
- **샘플 장비명 (Target Device)**: SAMPLE_TOR_SW_01
- **이벤트명 (Event)**: CRC Error Increase followed by Link Down
- **심각도 (Severity)**: SEV-2 (Major Impact - 교육용 설정)

## 2. 관찰 내용 (Observations)
- **상세 관찰 로그 및 내용**:
  - `SAMPLE_TOR_SW_01` 장비의 `Ethernet1/1` 인터페이스에서 CRC 에러 카운터가 급격히 증가하는 현상이 감지됨.
  - CRC 에러 수치가 임계치(10,000/min)를 초과한 후 약 5분 뒤 해당 포트가 `Link Down (Protocol Down)` 상태로 전환됨.
  - 물리 계층(Physical Layer) 또는 케이블 접촉 불량(EDU_CABLE_ISSUE)의 가능성이 있음.
  - 인접한 샘플 서버(SAMPLE_SRV_01)와의 통신이 단절된 상태임.

## 3. 에스컬레이션 필요 여부 (Escalation Required)
- **필요 여부**: YES
- **에스컬레이션 대상**: EDU_DCO_L2_SUPPORT (교육용 인프라 운영 2차 조직)
- **이유**: 물리적 케이블 상태 점검 및 커넥터 재장착(Reseat) 또는 샘플 부품 교체 검토가 필요함.

## 4. 보안 주의사항 (Security Precautions)
> [!IMPORTANT]
> 본 티켓은 교육용 실습 데이터로 작성되었습니다.
> - 실제 운영 환경의 IP 주소, 장비 시리얼 넘버, 계정 정보 및 고객 개인정보를 본 티켓에 절대 기재하지 마십시오.
> - 모든 IP 주소 및 시스템 명칭은 `SAMPLE` 및 `EDU` 접두어가 적용된 가상 데이터를 사용해야 합니다.
