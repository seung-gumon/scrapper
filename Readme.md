# 크롤링 대상의 조건

설치 커맨드

# pip3 install {Pacakge name}

크롤링을 진행할 때, 다음의 조건들을 만족해야 합니다:

# Bucket Folder 규칙

face book (killing Time) 의 folder name 은
f_1입니다.

현재 그 외에는 cum (커뮤니티) 입니다.

1. **비디오 제외:** 크롤링한 포스트에는 비디오가 포함되어 있으면 안됩니다.
2. **속성 제거:** 포스트에서 `id`, `style`, `class` 속성들을 모두 지워야 합니다.

# 2024 04 29

Id 를 만드는데에는 규칙이 있다.
2404290113kil-97a8 라면
년월일시분(커뮤니티 3글자)-uuid.slice(0,4) 입니다.
