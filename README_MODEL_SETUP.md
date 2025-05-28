# Word2Vec 모델 파일 설정 안내서

## 개요

snap-it-word2vec 서비스는 Google의 News 데이터셋으로 학습된 Word2Vec 모델을 사용합니다. 이 모델 파일(`GoogleNews-vectors-negative300.bin.gz`)은 약 1.5GB 크기로, 대용량이기 때문에 GitHub에 직접 업로드하지 않고 별도로 관리합니다.

## 모델 파일 준비 (Persistent Volume 방식)

### 1. 호스트 시스템에 디렉토리 생성
```bash
sudo mkdir -p /mnt/data/models
sudo chmod 755 /mnt/data/models
```

### 2. 모델 파일 다운로드 및 복사
```bash
# 옵션 1: 직접 다운로드
sudo wget -O /mnt/data/models/GoogleNews-vectors-negative300.bin.gz https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz

# 옵션 2: 로컬에서 다운로드 후 복사
wget -O GoogleNews-vectors-negative300.bin.gz https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
sudo cp GoogleNews-vectors-negative300.bin.gz /mnt/data/models/
```

### 3. 파일 권한 설정
```bash
sudo chmod 644 /mnt/data/models/GoogleNews-vectors-negative300.bin.gz
```

### 4. PV/PVC 생성
```bash
kubectl apply -f snap-it-word2vec-manifest/templates/pv.yaml
```

### 5. 배포 적용
```bash
kubectl apply -f snap-it-word2vec-manifest/templates/deployment.yaml
kubectl apply -f snap-it-word2vec-manifest/templates/service.yaml
```

## 모델 파일 대체 다운로드 소스

공식 링크가 작동하지 않는 경우, 다음 대체 소스를 사용할 수 있습니다:
- [Kaggle Dataset](https://www.kaggle.com/datasets/leadbest/googlenewsvectorsnegative300)
- [Hugging Face](https://huggingface.co/fse/word2vec-google-news-300)

## 문제 해결

1. 모델 파일이 로드되지 않는 경우:
   - 파일 경로 확인: `kubectl exec -it <pod-name> -n snapit-word2voc -- ls -la /app/models`
   - 권한 확인: `kubectl exec -it <pod-name> -n snapit-word2voc -- ls -la /mnt/data/models`

2. 볼륨 마운트 문제:
   - 이벤트 확인: `kubectl get events -n snapit-word2voc`
   - PV/PVC 상태 확인: `kubectl get pv,pvc -n snapit-word2voc`
   - 파드 로그 확인: `kubectl logs <pod-name> -n snapit-word2voc` 