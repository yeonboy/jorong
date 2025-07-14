import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import re
from collections importCounter

class NewsYoutubeTrainingProcessor:
    def __init__(self):
        self.processed_data = []

        # 플랫폼별 언어적 특징 매핑
        self.platform_characteristics = {
            'naver_news': {
                'formality': 'medium_high',
                'emotion_expression': 'restrained_anger',
                'political_sensitivity': 'high',
                'criticism_style': 'direct_frustration'
            },
            'youtube': {
                'formality': 'very_low',
                'emotion_expression': 'extreme_enthusiasm',
                'slang_usage': 'very_high',
                'reaction_intensity': 'amplified'
            },
            'daum_news': {
                'formality': 'medium',
                'emotion_expression': 'empathetic_concern',
                'social_awareness': 'high',
                'tone': 'considerate'
            }
        }

        # 감정 강도별 표현 패턴
        self.intensity_patterns = {
            'extreme_positive': ['와...', '진짜 국보급', '명작 스멜', '1일 1직캠', '알고리즘님 감사'],
            'extreme_negative': ['이게 대책이라고', '민주주의 맞냐', '다음 선거 때 보자'],
            'empathetic_concern': ['진짜 아프긴 한가 보네', '고생 많으십니다', '정부는 대책 좀'],
            'humorous_understanding': ['개웃기네 진짜', '공감은 간다', '서로 이해하려는 노력'],
            'social_despair': ['상대적 박탈감', '서민들은 한 평생', '이런 기사 안 보고 싶다']
        }

        self.platform_patterns = {
            'naver_news': {
                'characteristics': ['냉소적', '정치적', '현실적'],
                'common_phrases': ['이게 대책이라고', '서민들은', '다음 선거 때']
            },
            'youtube': {
                'characteristics': ['감탄사', '극찬', '밈 문화'],
                'common_phrases': ['국보급', '명작 스멜', '알고리즘님 감사']
            },
            'daum_news': {
                'characteristics': ['감정적', '공감적', '걱정'],
                'common_phrases': ['마음이', '고생 많으십니다', '조심하세요']
            }
        }

    def analyze_comment_psychology(self, comment_data: Dict[str, Any]) -> Dict[str, Any]:
        """댓글의 심리적 메커니즘 분석"""
        content = comment_data.get('content', '')
        speech_pattern = comment_data.get('speech_pattern', '')
        emotional_intensity = comment_data.get('emotional_intensity', 0)
        stance = comment_data.get('stance', 'neutral')

        # 심리적 동기 분석
        psychological_drivers = []

        if stance == 'strong_negative' and emotional_intensity > 9:
            psychological_drivers.extend(['분노_표출', '정치적_좌절감', '시스템_불신'])
        elif stance == 'strong_positive' and emotional_intensity > 9:
            psychological_drivers.extend(['팬덤_소속감', '집단_정체성', '감정_과몰입'])
        elif 'empathetic' in speech_pattern:
            psychological_drivers.extend(['사회적_공감', '타인_배려', '집단_연대'])
        elif 'humorous' in speech_pattern:
            psychological_drivers.extend(['긴장_완화', '세대_이해', '균형_감각'])

        # 언어적 전략 분석
        linguistic_strategies = self._extract_linguistic_strategies(content, speech_pattern)

        # 바이럴 요소 식별
        viral_elements = self._identify_viral_elements(comment_data)

        return {
            'psychological_drivers': psychological_drivers,
            'linguistic_strategies': linguistic_strategies,
            'viral_elements': viral_elements,
            'engagement_prediction': self._predict_engagement(comment_data)
        }

    def _extract_linguistic_strategies(self, content: str, speech_pattern: str) -> List[str]:
        """언어적 전략 추출"""
        strategies = []

        # 수사 기법 분석
        if '...' in content:
            strategies.append('말줄임_여운')
        if re.search(r'ㅋ{2,}', content):
            strategies.append('웃음_표현_증폭')
        if '?' in content and '맞냐' in content:
            strategies.append('반문법_압박')
        if '진짜' in content or '완전' in content:
            strategies.append('강화어_사용')
        if '님' in content:
            strategies.append('존댓말_친근감')

        # 플랫폼별 특징
        if 'youtube' in speech_pattern:
            strategies.extend(['감탄사_과용', '구독_유도', '알고리즘_언급'])
        elif 'news' in speech_pattern:
            strategies.extend(['정치적_비판', '사회_현실_지적', '정책_평가'])

        return strategies

    def _identify_viral_elements(self, comment_data: Dict[str, Any]) -> List[str]:
        """바이럴 요소 식별"""
        viral_elements = []

        score = comment_data.get('score', 0)
        comments = comment_data.get('num_comments', 0)
        content = comment_data.get('content', '')

        # 수치 기반 바이럴 요소
        if score > 10000:
            viral_elements.append('초고참여도')
        if comments > 2000:
            viral_elements.append('논쟁_유발성')

        # 내용 기반 바이럴 요소
        if any(word in content for word in ['국보급', '명작', '레전드']):
            viral_elements.append('극찬_표현')
        if any(word in content for word in ['민주주의', '선거', '정부']):
            viral_elements.append('정치적_논란성')
        if '공감' in content or '이해' in content:
            viral_elements.append('공감대_형성')

        return viral_elements

    def _predict_engagement(self, comment_data: Dict[str, Any]) -> Dict[str, Any]:
        """참여도 예측"""
        emotional_intensity = comment_data.get('emotional_intensity', 0)
        data_type = comment_data.get('data_type', '')
        stance = comment_data.get('stance', 'neutral')

        # 참여도 예측 모델
        base_score = emotional_intensity * 10

        # 데이터 타입별 가중치
        type_multipliers = {
            'political_opposition': 1.5,
            'fandom_worship': 1.3,
            'generational_humor': 1.2,
            'social_criticism': 1.1,
            'entertainment_reaction': 1.0
        }

        multiplier = type_multipliers.get(data_type, 1.0)
        predicted_score = base_score * multiplier

        return {
            'predicted_engagement_score': predicted_score,
            'viral_probability': min(predicted_score / 100, 1.0),
            'controversy_level': 'high' if 'negative' in stance else 'medium'
        }

    def generate_tone_mapping(self, comment_data: Dict[str, Any]) -> List[str]:
        """댓글 특성에 맞는 톤 매핑"""
        speech_pattern = comment_data.get('speech_pattern', '')
        data_type = comment_data.get('data_type', '')
        stance = comment_data.get('stance', 'neutral')
        emotional_intensity = comment_data.get('emotional_intensity', 0)

        tone_recommendations = []

        # 패턴별 톤 매핑
        if 'cynical' in speech_pattern:
            tone_recommendations.extend(['냉소 톤', '논리적으로 반박하는', '풍자적'])
        elif 'praise' in speech_pattern:
            tone_recommendations.extend(['애교 톤', '감성 에세이 톤', '유머러스하게'])
        elif 'empathetic' in speech_pattern:
            tone_recommendations.extend(['에겐톤', '감성 에세이 톤'])
        elif 'aggressive' in speech_pattern:
            tone_recommendations.extend(['논리적으로 반박하는', '냉소 톤'])
        elif 'fandom' in speech_pattern:
            tone_recommendations.extend(['애교 톤', 'MZ 반말 톤', '정신나간 톤'])
        elif 'relatable' in speech_pattern:
            tone_recommendations.extend(['MZ 반말 톤', '유머러스하게'])

        # 감정 강도별 추가 톤
        if emotional_intensity > 9:
            tone_recommendations.extend(['정신나간 톤', '소심한 공격 톤'])
        elif emotional_intensity > 7:
            tone_recommendations.extend(['풍자적', '비꼬는 듯이'])

        return list(set(tone_recommendations))

    def process_news_youtube_data(self, raw_data: List[Dict]) -> List[Dict]:
        """뉴스/유튜브 댓글 데이터를 학습용으로 변환"""
        processed_data = []

        for item in raw_data:
            processed_item = {
                'raw_data': item,
                'processed_at': datetime.now().isoformat(),
                'platform_type': self._identify_platform(item.get('source', '')),
                'speech_pattern': item.get('speech_pattern', 'unknown'),
                'emotional_intensity': item.get('emotional_intensity', 5.0),
                'psychological_drivers': self._extract_psychological_drivers(item),
                'viral_potential': self._calculate_viral_potential(item),
                'recommended_adaptations': self._suggest_adaptations(item)
            }
            processed_data.append(processed_item)

        return processed_data

    def _extract_platform(self, source: str) -> str:
        """소스에서 플랫폼 추출"""
        if 'naver' in source:
            return 'naver_news'
        elif 'youtube' in source:
            return 'youtube'
        elif 'daum' in source:
            return 'daum_news'
        return 'unknown'

    def _identify_platform(self, source: str) -> str:
        """소스를 기반으로 플랫폼을 식별합니다."""
        if 'naver' in source:
            return 'naver_news'
        elif 'youtube' in source:
            return 'youtube'
        elif 'daum' in source:
            return 'daum_news'
        else:
            return 'unknown'

    def _extract_psychological_drivers(self, item: Dict) -> List[str]:
        """심리적 동기 요소를 추출합니다."""
        drivers = []
        content = item.get('content', '').lower()
        stance = item.get('stance', 'neutral')

        # 심리적 동기 패턴
        if stance == 'negative':
            drivers.append('frustration_release')
        elif stance == 'positive':
            drivers.append('validation_seeking')

        if '진짜' in content or '완전' in content:
            drivers.append('emphasis_need')
        if '감사' in content or '고마' in content:
            drivers.append('gratitude_expression')
        if '걱정' in content or '조심' in content:
            drivers.append('care_showing')

        return drivers

    def _calculate_viral_potential(self, item: Dict) -> float:
        """바이럴 잠재력을 계산합니다."""
        score = item.get('score', 0)
        comments = item.get('num_comments', 0)
        emotional_intensity = item.get('emotional_intensity', 5.0)

        # 가중치 적용한 바이럴 점수
        viral_score = (score * 0.4 + comments * 0.3 + emotional_intensity * 1000 * 0.3) / 10000
        return min(viral_score, 1.0)

    def _suggest_adaptations(self, item: Dict) -> List[str]:
        """적응 방안을 제안합니다."""
        adaptations = []
        platform = self._identify_platform(item.get('source', ''))

        if platform == 'naver_news':
            adaptations.extend(['냉소 톤', '논리적으로 반박하는'])
        elif platform == 'youtube':
            adaptations.extend(['유머러스하게', 'MZ 반말 톤'])
        elif platform == 'daum_news':
            adaptations.extend(['감성 에세이 톤', '에겐톤'])

        return adaptations[:2]  # 최대 2개

    def generate_insights(self, processed_data: List[Dict]) -> Dict[str, Any]:
        """처리된 데이터에서 인사이트 생성"""
        insights = {
            'total_samples': len(processed_data),
            'platform_distribution': {},
            'emotional_intensity_stats': {},
            'top_psychological_drivers': [],
            'recommended_tones': {},
            'viral_potential_analysis': {}
        }

        # 플랫폼 분포
        platform_counts = Counter([sample['raw_data']['platform'] for sample in processed_data])
        insights['platform_distribution'] = dict(platform_counts)

        # 감정 강도 통계
        intensities = [sample['raw_data']['emotional_intensity'] for sample in processed_data]
        insights['emotional_intensity_stats'] = {
            'average': sum(intensities) / len(intensities) if intensities else 0,
            'max': max(intensities) if intensities else 0,
            'extreme_count': len([i for i in intensities if i > 9])
        }

        # 심리적 동기 분석
        all_drivers = []
        for sample in processed_data:
            all_drivers.extend(sample['processed_data']['psychology_analysis']['psychological_drivers'])
        insights['top_psychological_drivers'] = Counter(all_drivers).most_common(10)

        # 톤 추천 분석
        all_tones = []
        for sample in processed_data:
            all_tones.extend(sample['processed_data']['tone_recommendations'])
        insights['recommended_tones'] = Counter(all_tones).most_common(15)

        # 바이럴 잠재력 분석
        viral_scores = [sample['processed_data']['viral_potential'] for sample in processed_data]
        insights['viral_potential_analysis'] = {
            'average_viral_score': sum(viral_scores) / len(viral_scores) if viral_scores else 0,
            'high_viral_count': len([v for v in viral_scores if v > 0.7])
        }

        return insights

    def generate_insights(self, processed_data: List[Dict]) -> Dict:
        """처리된 데이터에서 인사이트를 생성합니다."""
        total_samples = len(processed_data)

        # 플랫폼 분포
        platform_distribution = {}
        for item in processed_data:
            platform = item['platform_type']
            platform_distribution[platform] = platform_distribution.get(platform, 0) + 1

        # 심리적 동기 분석
        psychological_drivers = {}
        for item in processed_data:
            for driver in item['psychological_drivers']:
                psychological_drivers[driver] = psychological_drivers.get(driver, 0) + 1

        # 바이럴 잠재력 분석
        viral_scores = [item['viral_potential'] for item in processed_data]
        high_viral_threshold = 0.7
        high_viral_count = len([score for score in viral_scores if score > high_viral_threshold])

        # 감정 강도 통계
        emotional_intensities = [item['emotional_intensity'] for item in processed_data]
        extreme_threshold = 8.5
        extreme_count = len([intensity for intensity in emotional_intensities if intensity > extreme_threshold])

        # 추천 톤 분석
        recommended_tones = {}
        for item in processed_data:
            for tone in item['recommended_adaptations']:
                recommended_tones[tone] = recommended_tones.get(tone, 0) + 1

        return {
            'total_samples': total_samples,
            'platform_distribution': platform_distribution,
            'top_psychological_drivers': sorted(psychological_drivers.items(), key=lambda x: x[1], reverse=True),
            'viral_potential_analysis': {
                'average_viral_score': sum(viral_scores) / len(viral_scores) if viral_scores else 0,
                'high_viral_count': high_viral_count,
                'viral_rate': high_viral_count / total_samples if total_samples > 0 else 0
            },
            'emotional_intensity_stats': {
                'average': sum(emotional_intensities) / len(emotional_intensities) if emotional_intensities else 0,
                'extreme_count': extreme_count,
                'extreme_rate': extreme_count / total_samples if total_samples > 0 else 0
            },
            'recommended_tones': sorted(recommended_tones.items(), key=lambda x: x[1], reverse=True)
        }

def process_news_youtube_training_data():
    """뉴스/유튜브 댓글 학습 데이터 처리 메인 함수"""
    processor = NewsYoutubeTrainingProcessor()

    # 첨부된 데이터 로드
    comment_data = [
        {
            "source": "simulated_naver_news_comment",
            "title": "[속보] 정부, 3기 신도시 추가 공급 및 DSR 규제 완화 발표",
            "content": "이게 대책이라고 내놓은건가? 집값 잡을 생각은 없고 그냥 건설사들 배만 불려주자는 거잖아. 서민들은 어차피 대출도 안나와서 그림의 떡임.",
            "score": 5820,
            "num_comments": 1250,
            "data_type": "policy_criticism",
            "speech_pattern": "news_comment_cynical",
            "emotional_intensity": 9.3,
            "stance": "negative"
        },
        {
            "source": "simulated_youtube_comment",
            "title": "영화 '광해 2' 예고편 최초 공개! 배우 이병헌 1인 2역 복귀",
            "content": "와... 예고편만 봤는데 벌써 명작 스멜이 난다. 이병헌 연기는 진짜 국보급이네. 천만 관객 그냥 넘을 듯 ㄷㄷ",
            "score": 12000,
            "num_comments": 3400,
            "data_type": "entertainment_reaction",
            "speech_pattern": "youtube_comment_praise",
            "emotional_intensity": 9.0,
            "stance": "positive"
        },
        {
            "source": "simulated_daum_news_comment",
            "title": "역대급 폭염에 전력수급 '경고'… 7월인데 벌써 38도",
            "content": "지구가 진짜 아프긴 한가 보네요... 다들 더위 조심하시고, 특히 야외에서 일하시는 분들 정말 고생 많으십니다. 정부는 전기세 지원 같은 대책 좀 세워주세요.",
            "score": 3500,
            "num_comments": 880,
            "data_type": "social_concern",
            "speech_pattern": "news_comment_empathetic",
            "emotional_intensity": 7.5,
            "stance": "concerned_neutral"
        },
        {
            "source": "simulated_youtube_comment",
            "title": "요즘 MZ 신입사원 특징.mp4 (feat. 라떼는 말이야)",
            "content": "ㅋㅋㅋㅋㅋ 개웃기네 진짜 우리 회사 부장님 보는 줄. 근데 솔직히 서로 이해하려는 노력이 필요함. 저렇게까지 하는 신입은 없지만 어느 정도 공감은 간다.",
            "score": 8800,
            "num_comments": 2100,
            "data_type": "generational_humor",
            "speech_pattern": "youtube_comment_relatable",
            "emotional_intensity": 8.2,
            "stance": "humorous_neutral"
        },
        {
            "source": "simulated_naver_news_comment",
            "title": "논란의 'OOO법' 국회 통과… 시민단체 강력 반발",
            "content": "이게 민주주의 국가 맞냐? 국민 의견은 싹 다 무시하고 그냥 밀어붙이네. 다음 선거 때 보자.",
            "score": 7600,
            "num_comments": 3200,
            "data_type": "political_opposition",
            "speech_pattern": "news_comment_aggressive",
            "emotional_intensity": 9.8,
            "stance": "strong_negative"
        },
        {
            "source": "simulated_youtube_comment",
            "title": "[4K 직캠] XXX 아이돌 신곡 'FANTASY' 쇼케이스 무대",
            "content": "알고리즘님, 저를 이곳으로 인도해주셔서 감사합니다... 매일 보러 오겠습니다. 1일 1직캠 필수.",
            "score": 25000,
            "num_comments": 5500,
            "data_type": "fandom_worship",
            "speech_pattern": "youtube_comment_fandom",
            "emotional_intensity": 9.5,
            "stance": "strong_positive"
        },
        {
            "source": "simulated_daum_news_comment",
            "title": "[단독] 유명 연예인 OOO, 100억대 건물 매입",
            "content": "이런 기사 좀 안 보고 싶다. 상대적 박탈감만 드네. 서민들은 한 평생 모아도 대출 갚기 힘든데...",
            "score": 4100,
            "num_comments": 1500,
            "data_type": "social_criticism",
            "speech_pattern": "news_comment_despair",
            "emotional_intensity": 8.0,
            "stance": "negative"
        },
        {
            "source": "simulated_youtube_comment",
            "title": "10분만에 이해하는 양자역학",
            "content": "와... 설명을 너무 잘해주셔서 문과생인데 처음으로 이해했어요. 10분 순삭이네요. 구독하고 갑니다!",
            "score": 15000,
            "num_comments": 2800,
            "data_type": "educational_feedback",
            "speech_pattern": "youtube_comment_appreciation",
            "emotional_intensity": 7.0,
            "stance": "positive"
        }
    ]

    # 데이터 처리
    processed_data = processor.process_news_youtube_data(comment_data)

    # 인사이트 생성
    insights = processor.generate_insights(processed_data)

    # 결과 출력
    print("\n" + "="*60)
    print("📺 뉴스/유튜브 댓글 학습 데이터 처리 완료")
    print("="*60)

    print(f"\n📈 처리 결과:")
    print(f"  • 총 학습 샘플: {insights['total_samples']}개")
    print(f"  • 평균 감정 강도: {insights['emotional_intensity_stats']['average']:.2f}")
    print(f"  • 극강 감정 댓글: {insights['emotional_intensity_stats']['extreme_count']}개")
    print(f"  • 평균 바이럴 점수: {insights['viral_potential_analysis']['average_viral_score']:.3f}")

    print(f"\n🌐 플랫폼 분포:")
    for platform, count in insights['platform_distribution'].items():
        print(f"  • {platform}: {count}개")

    print(f"\n🧠 상위 심리적 동기:")
    for driver, count in insights['top_psychological_drivers'][:5]:
        print(f"  • {driver}: {count}회")

    print(f"\n🎭 추천 톤 분포:")
        for tone, count in insights['recommended_tones'][:5]:
            print(f"  • {tone}: {count}회")

        return processed_data, insights

if __name__ == "__main__":
    process_news_youtube_training_data()