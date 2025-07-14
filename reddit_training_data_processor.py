import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import re

class RedditTrainingDataProcessor:
    def __init__(self):
        self.processed_data = []
        self.emotion_mapping = {
            'theqoo_style': {'primary': 'empathy', 'secondary': 'social_validation'},
            'mlbpark_style': {'primary': 'superiority', 'secondary': 'catharsis'},
            'instiz_style': {'primary': 'social_validation', 'secondary': 'empathy'},
            'dc_style': {'primary': 'catharsis', 'secondary': 'superiority'},
            'pann_style': {'primary': 'empathy', 'secondary': 'social_validation'}
        }
        
        # 2025년 Reddit 트렌드 키워드
        self.trending_keywords = {
            'cost_of_living': ['월세', '물가', '생활비', '집값', '부동산', '경제', '인플레이션'],
            'travel_tips': ['여행', 'KTX', '교통카드', 'T-money', 'Naver Maps', '부산', '경주'],
            'social_culture': ['데이팅 앱', '세대 갈등', 'MZ세대', '직장', '회식', '문화'],
            'korean_lifestyle': ['한국', '서울', '외국인', '치안', '캐리어', '혼자 여행']
        }
    
    def extract_reddit_data(self, file_content: str) -> List[Dict[str, Any]]:
        """Reddit 데이터 파일에서 구조화된 데이터 추출"""
        try:
            # 파일 내용에서 JSON 형태의 데이터 추출
            data_start = file_content.find('[')
            data_end = file_content.rfind(']') + 1
            
            if data_start != -1 and data_end != -1:
                json_data = file_content[data_start:data_end]
                return json.loads(json_data)
            else:
                logging.error("Reddit 데이터 형식을 찾을 수 없습니다.")
                return []
                
        except json.JSONDecodeError as e:
            logging.error(f"JSON 파싱 오류: {str(e)}")
            return []
    
    def analyze_viral_potential(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """게시물의 바이럴 잠재력 분석"""
        score = post_data.get('score', 0)
        comments = post_data.get('num_comments', 0)
        title = post_data.get('title', '')
        content = post_data.get('content', '')
        
        # 바이럴 지수 계산
        viral_score = 0
        if score > 500: viral_score += 3
        elif score > 100: viral_score += 2
        elif score > 50: viral_score += 1
        
        if comments > 100: viral_score += 2
        elif comments > 50: viral_score += 1
        
        # 감정 자극 요소 분석
        emotion_triggers = []
        text = f"{title} {content}".lower()
        
        if any(word in text for word in ['실화', '진짜', '미쳤다', '헐', '대박']):
            emotion_triggers.append('충격성')
        if any(word in text for word in ['ㅋㅋ', '웃기', '개웃김', '레전드']):
            emotion_triggers.append('유머성')
        if any(word in text for word in ['공감', '저도', '맞아', '같은']):
            emotion_triggers.append('공감성')
        
        return {
            'viral_score': viral_score,
            'emotion_triggers': emotion_triggers,
            'engagement_ratio': comments / max(score, 1),
            'trend_category': self.categorize_trend(text)
        }
    
    def categorize_trend(self, text: str) -> str:
        """텍스트를 트렌드 카테고리로 분류"""
        for category, keywords in self.trending_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category
        return 'general'
    
    def extract_linguistic_features(self, text: str, speech_pattern: str = None) -> Dict[str, Any]:
        """언어적 특징 추출"""
        features = {
            'length': len(text),
            'sentence_count': len(re.split(r'[.!?]', text)),
            'question_marks': text.count('?'),
            'exclamation_marks': text.count('!'),
            'laugh_expressions': len(re.findall(r'ㅋ+', text)),
            'slang_intensity': 0,
            'formality_level': 'medium'
        }
        
        # 슬랭 강도 측정
        slang_words = ['개', '완전', '진짜', '미쳤다', '헐', '대박', 'ㄹㅇ', 'ㅇㅈ']
        features['slang_intensity'] = sum(1 for word in slang_words if word in text)
        
        # 격식성 수준 판단
        formal_endings = ['습니다', '였습니다', '입니다']
        informal_endings = ['해', '야', '지', 'ㅋㅋ']
        
        if any(ending in text for ending in formal_endings):
            features['formality_level'] = 'high'
        elif any(ending in text for ending in informal_endings):
            features['formality_level'] = 'low'
        
        # 커뮤니티별 특징
        if speech_pattern:
            features['speech_pattern'] = speech_pattern
            features['emotion_mapping'] = self.emotion_mapping.get(speech_pattern, {})
        
        return features
    
    def generate_tone_recommendations(self, post_data: Dict[str, Any]) -> List[str]:
        """게시물 특성에 따른 톤 추천"""
        recommendations = []
        
        viral_analysis = self.analyze_viral_potential(post_data)
        trend_category = viral_analysis['trend_category']
        
        # 트렌드 카테고리별 톤 추천
        if trend_category == 'cost_of_living':
            recommendations.extend(['냉소 톤', '논리적으로 반박하는', '현실적 톤'])
        elif trend_category == 'travel_tips':
            recommendations.extend(['친절한 톤', '정보 제공 톤', '경험 공유 톤'])
        elif trend_category == 'social_culture':
            recommendations.extend(['풍자적', '세대 공감 톤', 'MZ 반말 톤'])
        
        # 바이럴 점수에 따른 톤 추천
        if viral_analysis['viral_score'] > 4:
            recommendations.extend(['말줄임 밈 톤', '정신나간 톤', '틱톡 트렌드 톤'])
        elif viral_analysis['viral_score'] > 2:
            recommendations.extend(['유머러스하게', '풍자적', 'MZ 반말 톤'])
        
        return list(set(recommendations))
    
    def process_reddit_data(self, reddit_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Reddit 데이터를 학습용 데이터로 변환"""
        processed_data = []
        
        for post in reddit_data:
            try:
                # 기본 정보 추출
                title = post.get('title', '')
                content = post.get('content', '')
                full_text = f"{title} {content}"
                
                # 언어적 특징 분석
                linguistic_features = self.extract_linguistic_features(
                    full_text, 
                    post.get('speech_pattern')
                )
                
                # 바이럴 잠재력 분석
                viral_analysis = self.analyze_viral_potential(post)
                
                # 톤 추천
                tone_recommendations = self.generate_tone_recommendations(post)
                
                # 학습 데이터 구조화
                training_sample = {
                    'dataset_name': f"Reddit_2025_{post.get('source', 'unknown')}",
                    'content_type': 'reddit_community_data',
                    'raw_data': {
                        'title': title,
                        'content': content,
                        'score': post.get('score', 0),
                        'comments': post.get('num_comments', 0),
                        'source': post.get('source', ''),
                        'subreddit': post.get('subreddit', ''),
                        'created_utc': post.get('created_utc', 0)
                    },
                    'processed_data': {
                        'linguistic_features': linguistic_features,
                        'viral_analysis': viral_analysis,
                        'tone_recommendations': tone_recommendations,
                        'emotion_triggers': viral_analysis['emotion_triggers'],
                        'trend_category': viral_analysis['trend_category'],
                        'learning_priority': 'high' if viral_analysis['viral_score'] > 3 else 'medium'
                    },
                    'metadata': {
                        'processing_date': datetime.now().isoformat(),
                        'data_source': 'reddit_2025_trending',
                        'quality_indicators': {
                            'engagement_score': post.get('score', 0),
                            'discussion_depth': post.get('num_comments', 0),
                            'viral_potential': viral_analysis['viral_score']
                        }
                    },
                    'quality_score': min(9.0, 5.0 + (viral_analysis['viral_score'] * 0.8))
                }
                
                processed_data.append(training_sample)
                
            except Exception as e:
                logging.error(f"데이터 처리 오류: {str(e)}")
                continue
        
        return processed_data
    
    def generate_training_insights(self, processed_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """처리된 데이터에서 학습 인사이트 생성"""
        insights = {
            'total_samples': len(processed_data),
            'trend_distribution': {},
            'viral_score_stats': {},
            'top_emotion_triggers': [],
            'recommended_tones': {},
            'quality_distribution': {}
        }
        
        # 트렌드 분포 분석
        trend_counts = {}
        viral_scores = []
        emotion_triggers = []
        tone_recommendations = []
        quality_scores = []
        
        for sample in processed_data:
            # 트렌드 카테고리 분포
            trend = sample['processed_data']['trend_category']
            trend_counts[trend] = trend_counts.get(trend, 0) + 1
            
            # 바이럴 점수 통계
            viral_scores.append(sample['processed_data']['viral_analysis']['viral_score'])
            
            # 감정 트리거 수집
            emotion_triggers.extend(sample['processed_data']['emotion_triggers'])
            
            # 톤 추천 수집
            tone_recommendations.extend(sample['processed_data']['tone_recommendations'])
            
            # 품질 점수 수집
            quality_scores.append(sample['quality_score'])
        
        insights['trend_distribution'] = trend_counts
        insights['viral_score_stats'] = {
            'average': sum(viral_scores) / len(viral_scores) if viral_scores else 0,
            'max': max(viral_scores) if viral_scores else 0,
            'min': min(viral_scores) if viral_scores else 0
        }
        
        # 상위 감정 트리거
        from collections import Counter
        insights['top_emotion_triggers'] = Counter(emotion_triggers).most_common(10)
        
        # 추천 톤 분포
        insights['recommended_tones'] = Counter(tone_recommendations).most_common(15)
        
        # 품질 분포
        insights['quality_distribution'] = {
            'average': sum(quality_scores) / len(quality_scores) if quality_scores else 0,
            'high_quality_count': len([q for q in quality_scores if q >= 8.0]),
            'total_count': len(quality_scores)
        }
        
        return insights
    
    def export_training_data(self, processed_data: List[Dict[str, Any]], filename: str = None) -> str:
        """처리된 데이터를 학습용 파일로 저장"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reddit_training_data_{timestamp}.json"
        
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'data_source': 'reddit_2025_trending',
                'total_samples': len(processed_data),
                'processing_version': '1.0'
            },
            'training_samples': processed_data,
            'insights': self.generate_training_insights(processed_data)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
        
        logging.info(f"학습 데이터 저장 완료: {filename}")
        return filename
```

```python
    def __init__(self):
        self.trend_categories = {
            'cost_of_living': ['월세', '물가', '생활비', '집값', '경제'],
            'entertainment': ['영화', '드라마', '아이돌', '연예인'],
            'social_dynamics': ['세대', '직장', '문화', 'MZ'],
            'politics': ['정부', '정책', '법', '민주주의'],
            'inequality': ['부동산', '상대적 박탈감', '서민']
        }

    def process_reddit_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Reddit 데이터를 학습용으로 처리합니다."""
        processed_data = []

        for item in raw_data:
            processed_item = {
                'raw_data': item,
                'processed_at': datetime.now().isoformat(),
                'trend_category': self._categorize_trend(item.get('content', '')),
                'emotion_triggers': self._extract_emotion_triggers(item),
                'viral_potential': self._calculate_viral_potential(item),
                'recommended_tones': self._suggest_tones(item)
            }
            processed_data.append(processed_item)

        return processed_data

    def _categorize_trend(self, content: str) -> str:
        """내용을 기반으로 트렌드 카테고리를 분류합니다."""
        content_lower = content.lower()

        for category, keywords in self.trend_categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category

        return 'general'

    def _extract_emotion_triggers(self, item: Dict) -> List[str]:
        """감정 트리거 요소를 추출합니다."""
        triggers = []
        content = item.get('content', '').lower()

        # 기본 감정 트리거 패턴
        trigger_patterns = {
            'frustration': ['진짜', '정말', '숨이 막히다', '스트레스'],
            'empathy': ['다들', '여러분', '우리'],
            'superiority': ['차이', '수준', '격차'],
            'validation': ['맞다', '공감', '동감']
        }

        for trigger_type, patterns in trigger_patterns.items():
            if any(pattern in content for pattern in patterns):
                triggers.append(trigger_type)

        return triggers

    def _calculate_viral_potential(self, item: Dict) -> float:
        """바이럴 잠재력을 계산합니다."""
        score = item.get('score', 0)
        comments = item.get('num_comments', 0)

        # 간단한 바이럴 점수 계산
        viral_score = (score * 0.7 + comments * 0.3) / 1000
        return min(viral_score, 10.0)

    def _suggest_tones(self, item: Dict) -> List[str]:
        """적합한 톤을 제안합니다."""
        content = item.get('content', '').lower()
        suggested_tones = []

        if '스트레스' in content or '힘들다' in content:
            suggested_tones.append('공감 톤')
        if '차이' in content or '세대' in content:
            suggested_tones.append('풍자적')
        if '진짜' in content or '정말' in content:
            suggested_tones.append('MZ 반말 톤')

        return suggested_tones[:3]  # 최대 3개

    def generate_training_insights(self, processed_data: List[Dict]) -> Dict:
        """처리된 데이터에서 인사이트를 생성합니다."""
        total_samples = len(processed_data)

        # 트렌드 분포
        trend_distribution = {}
        for item in processed_data:
            trend = item['trend_category']
            trend_distribution[trend] = trend_distribution.get(trend, 0) + 1

        # 감정 트리거 분석
        emotion_triggers = {}
        for item in processed_data:
            for trigger in item['emotion_triggers']:
                emotion_triggers[trigger] = emotion_triggers.get(trigger, 0) + 1

        # 추천 톤 분석
        recommended_tones = {}
        for item in processed_data:
            for tone in item['recommended_tones']:
                recommended_tones[tone] = recommended_tones.get(tone, 0) + 1

        return {
            'total_samples': total_samples,
            'trend_distribution': trend_distribution,
            'top_emotion_triggers': sorted(emotion_triggers.items(), key=lambda x: x[1], reverse=True),
            'recommended_tones': sorted(recommended_tones.items(), key=lambda x: x[1], reverse=True),
            'quality_distribution': {
                'average': sum(item['viral_potential'] for item in processed_data) / total_samples if total_samples > 0 else 0
            }
        }
```

The edited code provides a new implementation of `__init__`, `process_reddit_data`, `_categorize_trend`, `_extract_emotion_triggers`, `_calculate_viral_potential`, `_suggest_tones`, and `generate_training_insights`. These methods will replace the original implementations in the `RedditTrainingDataProcessor` class. The other methods like `extract_reddit_data`, `analyze_viral_potential`, `extract_linguistic_features`, `generate_tone_recommendations`, and `export_training_data` will be kept from the original code.

```python
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import re

class RedditTrainingDataProcessor:
    def __init__(self):
        self.trend_categories = {
            'cost_of_living': ['월세', '물가', '생활비', '집값', '경제'],
            'entertainment': ['영화', '드라마', '아이돌', '연예인'],
            'social_dynamics': ['세대', '직장', '문화', 'MZ'],
            'politics': ['정부', '정책', '법', '민주주의'],
            'inequality': ['부동산', '상대적 박탈감', '서민']
        }
    
    def extract_reddit_data(self, file_content: str) -> List[Dict[str, Any]]:
        """Reddit 데이터 파일에서 구조화된 데이터 추출"""
        try:
            # 파일 내용에서 JSON 형태의 데이터 추출
            data_start = file_content.find('[')
            data_end = file_content.rfind(']') + 1
            
            if data_start != -1 and data_end != -1:
                json_data = file_content[data_start:data_end]
                return json.loads(json_data)
            else:
                logging.error("Reddit 데이터 형식을 찾을 수 없습니다.")
                return []
                
        except json.JSONDecodeError as e:
            logging.error(f"JSON 파싱 오류: {str(e)}")
            return []
    
    def analyze_viral_potential(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """게시물의 바이럴 잠재력 분석"""
        score = post_data.get('score', 0)
        comments = post_data.get('num_comments', 0)
        title = post_data.get('title', '')
        content = post_data.get('content', '')
        
        # 바이럴 지수 계산
        viral_score = 0
        if score > 500: viral_score += 3
        elif score > 100: viral_score += 2
        elif score > 50: viral_score += 1
        
        if comments > 100: viral_score += 2
        elif comments > 50: viral_score += 1
        
        # 감정 자극 요소 분석
        emotion_triggers = []
        text = f"{title} {content}".lower()
        
        if any(word in text for word in ['실화', '진짜', '미쳤다', '헐', '대박']):
            emotion_triggers.append('충격성')
        if any(word in text for word in ['ㅋㅋ', '웃기', '개웃김', '레전드']):
            emotion_triggers.append('유머성')
        if any(word in text for word in ['공감', '저도', '맞아', '같은']):
            emotion_triggers.append('공감성')
        
        return {
            'viral_score': viral_score,
            'emotion_triggers': emotion_triggers,
            'engagement_ratio': comments / max(score, 1),
            'trend_category': self.categorize_trend(text)
        }
    
    def categorize_trend(self, text: str) -> str:
        """텍스트를 트렌드 카테고리로 분류"""
        for category, keywords in self.trending_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category
        return 'general'
    
    def extract_linguistic_features(self, text: str, speech_pattern: str = None) -> Dict[str, Any]:
        """언어적 특징 추출"""
        features = {
            'length': len(text),
            'sentence_count': len(re.split(r'[.!?]', text)),
            'question_marks': text.count('?'),
            'exclamation_marks': text.count('!'),
            'laugh_expressions': len(re.findall(r'ㅋ+', text)),
            'slang_intensity': 0,
            'formality_level': 'medium'
        }
        
        # 슬랭 강도 측정
        slang_words = ['개', '완전', '진짜', '미쳤다', '헐', '대박', 'ㄹㅇ', 'ㅇㅈ']
        features['slang_intensity'] = sum(1 for word in slang_words if word in text)
        
        # 격식성 수준 판단
        formal_endings = ['습니다', '였습니다', '입니다']
        informal_endings = ['해', '야', '지', 'ㅋㅋ']
        
        if any(ending in text for ending in formal_endings):
            features['formality_level'] = 'high'
        elif any(ending in text for ending in informal_endings):
            features['formality_level'] = 'low'
        
        # 커뮤니티별 특징
        if speech_pattern:
            features['speech_pattern'] = speech_pattern
            features['emotion_mapping'] = self.emotion_mapping.get(speech_pattern, {})
        
        return features
    
    def generate_tone_recommendations(self, post_data: Dict[str, Any]) -> List[str]:
        """게시물 특성에 따른 톤 추천"""
        recommendations = []
        
        viral_analysis = self.analyze_viral_potential(post_data)
        trend_category = viral_analysis['trend_category']
        
        # 트렌드 카테고리별 톤 추천
        if trend_category == 'cost_of_living':
            recommendations.extend(['냉소 톤', '논리적으로 반박하는', '현실적 톤'])
        elif trend_category == 'travel_tips':
            recommendations.extend(['친절한 톤', '정보 제공 톤', '경험 공유 톤'])
        elif trend_category == 'social_culture':
            recommendations.extend(['풍자적', '세대 공감 톤', 'MZ 반말 톤'])
        
        # 바이럴 점수에 따른 톤 추천
        if viral_analysis['viral_score'] > 4:
            recommendations.extend(['말줄임 밈 톤', '정신나간 톤', '틱톡 트렌드 톤'])
        elif viral_analysis['viral_score'] > 2:
            recommendations.extend(['유머러스하게', '풍자적', 'MZ 반말 톤'])
        
        return list(set(recommendations))
    
    def process_reddit_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Reddit 데이터를 학습용으로 처리합니다."""
        processed_data = []

        for item in raw_data:
            processed_item = {
                'raw_data': item,
                'processed_at': datetime.now().isoformat(),
                'trend_category': self._categorize_trend(item.get('content', '')),
                'emotion_triggers': self._extract_emotion_triggers(item),
                'viral_potential': self._calculate_viral_potential(item),
                'recommended_tones': self._suggest_tones(item)
            }
            processed_data.append(processed_item)

        return processed_data

    def _categorize_trend(self, content: str) -> str:
        """내용을 기반으로 트렌드 카테고리를 분류합니다."""
        content_lower = content.lower()

        for category, keywords in self.trend_categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category

        return 'general'

    def _extract_emotion_triggers(self, item: Dict) -> List[str]:
        """감정 트리거 요소를 추출합니다."""
        triggers = []
        content = item.get('content', '').lower()

        # 기본 감정 트리거 패턴
        trigger_patterns = {
            'frustration': ['진짜', '정말', '숨이 막히다', '스트레스'],
            'empathy': ['다들', '여러분', '우리'],
            'superiority': ['차이', '수준', '격차'],
            'validation': ['맞다', '공감', '동감']
        }

        for trigger_type, patterns in trigger_patterns.items():
            if any(pattern in content for pattern in patterns):
                triggers.append(trigger_type)

        return triggers

    def _calculate_viral_potential(self, item: Dict) -> float:
        """바이럴 잠재력을 계산합니다."""
        score = item.get('score', 0)
        comments = item.get('num_comments', 0)

        # 간단한 바이럴 점수 계산
        viral_score = (score * 0.7 + comments * 0.3) / 1000
        return min(viral_score, 10.0)

    def _suggest_tones(self, item: Dict) -> List[str]:
        """적합한 톤을 제안합니다."""
        content = item.get('content', '').lower()
        suggested_tones = []

        if '스트레스' in content or '힘들다' in content:
            suggested_tones.append('공감 톤')
        if '차이' in content or '세대' in content:
            suggested_tones.append('풍자적')
        if '진짜' in content or '정말' in content:
            suggested_tones.append('MZ 반말 톤')

        return suggested_tones[:3]  # 최대 3개

    def generate_training_insights(self, processed_data: List[Dict]) -> Dict:
        """처리된 데이터에서 인사이트를 생성합니다."""
        total_samples = len(processed_data)

        # 트렌드 분포
        trend_distribution = {}
        for item in processed_data:
            trend = item['trend_category']
            trend_distribution[trend] = trend_distribution.get(trend, 0) + 1

        # 감정 트리거 분석
        emotion_triggers = {}
        for item in processed_data:
            for trigger in item['emotion_triggers']:
                emotion_triggers[trigger] = emotion_triggers.get(trigger, 0) + 1

        # 추천 톤 분석
        recommended_tones = {}
        for item in processed_data:
            for tone in item['recommended_tones']:
                recommended_tones[tone] = recommended_tones.get(tone, 0) + 1

        return {
            'total_samples': total_samples,
            'trend_distribution': trend_distribution,
            'top_emotion_triggers': sorted(emotion_triggers.items(), key=lambda x: x[1], reverse=True),
            'recommended_tones': sorted(recommended_tones.items(), key=lambda x: x[1], reverse=True),
            'quality_distribution': {
                'average': sum(item['viral_potential'] for item in processed_data) / total_samples if total_samples > 0 else 0
            }
        }
    
    def export_training_data(self, processed_data: List[Dict[str, Any]], filename: str = None) -> str:
        """처리된 데이터를 학습용 파일로 저장"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reddit_training_data_{timestamp}.json"
        
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'data_source': 'reddit_2025_trending',
                'total_samples': len(processed_data),
                'processing_version': '1.0'
            },
            'training_samples': processed_data,
            'insights': self.generate_training_insights(processed_data)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
        
        logging.info(f"학습 데이터 저장 완료: {filename}")
        return filename
```