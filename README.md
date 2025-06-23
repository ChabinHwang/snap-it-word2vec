# Snap-It Word2Vec API 서비스

Snap-it 서비스를 위한 단어 유사도 분석 API입니다. Google News 데이터셋으로 학습된 Word2Vec 모델을 활용하여 두 단어 간의 의미적 유사도를 계산합니다.

## 🚀 주요 기능

- **단어 유사도 계산**: 두 단어 간의 코사인 유사도 측정 (0.0 ~ 1.0)
- **FastAPI 기반**: 고성능 웹 API 프레임워크 사용
- **프로덕션 Ready**: Health check, readiness/liveness probe 지원
- **Kubernetes 배포**: 컨테이너화된 환경에서 안정적 운영
- **대용량 모델 지원**: Persistent Volume을 통한 효율적 모델 관리

## 📋 API 엔드포인트

| 엔드포인트 | 메서드 | 설명 | 예시 |
|------------|---------|------|------|
| `/` | GET | 서비스 상태 확인 | - |
| `/health` | GET | 헬스 체크 (모델 로드 상태 포함) | - |
| `/similarity` | GET | 두 단어 간 유사도 계산 | `?first_word=apple&second_word=orange` |

### API 응답 예시

```json
// GET /similarity?first_word=king&second_word=queen
{
  "similarity": 0.6510956883430481
}

// 단어를 찾을 수 없는 경우
{
  "similarity": 0.0
}
```

## 🛠️ 기술 스택

- **Python 3.9**: 기본 런타임
- **FastAPI 0.104.1**: 웹 API 프레임워크
- **Gensim 4.3.3**: Word2Vec 모델 처리
- **Uvicorn**: ASGI 서버
- **Google News Word2Vec**: 사전 훈련된 모델 (300차원, 3백만 단어)

## 🔧 로컬 개발 환경 설정

### 필수 요구사항
- Python 3.8 이상
- 최소 6GB RAM (모델 로딩용)
- 약 2GB 디스크 공간

### 설치 및 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 모델 파일 다운로드 (약 1.5GB)
wget -O GoogleNews-vectors-negative300.bin.gz \
  https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz

# 서버 실행
python main.py
```

서버가 시작되면 http://localhost:8000 에서 접근 가능합니다.

### API 테스트

```bash
# 기본 상태 확인
curl http://localhost:8000/

# 헬스 체크
curl http://localhost:8000/health

# 단어 유사도 계산
curl "http://localhost:8000/similarity?first_word=king&second_word=queen"
```

## 🐳 Docker 실행

```bash
# 이미지 빌드
docker build -t snap-it-word2vec .

# 컨테이너 실행 (모델 파일이 현재 디렉터리에 있는 경우)
docker run -p 8000:8000 \
  -v $(pwd)/GoogleNews-vectors-negative300.bin.gz:/app/models/GoogleNews-vectors-negative300.bin.gz:ro \
  snap-it-word2vec
```

## ☸️ Kubernetes 배포

### 1. 네임스페이스 및 모델 파일 준비

```bash
# 네임스페이스 생성
kubectl create namespace snapit-word2voc

# 호스트에 모델 파일 준비
sudo mkdir -p /mnt/data/models
sudo wget -O /mnt/data/models/GoogleNews-vectors-negative300.bin.gz \
  https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
sudo chmod 644 /mnt/data/models/GoogleNews-vectors-negative300.bin.gz
```

### 2. 매니페스트 배포

```bash
# PV/PVC 생성
kubectl apply -f ../snap-it-word2vec-manifest/templates/pv.yaml

# 서비스 배포
kubectl apply -f ../snap-it-word2vec-manifest/templates/deployment.yaml
kubectl apply -f ../snap-it-word2vec-manifest/templates/service.yaml
```

### 3. 배포 확인

```bash
# 파드 상태 확인
kubectl get pods -n snapit-word2voc

# 서비스 접근
kubectl get svc -n snapit-word2voc
```

## 📊 리소스 요구사항

| 구분 | 최소 | 권장 | 프로덕션 |
|------|------|------|----------|
| CPU | 500m | 1000m | 1500m |
| Memory | 4GB | 5GB | 5GB |
| Storage | 2GB | 3GB | 5GB |

## 🔍 모니터링 및 문제 해결

### 로그 확인
```bash
# 파드 로그 확인
kubectl logs -f deployment/snap-it-word2vec -n snapit-word2voc

# 모델 로딩 상태 확인
kubectl exec -it <pod-name> -n snapit-word2voc -- ls -la /app/models/
```

### 일반적인 문제

1. **모델 로딩 실패**
   - 메모리 부족: 최소 4GB RAM 필요
   - 파일 누락: 모델 파일 경로 확인

2. **성능 이슈**
   - 첫 번째 요청 시 모델 로딩으로 인한 지연 (30-60초)
   - CPU 사용량 증가 시 리소스 제한 조정

## 📚 관련 문서

- [모델 설정 가이드](./README_MODEL_SETUP.md)
- [Kubernetes 매니페스트](../snap-it-word2vec-manifest/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Gensim Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.
