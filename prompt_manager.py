"""나만의 프롬프트 관리 프로그램

GenAI 프롬프트를 카테고리별로 정리하고 검색·즐겨찾기할 수 있는 콘솔 프로그램입니다.
"""

import json
import os
import sys

# Windows 콘솔의 기본 인코딩(cp949)에서는 별표(⭐) 출력이 오류를 일으킨다.
# 표준 출력을 UTF-8로 다시 설정해 어떤 터미널에서도 깨지지 않게 한다.
sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------- 상수

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "prompts.json")
EXPORT_DIR = "export"

CATEGORIES = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타",
]

# ------------------------------------------------------- 기본 프롬프트

DEFAULT_PROMPTS = [
    {
        "title": "블로그 글 작성 도우미",
        "content": (
            "당신은 10년 경력의 전문 블로거입니다.\n"
            "주어진 주제에 대해 SEO에 최적화된 블로그 글을 작성해주세요.\n"
            "서론, 본론, 결론 구조를 갖추고 소제목을 3개 이상 넣어주세요.\n"
            "독자의 관심을 끄는 제목을 3개 제안하고, 각 제목의 선택 이유를 한 줄로 설명해주세요."
        ),
        "category": "텍스트 생성",
        "favorite": True,
    },
    {
        "title": "제품 썸네일 생성",
        "content": (
            "다음 제품의 매력적인 썸네일 이미지를 생성해주세요.\n"
            "제품: {제품명}\n"
            "스타일: 미니멀, 스튜디오 조명, 흰색 배경\n"
            "구도: 정면 45도, 제품이 프레임의 70%를 차지\n"
            "비율: 1:1, 텍스트 없음, 사실적인 질감"
        ),
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "숏폼 광고 스크립트 작성",
        "content": (
            "15초 분량의 숏폼 광고 영상 스크립트를 작성해주세요.\n"
            "제품: {제품명}\n"
            "타깃: {타깃 고객}\n"
            "장면별로 화면 구성, 자막, 나레이션을 표로 정리해주세요.\n"
            "첫 3초 안에 시청자의 이탈을 막을 후킹 문장을 반드시 포함해주세요."
        ),
        "category": "영상 생성",
        "favorite": False,
    },
    {
        "title": "IT 컨설턴트 페르소나",
        "content": (
            "당신은 중소기업의 디지털 전환을 15년간 자문해온 IT 컨설턴트입니다.\n"
            "전문 용어는 반드시 비유를 들어 풀어서 설명하고,\n"
            "제안할 때는 항상 비용·기간·리스크를 함께 제시합니다.\n"
            "확신이 없는 부분은 추측하지 않고 '확인이 필요하다'고 명확히 말합니다."
        ),
        "category": "페르소나",
        "favorite": False,
    },
    {
        "title": "뉴스 요약 자동화 프롬프트",
        "content": (
            "아래 뉴스 기사 본문을 다음 형식으로 요약해주세요.\n"
            "1) 한 줄 요약\n"
            "2) 핵심 사실 3가지 (각 30자 이내)\n"
            "3) 이 소식이 우리 업계에 미치는 영향 2줄\n"
            "출력은 JSON 형식으로만 반환하고 다른 설명은 붙이지 마세요.\n"
            "기사 본문: {본문}"
        ),
        "category": "자동화",
        "favorite": False,
    },
    {
        "title": "프롬프트 품질 점검 체크리스트",
        "content": (
            "아래 프롬프트를 검토하고 개선안을 제시해주세요.\n"
            "점검 항목: 역할 부여, 목표 명확성, 출력 형식 지정, 제약 조건, 예시 포함 여부\n"
            "각 항목을 O/X로 평가한 뒤, X인 항목을 반영한 개선 프롬프트를 다시 작성해주세요.\n"
            "원본 프롬프트: {프롬프트}"
        ),
        "category": "기타",
        "favorite": False,
    },
]

# ------------------------------------------------------------ 화면 출력

def show_menu():
    """메뉴를 출력한다."""
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("8. JSON 파일로 저장")
    print("9. JSON 파일에서 불러오기")
    print("10. Markdown으로 내보내기")
    print("0. 종료")


# ------------------------------------------------------------ 입력 헬퍼

def input_nonempty(label):
    """빈 값이 아닐 때까지 입력을 받는다."""
    while True:
        value = input(label).strip()
        if value:
            return value
        print("값을 입력해주세요.")


def choose_category():
    """카테고리를 목록에서 고르거나 직접 입력받는다."""
    print("\n카테고리 선택:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}) {category}")
    print("0) 직접 입력")

    while True:
        choice = input("선택: ").strip()
        if choice == "0":
            return input_nonempty("카테고리 직접 입력: ")
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("올바른 번호를 입력해주세요.")


# ------------------------------------------------------------ 기능 함수

def add_prompt(prompts):
    """새 프롬프트를 등록한다."""
    print("\n=== 프롬프트 추가 ===")
    title = input_nonempty("제목: ")
    content = input_nonempty("내용: ")
    category = choose_category()

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
    })
    print("\n프롬프트가 추가되었습니다!")


# ------------------------------------------------------------- 진입점

def main():
    """메뉴 루프를 실행한다."""
    prompts = [dict(prompt) for prompt in DEFAULT_PROMPTS]
    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        elif choice == "1":
            add_prompt(prompts)
        elif choice in {"2", "3", "4", "5", "6", "7", "8", "9", "10"}:
            print(f"(아직 구현되지 않은 기능입니다: {choice})")
        else:
            print("올바른 번호를 입력해주세요.")


if __name__ == "__main__":
    main()
