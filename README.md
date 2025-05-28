# snap-it-word2vec

Snap-it 서비스의 단어 유사도를 파악하는 word2vec 모델 FastAPI 리포지토리입니다.

## 프로젝트 개요

이 프로젝트는 word2vec 모델을 사용하여 단어 간 유사도를 분석하고 API로 제공합니다. FastAPI 프레임워크를 사용하여 구현되었으며, Kubernetes 환경에서 실행됩니다.

## 배포 정보

- **네임스페이스**: `snapit-word2voc`
- **이미지 저장소**: `ghcr.io/chabinhwang/snap-it-word2vec`
- **리소스 제한**:
  - CPU: 1000m (1 코어)
  - 메모리: 5120Mi (5GB)

## 모델 파일 정보

이 서비스는 Google의 pre-trained Word2Vec 모델(`GoogleNews-vectors-negative300.bin.gz`)을 사용합니다. 모델 파일은 Kubernetes Persistent Volume을 통해 제공됩니다.

- **모델 경로**: `/mnt/data/models/GoogleNews-vectors-negative300.bin.gz`
- **모델 크기**: 약 1.5GB

## 개발 환경 설정

### 필수 요구사항
- Python 3.8 이상
- Docker
- Kubernetes (로컬 개발 시 minikube 등)

### 로컬 실행 방법
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 모델 파일이 로컬에 없는 경우
# 아래 경로에 모델 파일을 준비하세요 (필요한 경우에만)
# wget -O GoogleNews-vectors-negative300.bin.gz https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz

# 서버 실행
python main.py
```

## 엔드포인트

- `GET /`: 서버 상태 확인
- `GET /health`: 헬스 체크 엔드포인트
- `GET /similarity?first_word=apple&second_word=orange`: 두 단어 간의 유사도 계산

## Kubernetes 배포

1. PV에 모델 파일이 있는지 확인:
```bash
# 호스트 노드에서
ls -l /mnt/data/models/GoogleNews-vectors-negative300.bin.gz
```

2. 네임스페이스와 PV/PVC 생성:
```bash
kubectl create namespace snapit-word2voc
kubectl apply -f snap-it-word2vec-manifest/templates/pv.yaml
```

3. 배포 적용:
```bash
kubectl apply -f snap-it-word2vec-manifest/templates/deployment.yaml
kubectl apply -f snap-it-word2vec-manifest/templates/service.yaml
```

## CI/CD 파이프라인

`main` 브랜치에 코드를 푸시하면 GitHub Actions 워크플로우가 자동으로 실행되어 다음 작업을 수행합니다:

1. 소스 코드 테스트
2. Docker 이미지 빌드 및 GitHub Container Registry에 푸시
3. Kubernetes 매니페스트 업데이트

자세한 배포 정보는 [snap-it-word2vec-manifest](https://github.com/chabinhwang/snap-it-word2vec-manifest) 저장소를 참조하세요.
