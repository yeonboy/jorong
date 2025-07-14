
# ====================================================================
# 파일: prompt_config.py
# 설명: 프롬프트 생성을 위한 거대 설정 데이터들을 보관합니다.
# ====================================================================

# 감정선 겨냥 시스템
EMOTION_TARGET_SYSTEM = {
    'superiority': { 'description': '독자의 우월감을 자극하여 대상에 대한 비판적 시각 강화', 'triggers': ['비교우위', '능력부족지적', '상식결여부각', '실수반복패턴'], 'psychological_effect': '독자가 자신이 더 나은 상황에 있다고 느끼게 함' },
    'empathy': { 'description': '독자의 공통 경험과 불만을 건드려 강한 공감대 형성', 'triggers': ['공통불만사항', '사회적스트레스', '일상짜증요소', '집단경험'], 'psychological_effect': '독자가 "나도 그랬어" 하며 감정적 동조 유발' },
    'catharsis': { 'description': '독자가 말하지 못했던 속마음을 대신 표현해주는 역할', 'triggers': ['억압된감정해소', '속마음대변', '금기어표현', '직설적비판'], 'psychological_effect': '독자가 시원함과 해방감을 느끼게 함' },
    'social_validation': { 'description': '독자가 다른 사람과 공유하고 싶어지는 사회적 가치 제공', 'triggers': ['공유욕구자극', '재치있는표현', '밈문화반영', '트렌드활용'], 'psychological_effect': '독자가 타인에게 보여주고 싶어하는 욕구 자극' }
}

# 톤 설명 및 전략
TONE_DESCRIPTIONS = {
    '유머러스하게': { 'style': '재미있고 밝은 분위기로, 독자가 웃을 수 있는 유머 요소를 포함하여 작성', 'emotion_strategy': ['empathy', 'social_validation'], 'targeting_method': '공통 경험을 우스꽝스럽게 과장하여 공감대 형성 후 공유욕구 자극', 'psychological_hook': '독자가 "이거 완전 우리 회사 이야기네 ㅋㅋ" 하며 주변에 보여주고 싶게 만들기' },
    '풍자적': { 'style': '비유와 비판을 담아, 간접적으로 놀리는 듯한 느낌으로 작성', 'emotion_strategy': ['superiority', 'catharsis'], 'targeting_method': '지적인 비유를 통해 독자의 우월감 자극하며 직접 말하기 어려운 비판 대신 표현', 'psychological_hook': '독자가 "역시 이렇게 말해야 품격 있지" 하며 자신의 지적 수준을 확인받는 느낌' },
    '비꼬는 듯이': { 'style': '은근히 놀리는 듯한, 살짝 빈정거리는 듯한 어조로 작성', 'emotion_strategy': ['catharsis', 'superiority'], 'targeting_method': '간접적 비꼬기로 독자의 억압된 감정 해소 및 도덕적 우위감 제공', 'psychological_hook': '독자가 "이렇게 돌려서 말하니까 더 임팩트 있네" 하며 만족감 느끼기' },
    '논리적으로 반박하는': { 'style': '팩트와 논리를 기반으로, 상대방의 주장을 차분하지만 효과적으로 반박하는 어조로 작성', 'emotion_strategy': ['superiority', 'catharsis'], 'targeting_method': '논리적 근거 제시로 독자의 지적 우월감 충족 및 정의감 만족', 'psychological_hook': '독자가 "역시 팩트로 때려야 제맛이지" 하며 지적 만족감 획득' },
    'MZ 반말 톤': { 'style': '인터넷 슬랭과 줄임말을 사용하는 친근하고 솔직한 친구 같은 느낌으로 작성', 'emotion_strategy': ['empathy', 'social_validation'], 'targeting_method': 'MZ세대 공통 언어로 강한 소속감과 세대 연대감 형성', 'psychological_hook': '독자가 "완전 내 또래 말투네 ㅋㅋ 완전 공감" 하며 세대적 동질감 느끼기' },
    '애교 톤': { 'style': '귀엽고 사랑스러운 느낌을 주며, 어미를 늘리거나 부드러운 표현을 사용하여 작성', 'emotion_strategy': ['catharsis', 'social_validation'], 'targeting_method': '귀여운 표현으로 독자의 모성/부성본능 자극하며 부드러운 비판으로 카타르시스 제공', 'psychological_hook': '독자가 "이렇게 귀엽게 말해도 뼈 있는 말이네" 하며 애정어린 비판으로 받아들이기' },
    '헬창 톤': { 'style': '운동 문화 슬랭과 에너지 넘치는 동기부여, 자신감을 표현하는 어조로 작성', 'emotion_strategy': ['superiority', 'social_validation'], 'targeting_method': '운동 문화의 긍정 에너지로 독자의 자신감 부스팅 및 건강한 우월감 제공', 'psychological_hook': '독자가 "역시 운동하는 사람 마인드가 다르네" 하며 라이프스타일 우월감 느끼기' },
    '감성 에세이 톤': { 'style': '깊이 있고 시적인 표현, 인스타그램 감성 캡션과 같은 문학적인 느낌으로 작성', 'emotion_strategy': ['catharsis', 'social_validation'], 'targeting_method': '감성적 표현으로 독자의 내면 감정 건드리며 심미적 만족감 제공', 'psychological_hook': '독자가 "이 글 진짜 감성적이네, 인스타에 올려야지" 하며 감성 공유욕구 자극' },
    '해시태그 스타일': { 'style': '인스타그램에서 해시태그를 여러 개 나열하듯이, 트렌디하고 간결하게 작성', 'emotion_strategy': ['social_validation', 'empathy'], 'targeting_method': 'SNS 문화 반영으로 트렌드 민감성 자극 및 즉시 공유 가능한 형태 제공', 'psychological_hook': '독자가 "이거 완전 인스타 감성이네, 스토리에 올려야지" 하며 즉시 공유 욕구 발생' },
    '초성체 스타일': { 'style': '한국어 자음 줄임말(예: ㅇㅈ, ㄹㅇ, ㅊㅋ)을 사용하여 젊은 세대의 대화처럼 작성', 'emotion_strategy': ['empathy', 'social_validation'], 'targeting_method': '세대 특화 언어로 강한 소속감과 세대 연대감 형성', 'psychological_hook': '독자가 "ㅋㅋㅋ 이 표현 완전 찰떡" 하며 세대 공감대와 언어적 즐거움 동시 충족' },
    '야민정음 스타일': { 'style': '의도적인 오타나 단어 변형(예: 띵작, 커여워)을 활용하여 재미있고 유머러스하게 작성', 'emotion_strategy': ['social_validation', 'empathy'], 'targeting_method': '인터넷 문화의 창의적 언어유희로 독자의 문화 이해도 자랑욕구 및 재미 제공', 'psychological_hook': '독자가 "이 표현 알아듣는 나도 인터넷 고수 ㅋㅋ" 하며 문화적 우월감과 재미 동시 획득' },
    '냉소 톤': { 'style': '쿨하고 현실적이며, 미묘한 아이러니와 재치를 사용하여 비판적인 시각을 드러내는 어조로 작성', 'emotion_strategy': ['superiority', 'catharsis'], 'targeting_method': '현실 인식의 깊이로 독자의 지적 우월감 충족 및 냉정한 비판으로 카타르시스 제공', 'psychological_hook': '독자가 "역시 현실을 제대로 아는 사람의 시각이네" 하며 현실 인식력 우월감 느끼기' },
    '정신나간 톤': { 'style': '완전 자유분방하고 예측 불가능하며, 밈(meme)과 혼란스러운 에너지를 활용하여 작성', 'emotion_strategy': ['social_validation', 'catharsis'], 'targeting_method': '예측 불가능한 유머로 독자의 일상 스트레스 해소 및 밈 문화 공유욕구 자극', 'psychological_hook': '독자가 "이거 완전 미친 거 아니야? ㅋㅋㅋ 친구들한테 보여줘야지" 하며 충격과 재미로 공유 충동 발생' },
    '유튜브 쇼츠 톤': { 'style': '짧은 영상 콘텐츠처럼 시선을 사로잡는 오프닝(예: 잠깐! 이거 안보면 후회함)과 간결한 전달 방식으로 작성', 'emotion_strategy': ['social_validation', 'superiority'], 'targeting_method': '어텐션 그래빙으로 즉시 관심 집중 후 쇼츠 문화 이해도로 트렌드 우월감 제공', 'psychological_hook': '독자가 "와 이거 완전 쇼츠 감성이네, 진짜 요즘 트렌드 제대로 아는구나" 하며 트렌드 감각 우월감 느끼기' },
    '틱톡 트렌드 톤': { 'style': '#hopecore, #coquette 등 틱톡의 바이럴 트렌드와 유행하는 표현을 적극적으로 사용하여 작성', 'emotion_strategy': ['social_validation', 'empathy'], 'targeting_method': '최신 바이럴 트렌드 반영으로 독자의 트렌드 민감성 자극 및 글로벌 문화 동참감 제공', 'psychological_hook': '독자가 "오 이 트렌드 나도 알아, 완전 글로벌 감성" 하며 문화적 동참감과 우월감 동시 충족' },
    '에겐톤': { 'style': '감수성이 높고 섬세하며, 관계의 조화를 중시하는 간접적이고 부드러운 표현으로 작성. 해요체를 기본으로 하며 완곡어법과 감정적 배려가 풍부함', 'emotion_strategy': ['empathy', 'social_validation'], 'targeting_method': '상대방의 감정을 세심하게 배려하며 갈등을 회피하고 정서적 유대감을 형성하는 관계 지향적 소통', 'psychological_hook': '독자가 "이렇게 배려깊게 말해주니 마음이 따뜻해진다" 하며 정서적 안정감과 소속감을 느끼게 함', 'linguistic_features': { 'formality_level': '해요체 중심', 'sentence_types': '의문문, 청유문 선호', 'vocabulary': '감성적, 정서적 어휘 빈번 사용', 'hedging': '높은 수준의 완곡어법 사용', 'examples': ['혹시 괜찮으시다면...', '제 생각에는... 인 것 같아요', '마음이 복잡하시겠어요'] } },
    '테토 톤': { 'style': '논리적이고 직설적이며 효율성을 중시하는 단정적 표현으로 작성. 해체나 해라체를 편안하게 사용하며 사실 중심의 명료한 소통을 선호함', 'emotion_strategy': ['superiority', 'catharsis'], 'targeting_method': '감정적 위로보다 실질적 해결책 제시를 통해 문제를 효율적으로 해결하려는 행동 지향적 소통', 'psychological_hook': '독자가 "역시 이렇게 명확하게 말해야 문제가 해결되지" 하며 논리적 명쾌함과 효율성에 만족감을 느끼게 함', 'linguistic_features': { 'formality_level': '해체, 해라체 중심 (상황에 따라 해요체)', 'sentence_types': '평서문, 명령문 주도적 사용', 'vocabulary': '사실적, 행동 지향적 어휘', 'hedging': '낮은 수준의 완곡어법, 직설적 표현', 'examples': ['그래서 결론이 뭔데?', '이거부터 처리하자', '팩트는 이거야'] } },
    '소심한 공격 톤': { 'style': 'Aposiopesis 기법을 활용하여 하고 싶은 말은 많지만 용기가 없는 척하며 상대를 더 효과적으로 조롱하는 말줄임 방식으로 작성', 'emotion_strategy': ['superiority', 'catharsis', 'social_validation'], 'targeting_method': '직접 공격을 회피하면서도 상대가 스스로 모욕을 완성하게 만드는 고도의 심리전으로 지적 우월감과 카타르시스 동시 제공', 'psychological_hook': '독자가 "이런 식으로 공격하는 것도 있구나, 완전 고급 기술이네" 하며 언어적 기교에 대한 감탄과 공유욕구 발생' },
    '말줄임 밈 톤': { 'style': '인터넷 밈 문화와 결합된 Aposiopesis 기법으로 바이럴 잠재력을 극대화하며 의도적 미완성 문장과 가짜 당황으로 작성', 'emotion_strategy': ['social_validation', 'empathy', 'catharsis'], 'targeting_method': 'SNS 밈 문화 반영으로 MZ세대 공감대 형성 및 바이럴 확산 욕구 자극하며 계산된 실수로 재미 창출', 'psychological_hook': '독자가 "이거 완전 밈 될 것 같은데? 친구들한테 보여줘야지" 하며 밈 문화 이해도와 트렌드 감각 우월감 느끼기' }
}

# 마스터피스 조롱 예시들
MASTERPIECE_TAUNTS = {
    "지적_허영심": [
        { "text": "자네 글은 마치 학사 논문 같군. 아무도 읽지 않겠지만.", "context": "지식을 과시하는 사람에게", "psychological_tactic": "지적 자존심 깎아내리기", "stimulation_index": 7 },
        { "text": "박사 학위는 있으신가? 아니면 그냥 아는 척하는 건가?", "context": "전문가인 척하는 사람에게", "psychological_tactic": "권위에 대한 의문 제기", "stimulation_index": 8 }
    ],
    "인정_욕구": [
        { "text": "좋아요 구걸하는 것도 능력이라 쳐주자.", "context": "SNS 중독자에게", "psychological_tactic": "관심 갈구 비판", "stimulation_index": 6 },
        { "text": "인정받고 싶어서 안달난 모습, 보기 안쓰럽네.", "context": "관심을 원하는 사람에게", "psychological_tactic": "동정심 유발", "stimulation_index": 7 }
    ],
    "허영심": [
        { "text": "그 돈으로 책이라도 사보지 그래?", "context": "사치스러운 사람에게", "psychological_tactic": "가치관 비판", "stimulation_index": 5 },
        { "text": "명품으로 포장해도 네 속은 텅 비었잖아.", "context": "겉치레에만 신경 쓰는 사람에게", "psychological_tactic": "내면의 공허함 지적", "stimulation_index": 8 }
    ],
    "무기력감": [
        { "text": "숨 쉬는 것 빼고 뭘 할 수 있지?", "context": "무기력한 사람에게", "psychological_tactic": "존재 가치 폄하", "stimulation_index": 6 },
        { "text": "그렇게 살 거면 그냥 누워 있는 게 낫지 않아?", "context": "게으른 사람에게", "psychological_tactic": "삶의 의욕 저하", "stimulation_index": 7 }
    ],
    "소외감": [
        { "text": "너만 이해할 수 있는 유머는 대체 뭔데?", "context": "특이한 유머를 구사하는 사람에게", "psychological_tactic": "소통 단절 비판", "stimulation_index": 5 },
        { "text": "혼자만 다른 세상 사는 것 같아.", "context": "튀는 행동을 하는 사람에게", "psychological_tactic": "고립감 조성", "stimulation_index": 7 }
    ],
    "일반적_약점": [
        { "text": "그러니까 네가 [문제점]인 거야.", "context": "일반적인 문제점을 지적할 때", "psychological_tactic": "단순 비판", "stimulation_index": 4 },
        { "text": "세상에 너 같은 사람은 처음 봐.", "context": "특이한 사람에게", "psychological_tactic": "관심 집중 (부정적)", "stimulation_index": 5 }
    ]
}

# 2025년 한국 온라인 트렌드 데이터
KOREA_TRENDS = {
    'cost_of_living': {
        'keywords': ['월세', '물가', '생활비', '집값', '경제', 'DSR', '신도시', '대출'],
        'tone_style': '현실적이고 냉소적인 톤으로 경제적 어려움에 대한 공감대 형성',
        'viral_pattern': '구체적인 금액과 실제 경험담을 통한 충격적 현실 제시',
        'comment_style': '뉴스 댓글 냉소톤: "이게 대책이라고", "서민들은 그림의 떡"'
    },
    'entertainment_culture': {
        'keywords': ['영화', '드라마', '아이돌', '연예인', '직캠', '쇼케이스'],
        'tone_style': '과몰입과 극찬을 통한 팬덤 감정 표현',
        'viral_pattern': '극찬 표현과 감탄사를 통한 감정 폭발',
        'comment_style': '유튜브 극찬톤: "국보급", "명작 스멜", "알고리즘님 감사"'
    },
    'social_dynamics': {
        'keywords': ['세대', '직장', '문화', 'MZ', '신입사원', '라떼'],
        'tone_style': '세대 간 차이를 재치있게 지적하는 풍자적 톤',
        'viral_pattern': '공통 경험에 대한 공감대 형성과 세대별 특징 부각',
        'comment_style': '유튜브 공감톤: "개웃기네", "공감은 간다", "서로 이해하려는 노력"'
    },
    'political_social_issues': {
        'keywords': ['정부', '정책', '법', '민주주의', '선거', '시민'],
        'tone_style': '강한 정치적 비판과 분노 표출',
        'viral_pattern': '직접적인 정치 비판과 감정적 반발',
        'comment_style': '뉴스 분노톤: "민주주의 맞냐", "다음 선거 때 보자", "밀어붙이네"'
    },
    'social_inequality': {
        'keywords': ['부동산', '연예인', '상대적 박탈감', '서민', '격차'],
        'tone_style': '사회적 불평등에 대한 절망과 비관',
        'viral_pattern': '현실적 좌절감과 사회 구조적 문제 지적',
        'comment_style': '뉴스 절망톤: "상대적 박탈감", "한 평생 모아도", "이런 기사 안 보고 싶다"'
    }
}

# 흑화 단계별 설정
DARKNESS_CONFIG = {
    1: {"name": "순수 유머", "intensity": "매우 약함", "approach": "완전히 건전하고 밝은 유머로만 작성", "persona": "순수한 유머 전문가"},
    2: {"name": "가벼운 놀림", "intensity": "약함", "approach": "친구 사이의 장난스러운 놀림 수준으로 작성", "persona": "친근한 장난 전문가"},
    3: {"name": "날카로운 지적", "intensity": "보통", "approach": "문제점을 명확히 짚어내되 건설적 의도를 포함하여 작성", "persona": "객관적인 비평가"},
    4: {"name": "강한 조롱", "intensity": "강함", "approach": "상당한 감정적 타격을 주되 인격 모독은 피하여 작성", "persona": "신랄한 풍자 작가"},
    5: {"name": "파괴적 공격", "intensity": "매우 강함", "approach": "극도로 강한 조롱과 인격적 비하를 포함하여 작성", "persona": "악마 편집자"}
}
