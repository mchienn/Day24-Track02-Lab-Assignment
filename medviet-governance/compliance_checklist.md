# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [ ] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [ ] Backup cũng phải ở trong lãnh thổ VN
- [ ] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [ ] Thu thập consent trước khi dùng data cho AI training
- [ ] Có mechanism để user rút consent (Right to Erasure)
- [ ] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [ ] Có incident response plan
- [ ] Alert tự động khi phát hiện breach
- [ ] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [ ] Đã bổ nhiệm Data Protection Officer
- [ ] DPO có thể liên hệ tại: ___

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest, TLS 1.3 in transit | 🚧 In Progress | Infra Team |
| Audit logging | CloudTrail + API access logs | ⬜ Todo | Platform Team |
| Breach detection | Anomaly monitoring (Prometheus) | ⬜ Todo | Security Team |

## F. Technical Solutions for Todo Items

### Audit logging
Implement centralized audit logging using AWS CloudTrail for infrastructure-level API calls combined with application-level structured logging via FastAPI middleware. Each access to patient data will log: user_id, action, resource, timestamp, IP address, and outcome (allow/deny). Logs will be stored in immutable S3 bucket with 1-year retention and integrated with SIEM for alerting.

### Breach detection
Deploy Prometheus + Grafana monitoring stack with custom alert rules:
- Monitor API request patterns (unusual spike in 403 errors → potential scanning)
- Track data export volume anomalies (sudden large CSV downloads)
- Set up Prometheus AlertManager for real-time notifications via PagerDuty/Slack
- Integrate with OPA for runtime access pattern analysis
- Implement 72-hour breach notification workflow: detection → containment → forensic analysis → regulatory reporting
