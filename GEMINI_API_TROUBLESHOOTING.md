# 🔍 Gemini API 오류 진단 가이드 (설정 변경 없이 갑자기 발생한 경우)

## 가능한 원인들

설정을 바꾸지 않았는데 갑자기 문제가 생기는 경우, 다음 원인들이 가능합니다:

### 1. 🔑 API 키 만료 또는 비활성화 (가장 흔함)
- Google에서 API 키를 자동으로 비활성화할 수 있음
- API 키 사용 정책 위반 시 비활성화
- 일정 기간 미사용 시 만료

### 2. ⚡ API 사용량 제한 (Rate Limit)
- 무료 플랜: 분당/일일 요청 수 제한
- 갑자기 많은 요청 시 일시적으로 차단
- 429 오류 발생

### 3. 🌐 네트워크/서비스 일시적 문제
- Google Gemini API 서버 일시적 장애
- Streamlit Cloud 네트워크 문제
- 타임아웃 발생

### 4. 🔄 Streamlit Cloud 환경 변수 로드 문제
- Secrets가 일시적으로 로드되지 않음
- 앱 재시작 필요

### 5. 📊 API 키 권한 변경
- Google에서 API 키 권한 변경
- 특정 모델 접근 권한 제한

---

## 진단 방법: Streamlit Cloud 로그 확인

### 1단계: 로그 페이지 접속

**방법 1: 앱에서 직접**
1. 앱 하단의 **"< Manage app"** 링크 클릭
2. 또는 URL에 `/manage` 추가:
   ```
   https://cardnews1-hd646zyxsbzawjaibtjgar.streamlit.app/manage
   ```
3. **"Logs"** 탭 클릭

**방법 2: Streamlit Cloud 대시보드**
1. https://share.streamlit.io/ 접속
2. `cardnews1` 앱 선택
3. **"Manage app"** → **"Logs"** 탭

### 2단계: 카드뉴스 생성 시도 후 로그 확인

1. **로그 페이지를 열어둔 상태에서**
2. **다른 탭에서 앱 열기**
3. **카드뉴스 생성 버튼 클릭**
4. **로그 페이지로 돌아와서 새로고침 (F5)**
5. **다음 메시지들 확인:**

---

## 로그에서 확인할 오류 메시지

### ✅ 정상 작동 시
```
[Gemini 성공] XXX자 생성됨
```

### ❌ 오류 메시지별 원인 및 해결

#### 1. `[Gemini HTTP 오류] 401`
**의미**: API 키가 유효하지 않음
**원인**: 
- API 키가 만료되었거나 비활성화됨
- API 키가 잘못됨

**해결 방법**:
1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. API 키 상태 확인
3. 필요시 새 API 키 생성
4. Streamlit Cloud Secrets에 새 키 업데이트

---

#### 2. `[Gemini HTTP 오류] 429`
**의미**: API 사용량 제한 초과 (Rate Limit)
**원인**: 
- 너무 많은 요청을 짧은 시간에 보냄
- 무료 플랜의 일일/분당 제한 초과

**해결 방법**:
1. **잠시 기다리기** (5-10분)
2. **API 사용량 확인**: Google AI Studio에서 확인
3. **요청 간격 두기**: 연속으로 여러 번 생성하지 않기

---

#### 3. `[Gemini HTTP 오류] 500` 또는 `503`
**의미**: Google 서버 일시적 오류
**원인**: 
- Gemini API 서버 문제
- 일시적 장애

**해결 방법**:
1. **잠시 기다리기** (10-30분)
2. **나중에 다시 시도**
3. [Google Cloud Status](https://status.cloud.google.com/) 확인

---

#### 4. `[Gemini 타임아웃]`
**의미**: 요청이 60초 내에 완료되지 않음
**원인**: 
- 네트워크 지연
- API 서버 응답 지연
- 요청이 너무 복잡함

**해결 방법**:
1. **다시 시도** (자동으로 재시도됨)
2. **네트워크 연결 확인**
3. **나중에 다시 시도**

---

#### 5. `[Gemini 응답 경고] candidates가 비어 있습니다`
**의미**: API는 응답했지만 내용이 없음
**원인**: 
- API가 안전 필터에 걸림
- 응답 생성 실패

**해결 방법**:
1. **다른 기사로 시도**
2. **"새로 생성" 버튼으로 재시도**
3. **프롬프트가 너무 길거나 복잡한 경우 간소화**

---

#### 6. `GEMINI_API_KEY 환경 변수가 설정되지 않았습니다`
**의미**: 환경 변수가 로드되지 않음
**원인**: 
- Streamlit Cloud Secrets가 로드되지 않음
- Secrets 설정 오류

**해결 방법**:
1. **Streamlit Cloud → Settings → Secrets 확인**
2. **`GEMINI_API_KEY`가 올바른 형식인지 확인**
3. **앱 재시작**: Settings → "Reboot app"

---

#### 7. `[오류] 사용 가능한 Gemini 모델을 찾을 수 없습니다`
**의미**: API 키로 모델 목록을 조회할 수 없음
**원인**: 
- API 키 권한 문제
- API 키가 모델 접근 권한이 없음

**해결 방법**:
1. **새 API 키 생성**
2. **Google AI Studio에서 권한 확인**

---

## 빠른 해결 체크리스트

### 즉시 확인 사항
- [ ] Streamlit Cloud 로그에서 정확한 오류 메시지 확인
- [ ] Google AI Studio에서 API 키 상태 확인
- [ ] API 사용량 제한 확인

### 시도해볼 해결 방법
1. **앱 재시작**
   - Streamlit Cloud → Settings → "Reboot app"
   
2. **잠시 기다리기** (Rate Limit인 경우)
   - 5-10분 후 다시 시도
   
3. **새 API 키 생성** (401 오류인 경우)
   - Google AI Studio에서 새 키 생성
   - Streamlit Cloud Secrets 업데이트

4. **다른 기사로 테스트**
   - 특정 기사에서만 문제가 발생할 수 있음

---

## 예방 방법

### 1. API 키 관리
- 정기적으로 API 키 상태 확인
- 여러 API 키를 준비해두기 (백업용)

### 2. 사용량 모니터링
- Google AI Studio에서 사용량 확인
- 일일/월일 제한 확인

### 3. 에러 처리 개선
- 자동 재시도 로직 활용 (이미 구현됨)
- 오류 발생 시 사용자에게 명확한 메시지 표시

---

## 추가 도움

### 로그 확인이 어려운 경우
1. **Streamlit Cloud → Settings → "Reboot app"** 클릭
2. **5분 후 다시 시도**
3. **여전히 안 되면**: 로그를 스크린샷해서 확인

### Google AI Studio 확인
- https://aistudio.google.com/app/apikey
- API 키 목록 확인
- 사용량 및 제한 확인

---

**가장 중요한 것**: Streamlit Cloud 로그에서 정확한 오류 메시지를 확인하는 것입니다!
로그 메시지를 알려주시면 더 정확한 해결 방법을 제시할 수 있습니다.
