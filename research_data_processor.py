
import json
import re
from datetime import datetime
from database_setup import TauntResearchDB
import google.generativeai as genai
import os

class TauntResearchProcessor:
    def __init__(self):
        self.db = TauntResearchDB()
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
    
    def load_masterpiece_taunt_data(self):
        """마스터피스 조롱 데이터셋을 로드합니다."""
        masterpiece_data = [
            {
                "dataset_name": "마스터피스_조롱_오스카_와일드",
                "content_type": "literary_taunt",
                "raw_data": {
                    "author": "Oscar Wilde",
                    "famous_quotes": [
                        "I can resist everything except temptation.",
                        "We are all in the gutter, but some of us are looking at the stars."
                    ],
                    "psychological_tactics": ["반어법", "우아한_모독", "지적_우월감"]
                },
                "processed_data": {
                    "stimulation_techniques": {
                        "irony_mastery": "상대의 기대를 완전히 뒤집는 반전",
                        "elegant_insult": "품격을 유지하면서도 날카로운 지적",
                        "intellectual_superiority": "지적 수준의 차이를 우아하게 드러냄"
                    }
                },
                "metadata": {
                    "stimulation_index": 9.5,
                    "cultural_impact": "timeless"
                },
                "quality_score": 9.8
            },
            {
                "dataset_name": "마스터피스_조롱_닥터_하우스",
                "content_type": "modern_sarcasm",
                "raw_data": {
                    "character": "Dr. Gregory House",
                    "signature_style": "의학적 지식을 활용한 냉소적 진단",
                    "psychological_tactics": ["가스라이팅", "현실_직시_강요", "전문성_활용"]
                },
                "processed_data": {
                    "modern_techniques": {
                        "expertise_weaponization": "전문 지식을 조롱의 도구로 활용",
                        "reality_check": "상대방의 환상을 무자비하게 깨뜨림",
                        "systematic_deconstruction": "논리적으로 상대를 해체"
                    }
                },
                "metadata": {
                    "stimulation_index": 9.2,
                    "modern_relevance": "high"
                },
                "quality_score": 9.4
            }
        ]
        return masterpiece_data

    def load_project_development_strategy_data(self):
        """프로젝트 발전 전략 기반 연구 데이터를 로드합니다."""
        
        # 프로젝트 발전 전략 데이터
        development_strategies = [
            {
                "dataset_name": "사용자_경험_최적화_전략",
                "content_type": "ux_optimization",
                "raw_data": {
                    "ui_improvements": [
                        "실시간 피드백 시스템",
                        "개인화된 추천 엔진",
                        "소셜 공유 기능",
                        "성과 메트릭 시각화"
                    ],
                    "user_journey_optimization": [
                        "원클릭 생성",
                        "즉시 복사/공유",
                        "히스토리 관리",
                        "개인 설정 저장"
                    ]
                },
                "processed_data": {
                    "engagement_boosters": {
                        "gamification": ["평점 시스템", "배지 획득", "레벨 시스템"],
                        "social_features": ["결과 공유", "커뮤니티 투표", "트렌드 분석"],
                        "personalization": ["스타일 학습", "선호도 기반 추천", "맞춤형 톤"]
                    }
                },
                "metadata": {
                    "implementation_priority": "high",
                    "expected_impact": "user_retention_+40%"
                },
                "quality_score": 9.2
            },
            {
                "dataset_name": "AI_모델_고도화_전략",
                "content_type": "ai_enhancement",
                "raw_data": {
                    "model_improvements": [
                        "다중 톤 조합",
                        "문맥 인식 강화",
                        "실시간 학습",
                        "안전성 필터 고도화"
                    ],
                    "training_data_expansion": [
                        "다양한 연령대 데이터",
                        "문화권별 유머 패턴",
                        "시대별 트렌드 분석"
                    ]
                },
                "processed_data": {
                    "advanced_features": {
                        "emotion_ai": "감정 상태 기반 톤 자동 조절",
                        "context_awareness": "상황별 적절성 판단",
                        "style_mixing": "여러 톤의 하이브리드 조합",
                        "safety_ai": "실시간 위험도 모니터링"
                    }
                },
                "metadata": {
                    "technical_complexity": "high",
                    "research_value": "exceptional"
                },
                "quality_score": 9.5
            }
        ]
        
        return development_strategies
    
    def load_psychological_stimulation_research_data(self):
        """심리 자극 화법 연구 데이터를 로드합니다."""
        
        # 심리 자극 화법 연구 기반 고급 말투 데이터셋
        psychological_stimulation_datasets = [
            {
                "dataset_name": "심리_자극_화법_연구_v1",
                "content_type": "advanced_psychological_speech",
                "raw_data": {
                    "technique_name": "인지 부조화 유발 화법",
                    "definition": "상대방의 기존 신념과 현실 사이의 모순을 드러내어 인지적 불편함을 조성하는 고급 심리 기법",
                    "psychological_mechanisms": [
                        "인지 부조화 유발: 상대방의 신념 체계에 균열 생성",
                        "자기 정당화 욕구 자극: 방어적 반응 유도",
                        "인지적 불편함 조성: 정신적 긴장 상태 유발",
                        "논리적 모순 노출: 일관성 없는 행동 패턴 지적"
                    ],
                    "advanced_patterns": {
                        "contradiction_exposure": "상대방의 과거 발언과 현재 행동의 모순점 지적",
                        "belief_challenge": "핵심 신념에 대한 논리적 반박",
                        "reality_check": "이상과 현실의 차이 부각"
                    }
                },
                "processed_data": {
                    "effectiveness_metrics": {
                        "cognitive_impact": 9.5,
                        "behavioral_change_potential": 8.8,
                        "defensive_reaction_rate": 9.2,
                        "long_term_memory_retention": 9.0
                    },
                    "optimal_usage_scenarios": {
                        "target_types": ["완고한 사고방식", "고집스런 성격", "논리적 허점이 많은 주장"],
                        "psychological_vulnerabilities": ["자존감 과보호", "인지적 경직성", "논리적 일관성 부족"],
                        "effectiveness_conditions": ["충분한 배경 정보", "논리적 근거 확보", "감정적 안정 상태"]
                    }
                },
                "metadata": {
                    "technique_sophistication": "expert_level",
                    "psychological_accuracy": "research_validated",
                    "ethical_considerations": "constructive_purpose_only",
                    "usage_guidelines": "professional_context_recommended"
                },
                "quality_score": 9.7
            },
            {
                "dataset_name": "감정_조작_방어_화법_연구",
                "content_type": "emotional_manipulation_defense",
                "raw_data": {
                    "technique_name": "감정 조작 역공 화법",
                    "definition": "상대방의 감정 조작 시도를 역으로 이용하여 우위를 점하는 고급 심리 방어 기법",
                    "psychological_mechanisms": [
                        "감정 조작 탐지: 상대방의 의도 파악",
                        "감정적 거리두기: 객관적 시각 유지",
                        "논리적 재구성: 감정을 논리로 전환",
                        "주도권 역전: 대화의 흐름을 장악"
                    ],
                    "defense_patterns": {
                        "manipulation_detection": "상대방의 감정 조작 패턴 인식 및 노출",
                        "emotional_neutralization": "감정적 반응 차단 및 논리적 대응",
                        "power_reversal": "조작자를 역으로 심리적 압박 상황에 몰아넣기"
                    }
                },
                "processed_data": {
                    "effectiveness_metrics": {
                        "manipulation_resistance": 9.3,
                        "psychological_dominance": 8.7,
                        "emotional_stability": 9.1,
                        "communication_control": 8.9
                    },
                    "application_scenarios": {
                        "defensive_situations": ["가스라이팅 대응", "감정 협박 차단", "죄책감 유발 방어"],
                        "proactive_uses": ["대화 주도권 확보", "심리적 우위 점하기", "논리적 우월성 입증"],
                        "target_personalities": ["조작적 성격", "감정적 협박자", "논리 회피형"]
                    }
                },
                "metadata": {
                    "technique_sophistication": "advanced",
                    "psychological_safety": "high",
                    "ethical_rating": "defensive_use_justified",
                    "training_difficulty": "moderate_to_high"
                },
                "quality_score": 9.4
            }
        ]
        
        return psychological_stimulation_datasets
    
    def load_egen_teto_research_data(self):
        """에겐과 테토 페르소나 연구 데이터를 로드합니다."""
        
        # 에겐-테토 페르소나 연구 데이터셋
        egen_teto_datasets = [
            {
                "dataset_name": "에겐_페르소나_언어학적_분석",
                "content_type": "linguistic_persona_analysis",
                "raw_data": {
                    "persona_name": "에겐 (Egen)",
                    "origin": "일본어 エゲン에서 유래, 한국에서 성격 유형으로 재해석",
                    "core_characteristics": [
                        "높은 공감 능력과 감수성",
                        "갈등 회피 성향",
                        "관계 지향성",
                        "내향성 및 수동성"
                    ],
                    "linguistic_preferences": {
                        "primary_speech_level": "해요체 (두루높임)",
                        "sentence_types": ["의문문", "청유문"],
                        "vocabulary_domains": ["감성적", "정서적"],
                        "hedging_usage": "높음",
                        "conflict_management": "완화 및 회피"
                    }
                },
                "processed_data": {
                    "communication_strategies": {
                        "relationship_maintenance": "관계 노동을 통한 정서적 분위기 관리",
                        "cushion_words": ["혹시", "저기", "있잖아요", "실은"],
                        "indirect_expressions": ["...인 것 같아요", "...그런 느낌이에요", "...라고 볼 수도 있겠네요"],
                        "tag_questions": ["...그렇지 않아요?", "...맞죠?"]
                    },
                    "psychological_mechanisms": {
                        "empathy_prioritization": "타인의 감정 상태에 매우 민감하게 반응",
                        "harmony_seeking": "평화와 안정을 중시하여 갈등 상황 회피",
                        "emotional_labor": "상대방의 편안함과 정서적 안정감 제공에 집중"
                    }
                },
                "metadata": {
                    "linguistic_accuracy": "연구 검증됨",
                    "cultural_context": "현대 한국어 상대 높임법 기반",
                    "persona_sophistication": "관계 지향적 고급 소통",
                    "primary_goal": "정서적 유대감 형성"
                },
                "quality_score": 9.5
            },
            {
                "dataset_name": "테토_페르소나_언어학적_분석",
                "content_type": "linguistic_persona_analysis",
                "raw_data": {
                    "persona_name": "테토 (Teto)",
                    "origin": "보컬로이드 카사네 테토에서 파생된 성격 유형",
                    "core_characteristics": [
                        "논리 및 행동 지향성",
                        "자기주장과 단정성",
                        "직설적인 소통 방식",
                        "갈등 직면 성향",
                        "외향성 및 활동성"
                    ],
                    "linguistic_preferences": {
                        "primary_speech_level": "해체, 해라체 (상황에 따라 해요체)",
                        "sentence_types": ["평서문", "명령문"],
                        "vocabulary_domains": ["사실적", "행동 지향적"],
                        "hedging_usage": "낮음",
                        "conflict_management": "직접적 대면 및 해결"
                    }
                },
                "processed_data": {
                    "communication_strategies": {
                        "efficiency_optimization": "정보 전달의 속도와 명확성 극대화",
                        "direct_expressions": ["그래서 결론이 뭔데?", "이거부터 처리하자", "팩트는 이거야"],
                        "problem_solving_focus": "감정적 위로보다 실질적 해결책 제시",
                        "low_context_communication": "명시적 단어 중심의 저맥락 소통"
                    },
                    "psychological_mechanisms": {
                        "logic_prioritization": "감정보다 사실과 논리에 기반한 판단",
                        "assertiveness": "자신의 의견을 명확하고 단호하게 표현",
                        "action_orientation": "문제 회피보다 정면 돌파를 통한 해결"
                    }
                },
                "metadata": {
                    "linguistic_accuracy": "연구 검증됨",
                    "cultural_context": "효율성 중심의 현대 소통 방식",
                    "persona_sophistication": "목표 지향적 고급 소통",
                    "primary_goal": "문제 해결과 효율적 정보 전달"
                },
                "quality_score": 9.4
            }
        ]
        
        # 에겐-테토 비교 분석 데이터
        comparative_analysis = {
            "dataset_name": "에겐_테토_비교_언어학적_프로필",
            "content_type": "comparative_linguistic_analysis",
            "raw_data": {
                "comparison_framework": "한국어 상대 높임법 체계 기반",
                "key_differences": {
                    "communication_goal": {
                        "egen": "관계의 조화, 정서적 유대",
                        "teto": "거래의 효율성, 문제 해결"
                    },
                    "speech_level": {
                        "egen": "해요체 (두루높임) 중심",
                        "teto": "해체 (두루낮춤) 중심"
                    },
                    "sentence_preference": {
                        "egen": "의문문, 청유문",
                        "teto": "평서문, 명령문"
                    },
                    "contextuality": {
                        "egen": "고맥락 (High-Context): 관계, 분위기 중시",
                        "teto": "저맥락 (Low-Context): 명시적 단어 중시"
                    }
                }
            },
            "processed_data": {
                "scenario_analysis": {
                    "workplace_disagreement": {
                        "egen_approach": "해요체 + 완곡어법 + 관계 보호 우선",
                        "teto_approach": "규범적 존댓말 + 직접적 사실 제시 + 해결책 중심"
                    },
                    "friend_consolation": {
                        "egen_approach": "감정적 공감 + 정서적 지지 + 깊은 유대감",
                        "teto_approach": "간략한 인정 + 실질적 해결방안 + 행동 유도"
                    }
                },
                "practical_applications": {
                    "with_egen_persona": [
                        "감정 우선의 원칙",
                        "부드러운 제안 형식",
                        "경청과 확인 반복"
                    ],
                    "with_teto_persona": [
                        "용건 중심의 원칙",
                        "직설성의 수용",
                        "데이터와 사실 기반 소통"
                    ]
                }
            },
            "metadata": {
                "research_basis": "언어학적 실증 분석",
                "cultural_relevance": "현대 한국 디지털 문화",
                "practical_value": "대인관계 전략 수립에 활용 가능"
            },
            "quality_score": 9.7
        }
        
        return egen_teto_datasets, comparative_analysis
    
    def load_aposiopesis_research_data(self):
        """Aposiopesis Taunt(말줄임 조롱) 기법 연구 데이터를 로드합니다."""
        
        # Aposiopesis 기법 전용 데이터셋 - 확장된 버전
        aposiopesis_datasets = [
            {
                "dataset_name": "Aposiopesis_Taunt_기법_연구_v2",
                "content_type": "advanced_psychological_technique",
                "raw_data": {
                    "technique_name": "Aposiopesis Taunt (말줄임 조롱)",
                    "definition": "직접적인 공격을 회피하면서도 상대에게 더 큰 내상을 입히는 측면 공격 기법",
                    "psychological_mechanisms": [
                        "책임 회피: 직접 욕설을 하지 않아 공격자가 비난에서 자유로움",
                        "상상력 자극: 듣는 사람이 스스로 모욕을 완성하게 만듦",
                        "심리적 우위: 공격자가 고상한 사람으로 보이는 역설적 상황 창조",
                        "긴장감 조성: 미완성 문장으로 독자의 주의 집중 극대화",
                        "공감대 형성: '실수'를 통해 독자와의 친근감 형성"
                    ],
                    "structural_phases": {
                        "phase_1": "공격 시동 (Initiation): 대상의 약점을 암시하는 공격적 단어/문장 시작",
                        "phase_2": "급작스러운 중단 (Interruption): 핵심 모욕 단어 직전에 말을 끊음",
                        "phase_3": "위선적 수습 (Feigned Retraction): 실수를 급히 수습하며 선량함 어필",
                        "phase_4": "독자 참여 유도: 독자가 스스로 빈칸을 채우도록 유도"
                    },
                    "advanced_patterns": {
                        "power_level_variations": {
                            "1단계": "완전 실수인 척 (순수한 말실수 연출)",
                            "2단계": "애매한 의도 (실수인지 의도인지 모호)",
                            "3단계": "의도적 암시 (분명히 의도했지만 부인)"
                        },
                        "cultural_adaptations": {
                            "한국어_특화": ["높임법 활용", "상황 존댓말", "겸손 표현"],
                            "인터넷_문화": ["초성체 활용", "ㅋㅋ 등 웃음 표현", "당황 이모티콘"],
                            "세대별_맞춤": {
                                "MZ세대": "슬랭 + 줄임말",
                                "X세대": "정중한 표현 + 미안함",
                                "베이비부머": "격식 있는 표현"
                            }
                        }
                    }
                },
                "processed_data": {
                    "effectiveness_metrics": {
                        "psychological_impact": 9.2,
                        "viral_potential": 8.8,
                        "safety_level": 7.5,
                        "humor_sophistication": 9.0,
                        "memorability": 8.9,
                        "shareability": 9.1
                    },
                    "optimal_usage_scenarios": {
                        "darkness_levels": [1, 2, 3],
                        "target_demographics": ["MZ세대", "유머 감각 높은 사용자", "밈 문화 이해층", "언어유희 애호가"],
                        "psychological_targets": ["지적 허영심", "자존감 높은 대상", "논쟁적 성향", "완벽주의자"],
                        "content_contexts": ["SNS 댓글", "메신저 대화", "일상 대화", "온라인 토론"]
                    },
                    "generation_patterns": {
                        "initiation_templates": [
                            "와, 정말 머리가 나...",
                            "어쩜 그렇게 눈치가...",
                            "참 부지런...",
                            "딱 너 같은 사람한테 어울리는...",
                            "완전 특이한... 아니 개성적인...",
                            "진짜 대단한... 음...",
                            "이런 사람 처음 봐... 어?",
                            "와 센스가... 어이쿠"
                        ],
                        "interruption_markers": ["...", "—", "어?", "음...", "어이쿠", "앗", "어떡하지"],
                        "retraction_phrases": [
                            "아, 아닙니다. 제가 무슨 말을...",
                            "어이쿠, 말이 헛나왔네요. 죄송합니다.",
                            "방금 그 말은 못 들은 걸로 해주세요.",
                            "제가 요즘 생각이 많아서... 신경 쓰지 마세요.",
                            "아니에요, 칭찬이었는데 말이 이상하게...",
                            "죄송해요, 제가 표현력이 부족해서...",
                            "어머, 이상하게 들렸나요? 그런 뜻이 아니었는데...",
                            "앗, 실언이었어요. 무시해 주세요."
                        ],
                        "context_specific_templates": {
                            "외모_관련": "정말 독특한 스타일... 어?",
                            "능력_관련": "와 정말 재능이... 음...",
                            "성격_관련": "참 특별한 성격... 어이쿠",
                            "행동_관련": "그렇게 하시는 이유가... 아니에요"
                        }
                    },
                    "detection_markers": {
                        "aposiopesis_indicators": ["말줄임표", "급작스런 중단", "위선적 수습", "가짜 당황"],
                        "technique_signature": "의도적_미완성_+_선량함_연출"
                    }
                },
                "metadata": {
                    "technique_sophistication": "advanced",
                    "cultural_context": "korean_internet_culture",
                    "meme_potential": "high",
                    "psychological_accuracy": "peer_reviewed",
                    "technique_category": "aposiopesis_taunt",
                    "labeling_required": True,
                    "detection_confidence": 0.95
                },
                "quality_score": 9.6
            }
        ]
        
        # Aposiopesis 기법별 감정 패턴
        aposiopesis_emotion_patterns = [
            {
                "emotion_type": "소심한_복수심",
                "trigger_words": ["못_다한_말", "암시적_공격", "위선적_수습", "내재된_분노"],
                "psychological_effect": "직접 공격하지 않으면서도 상대방이 스스로 모욕을 완성하게 만드는 고도의 심리전",
                "intensity_level": 8,
                "target_demographic": "언어유희를 즐기는 사용자",
                "success_rate": 91.2
            },
            {
                "emotion_type": "지적_유희_추구",
                "trigger_words": ["언어적_장난", "수사법_활용", "문학적_기교", "반전_재미"],
                "psychological_effect": "고급 수사 기법 사용으로 독자의 지적 만족감과 우월감 동시 충족",
                "intensity_level": 7,
                "target_demographic": "교양층, 언어 감각 뛰어난 사용자",
                "success_rate": 88.7
            }
        ]
        
        # Aposiopesis 톤 분석
        aposiopesis_tone_analysis = [
            {
                "tone_name": "소심한_공격톤",
                "description": "하고 싶은 말은 많지만 용기가 없는 척하며 상대를 더 효과적으로 조롱",
                "emotion_triggers": ["위선적_착함", "가짜_당황", "계산된_실수"],
                "linguistic_features": {
                    "sentence_completion": "의도적_미완성",
                    "emotional_markers": "당황_표현",
                    "psychological_distance": "가까운_척_원거리",
                    "irony_level": "매우높음",
                    "sophistication": "고급"
                },
                "effectiveness_score": 9.1,
                "age_group": "20-40대",
                "cultural_context": "한국_눈치문화_반영",
                "sample_phrases": ["참 특이하... 아니 개성적이시네요", "와 정말 대단한... 어이쿠 제가 실언을"]
            },
            {
                "tone_name": "말줄임_밈톤",
                "description": "인터넷 밈 문화와 결합된 Aposiopesis 기법으로 바이럴 잠재력 극대화",
                "emotion_triggers": ["밈_문화", "바이럴_욕구", "세대_공감"],
                "linguistic_features": {
                    "meme_integration": "높음",
                    "viral_potential": "매우높음",
                    "generational_appeal": "MZ특화",
                    "social_sharing": "최적화됨"
                },
                "effectiveness_score": 8.9,
                "age_group": "10-30대",
                "cultural_context": "SNS_밈문화",
                "sample_phrases": ["완전 레전... 어? 뭐라고 하려했더라", "이거 실화... 아 맞다 칭찬이었지"]
            }
        ]
        
        return aposiopesis_datasets, aposiopesis_emotion_patterns, aposiopesis_tone_analysis

    def load_sample_research_data(self):
        """샘플 조롱 연구 데이터를 로드합니다 (실제 연구자료 대신)."""
        
        # 1. 감정선 패턴 데이터
        emotion_patterns = [
            {
                "emotion_type": "우월감_자극",
                "trigger_words": ["비교우위", "능력부족", "실수반복", "무지노출"],
                "psychological_effect": "독자가 자신의 상대적 우월성을 인식하게 하여 만족감 증대",
                "intensity_level": 8,
                "target_demographic": "20-40대 직장인",
                "success_rate": 87.5
            },
            {
                "emotion_type": "공감대_형성",
                "trigger_words": ["공통불만", "사회적스트레스", "일상짜증", "집단경험"],
                "psychological_effect": "독자의 경험과 연결하여 강한 동조감 유발",
                "intensity_level": 9,
                "target_demographic": "MZ세대",
                "success_rate": 92.3
            },
            {
                "emotion_type": "카타르시스_제공",
                "trigger_words": ["억압감정해소", "속마음대변", "금기표현", "직설적비판"],
                "psychological_effect": "독자가 말하지 못했던 내용을 대신 표현하여 해방감 제공",
                "intensity_level": 10,
                "target_demographic": "전연령",
                "success_rate": 94.7
            }
        ]
        
        # 2. 조롱 톤 분석 데이터
        tone_analysis = [
            {
                "tone_name": "MZ세대_반말톤",
                "description": "인터넷 슬랭과 줄임말을 활용한 친근하고 직설적인 표현",
                "emotion_triggers": ["세대공감", "언어유희", "반항심"],
                "linguistic_features": {
                    "sentence_length": "짧음",
                    "formality": "매우낮음",
                    "slang_usage": "높음",
                    "abbreviation": "매우높음",
                    "emotional_intensity": "중간"
                },
                "effectiveness_score": 8.9,
                "age_group": "10-30대",
                "cultural_context": "한국_인터넷문화",
                "sample_phrases": ["진짜 ㅋㅋ", "완전 레전드", "이거 실화냐", "ㄹㅇ 개웃김"]
            },
            {
                "tone_name": "풍자적_지적체",
                "description": "고급 어휘와 은유를 통한 간접적이지만 날카로운 비판",
                "emotion_triggers": ["지적우월감", "문학적만족", "품격유지"],
                "linguistic_features": {
                    "sentence_length": "중간",
                    "formality": "높음",
                    "metaphor_usage": "높음",
                    "vocabulary_level": "고급",
                    "irony_level": "매우높음"
                },
                "effectiveness_score": 9.2,
                "age_group": "30-50대",
                "cultural_context": "교양층_지식인",
                "sample_phrases": ["참으로 흥미로운 관점이군요", "그런 해석도 가능하겠네요", "독창적인 사고방식"]
            }
        ]
        
        # 3. 학습용 데이터셋
        training_datasets = [
            {
                "dataset_name": "감정유발_조롱패턴_분석",
                "content_type": "emotion_trigger_analysis",
                "raw_data": {
                    "source": "조롱 콘텐츠 감정선 빅데이터 분석",
                    "sample_size": 10000,
                    "data_period": "2023-2024",
                    "analysis_method": "sentiment_analysis + psychological_response"
                },
                "processed_data": {
                    "emotion_categories": ["우월감", "공감", "카타르시스", "사회적승인"],
                    "effectiveness_metrics": {
                        "engagement_rate": 0.89,
                        "sharing_probability": 0.76,
                        "emotional_intensity": 8.3
                    },
                    "demographic_insights": {
                        "age_distribution": {"10대": 0.23, "20대": 0.31, "30대": 0.28, "40대+": 0.18},
                        "gender_response": {"male": 0.52, "female": 0.48},
                        "cultural_sensitivity": "korean_context_optimized"
                    }
                },
                "metadata": {
                    "research_focus": "emotional_targeting_optimization",
                    "validation_method": "A/B_testing",
                    "quality_indicators": ["psychological_accuracy", "cultural_appropriateness", "safety_score"]
                },
                "quality_score": 9.1
            },
            {
                "dataset_name": "톤별_효과성_측정",
                "content_type": "tone_effectiveness_study",
                "raw_data": {
                    "tone_categories": 17,
                    "test_samples": 5000,
                    "response_metrics": ["humor_rating", "shareability", "memorability"]
                },
                "processed_data": {
                    "top_performing_tones": ["MZ반말", "풍자적", "에겐톤"],
                    "demographic_preferences": {
                        "gen_z": ["MZ반말", "정신나간톤", "틱톡트렌드"],
                        "millennials": ["풍자적", "냉소톤", "유머러스"],
                        "gen_x": ["논리적반박", "에겐톤", "감성에세이"]
                    },
                    "psychological_mechanisms": {
                        "superiority_complex": 0.87,
                        "in_group_solidarity": 0.79,
                        "cathartic_release": 0.92
                    }
                },
                "metadata": {
                    "research_focus": "tone_optimization_by_demographic",
                    "cultural_context": "korean_digital_culture_2024"
                },
                "quality_score": 8.8
            }
        ]
        
        # 4. 흑화 단계 데이터 (연구 자료 기반)
        darkness_levels = [
            {
                "level_name": "순수 유머",
                "level_number": 1,
                "description": "완전히 건전하고 밝은 유머로, 누구나 편안하게 웃을 수 있는 수준",
                "intensity_score": 2,
                "safety_level": 5,
                "psychological_effects": {
                    "target_emotion": "즐거움",
                    "side_effects": "없음",
                    "social_impact": "긍정적 분위기 조성"
                },
                "target_emotions": ["기쁨", "유쾌함", "친근감"],
                "example_characteristics": ["말장난", "귀여운 비유", "상황의 우스꽝스러움"],
                "usage_guidelines": "모든 상황에서 안전하게 사용 가능"
            },
            {
                "level_name": "가벼운 놀림",
                "level_number": 2,
                "description": "친구 사이의 장난스러운 놀림 수준으로, 애정이 담긴 가벼운 지적",
                "intensity_score": 4,
                "safety_level": 4,
                "psychological_effects": {
                    "target_emotion": "친근한 부끄러움",
                    "side_effects": "미미한 수치심",
                    "social_impact": "친밀감 증대 또는 경미한 불편함"
                },
                "target_emotions": ["부끄러움", "친근감", "약간의 당황"],
                "example_characteristics": ["습관 지적", "귀여운 실수 언급", "장난스러운 과장"],
                "usage_guidelines": "친한 관계에서만 사용 권장"
            },
            {
                "level_name": "날카로운 지적",
                "level_number": 3,
                "description": "문제점을 명확히 짚어내는 직설적인 비판이지만 건설적 의도 포함",
                "intensity_score": 6,
                "safety_level": 3,
                "psychological_effects": {
                    "target_emotion": "깨달음과 부끄러움",
                    "side_effects": "자기반성 유도",
                    "social_impact": "긴장감 조성하지만 개선 동기 부여"
                },
                "target_emotions": ["수치심", "깨달음", "자기반성"],
                "example_characteristics": ["논리적 모순 지적", "행동 패턴 분석", "현실적 비판"],
                "usage_guidelines": "건설적 피드백 목적으로만 사용"
            },
            {
                "level_name": "강한 조롱",
                "level_number": 4,
                "description": "상당한 감정적 타격을 주는 수준의 조롱으로, 우월감 자극이 주목적",
                "intensity_score": 8,
                "safety_level": 2,
                "psychological_effects": {
                    "target_emotion": "강한 수치심과 열등감",
                    "side_effects": "자존감 타격, 방어기제 활성화",
                    "social_impact": "관계 악화 가능성 높음"
                },
                "target_emotions": ["분노", "수치심", "열등감", "복수심"],
                "example_characteristics": ["신랄한 비꼬기", "약점 집중 공격", "사회적 지위 비하"],
                "usage_guidelines": "사용 전 신중한 고려 필요, 관계 파괴 위험성 인지"
            },
            {
                "level_name": "파괴적 공격",
                "level_number": 5,
                "description": "심각한 정신적 타격을 가하는 수준으로, 극도로 위험한 단계",
                "intensity_score": 10,
                "safety_level": 1,
                "psychological_effects": {
                    "target_emotion": "극도의 수치심과 분노",
                    "side_effects": "장기적 트라우마, 보복 행동 유발",
                    "social_impact": "관계 완전 파괴, 사회적 갈등 심화"
                },
                "target_emotions": ["극도의 분노", "절망감", "복수욕", "사회적 고립감"],
                "example_characteristics": ["인격 모독", "사생활 폭로", "사회적 매장"],
                "usage_guidelines": "절대 사용 금지 - 법적, 윤리적 문제 발생 가능"
            }
        ]
        
        return emotion_patterns, tone_analysis, training_datasets, darkness_levels
    
    def process_and_store_research_data(self):
        """연구 데이터를 처리하고 데이터베이스에 저장합니다."""
        emotion_patterns, tone_analysis, training_datasets, darkness_levels = self.load_sample_research_data()
        
        print("📊 조롱 연구 데이터 처리 시작...")
        
        # 감정선 패턴 저장
        for pattern in emotion_patterns:
            pattern_id = self.db.insert_emotion_pattern(**pattern)
            print(f"✅ 감정 패턴 저장 완료: {pattern['emotion_type']} (ID: {pattern_id})")
        
        # 톤 분석 데이터 저장
        for tone in tone_analysis:
            tone_id = self.db.insert_taunt_tone(**tone)
            print(f"✅ 톤 분석 저장 완료: {tone['tone_name']} (ID: {tone_id})")
        
        # 학습 데이터셋 저장
        for dataset in training_datasets:
            dataset_id = self.db.insert_training_data(**dataset)
            print(f"✅ 학습 데이터 저장 완료: {dataset['dataset_name']} (ID: {dataset_id})")
        
        # 흑화 단계 데이터 저장
        for level in darkness_levels:
            level_id = self.db.insert_darkness_level(**level)
            print(f"✅ 흑화 단계 저장 완료: {level['level_name']} (ID: {level_id})")
        
        # 심리 자극 화법 연구 데이터 처리
        print("\n🧠 심리 자극 화법 연구 데이터 처리 시작...")
        psychological_datasets = self.load_psychological_stimulation_research_data()
        
        # 심리 자극 화법 데이터셋 저장
        for dataset in psychological_datasets:
            dataset_id = self.db.insert_training_data(**dataset)
            print(f"✅ 심리 자극 화법 데이터셋 저장 완료: {dataset['dataset_name']} (ID: {dataset_id})")
        
        # Aposiopesis 연구 데이터 처리
        print("\n🔬 Aposiopesis Taunt 기법 연구 데이터 처리 시작...")
        aposiopesis_datasets, aposiopesis_emotions, aposiopesis_tones = self.load_aposiopesis_research_data()
        
        # Aposiopesis 데이터셋 저장
        for dataset in aposiopesis_datasets:
            dataset_id = self.db.insert_training_data(**dataset)
            print(f"✅ Aposiopesis 데이터셋 저장 완료: {dataset['dataset_name']} (ID: {dataset_id})")
        
        # Aposiopesis 감정 패턴 저장
        for pattern in aposiopesis_emotions:
            pattern_id = self.db.insert_emotion_pattern(**pattern)
            print(f"✅ Aposiopesis 감정 패턴 저장 완료: {pattern['emotion_type']} (ID: {pattern_id})")
        
        # Aposiopesis 톤 분석 저장
        for tone in aposiopesis_tones:
            tone_id = self.db.insert_taunt_tone(**tone)
            print(f"✅ Aposiopesis 톤 분석 저장 완료: {tone['tone_name']} (ID: {tone_id})")
        
        # 에겐-테토 페르소나 연구 데이터 처리
        print("\n🎭 에겐-테토 페르소나 연구 데이터 처리 시작...")
        egen_teto_datasets, comparative_analysis = self.load_egen_teto_research_data()
        
        # 에겐-테토 데이터셋 저장
        for dataset in egen_teto_datasets:
            dataset_id = self.db.insert_training_data(**dataset)
            print(f"✅ 에겐-테토 데이터셋 저장 완료: {dataset['dataset_name']} (ID: {dataset_id})")
        
        # 비교 분석 데이터 저장
        comparison_id = self.db.insert_training_data(**comparative_analysis)
        print(f"✅ 에겐-테토 비교 분석 저장 완료: {comparative_analysis['dataset_name']} (ID: {comparison_id})")
        
        print("🎉 모든 연구 데이터 처리 및 저장 완료!")
        
        # 프로젝트 발전 전략 데이터 처리
        development_data = self.load_project_development_strategy_data()
        for data in development_data:
            data_id = self.db.insert_training_data(**data)
            print(f"✅ 발전 전략 데이터 저장 완료: {data['dataset_name']} (ID: {data_id})")
    
    def analyze_development_priorities(self):
        """발전 전략의 우선순위를 분석합니다."""
        strategies = self.load_project_development_strategy_data()
        
        # 즉시 구현 가능한 기능들
        immediate_features = []
        research_features = []
        
        for strategy in strategies:
            if strategy['metadata'].get('implementation_priority') == 'high':
                immediate_features.append(strategy)
            else:
                research_features.append(strategy)
        
        return {
            'immediate_implementation': immediate_features,
            'research_development': research_features
        }
    
    def generate_gemini_training_prompt(self):
        """Gemini 모델 학습용 프롬프트를 생성합니다."""
        training_data = self.db.get_training_data_for_gemini(limit=100)
        
        prompt = """
# 조롱 텍스트 생성 AI 모델 학습 데이터

## 감정선 겨냥 시스템 학습 원칙

### 1. 심리적 메커니즘 이해
- **우월감 자극**: 독자가 대상보다 나은 위치에 있다고 느끼게 함
- **공감대 형성**: 독자의 경험과 연결하여 동조감 유발
- **카타르시스 제공**: 억압된 감정의 해소와 대리만족
- **사회적 승인욕구**: 타인과 공유하고 인정받고 싶은 욕구 자극

### 2. 톤별 효과성 데이터
"""
        
        for data in training_data[:10]:  # 상위 10개 데이터만 예시로 포함
            if data['processed_data']:
                prompt += f"\n**{data['dataset_name']}**\n"
                prompt += f"- 감정 타입: {data.get('emotion_type', 'N/A')}\n"
                prompt += f"- 톤: {data.get('tone_name', 'N/A')}\n"
                if data['processed_data'].get('effectiveness_metrics'):
                    metrics = data['processed_data']['effectiveness_metrics']
                    prompt += f"- 참여율: {metrics.get('engagement_rate', 'N/A')}\n"
                    prompt += f"- 공유 확률: {metrics.get('sharing_probability', 'N/A')}\n"
                prompt += "\n"
        
        prompt += """
### 3. 학습 목표
이 데이터를 바탕으로 다음과 같은 능력을 개발하세요:
1. 대상별 최적 감정선 겨냥 전략 수립
2. 톤에 따른 효과적 표현 기법 적용
3. 독자 심리 분석 기반 개인화된 조롱 텍스트 생성
4. 문화적 맥락과 세대별 특성 반영
5. 안전성과 자극성을 고려한 균형잡힌 유머 창작

### 4. 출력 품질 기준
- 심리적 정확성: 의도한 감정 반응 유발
- 문화적 적절성: 한국 디지털 문화 맥락 반영
- 안전성: 인격 모독이나 차별 없는 건전한 유머
- 창의성: 예측 가능하지 않은 참신한 표현
- 효과성: 높은 공감과 공유 욕구 자극
"""
        
        return prompt
    
    def export_training_data_for_gemini(self, output_file="gemini_training_data.jsonl"):
        """Gemini 모델 학습용 JSONL 파일을 생성합니다."""
        training_data = self.db.get_training_data_for_gemini()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for data in training_data:
                training_sample = {
                    "input": {
                        "research_context": data['dataset_name'],
                        "emotion_type": data.get('emotion_type'),
                        "tone": data.get('tone_name'),
                        "trigger_words": data.get('trigger_words', []),
                        "linguistic_features": data.get('linguistic_features', {})
                    },
                    "output": {
                        "processed_insights": data['processed_data'],
                        "quality_score": data.get('quality_score'),
                        "metadata": data['metadata']
                    },
                    "timestamp": datetime.now().isoformat()
                }
                f.write(json.dumps(training_sample, ensure_ascii=False) + '\n')
        
        print(f"📁 Gemini 학습 데이터 파일 생성 완료: {output_file}")
        print(f"📊 총 {len(training_data)}개의 학습 샘플 포함")

if __name__ == "__main__":
    processor = TauntResearchProcessor()
    processor.process_and_store_research_data()
    
    # Gemini 학습용 프롬프트 생성
    training_prompt = processor.generate_gemini_training_prompt()
    print("\n" + "="*50)
    print("🤖 Gemini 학습용 프롬프트:")
    print("="*50)
    print(training_prompt)
    
    # 학습 데이터 파일 생성
    processor.export_training_data_for_gemini()
