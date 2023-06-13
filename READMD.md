# 아그리콜라 프로젝트 티모 백엔드

## 개발 환경 설정 (데이터베이스 서버 설정)

```shell
docker-compose up
virtualenv .venv -p python3.10
source .venv/bin/activate
```

## 환경 설명

### 만약, 별다른 설정 없이 게임을 즐기고 싶다면

cards/app.py 단에 존재하는 코드의 주석들을 모두 풀고

```shell
source .venv/bin/activate
daphne -b 0.0.0.0 -p 8000 agricola.asgi:application
```

를 실행시키면 됩니다.

### 만약, 방 생성 로직 없이 빠르게 게임을 만들고 싶다면

cards/app.py 단에 존재하는 코드의 주석들을 유지 시킨채로

```shell
source .venv/bin/activate
python3 main.py
daphne -b 0.0.0.0 -p 8000 agricola.asgi:application
```

### 만약, 시연 환경에서 제공된 상태로 게임을 진행하고 싶다면

cards/app.py 단에 존재하는 코드의 주석들을 유지 시킨채로

```shell
source .venv/bin/activate
python3 test.py
daphne -b 0.0.0.0 -p 8000 agricola.asgi:application
```

## 전체 서비스 실행

```shell
sh start.sh
```