# 컴룸닷넷

> 학교 컴퓨터실(특별실) 예약관리 사이트

http://comroom.net  

컴퓨터실(특별실) 사용 예약을 할 수 있는 사이트입니다. 

## 함께 개발하실 분을 찾습니다.

- 전국 초등학교에서 사용하는 사이트를 함께 개발해 나가실 선생님(혹은 개발자)을 찾습니다!
- 개발을 잘 못하셔도, 웹 개발이 처음이어도 상관없습니다. 파이썬을 해보셨다면 공부하면서 기여할 수 있는 부분만 기여해주셔도 충분합니다!
- 비영리 사이트이기 때문에 수익이 없고, 보수도 드리지 못합니다. 다만, 기여를 전혀하지 않고, 질문만 하시는 분도 환영합니다! 공부를 위해, 혹은 단순한 호기심에라도 함께 해주신다면 환영입니다!

## 개발 일지

- [데이터베이스(DB) 구조 - ERD](https://ssamko.tistory.com/2)  
- [로그인 페이지 - 한 페이지에서 여러 개의 Form 다루기](https://ssamko.tistory.com/4)  
- [회원가입 페이지 - Django에서 하나의 폼으로 여러 테이블에 데이터 작성하기 | transaction.atomic](https://ssamko.tistory.com/5)


## API

[api apecification](http://api.comroom.net/api/schema/swagger-ui)

## Project structure

- afterschool(개발중)
    - 방과후신청을 위한 APP. 
- common
    - 다양한, 일반적인 용도로 사용되는 APP
- dev
    - 컴룸닷넷 개발과 관련된 내용들을 보여주기 위한 APP
- etc
    - 기타 컴룸닷넷에 포함된 간단한 앱들
- school
    - 학교와 관련된 것들을 다루는 APP
    - 가입, 관리자 화면 등
    - TODO: 과거에 사용했던 페이지 렌더링을 위한 view함수들 정리
- timetable
    - 시간표와 관련된 것들을 다루는 APP
