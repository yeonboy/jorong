
import json
import re
from datetime import datetime
from database_setup import TauntResearchDB
import logging

class MarketingStrategyProcessor:
    def __init__(self):
        self.db = TauntResearchDB()
        
        # 마케팅 전략 핵심 키워드 매핑
        self.strategy_keywords = {
            "target_personas": {
                "경쟁적 게이머": ["게이머", "트위치", "디스코드", "인벤", "트래시 토크", "경쟁심", "반사신경"],
                "온라인 토론가": ["토론가", "클리앙", "뽐뿌", "논리", "증거", "수사학", "팩트폭력"],
                "풍자 애호가": ["풍자", "밈", "틱톡", "아이러니", "냉소", "재치", "돌려까기"]
            },
            "viral_tactics": {
                "전국 드립력 경진대회": ["경진대회", "경쟁", "드립력", "재치", "위트"],
                "도발 아레나": ["아레나", "인터랙티브", "웹 데모", "바이럴", "공유"],
                "A-B 콘텐츠": ["비교", "일반 AI", "조롱 AI", "대비 효과", "숏폼"]
            },
            "monetization": {
                "WaaS": ["위트 기반 서비스", "Wit-as-a-Service", "프리미엄", "구독"],
                "API": ["조롱 API", "B2B", "통합", "인프라"],
                "커뮤니티": ["디스코드 길드", "슈퍼 유저", "충성도", "독점 콘텐츠"]
            },
            "content_types": {
                "팩트폭력": ["논리적", "증거 기반", "토론 종결", "감정적 무력화"],
                "말줄임표 도발": ["심리전", "긴장감", "미완성 위협", "자이가르닉 효과"],
                "쿨찐식 냉소": ["초월적", "아이러니", "지적 우월감", "초연함"],
                "씹선비식 훈계": ["도덕적 우위", "정의로운 분노", "낙인"],
                "돌려까기": ["수동-공격적", "칭찬 속 비난", "미묘한 침습"]
            }
        }
        
        # 심리학적 기법 매핑
        self.psychological_techniques = {
            "자이가르닉 효과": {
                "description": "미완성된 과제나 중단된 활동에 대한 기억이 더 오래 남는 현상",
                "application": "말줄임표 도발에서 상대방이 스스로 모욕을 완성하도록 유도",
                "effectiveness_score": 9.2
            },
            "공손성 이론": {
                "description": "브라운과 레빈슨의 언어학적 공손성 프레임워크",
                "application": "표면적 예의 뒤에 숨긴 도발과 비판",
                "effectiveness_score": 8.7
            },
            "펀칭 업": {
                "description": "권력자나 부조리한 사상을 비판하는 윤리적 풍자 원칙",
                "application": "개인 공격이 아닌 구조적 비판으로 안전성 확보",
                "effectiveness_score": 9.5
            }
        }
        
    def extract_strategy_elements(self, text):
        """마케팅 전략 텍스트에서 핵심 요소들을 추출합니다."""
        extracted_data = {
            "personas": [],
            "tactics": [],
            "content_types": [],
            "psychological_elements": [],
            "kpis": [],
            "viral_mechanics": []
        }
        
        text_lower = text.lower()
        
        # 타겟 페르소나 추출
        for persona, keywords in self.strategy_keywords["target_personas"].items():
            if any(keyword in text_lower for keyword in keywords):
                extracted_data["personas"].append({
                    "name": persona,
                    "keywords_found": [kw for kw in keywords if kw in text_lower],
                    "strategy_priority": "high" if len([kw for kw in keywords if kw in text_lower]) > 3 else "medium"
                })
        
        # 바이럴 전술 추출
        for tactic, keywords in self.strategy_keywords["viral_tactics"].items():
            if any(keyword in text_lower for keyword in keywords):
                extracted_data["tactics"].append({
                    "name": tactic,
                    "keywords_found": [kw for kw in keywords if kw in text_lower],
                    "implementation_phase": self._determine_phase(tactic)
                })
        
        # 콘텐츠 타입 추출
        for content_type, keywords in self.strategy_keywords["content_types"].items():
            if any(keyword in text_lower for keyword in keywords):
                extracted_data["content_types"].append({
                    "type": content_type,
                    "keywords_found": [kw for kw in keywords if kw in text_lower],
                    "psychological_basis": self._get_psychological_basis(content_type)
                })
        
        # KPI 및 성과 지표 추출
        kpi_patterns = [
            r"(\d+)%\s*증가", r"바이럴 계수", r"k-factor", 
            r"트래픽\s*(\d+)%", r"사용자\s*(\d+)만", r"월 매출\s*(\d+)억"
        ]
        
        for pattern in kpi_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                extracted_data["kpis"].extend(matches)
        
        return extracted_data
    
    def _determine_phase(self, tactic):
        """전술의 구현 단계를 결정합니다."""
        phase_mapping = {
            "전국 드립력 경진대회": "론칭",
            "도발 아레나": "사전 론칭",
            "A-B 콘텐츠": "성장"
        }
        return phase_mapping.get(tactic, "일반")
    
    def _get_psychological_basis(self, content_type):
        """콘텐츠 타입의 심리학적 기반을 반환합니다."""
        basis_mapping = {
            "팩트폭력": "인지적 우월감",
            "말줄임표 도발": "자이가르닉 효과",
            "쿨찐식 냉소": "지적 권위",
            "씹선비식 훈계": "도덕적 우월감",
            "돌려까기": "사회적 지배"
        }
        return basis_mapping.get(content_type, "일반적 심리")
    
    def process_marketing_strategy(self, strategy_text):
        """마케팅 전략을 처리하고 데이터베이스에 저장합니다."""
        logging.info("🎯 마케팅 전략 NLP 처리 시작...")
        
        # 전략 요소 추출
        extracted_data = self.extract_strategy_elements(strategy_text)
        
        # 데이터베이스에 저장
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                # 마케팅 전략 테이블이 없다면 생성
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS marketing_strategy_data (
                        id SERIAL PRIMARY KEY,
                        strategy_type VARCHAR(100),
                        element_name VARCHAR(200),
                        keywords_found TEXT[],
                        metadata JSONB,
                        priority_level VARCHAR(50),
                        implementation_phase VARCHAR(50),
                        psychological_basis VARCHAR(100),
                        effectiveness_score FLOAT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 타겟 페르소나 저장
                for persona in extracted_data["personas"]:
                    cur.execute("""
                        INSERT INTO marketing_strategy_data 
                        (strategy_type, element_name, keywords_found, metadata, priority_level, implementation_phase)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        "target_persona",
                        persona["name"],
                        persona["keywords_found"],
                        json.dumps(persona),
                        persona["strategy_priority"],
                        "타겟팅"
                    ))
                
                # 바이럴 전술 저장
                for tactic in extracted_data["tactics"]:
                    cur.execute("""
                        INSERT INTO marketing_strategy_data 
                        (strategy_type, element_name, keywords_found, metadata, implementation_phase, effectiveness_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        "viral_tactic",
                        tactic["name"],
                        tactic["keywords_found"],
                        json.dumps(tactic),
                        tactic["implementation_phase"],
                        8.5  # 기본 효과성 점수
                    ))
                
                # 콘텐츠 타입 저장
                for content in extracted_data["content_types"]:
                    cur.execute("""
                        INSERT INTO marketing_strategy_data 
                        (strategy_type, element_name, keywords_found, metadata, psychological_basis, effectiveness_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        "content_type",
                        content["type"],
                        content["keywords_found"],
                        json.dumps(content),
                        content["psychological_basis"],
                        self._get_content_effectiveness(content["type"])
                    ))
                
                # 심리학적 기법 저장
                for technique, data in self.psychological_techniques.items():
                    cur.execute("""
                        INSERT INTO marketing_strategy_data 
                        (strategy_type, element_name, metadata, psychological_basis, effectiveness_score)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        "psychological_technique",
                        technique,
                        json.dumps(data),
                        data["description"],
                        data["effectiveness_score"]
                    ))
                
                conn.commit()
        
        logging.info("✅ 마케팅 전략 데이터 저장 완료")
        return extracted_data
    
    def _get_content_effectiveness(self, content_type):
        """콘텐츠 타입별 효과성 점수를 반환합니다."""
        effectiveness_scores = {
            "팩트폭력": 9.1,
            "말줄임표 도발": 8.8,
            "쿨찐식 냉소": 8.3,
            "씹선비식 훈계": 7.9,
            "돌려까기": 8.6
        }
        return effectiveness_scores.get(content_type, 7.5)
    
    def integrate_with_existing_prompts(self):
        """기존 프롬프트 시스템과 마케팅 전략을 통합합니다."""
        logging.info("🔗 기존 시스템과 마케팅 전략 통합 중...")
        
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                # 마케팅 전략 데이터 조회
                cur.execute("""
                    SELECT strategy_type, element_name, psychological_basis, effectiveness_score, metadata
                    FROM marketing_strategy_data
                    WHERE effectiveness_score > 8.0
                    ORDER BY effectiveness_score DESC;
                """)
                
                high_impact_strategies = cur.fetchall()
                
                # 기존 QA 히스토리에 마케팅 전략 태그 추가
                for strategy in high_impact_strategies:
                    strategy_type, element_name, psych_basis, score, metadata = strategy
                    
                    # 관련 QA 기록 업데이트
                    cur.execute("""
                        UPDATE qa_history 
                        SET marketing_strategy_applied = COALESCE(marketing_strategy_applied, '[]'::jsonb) || %s::jsonb
                        WHERE tone_used LIKE %s OR target_subject LIKE %s;
                    """, (
                        json.dumps({
                            "strategy": element_name,
                            "psychological_basis": psych_basis,
                            "effectiveness_score": score
                        }),
                        f"%{element_name}%",
                        f"%{element_name}%"
                    ))
                
                conn.commit()
        
        logging.info("✅ 마케팅 전략 통합 완료")
    
    def generate_strategy_insights(self):
        """마케팅 전략 기반 인사이트를 생성합니다."""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                # 가장 효과적인 전략 조합 분석
                cur.execute("""
                    SELECT 
                        element_name,
                        psychological_basis,
                        effectiveness_score,
                        COUNT(*) as usage_count
                    FROM marketing_strategy_data msd
                    LEFT JOIN qa_history qh ON qh.marketing_strategy_applied::text LIKE '%' || msd.element_name || '%'
                    WHERE strategy_type = 'content_type'
                    GROUP BY element_name, psychological_basis, effectiveness_score
                    ORDER BY effectiveness_score DESC, usage_count DESC;
                """)
                
                strategy_performance = cur.fetchall()
                
                insights = []
                for strategy, psych_basis, score, usage in strategy_performance:
                    insights.append({
                        "strategy": strategy,
                        "psychological_basis": psych_basis,
                        "effectiveness": score,
                        "usage_frequency": usage,
                        "recommendation": self._generate_recommendation(strategy, score, usage)
                    })
                
                return insights
    
    def _generate_recommendation(self, strategy, score, usage):
        """전략별 맞춤 추천사항을 생성합니다."""
        if score > 9.0 and usage < 10:
            return f"{strategy} 전략은 높은 효과성을 보이므로 더 적극적으로 활용해야 합니다."
        elif score > 8.5 and usage > 50:
            return f"{strategy} 전략은 잘 활용되고 있으며, 변형 버전 개발을 고려해보세요."
        elif score < 8.0:
            return f"{strategy} 전략의 효과성을 높이기 위한 개선이 필요합니다."
        else:
            return f"{strategy} 전략은 균형잡힌 성과를 보이고 있습니다."

# 실제 마케팅 전략 텍스트 처리
def process_marketing_document():
    """첨부된 마케팅 전략 문서를 처리합니다."""
    
    # 첨부 파일에서 추출한 마케팅 전략 텍스트
    marketing_strategy_text = """
    조롱 프로젝트 - 폭발적 시장 지배를 위한 전략 청사진
    
    핵심 전략: 강력한 파급력을 지닌 인터랙티브 론칭 캠페인, 특정 온라인 하위문화 정밀 타겟 침투, 충성도 높은 슈퍼 유저 커뮤니티 육성
    
    핵심 아이디어: 전국 드립력 경진대회 - 사용자들이 조롱 AI와 자신의 재치를 겨루는 인터랙티브 웹 데모
    
    타겟 고객: 경쟁적 게이머, 온라인 토론가, 풍자 애호가 (지적 우월성 추구, 위트를 사회적 자본으로 간주)
    
    핵심 AI 도발 유형:
    - 팩트폭력: 논리적이고 증거 기반의 토론 종결자 모드
    - 말줄임표 도발: 심리전 모드, 자이가르닉 효과 활용
    - 쿨찐식 냉소: 초월적 지성 모드, 지적 우월감 과시
    - 씹선비식 훈계: 정의로운 분노 모드, 도덕적 우위
    - 돌려까기: 미묘한 침습 모드, 수동-공격적 재치
    
    마케팅 전략:
    1. 도발 아레나 인터랙티브 웹 데모
    2. A-B 콘텐츠 제작 (일반 AI vs 조롱 AI)
    3. 계층적 인플루언서 전략 (메가/매크로/마이크로)
    4. 디스코드 조롱 길드 커뮤니티
    
    성과 지표: 바이럴 계수, 트래픽 500% 증가, 사용자 참여율
    """
    
    processor = MarketingStrategyProcessor()
    
    # 전략 처리 및 데이터베이스 저장
    extracted_data = processor.process_marketing_strategy(marketing_strategy_text)
    
    # 기존 시스템과 통합
    processor.integrate_with_existing_prompts()
    
    # 인사이트 생성
    insights = processor.generate_strategy_insights()
    
    return extracted_data, insights

if __name__ == "__main__":
    extracted_data, insights = process_marketing_document()
    
    print("\n" + "="*60)
    print("🎯 마케팅 전략 NLP 처리 완료")
    print("="*60)
    
    print(f"\n📊 추출된 데이터:")
    print(f"  • 타겟 페르소나: {len(extracted_data['personas'])}개")
    print(f"  • 바이럴 전술: {len(extracted_data['tactics'])}개")
    print(f"  • 콘텐츠 타입: {len(extracted_data['content_types'])}개")
    
    print(f"\n💡 주요 인사이트:")
    for insight in insights[:3]:
        print(f"  🔍 {insight['strategy']}: {insight['recommendation']}")
