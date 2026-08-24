"""나만의 프롬프트 관리 프로그램

GenAI 프롬프트를 카테고리별로 정리하고 검색·즐겨찾기할 수 있는 콘솔 프로그램입니다.
"""

import json
import os
import sys

# Windows 콘솔의 기본 인코딩(cp949)에서는 별표(⭐) 출력이 오류를 일으키고,
# 파이프로 넘어온 한글 입력도 깨진다. 입출력을 모두 UTF-8로 다시 설정한다.
sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

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

# ------------------------------------------------------- 순수 필터 함수

def filter_by_category(prompts, category):
    """지정한 카테고리의 프롬프트만 원래 순서대로 반환한다."""
    return [prompt for prompt in prompts if prompt["category"] == category]


def filter_by_keyword(prompts, keyword):
    """제목 또는 내용에 키워드가 포함된 프롬프트를 반환한다 (대소문자 무시)."""
    key = keyword.strip().lower()
    if not key:
        return []
    return [
        prompt
        for prompt in prompts
        if key in prompt["title"].lower() or key in prompt["content"].lower()
    ]


def filter_favorites(prompts):
    """즐겨찾기로 지정된 프롬프트만 반환한다."""
    return [prompt for prompt in prompts if prompt["favorite"]]


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


def star(prompt):
    """즐겨찾기면 별 표시를 반환한다."""
    return " ⭐" if prompt["favorite"] else ""


def print_prompt_line(number, prompt):
    """프롬프트 한 줄을 '번호. [카테고리] 제목 ⭐' 형식으로 출력한다."""
    print(f"{number}. [{prompt['category']}] {prompt['title']}{star(prompt)}")


def print_prompt_list(items, empty_message):
    """프롬프트 목록과 총 개수를 출력한다."""
    if not items:
        print(empty_message)
        return
    for number, prompt in enumerate(items, start=1):
        print_prompt_line(number, prompt)
    print(f"\n총 {len(items)}개의 프롬프트")


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


def pick_prompt_index(prompts):
    """프롬프트 번호를 입력받아 0부터 시작하는 인덱스로 변환한다.

    잘못된 입력이면 안내 메시지를 출력하고 None을 반환한다.
    """
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return None

    choice = input("번호 입력: ").strip()
    if not choice.isdigit():
        print("숫자를 입력해주세요.")
        return None

    index = int(choice) - 1
    if not 0 <= index < len(prompts):
        print("존재하지 않는 번호입니다.")
        return None

    return index


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


def show_list(prompts):
    """저장된 모든 프롬프트를 출력한다."""
    print("\n=== 프롬프트 목록 ===")
    print_prompt_list(prompts, "등록된 프롬프트가 없습니다.")


def show_by_category(prompts):
    """카테고리를 선택받아 해당 프롬프트만 출력한다."""
    print("\n=== 카테고리별 조회 ===")
    category = choose_category()
    items = filter_by_category(prompts, category)

    print(f"\n[{category}] 카테고리 프롬프트:")
    print_prompt_list(items, "해당 카테고리에 등록된 프롬프트가 없습니다.")


def search_prompt(prompts):
    """키워드로 프롬프트를 검색한다."""
    print("\n=== 프롬프트 검색 ===")
    keyword = input_nonempty("검색어: ")
    items = filter_by_keyword(prompts, keyword)

    if not items:
        print("\n검색 결과가 없습니다.")
        return

    print("\n검색 결과:")
    for number, prompt in enumerate(items, start=1):
        print_prompt_line(number, prompt)
    print(f"\n{len(items)}개의 프롬프트를 찾았습니다.")


def show_detail(prompts):
    """프롬프트 하나의 전체 내용을 출력한다."""
    print("\n=== 프롬프트 상세 보기 ===")
    index = pick_prompt_index(prompts)
    if index is None:
        return

    prompt = prompts[index]
    line = "─" * 30
    print(f"\n{line}")
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '없음'}")
    print(line)
    print("내용:")
    print(prompt["content"])
    print(line)


def toggle_favorite(prompts):
    """프롬프트의 즐겨찾기 상태를 반전시킨다."""
    print("\n=== 즐겨찾기 관리 ===")
    print("(번호는 '프롬프트 목록' 기준입니다)")
    index = pick_prompt_index(prompts)
    if index is None:
        return

    prompt = prompts[index]
    prompt["favorite"] = not prompt["favorite"]

    if prompt["favorite"]:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다!")
    else:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다.")


def show_favorites(prompts):
    """즐겨찾기된 프롬프트만 출력한다."""
    print("\n=== 즐겨찾기 목록 ===")
    items = filter_favorites(prompts)

    if not items:
        print("즐겨찾기된 프롬프트가 없습니다.")
        return

    for number, prompt in enumerate(items, start=1):
        print_prompt_line(number, prompt)
    print(f"\n총 {len(items)}개의 즐겨찾기")


# --------------------------------------------------- 보너스: 파일 입출력

def save_to_json(prompts):
    """현재 프롬프트를 JSON 파일로 저장한다."""
    print("\n=== JSON 파일로 저장 ===")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(prompts, file, ensure_ascii=False, indent=2)
    print(f"{len(prompts)}개의 프롬프트를 {DATA_FILE}에 저장했습니다.")


def load_from_json(prompts):
    """JSON 파일에서 프롬프트를 불러와 현재 목록을 교체한다."""
    print("\n=== JSON 파일에서 불러오기 ===")
    if not os.path.exists(DATA_FILE):
        print("저장된 파일이 없습니다. 먼저 저장해주세요.")
        return

    try:
        with open(DATA_FILE, encoding="utf-8") as file:
            loaded = json.load(file)
    except (OSError, json.JSONDecodeError):
        print("파일을 읽을 수 없습니다. 기존 데이터를 유지합니다.")
        return

    if not isinstance(loaded, list):
        print("파일 형식이 올바르지 않습니다. 기존 데이터를 유지합니다.")
        return

    prompts.clear()
    prompts.extend(loaded)
    print(f"{len(prompts)}개의 프롬프트를 불러왔습니다.")


def safe_filename(name):
    """파일 이름에 쓸 수 없는 문자를 밑줄로 바꾼다."""
    for char in r'\/:*?"<>| ':
        name = name.replace(char, "_")
    return name


def export_markdown(prompts):
    """프롬프트를 카테고리별 Markdown 파일로 내보낸다."""
    print("\n=== Markdown으로 내보내기 ===")
    if not prompts:
        print("내보낼 프롬프트가 없습니다.")
        return

    os.makedirs(EXPORT_DIR, exist_ok=True)

    categories = []
    for prompt in prompts:
        if prompt["category"] not in categories:
            categories.append(prompt["category"])

    for category in categories:
        items = filter_by_category(prompts, category)
        path = os.path.join(EXPORT_DIR, f"{safe_filename(category)}.md")
        with open(path, "w", encoding="utf-8") as file:
            file.write(f"# {category}\n\n")
            for prompt in items:
                file.write(f"## {prompt['title']}{star(prompt)}\n\n")
                file.write(f"{prompt['content']}\n\n")
        print(f"- {path} ({len(items)}개)")

    print(f"\n{len(categories)}개 카테고리를 내보냈습니다.")


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
        elif choice == "2":
            show_list(prompts)
        elif choice == "3":
            show_by_category(prompts)
        elif choice == "4":
            search_prompt(prompts)
        elif choice == "5":
            show_detail(prompts)
        elif choice == "6":
            toggle_favorite(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "8":
            save_to_json(prompts)
        elif choice == "9":
            load_from_json(prompts)
        elif choice == "10":
            export_markdown(prompts)
        else:
            print("올바른 번호를 입력해주세요.")


if __name__ == "__main__":
    main()
