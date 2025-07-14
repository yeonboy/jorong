
# ====================================================================
# 파일: prompt_builder.py
# 설명: 프롬프트 생성과 관련된 모든 로직을 담당합니다.
# ====================================================================
from prompt_config import TONE_DESCRIPTIONS, KOREA_TRENDS, MASTERPIECE_TAUNTS, DARKNESS_CONFIG

def get_marketing_strategy_enhancement(tone, target, keywords):
    """마케팅 전략 기반 콘텐츠 최적화"""
    return "마케팅 전략 분석 기능은 현재 비활성화 상태입니다."

def get_psychological_enhancement(weakness_type):
    """심리적 약점 유형에 따른 강화 전략을 반환합니다."""
    enhancements = {
        "지적_허영심": "상대방의 지식 자랑이나 아는 척하는 행동을 미묘하게 지적하여 지적 우월감을 자극",
        "인정_욕구": "관심받고 싶어하는 행동 패턴을 드러내어 독자의 심리적 우위감 조성",
        "허영심": "겉치레나 과시에 치중하는 모습을 대비시켜 내실의 중요성 부각",
        "무기력감": "소극적이고 수동적인 태도를 지적하여 행동력의 중요성 강조",
        "소외감": "독특함을 추구하는 모습을 통해 소통의 어려움 부각",
        "일반적_약점": "보편적인 인간의 약점을 재치있게 지적하여 공감대 형성"
    }
    return enhancements.get(weakness_type, "일반적인 약점 지적을 통한 우월감 자극")

def analyze_psychological_weakness(keywords):
    """키워드를 분석하여 심리적 약점을 추정합니다."""
    keywords_lower = keywords.lower()

    if any(word in keywords_lower for word in ['똑똑', '지식', '박사', '전문가', '분석']):
        return "지적_허영심"
    elif any(word in keywords_lower for word in ['인정', '관심', '칭찬', '좋아요', 'sns']):
        return "인정_욕구"
    elif any(word in keywords_lower for word in ['돈', '명품', '자랑', '과시', '성공']):
        return "허영심"
    elif any(word in keywords_lower for word in ['게으름', '암것도', '빈둥', '놀림']):
        return "무기력감"
    elif any(word in keywords_lower for word in ['특이', '이상', '독특']):
        return "소외감"
    else:
        return "일반적_약점"

def get_relevant_masterpieces(weakness_type):
    """심리적 약점에 해당하는 마스터피스 조롱 사례를 반환합니다."""
    return MASTERPIECE_TAUNTS.get(weakness_type, MASTERPIECE_TAUNTS.get("일반적_약점", []))

def format_masterpiece_examples(examples):
    """마스터피스 예시들을 프롬프트용으로 포맷팅합니다."""
    if not examples:
        return "해당 분야의 마스터피스 사례 준비 중..."

    formatted = ""
    for i, example in enumerate(examples[:2], 1):  # 최대 2개만 사용
        formatted += f"""
**예시 {i}**: "{example['text']}"
- 상황: {example['context']}
- 심리 전술: {example['psychological_tactic']}
- 자극 지수: {example['stimulation_index']}/10
"""
    return formatted

def generate_aposiopesis_prompt_addition(tone, target, keywords):
    """Aposiopesis 기법 적용 시 추가되는 특별 프롬프트를 생성합니다."""
    if tone in ['소심한 공격 톤', '말줄임 밈 톤']:
        return f"""

**Aposiopesis Taunt (말줄임 조롱) 기법 적용**

당신은 이제 **소심한 복수자** 페르소나로 변신합니다. 하고 싶은 말은 많지만 대놓고 말할 용기는 없는 척하며, 상대방이 스스로 모욕을 완성하게 만드는 고도의 심리전을 구사합니다.

**3단계 Aposiopesis 생성 규칙:**

**1단계: 공격 시동** - {target}의 {keywords}와 관련된 가장 아픈 부분을 찌를 수 있는 공격적인 단어나 문장을 시작하되, 가장 핵심적인 단어는 절대 먼저 말하지 마세요
**2단계: 급작스러운 중단** - 핵심 단어가 나오기 직전에 "..." 또는 "어?" 등을 사용하여 말을 끊으세요
**3단계: 위선적 수습** - 마치 큰 실수를 한 것처럼 급하게 말을 수습하세요

**심리적 효과 목표:** 독자가 스스로 모욕을 완성하게 만들면서 당신은 끝까지 착한 사람으로 남기
"""
    return ""

def get_research_enhanced_prompt(target, keywords, tone, darkness_level, length, optimized_for_json=False):
    """연구 데이터를 기반으로 최적화된 프롬프트를 생성합니다."""
    
    current_darkness = DARKNESS_CONFIG.get(darkness_level, DARKNESS_CONFIG[2])
    
    # 키워드 기반 트렌드 매칭
    matched_trend = None
    for trend, data in KOREA_TRENDS.items():
        if any(keyword in keywords.lower() for keyword in data['keywords']):
            matched_trend = trend
            break

    # 5단계 강한 비판 처리  
    if darkness_level == 5:
        base_prompt = f"""
당신은 날카로운 비평가입니다. 다음 정보를 바탕으로 '{target}'에 대한 신랄하지만 재치있는 비평 텍스트를 생성해주세요.

**🔥 5단계 신랄한 비평 모드**
이 단계에서는 강한 풍자와 날카로운 지적을 포함하되, 창의적 표현으로 작성합니다.

**대상 분석:**
- 조롱 대상: {target}
- 핵심 키워드: {keywords}
- 목표 톤: {tone}
- 흑화 단계: {current_darkness['name']} ({current_darkness['intensity']})

**5단계 비평 지침:**
1. 날카로운 관찰과 신랄한 지적 활용
2. 창의적 비유와 풍자로 약점 부각
3. 강한 어조와 직설적 표현 사용
4. 심리적 임팩트를 극대화하는 내용 작성
5. 사회적 현실을 반영한 냉정한 분석

**길이:** 약 {length}자
"""
    else:
        # 연구 데이터 기반 심리적 약점 분석
        weakness_type = analyze_psychological_weakness(keywords)
        psychological_enhancement = get_psychological_enhancement(weakness_type)
        marketing_enhancement = get_marketing_strategy_enhancement(tone, target, keywords)
        
        # 관련 마스터피스 예시 조회
        relevant_masterpieces = get_relevant_masterpieces(weakness_type)
        formatted_examples = format_masterpiece_examples(relevant_masterpieces)

        base_prompt = f"""
당신은 **{current_darkness['persona']}**입니다. 다음 정보를 바탕으로 '{target}'에 대한 {tone} 스타일의 텍스트를 생성해주세요.

**대상 분석:**
- 조롱 대상: {target}
- 핵심 키워드: {keywords}
- 목표 톤: {tone}
- 흑화 단계: {current_darkness['name']} ({current_darkness['intensity']})
- 추정 심리적 특성: {weakness_type}

**2025년 한국 온라인 문화 트렌드 반영:**
{f"**매칭된 트렌드**: {matched_trend}" if matched_trend else "**일반 트렌드 적용**"}
{f"**톤 스타일**: {KOREA_TRENDS[matched_trend]['tone_style']}" if matched_trend else "**기본 톤 적용**"}
{f"**바이럴 패턴**: {KOREA_TRENDS[matched_trend]['viral_pattern']}" if matched_trend else "**기본 패턴 적용**"}
{f"**댓글 문화 반영**: {KOREA_TRENDS[matched_trend]['comment_style']}" if matched_trend else "**기본 댓글 스타일 적용**"}

**참고: 마스터피스 조롱 예시:**
{formatted_examples}

**2025년 인기 커뮤니티 화법 적용:**
- **더쿠 스타일**: 감정 강화어 활용 (진짜, 완전, 개, 미친) + 반응 패턴 (ㅋㅋㅋ, ㅠㅠ, 헐)
- **엠팍 스타일**: 논리적 권위 표현 (팩트, 객관적으로, 경험상) + 경쟁 언어 (압도, 완승, 우위)
- **인스티즈 스타일**: 미적 언어 (레전드, 찰떡, 취향저격) + 감정 표현 (심쿵, 개좋아)

**세부 지침:**
1. 제시된 심리적 약점을 활용하여 비판적 시각을 강화하세요.
2. 2025년 Reddit 트렌드와 한국 커뮤니티 화법을 적극 반영하세요.
3. 마스터피스 조롱 예시를 참고하여 창의적 표현을 구사하세요.
4. [대상]의 [구체적인 행동]에 대해 [톤]을 사용하여 조롱하세요.
5. [흑화 단계]에 맞는 강도로 감정적 임팩트를 극대화하세요.
6. 바이럴 확산 가능성을 고려한 공감대 형성과 공유 욕구 자극 요소 포함하세요.

**길이:** 약 {length}자
"""

        # 에겐-테토 특화 프롬프트 로직
        if tone == '에겐톤':
            base_prompt += f"""

**🎭 에겐 페르소나 특화 지침**

당신은 이제 **감수성이 높고 관계 지향적인 에겐 페르소나**로 변신합니다.

**핵심 언어적 전략:**
1. **해요체 중심 사용**: 기본적으로 '해요체'를 사용하여 심리적 거리를 좁히면서도 예의를 지킴
2. **완곡어법 활용**: "혹시", "저기", "...인 것 같아요", "...라고 볼 수도 있겠네요" 등으로 단정을 피함
3. **감정적 배려**: 상대방의 감정 상태를 세심하게 고려한 표현 사용
4. **관계 노동**: 갈등을 회피하고 조화로운 분위기 조성에 집중

이제 '{target}'에 대해 에겐 페르소나의 섬세하고 배려 깊은 방식으로 표현해주세요.
"""
        elif tone == '테토 톤':
            base_prompt += f"""

**⚡ 테토 페르소나 특화 지침**

당신은 이제 **논리적이고 효율성을 중시하는 테토 페르소나**로 변신합니다.

**핵심 언어적 전략:**
1. **직설적 표현**: 해체나 평서문을 사용하여 명확하고 단정적으로 표현
2. **사실 중심**: 감정적 수식어보다는 객관적 사실과 논리에 기반
3. **효율성 우선**: 불필요한 완곡어법 없이 핵심만 간결하게 전달
4. **문제 해결 지향**: 감정적 위로보다는 실질적 해결책 제시

이제 '{target}'에 대해 테토 페르소나의 직설적이고 효율적인 방식으로 표현해주세요.
"""

        # 톤 설정과 통합
        tone_config = TONE_DESCRIPTIONS.get(tone, {
            'style': '친근하고 유머러스한 어조',
            'emotion_strategy': ['empathy'],
            'targeting_method': '공통 경험 기반 공감대 형성',
            'psychological_hook': '독자의 공감과 재미 유발'
        })

        base_prompt += f"""

**감정선 겨냥 전략:**
- 스타일: {tone_config.get('style', '기본 스타일')}
- 감정 전략: {', '.join(tone_config.get('emotion_strategy', ['기본']))}
- 타겟팅 방법: {tone_config.get('targeting_method', '기본 방법')}
- 심리적 훅: {tone_config.get('psychological_hook', '기본 효과')}

**마케팅 전략 최적화:**
{marketing_enhancement}

{generate_aposiopesis_prompt_addition(tone, target, keywords)}

**창작 가이드라인:**
- 건전한 수준의 놀림과 지적은 허용
- 유머러스한 과장과 재치있는 비판 활용
- 한글, 영문, 숫자, 기본 문장부호 사용
- 창의적 비유와 풍자로 재미 창출
"""

    # JSON 최적화 옵션 추가
    if optimized_for_json:
        json_output_instruction = """

---
**최종 출력 형식 (JSON)**

이제까지의 모든 지침을 종합하여, 다음 JSON 스키마에 맞춰 결과를 생성해주세요.
모든 텍스트는 반드시 한국어로 작성되어야 합니다.

```json
{
  "generated_text": "[여기에 최종적으로 생성된 조롱 텍스트를 작성]",
  "safety_analysis": {
    "is_safe": [true 또는 false],
    "safety_message": "[안전성 평가 메시지. '안전합니다.' 또는 구체적인 우려 사항을 작성]"
  }
}
```

이제 JSON 형식으로 최종 결과물을 생성해주세요:
"""
        base_prompt += json_output_instruction

    return base_prompt
