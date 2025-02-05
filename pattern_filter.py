import json
import re
import ahocorasick

class PatternFilter:
    def __init__(self, pattern_file: str):
        """
        :param pattern_file: 패턴 목록을 담은 JSON 파일 경로.
        """
        self.pattern_file = 'patterns.json'
        self.literals = {}          # literal 패턴: {패턴: 카테고리}
        self.regex_dict = {}        # 원본 regex 패턴: {패턴: 카테고리}
        self.regex_patterns = []    # 기존 방식: list of (compiled_regex, 카테고리)
        self.combined_regex = None  # 개선 방식: 하나로 합친 정규식 (combined regex)
        self.combined_regex_map = {}# 그룹 이름 -> 카테고리 매핑
        self.automaton = None       # pyahocorasick 자동자
        
        self.load_patterns()
        self.build_automaton()
        self.build_combined_regex()  # regex 합치기

    def load_patterns(self):
        """
        JSON 파일로부터 패턴 목록을 로드합니다.
        파일 구조는 아래와 같이 되어야 합니다:
            {
                "literals": { "패턴1": "카테고리1", ... },
                "regex": { "패턴2": "카테고리2", ... }
            }
        """
        try:
            with open(self.pattern_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.literals = data.get("literals", {})
                self.regex_dict = data.get("regex", {})
                # 기존 개별 regex 매칭용 컴파일 (개선 전 fallback용)
                self.regex_patterns = [(re.compile(pat), cat) for pat, cat in self.regex_dict.items()]
        except FileNotFoundError:
            self.literals = {}
            self.regex_dict = {}
            self.regex_patterns = []

    def build_automaton(self):
        self.automaton = ahocorasick.Automaton()
        for pat, cat in self.literals.items():
            self.automaton.add_word(pat, (pat, cat))
        self.automaton.make_automaton()
    
    def build_combined_regex(self):
        self.combined_regex_map = {}
        combined_parts = []
        for idx, (pattern, cat) in enumerate(self.regex_dict.items()):
            group_name = f"rg{idx}"
            self.combined_regex_map[group_name] = cat
            combined_parts.append(f"(?P<{group_name}>{pattern})")
        if combined_parts:
            combined_pattern = "|".join(combined_parts)
            self.combined_regex = re.compile(combined_pattern)
        else:
            self.combined_regex = None

    def match(self, text: str):
        """
        텍스트 내에 등록된 패턴이 검출되었는지 확인
        
        :param text: 검사할 텍스트
        :return: (detected, categories) 튜플  
                 - detected: 하나라도 검출되면 True, 아니면 False  
                 - categories: 검출된 카테고리들의 리스트 
        """
        detected_categories = set()

        for end_index, (pat, cat) in self.automaton.iter(text):
            detected_categories.add(cat)
        
        if self.combined_regex:
            for match in self.combined_regex.finditer(text):
                for group_name, value in match.groupdict().items():
                    if value is not None:
                        detected_categories.add(self.combined_regex_map[group_name])
                        break
        else:
            for regex, cat in self.regex_patterns:
                if regex.search(text):
                    detected_categories.add(cat)
        
        detected = len(detected_categories) > 0
        return detected, list(detected_categories)
