from fastapi import FastAPI, HTTPException
import uvicorn
from gensim.models import KeyedVectors
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Word2Vec Similarity API",
    description="단어 간 유사도를 계산하는 API",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Word2Vec Similarity API is running", "status": "healthy"}

# 모델 로드 함수
def load_model():
    # 모델 파일 경로 (볼륨 마운트 위치 고려)
    model_paths = [
        '/app/models/GoogleNews-vectors-negative300.bin.gz',  # 볼륨 마운트 경로
        'GoogleNews-vectors-negative300.bin.gz',             # 로컬 개발용 경로
        '/app/GoogleNews-vectors-negative300.bin.gz'         # Dockerfile 내 경로
    ]
    
    # 존재하는 경로 찾기
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if not model_path:
        raise FileNotFoundError("모델 파일을 찾을 수 없습니다. 파일이 올바른 위치에 있는지 확인하세요.")
    
    logger.info(f"모델 로딩 시작: {model_path}")
    try:
        # 이진 형식으로 로드
        model = KeyedVectors.load_word2vec_format(
            model_path,
            binary=True
        )
        logger.info("모델 로딩 완료")
        return model
    except Exception as e:
        logger.error(f"모델 로딩 실패: {str(e)}")
        raise RuntimeError(f"모델 로딩 실패: {str(e)}")

# 모델 로드
try:
    model = load_model()
except Exception as e:
    logger.error(f"애플리케이션 시작 실패: {str(e)}")
    model = None

@app.get("/similarity")
async def similarity(first_word: str, second_word: str):
    if model is None:
        raise HTTPException(status_code=500, detail="모델이 로드되지 않았습니다")
    
    try:
        # 단어가 모델에 있는지 확인
        if first_word not in model or second_word not in model:
            missing_words = []
            if first_word not in model:
                missing_words.append(first_word)
            if second_word not in model:
                missing_words.append(second_word)
            raise HTTPException(
                status_code=404, 
                detail=f"단어를 찾을 수 없습니다: {', '.join(missing_words)}"
            )
            
        similarity_score = model.similarity(first_word, second_word)
        return {"similarity": float(similarity_score)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"유사도 계산 중 오류 발생: {str(e)}")

@app.get("/health")
async def health():
    if model is None:
        raise HTTPException(status_code=500, detail="모델이 로드되지 않았습니다")
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    ) 