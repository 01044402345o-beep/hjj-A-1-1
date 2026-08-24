# git clone 실행 결과

과제 요구사항 "공개 샘플 저장소 1개를 clone으로 내려받아 폴더 구조와 로그를 확인한다"를
수행한 기록입니다.

- 실행일: 2026-08-24
- 대상 저장소: [octocat/Hello-World](https://github.com/octocat/Hello-World) (GitHub 공식 샘플 저장소)
- 실행 위치: `C:\Test`

`clone`은 커밋 히스토리에 흔적을 남기지 않으므로, 터미널 출력을 이 문서에 기록합니다.

## 1. 저장소 내려받기

```powershell
cd C:\Test
git clone https://github.com/octocat/Hello-World.git clone-test
```

```
Cloning into 'clone-test'...
remote: Enumerating objects: 13, done.
remote: Total 13 (delta 0), reused 0 (delta 0), pack-reused 13 (from 1)
Receiving objects: 100% (13/13), done.
```

객체 13개를 모두 받아왔습니다.

## 2. 폴더 구조 확인

```powershell
cd clone-test
Get-ChildItem -Force
```

```
.
..
.git
README
```

`README` 파일 하나와 **`.git` 폴더**가 있습니다. `.git`이 함께 있다는 점이 중요합니다.
GitHub에서 ZIP으로 내려받으면 파일만 오지만, `clone`은 **커밋 히스토리 전체를 통째로**
복제하기 때문에 `.git` 폴더가 따라옵니다. 그래서 받은 직후부터 `git log`, `git checkout`
같은 명령을 그대로 쓸 수 있습니다.

## 3. 커밋 로그 확인

```powershell
git log --oneline --graph
```

```
*   7fd1a60 Merge pull request #6 from Spaceghost/patch-1
|\
| * 7629413 New line at end of file. --Signed off by Spaceghost
|/
* 553c207 first commit
```

커밋 3개와 병합 기록 1개가 보입니다. 남이 만든 저장소의 이력도 그대로 확인할 수
있습니다. 이 저장소도 `|\ … |/` 갈래가 있는데, 이 프로젝트에서 `--no-ff`로 만든 병합
기록과 같은 모양입니다.

## 4. 원격 주소 확인

```powershell
git remote -v
```

```
origin  https://github.com/octocat/Hello-World.git (fetch)
origin  https://github.com/octocat/Hello-World.git (push)
```

`clone`을 하면 받아온 주소가 `origin`이라는 이름으로 **자동 등록**됩니다. 이 프로젝트를
처음 만들 때는 `git remote add origin ...`을 직접 입력해야 했지만, `clone`은 그 과정이
필요 없습니다.

## 5. 브랜치 확인

```powershell
git branch -a
```

```
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/octocat-patch-1
  remotes/origin/test
```

원격 브랜치 목록까지 함께 받아옵니다. 이 저장소의 기본 브랜치는 `master`인데, 요즘
새로 만드는 저장소는 `main`을 기본값으로 씁니다. 이 프로젝트도 `main`을 씁니다.

## 6. 정리

확인을 마친 뒤 삭제했습니다.

```powershell
cd C:\Test
Remove-Item -Recurse -Force clone-test
```

## 정리하며 — clone으로 알게 된 것

| 항목 | 내용 |
|---|---|
| 무엇을 받나 | 파일뿐 아니라 `.git` 폴더(커밋 히스토리 전체)까지 |
| `origin` | 자동으로 등록됨. `remote add`를 따로 안 해도 됨 |
| 브랜치 | 원격 브랜치 목록도 함께 따라옴 |
| ZIP 다운로드와 차이 | ZIP은 특정 시점의 파일 스냅샷뿐, `clone`은 이력 전체 |
| 언제 쓰나 | 남의 저장소를 받아올 때, 다른 PC에서 내 저장소를 이어서 작업할 때 |
