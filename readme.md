
# Score Calcurator

카트 점수를 집계하기 위해 만든 것을<br>
다양한 상황에 쓸수있게 바꾸는 프로젝트<br>
Elo 기반 점수 측정으로 객관적인 실력의 정도를 확인 가능<br>
평순 통계 작성이 가능하여 다양한 분석 가능<br>
<br>
현재 이 프로그램의 가장 큰 문제점<br>

- 팀전을 포함할 경우 점수의 객관성이 떨어짐
- 점수 인플레이션이 너무 심하게 일어남

점수 확인 봇을 킬수 있는 bot.py<br>
[카트리그 데이터](https://github.com/KartRanking/KartRanking)를 가져오기 위한 writerecord.py<br>
점수를 계산해주는 ScoreCalcurate.py<br>
ScoreCalcurate.py를 실행해주는 mian.py<br>

## 사용 방법

1. [양식](https://docs.google.com/spreadsheets/d/1ivxhjaQ6Q4Z0Dx1_yf2j5I9GxV3LwQS_Bsn1tPeTrRM/edit#gid=544078275)에 들어가 사본을 만든다.
2. 닉네임과 등수 입력, 킬이 필요한 경우 킬수도 입력
3. [json 키 발급 방법](https://minimilab.tistory.com/37)에서 1~5번을 따라하고 json파일 이름을 **spreadjson.json**으로 바꾸고 exe파일이 있는 폴더로 옮긴다.


무언가에 대해 실력이 좋은지 확인을 할수있는 점수 계산기  
계산된 데이터를 봇으로 볼 수 있다.  

## 개발기간

2021/04 ~ 2021/06

## 사용 언어,프로그램 및 기술
python, visual studio code

## 느낀점

1. 독자적인 점수제를 사용하려 했으나 문제점이 많아 elo를 사용하게 되었다.
2. 편의성을 개선하기 위한 작업이 쉽지 않았다.



