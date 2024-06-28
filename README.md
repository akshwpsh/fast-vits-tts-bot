사용법

1.https://github.com/Plachtaa/VITS-fast-fine-tuning.git 클론하기
2. 클론한 폴더 이름 fast_vits로 변경
3. pip install -r requirements.txt
4. pastes안에 코드를 fast_vits 폴더 안에 붙여넣기(덮어쓰기)

5. 루트 폴더 위치에서
mkdir output
mkdir vits_models
mkdir vits_models/configs
mkdir vits_models/models

6. bot_config.json 생성
{
    "Token" : "your token",
    "Prefix" : "!"
}
