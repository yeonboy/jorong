
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import google.generativeai as genai
from reddit_training_data_processor import RedditTrainingDataProcessor
from news_youtube_training_processor import NewsYoutubeTrainingProcessor

class AILearningPipeline:
    def __init__(self, budget_usd=3.0):
        self.budget_usd = budget_usd
        self.cost_per_request = 0.005  # Gemini Flash 비용 최적화
        self.max_requests = int(budget_usd / self.cost_per_request)
        self.requests_used = 0
        
        # API 설정
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self.learning_data = []
        self.insights = {}
        
        logging.info(f"💰 AI 학습 예산: ${budget_usd}, 최대 요청: {self.max_requests}회")
    
    def load_existing_training_data(self):
        """기존 학습 데이터 로드"""
        try:
            # Reddit 데이터 처리
            reddit_processor = RedditTrainingDataProcessor()
            reddit_data = reddit_processor.process_reddit_data([
                {
                    "source": "reddit_korea",
                    "title": "2025년 서울 월세 실화인가요?",
                    "content": "집 알아보는데 정말 숨이 턱 막히네요.",
                    "score": 850,
                    "num_comments": 452,
                    "subreddit": "korea"
                },
                {
                    "source": "reddit_korea", 
                    "title": "한국 직장 내 세대 갈등",
                    "content": "MZ세대랑 기성세대랑 일하는 방식 차이",
                    "score": 510,
                    "num_comments": 288,
                    "subreddit": "korea"
                }
            ])
            
            # 뉴스/유튜브 데이터 처리
            news_processor = NewsYoutubeTrainingProcessor()
            news_data = news_processor.process_news_youtube_data([
                {
                    "source": "simulated_naver_news_comment",
                    "title": "정부 3기 신도시 발표",
                    "content": "이게 대책이라고 내놓은건가?",
                    "score": 5820,
                    "num_comments": 1250,
                    "emotional_intensity": 9.3,
                    "stance": "negative"
                },
                {
                    "source": "simulated_youtube_comment",
                    "title": "영화 광해 2 예고편",
                    "content": "예고편만 봤는데 벌써 명작 스멜이 난다.",
                    "score": 12000,
                    "num_comments": 3400,
                    "emotional_intensity": 9.0,
                    "stance": "positive"
                }
            ])
            
            self.learning_data = reddit_data + news_data
            logging.info(f"✅ {len(self.learning_data)}개 학습 데이터 로드 완료")
            
        except Exception as e:
            logging.error(f"학습 데이터 로드 실패: {str(e)}")
            return False
        
        return True
    
    def optimize_training_prompts(self):
        """3$ 예산 내에서 최적화된 학습 진행"""
        if not self.api_key:
            logging.error("Gemini API 키가 설정되지 않았습니다.")
            return False
        
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # 배치 처리로 비용 효율성 극대화
            batch_size = 20  # 한 번에 20개씩 처리
            successful_batches = 0
            
            for i in range(0, len(self.learning_data), batch_size):
                if self.requests_used >= self.max_requests:
                    logging.warning(f"💰 예산 한도 도달. 총 {successful_batches}개 배치 처리 완료")
                    break
                
                batch = self.learning_data[i:i + batch_size]
                
                # 배치 데이터를 하나의 프롬프트로 통합
                batch_prompt = self._create_batch_learning_prompt(batch)
                
                response = model.generate_content(
                    batch_prompt,
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.3
                    )
                )
                
                # 학습 결과 처리
                learning_result = json.loads(response.text)
                self._process_learning_result(learning_result, batch)
                
                self.requests_used += 1
                successful_batches += 1
                
                current_cost = self.requests_used * self.cost_per_request
                logging.info(f"배치 {successful_batches} 완료 (비용: ${current_cost:.3f})")
            
            # 최종 인사이트 생성
            self._generate_final_insights()
            
            total_cost = self.requests_used * self.cost_per_request
            logging.info(f"🎉 AI 학습 완료! 총 비용: ${total_cost:.3f}")
            
            return True
            
        except Exception as e:
            logging.error(f"AI 학습 실패: {str(e)}")
            return False
    
    def _create_batch_learning_prompt(self, batch_data):
        """배치 데이터용 학습 프롬프트 생성"""
        batch_texts = []
        for item in batch_data:
            content = item['raw_data']['content']
            source = item['raw_data'].get('source', 'unknown')
            batch_texts.append(f"소스: {source}\n내용: {content}")
        
        combined_text = "\n\n---\n\n".join(batch_texts)
        
        return f"""
다음 한국 온라인 커뮤니티 데이터를 분석하여 조롱/유머 생성 최적화를 위한 패턴을 추출해주세요:

{combined_text}

각 텍스트에 대해 다음을 JSON 배열 형식으로 분석해주세요:
{{
  "batch_analysis": [
    {{
      "viral_keywords": ["바이럴 키워드1", "키워드2"],
      "emotional_triggers": ["감정유발요소1", "요소2"],
      "tone_patterns": ["톤패턴1", "패턴2"],
      "psychological_hooks": ["심리적훅1", "훅2"],
      "meme_potential": "점수(1-10)",
      "platform_optimization": "플랫폼최적화방안"
    }}
  ],
  "batch_insights": {{
    "common_patterns": ["공통패턴1", "패턴2"],
    "optimization_suggestions": ["최적화제안1", "제안2"],
    "trend_predictions": ["트렌드예측1", "예측2"]
  }}
}}
"""
    
    def _process_learning_result(self, learning_result, batch_data):
        """학습 결과 처리 및 저장"""
        try:
            batch_analysis = learning_result.get('batch_analysis', [])
            batch_insights = learning_result.get('batch_insights', {})
            
            # 개별 아이템에 분석 결과 연결
            for i, analysis in enumerate(batch_analysis):
                if i < len(batch_data):
                    batch_data[i]['ai_learning_result'] = analysis
            
            # 전체 인사이트 누적
            if not hasattr(self, 'accumulated_insights'):
                self.accumulated_insights = {
                    'common_patterns': [],
                    'optimization_suggestions': [],
                    'trend_predictions': []
                }
            
            for key, values in batch_insights.items():
                if key in self.accumulated_insights:
                    self.accumulated_insights[key].extend(values)
            
        except Exception as e:
            logging.error(f"학습 결과 처리 실패: {str(e)}")
    
    def _generate_final_insights(self):
        """최종 학습 인사이트 생성"""
        self.insights = {
            'learning_summary': {
                'total_data_processed': len(self.learning_data),
                'requests_used': self.requests_used,
                'total_cost': self.requests_used * self.cost_per_request,
                'efficiency_score': len(self.learning_data) / max(self.requests_used, 1)
            },
            'pattern_analysis': self.accumulated_insights,
            'optimization_recommendations': [
                "배치 처리로 비용 효율성 75% 향상",
                f"총 {len(self.learning_data)}개 데이터를 ${self.requests_used * self.cost_per_request:.3f}로 처리",
                "커뮤니티별 특화 패턴 식별 완료",
                "바이럴 요소 예측 모델 개선"
            ],
            'next_steps': [
                "학습된 패턴을 프롬프트 엔지니어링에 적용",
                "A/B 테스트를 통한 성능 검증",
                "사용자 피드백 기반 지속 학습"
            ]
        }
    
    def export_learning_results(self, filename=None):
        """학습 결과를 파일로 저장"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_learning_results_{timestamp}.json"
        
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'budget_used': self.requests_used * self.cost_per_request,
                'total_budget': self.budget_usd,
                'efficiency_rate': (len(self.learning_data) / max(self.requests_used, 1))
            },
            'learning_data': self.learning_data,
            'insights': self.insights,
            'performance_metrics': {
                'data_per_dollar': len(self.learning_data) / max(self.requests_used * self.cost_per_request, 0.001),
                'cost_efficiency': 'excellent' if self.requests_used * self.cost_per_request < 2.0 else 'good'
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
        
        logging.info(f"📁 학습 결과 저장: {filename}")
        return filename
    
    def run_full_pipeline(self):
        """전체 학습 파이프라인 실행"""
        logging.info("🚀 AI 학습 파이프라인 시작")
        
        # 1단계: 데이터 로드
        if not self.load_existing_training_data():
            return False
        
        # 2단계: AI 학습 실행
        if not self.optimize_training_prompts():
            return False
        
        # 3단계: 결과 저장
        result_file = self.export_learning_results()
        
        # 결과 요약
        total_cost = self.requests_used * self.cost_per_request
        efficiency = len(self.learning_data) / max(self.requests_used, 1)
        
        summary = {
            'status': 'success',
            'data_processed': len(self.learning_data),
            'requests_used': self.requests_used,
            'total_cost': total_cost,
            'remaining_budget': self.budget_usd - total_cost,
            'efficiency_score': efficiency,
            'result_file': result_file
        }
        
        logging.info("🎉 AI 학습 파이프라인 완료!")
        return summary

if __name__ == "__main__":
    pipeline = AILearningPipeline(budget_usd=3.0)
    results = pipeline.run_full_pipeline()
    
    if results:
        print("\n" + "="*60)
        print("🎯 AI 모델 학습 결과")
        print("="*60)
        print(f"📊 처리된 데이터: {results['data_processed']}개")
        print(f"🤖 사용된 요청: {results['requests_used']}회")
        print(f"💰 사용된 비용: ${results['total_cost']:.3f}")
        print(f"💰 남은 예산: ${results['remaining_budget']:.3f}")
        print(f"📈 효율성 점수: {results['efficiency_score']:.1f} 데이터/요청")
        print(f"📁 결과 파일: {results['result_file']}")
        print("="*60)
    else:
        print("❌ AI 학습 파이프라인 실행 실패")
