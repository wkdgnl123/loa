# League of Artists


## 설치

- 아래 명령어를 순서대로 입력하여 설치할 수 있습니다.
- `pyyaml`은 Python 표준 라이브러리에 포함되지 않은 외부 라이브러리이기 때문에 설치를 해주시기 바랍니다.

```bash
conda install pyyaml
git clone https://github.com/daew0n/loa.git loa
cd loa
python setup.py develop
```

- `python setup.py install`이 아닌 `python setup.py develop`으로 설치하는 이유는 최신 버전의 `loa` 패키지를 `git pull` 명령어만으로 업데이트하기 위해서입니다.
- `python setup.py install`로 설치하시는 경우, `loa` 패키지를 업데이트 할 때마다 `python setup.py install`을 매번 실행해야 합니다.


## 예시 및 테스트

- [`loa/examples`](loa/examples) 디렉토리에는 `loa.Unit`과 `loa.Team` 클래스를 상속하여 나만의 유닛과 팀을 정의하는 방법과, `loa.Simulator`를 사용하는 방법에 대한 예시가 있습니다.
- `loa.TeamExaminer`의 `check` 함수를 이용하여, `loa.Team` 클래스의 파생 클래스를 제대로 작성하였는지 확인할 수 있습니다.
