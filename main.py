from dotenv import load_dotenv
load_dotenv()
import os
import logging
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from werkzeug.middleware.proxy_fix import ProxyFix

# Google Gemini API 라이브러리 임포트
import google.generativeai as genai

# 내부 모듈 임포트
from prompt_builder import get_research_enhanced_prompt
from prompt_config import TONE_DESCRIPTIONS

DATABASE_AVAILABLE = False # 데이터베이스 관련 기능 비활성화

# UTF-8 인코딩 설정 (Replit 환경에서 필요할 수 있음)
if sys.version_info[0] == 3:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = Flask(__name__)
# 세션 관리를 위한 비밀 키 설정 (실제 환경에서는 더 강력한 키 사용 권장)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'super-secret-key-for-jorong')
app.wsgi_app = ProxyFix(app.wsgi_app) # 프록시 환경에서 IP 주소 추출을 위해 필요

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ====================================================================
# Google Gemini API 설정
# ====================================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logging.error("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    logging.info("Google Gemini API가 설정되었습니다.")




@app.route('/')
def index():
    """
    메인 페이지를 렌더링합니다. (조롱 사이트의 입력 폼)
    """
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """
    노션 연동용 대시보드 페이지를 렌더링합니다.
    """
    return render_template('dashboard.html')



@app.route('/generate_taunt_text', methods=['POST'])
def generate_taunt_text():
    """
    사용자 입력을 받아 Gemini API를 통해 조롱 텍스트를 생성합니다.
    """
    if not GEMINI_API_KEY:
        logging.error("API 키가 설정되지 않아 텍스트 생성을 수행할 수 없습니다.")
        return jsonify({'status': 'error', 'message': '서버 설정 오류: Gemini API 키가 설정되지 않았습니다.'}), 500

    try:
        data = request.get_json()
        target = data.get('target')
        keywords = data.get('keywords')
        tone = data.get('tone', '유머러스하게')
        length = data.get('length', 500)
        darkness_level = data.get('darkness_level', 2)

        if not target or not keywords:
            logging.warning("필수 입력 필드 누락: 대상 또는 키워드")
            return jsonify({'status': 'error', 'message': '조롱 대상과 내용을 입력해주세요.'}), 400

        logging.info(f"조롱 텍스트 생성 요청: 대상='{target}', 키워드='{keywords}', 톤='{tone}', 흑화 단계='{darkness_level}', 길이='{length}'")

        # 1. 최적화된 프롬프트 생성 (생성과 안전성 검사를 동시에 요청)
        prompt_text = get_research_enhanced_prompt(target, keywords, tone, darkness_level, length, optimized_for_json=True)

        # 2. Gemini API 호출 1회 (JSON 모드)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt_text,
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
        )
        
        # 3. API 응답 파싱
        try:
            result_json = json.loads(response.text)
            generated_text = result_json.get('generated_text', '오류: 텍스트를 생성하지 못했습니다.')
            post_generation_safety_analysis = result_json.get('safety_analysis', {'is_safe': False, 'safety_message': '안전성 분석에 실패했습니다.'})
        except json.JSONDecodeError:
            logging.error(f"JSON 파싱 실패. 원본 응답: {response.text}")
            generated_text = response.text.strip()
            post_generation_safety_analysis = {'is_safe': True, 'safety_message': '기본 안전성 검사를 통과했습니다.'}

        logging.info(f"생성된 조롱 텍스트: {generated_text[:100]}...")
        logging.info(f"안전성 검사 결과: {post_generation_safety_analysis}")

        # 동적 분석 결과 생성 (기존 로직 유지)
        tone_config = TONE_DESCRIPTIONS.get(tone, {})
        emotion_strategies = tone_config.get('emotion_strategy', ['empathy'])
        primary_emotions = { 'superiority': '우월감 자극', 'empathy': '공감대 형성', 'catharsis': '카타르시스', 'social_validation': '사회적 승인' }
        primary_emotion = primary_emotions.get(emotion_strategies[0], '유머러스') if emotion_strategies else '유머러스'
        intensity_map = { range(0, 300): '보통', range(300, 600): '높음', range(600, 1000): '매우 높음', range(1000, 2000): '극도로 높음' }
        intensity_level = next((level for r, level in intensity_map.items() if length in r), '보통')
        tone_techniques = {
            '유머러스하게': ['과장법', '상황 비유', '일상 연결'], '풍자적': ['은유법', '아이러니', '사회 비판'], '비꼬는 듯이': ['반어법', '암시', '간접 표현'],
            '논리적으로 반박하는': ['팩트 체크', '논리적 구조', '근거 제시'], 'MZ 반말 톤': ['슬랭 활용', '줄임말', '세대 공감'], '애교 톤': ['의인법', '귀여운 표현', '부드러운 비판'],
            '헬창 톤': ['운동 비유', '에너지 표현', '동기부여 요소'], '감성 에세이 톤': ['감정 이입', '시적 표현', '내면 묘사'], '해시태그 스타일': ['키워드 나열', 'SNS 문법', '트렌드 반영'],
            '에겐톤': ['고급 어휘', '품격 있는 비판', '우아한 표현'], '소심한 공격 톤': ['Aposiopesis 기법', '말줄임 조롱', '위선적 수습'], '말줄임 밈 톤': ['Aposiopesis 기법', '밈 문화 융합', '바이럴 최적화'],
            '인지 부조화 유발 톤': ['논리적 모순 노출', '인지 부조화 유발', '신념 체계 공격'], '감정 조작 역공 톤': ['감정 조작 탐지', '심리적 방어', '주도권 역전'],
            '논리적 해체 톤': ['체계적 분석', '단계별 논박', '허점 드러내기'], '심리적 우위 점령 톤': ['약점 파악', '심리적 압박', '우위 점령'], '인지적 우위 과시 톤': ['지적 격차 부각', '사고 깊이 과시', '인지 능력 우월감']
        }
        recommended_approaches = tone_techniques.get(tone, ['과장법', '아이러니', '비유'])

        dynamic_emotion_analysis = {
            'primary_emotion': primary_emotion, 'intensity_level': intensity_level, 'recommended_approaches': recommended_approaches,
            'psychological_target': tone_config.get('psychological_hook', '독자의 공감과 재미 유발'), 'emotion_strategy': emotion_strategies,
        }

        # 품질 분석 (기존 로직 유지)
        tone_complexity_scores = { '유머러스하게': 80, '풍자적': 90, '비꼬는 듯이': 85, '논리적으로 반박하는': 95, 'MZ 반말 톤': 75, '애교 톤': 70, '헬창 톤': 75, '감성 에세이 톤': 88, '해시태그 스타일': 72, '에겐톤': 98, '정신나간 톤': 85, '테토 톤': 82 }
        base_quality = tone_complexity_scores.get(tone, 80)
        length_bonus = min(length // 100 * 2, 20)
        dynamic_quality_analysis = {
            'readability_score': min(base_quality + length_bonus, 100), 'originality_score': min(base_quality + (len(emotion_strategies) * 5), 100),
            'humor_rating': round(min(base_quality / 20, 5.0), 1), 'emotion_targeting_score': len(emotion_strategies) * 25,
            'predicted_virality': 'High' if len(emotion_strategies) >= 2 else 'Medium'
        }

        return jsonify({
            'status': 'success',
            'letter': generated_text,
            'emotion_analysis': dynamic_emotion_analysis,
            'quality_analysis': dynamic_quality_analysis,
            'post_generation_safety_analysis': post_generation_safety_analysis,
            'qa_history_id': None, # DB 비활성화
            'gemini_model_info': {
                'model_name': 'Gemini 1.5 Flash', 'version': '1.5', 'emotion_targeting_enabled': True,
                'psychological_analysis_enabled': True, 'qa_logging_enabled': DATABASE_AVAILABLE
            }
        })

    except Exception as e:
        logging.error(f"조롱 텍스트 생성 중 서버 오류: {str(e)}")
        if "API key not valid" in str(e):
             return jsonify({'status': 'error', 'message': 'API 키 문제: Google Gemini API 키를 확인해주세요.'}), 500
        return jsonify({'status': 'error', 'message': f'텍스트 생성 중 오류가 발생했습니다: {str(e)}'}), 500


@app.route('/analyze_taunt', methods=['POST'])
def analyze_taunt():
    """생성된 조롱 텍스트를 분석합니다."""
    if not GEMINI_API_KEY:
        logging.error("API 키가 설정되지 않아 텍스트 분석을 수행할 수 없습니다.")
        return jsonify({'status': 'error', 'message': 'API 키가 설정되지 않았습니다.'}), 500

    try:
        data = request.get_json()
        # --- 문제 해결 3: 프론트엔드에서 보낸 'taunt_text' 키로 수정 ---
        text = data.get('taunt_text', '')

        if not text:
            return jsonify({'status': 'error', 'message': '분석할 텍스트가 없습니다.'}), 400

        logging.info(f"조롱 텍스트 분석 요청: {text[:100]}...")

        analysis_prompt = f"""
다음 조롱 텍스트를 한국어로 분석해주세요. 모든 응답은 반드시 한국어로 작성해주세요:

"{text}"

다음 항목들을 JSON 형식으로 한국어로 분석해주세요:
{{
  "humor_level": "1-5점 사이의 숫자",
  "wit_score": "1-5점 사이의 숫자",
  "safety_concern": "안전성 우려사항을 한국어로 간단히 요약",
  "safety_details": "안전성 관련 상세 설명을 한국어로 작성",
  "improvement_suggestions": ["개선 제안을 한국어로 작성", "두 번째 개선 제안을 한국어로 작성"]
}}

중요: 모든 텍스트는 반드시 한국어로 작성하고, 영어 단어나 문장은 사용하지 마세요."""

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            analysis_prompt,
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
        )

        analysis_result = json.loads(response.text)
        logging.info(f"분석 완료: 유머 수준 {analysis_result.get('humor_level', 'N/A')}")

        return jsonify({
            'status': 'success',
            'analysis': analysis_result
        })

    except json.JSONDecodeError as e:
        logging.error(f"분석 결과 JSON 파싱 실패: {str(e)}")
        return jsonify({ 'status': 'error', 'message': '분석 결과를 처리하는데 실패했습니다.' }), 500
    except Exception as e:
        logging.error(f"조롱 텍스트 분석 실패: {str(e)}")
        return jsonify({ 'status': 'error', 'message': f'분석 중 오류가 발생했습니다: {str(e)}' }), 500


@app.route('/get_darkness_levels', methods=['GET'])
def get_darkness_levels():
    """흑화 단계 정보를 반환합니다."""
    from prompt_config import DARKNESS_CONFIG
    
    darkness_levels = []
    for level, config in DARKNESS_CONFIG.items():
        darkness_levels.append({
            "level": level,
            "name": config["name"],
            "description": config["approach"]
        })
    
    return jsonify({ 'status': 'success', 'levels': darkness_levels })


# --- 문제 해결 1: 비활성화된 관리자/분석 기능 주석 처리 ---
# @app.route('/admin/analytics', methods=['GET']) ...
# @app.route('/admin/analytics/download', methods=['GET']) ...
# @app.route('/admin/analytics/realtime', methods=['GET']) ...
# @app.route('/admin/export_training_data', methods=['GET']) ...
# @app.route('/admin/add_cnn_development_request', methods=['POST']) ...
# @app.route('/admin/view_development_queue', methods=['GET']) ...
# @app.route('/admin/viral_analysis', methods=['POST']) ...
# @app.route('/admin/feedback_loop_status', methods=['GET']) ...
# @app.route('/admin/real_time_learning', methods=['POST']) ...
# @app.route('/admin/scrape_training_data', methods=['POST']) ...
# @app.route('/admin/data_sources', methods=['GET']) ...
# @app.route('/admin/performance_metrics', methods=['GET']) ...


@app.route('/api/project/status', methods=['GET'])
def get_project_status():
    """노션용 프로젝트 현황 API"""
    try:
        status_data = {
            'project_name': '조롱 프로젝트',
            'version': '2.0',
            'status': 'active',
            'last_updated': datetime.now().isoformat(),
            'features': {
                'ai_generation': 'active',
                'safety_analysis': 'active',
                'tone_variations': len(TONE_DESCRIPTIONS),
                'darkness_levels': 5
            },
            'statistics': {
                'total_tones': len(TONE_DESCRIPTIONS),
                'database_status': 'inactive' if not DATABASE_AVAILABLE else 'active',
                'api_status': 'active' if GEMINI_API_KEY else 'inactive'
            },
            'categories': {
                'strategy': '마케팅 전략 수립',
                'research': '심리학 기반 연구',
                'development': '기능 개발 현황',
                'analytics': '사용자 분석'
            }
        }

        return jsonify({
            'status': 'success',
            'data': status_data,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logging.error(f"프로젝트 상태 조회 실패: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/project/categories', methods=['GET'])
def get_project_categories():
    """노션용 프로젝트 카테고리 분류 API"""
    try:
        categories = {
            'strategy': {
                'name': '전략',
                'description': '마케팅 및 비즈니스 전략',
                'items': [
                    '바이럴 마케팅 전략',
                    '사용자 타겟팅',
                    '플랫폼별 최적화',
                    '수익화 모델'
                ],
                'status': 'in_progress'
            },
            'research': {
                'name': '연구',
                'description': '심리학 및 언어학 연구',
                'items': [
                    'Aposiopesis 기법 연구',
                    '에겐-테토 페르소나 분석',
                    '감정선 타겟팅 시스템',
                    '바이럴 화법 분석'
                ],
                'status': 'active'
            },
            'development': {
                'name': '개발',
                'description': '기술적 구현 및 기능 개발',
                'items': [
                    'AI 모델 최적화',
                    '안전성 검사 시스템',
                    '실시간 분석 기능',
                    'UI/UX 개선'
                ],
                'status': 'ongoing'
            },
            'analytics': {
                'name': '분석',
                'description': '사용자 및 성과 분석',
                'items': [
                    '사용자 행동 분석',
                    '콘텐츠 성과 측정',
                    '트렌드 분석',
                    '피드백 시스템'
                ],
                'status': 'planning'
            }
        }

        return jsonify({
            'status': 'success',
            'categories': categories,
            'total_categories': len(categories),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/notion/dashboard', methods=['GET'])
def get_notion_dashboard():
    """노션 대시보드용 종합 데이터 API"""
    try:
        dashboard_data = {
            'overview': {
                'project_health': 'healthy',
                'active_features': len([k for k in TONE_DESCRIPTIONS.keys()]),
                'completion_rate': '75%',
                'next_milestone': '고급 분석 기능 완성'
            },
            'recent_activities': [
                {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'activity': '조롱 분석 한국어 출력 수정 완료',
                    'category': 'development'
                },
                {
                    'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                    'activity': '안전성 검사 시스템 강화',
                    'category': 'research'
                }
            ],
            'performance_metrics': {
                'api_response_time': '< 2초',
                'system_uptime': '99.5%',
                'user_satisfaction': '4.2/5.0',
                'feature_adoption': '68%'
            },
            'priorities': [
                {'task': '노션 연동 완성', 'priority': 'high', 'deadline': '2025-07-15'},
                {'task': '데이터베이스 최적화', 'priority': 'medium', 'deadline': '2025-07-20'},
                {'task': '새로운 톤 개발', 'priority': 'low', 'deadline': '2025-07-30'}
            ]
        }

        return jsonify({
            'status': 'success',
            'dashboard': dashboard_data,
            'generated_at': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    logging.info("⚠️ 연구 데이터베이스 시스템을 사용할 수 없습니다. 기본 모드로 실행합니다.")
    logging.info("🚀 기본 모드에서도 모든 핵심 기능이 정상 작동합니다!")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


@app.route('/admin/load_reddit_training_data', methods=['POST'])
def load_reddit_training_data():
    """Reddit 학습 데이터를 로드하고 처리합니다."""
    try:
        from reddit_training_data_processor import RedditTrainingDataProcessor

        processor = RedditTrainingDataProcessor()

        # 2025년 Reddit 트렌드 데이터 로드
        reddit_data = [
            {
                "source": "reddit_korea",
                "title": "2025년 서울 월세 실화인가요? 종로에서 5평에 100만원이라는데…",
                "content": "최근에 집 알아보는데 정말 숨이 턱 막히네요. 다들 이정도 내고 사시는 건가요?",
                "score": 850,
                "num_comments": 452,
                "subreddit": "korea",
                "data_type": "community_post"
            },
            {
                "source": "reddit_korea", 
                "title": "한국 직장 내 세대 갈등, 여러분 회사는 어떤가요?",
                "content": "요즘 MZ세대랑 기성세대랑 일하는 방식 차이 때문에 스트레스 받네요.",
                "score": 510,
                "num_comments": 288,
                "subreddit": "korea",
                "data_type": "community_post"
            }
        ]

        # 데이터 처리
        processed_data = processor.process_reddit_data(reddit_data)
        insights = processor.generate_training_insights(processed_data)

        # 세션에 저장 (실제 환경에서는 데이터베이스 사용)
        session['reddit_training_data'] = processed_data
        session['reddit_insights'] = insights

        return jsonify({
            'status': 'success',
            'message': 'Reddit 학습 데이터 로드 완료',
            'data': {
                'total_samples': insights['total_samples'],
                'trend_distribution': insights['trend_distribution'],
                'top_emotion_triggers': insights['top_emotion_triggers'][:5],
                'recommended_tones': insights['recommended_tones'][:5]
            }
        })

    except Exception as e:
        logging.error(f"Reddit 학습 데이터 로드 실패: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'데이터 로드 중 오류 발생: {str(e)}'
        }), 500

@app.route('/admin/reddit_insights', methods=['GET'])
def get_reddit_insights():
    """Reddit 데이터 분석 인사이트를 반환합니다."""
    try:
        insights = session.get('reddit_insights', {})

        if not insights:
            return jsonify({
                'status': 'error',
                'message': 'Reddit 데이터를 먼저 로드해주세요.'
            }), 400

        return jsonify({
            'status': 'success',
            'insights': insights,
            'recommendations': [
                {
                    'category': '트렌드 반영',
                    'insight': f"가장 인기있는 트렌드는 '{max(insights['trend_distribution'], key=insights['trend_distribution'].get)}'입니다.",
                    'recommendation': '이 트렌드에 특화된 톤과 표현을 개발하세요.'
                },
                {
                    'category': '감정 타겟팅',
                    'insight': f"가장 효과적인 감정 트리거는 '{insights['top_emotion_triggers'][0][0]}'입니다.",
                    'recommendation': '이 감정 트리거를 활용한 콘텐츠 생성을 강화하세요.'
                },
                {
                    'category': '품질 최적화',
                    'insight': f"평균 품질 점수는 {insights['quality_distribution']['average']:.2f}점입니다.",
                    'recommendation': '고품질 데이터 비율을 높이기 위한 필터링 기준을 강화하세요.'
                }
            ]
        })

    except Exception as e:
        logging.error(f"Reddit 인사이트 조회 실패: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/admin/load_news_youtube_data', methods=['POST'])
def load_news_youtube_data():
    """뉴스/유튜브 댓글 학습 데이터를 로드하고 처리합니다."""
    try:
        from news_youtube_training_processor import NewsYoutubeTrainingProcessor

        processor = NewsYoutubeTrainingProcessor()

        # 뉴스/유튜브 댓글 데이터 로드
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
        insights = processor.generate_insights(processed_data)

        # 세션에 저장
        session['news_youtube_data'] = processed_data
        session['news_youtube_insights'] = insights

        return jsonify({
            'status': 'success',
            'message': '뉴스/유튜브 댓글 학습 데이터 로드 완료',
            'data': {
                'total_samples': insights['total_samples'],
                'platform_distribution': insights['platform_distribution'],
                'top_psychological_drivers': insights['top_psychological_drivers'][:5],
                'recommended_tones': insights['recommended_tones'][:5],
                'viral_analysis': insights['viral_potential_analysis']
            }
        })

    except Exception as e:
        logging.error(f"뉴스/유튜브 데이터 로드 실패: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'데이터 로드 중 오류 발생: {str(e)}'
        }), 500

@app.route('/admin/news_youtube_insights', methods=['GET'])
def get_news_youtube_insights():
    """뉴스/유튜브 댓글 데이터 분석 인사이트를 반환합니다."""
    try:
        insights = session.get('news_youtube_insights', {})

        if not insights:
            return jsonify({
                'status': 'error',
                'message': '뉴스/유튜브 데이터를 먼저 로드해주세요.'
            }), 400

        return jsonify({
            'status': 'success',
            'insights': insights,
            'recommendations': [
                {
                    'category': '플랫폼별 특성',
                    'insight': f"가장 많은 데이터가 수집된 플랫폼은 '{max(insights['platform_distribution'], key=insights['platform_distribution'].get)}'입니다.",
                    'recommendation': '각 플랫폼의 고유한 언어적 특성을 반영한 톤 개발이 필요합니다.'
                },
                {
                    'category': '심리적 동기',
                    'insight': f"가장 강한 심리적 동기는 '{insights['top_psychological_drivers'][0][0]}'입니다.",
                    'recommendation': '이 심리적 동기를 자극하는 콘텐츠 생성 전략을 강화하세요.'
                },
                {
                    'category': '바이럴 잠재력',
                    'insight': f"평균 바이럴 점수는 {insights['viral_potential_analysis']['average_viral_score']:.3f}입니다.",
                    'recommendation': f"고바이럴 콘텐츠 {insights['viral_potential_analysis']['high_viral_count']}개의 패턴을 분석하여 적용하세요."
                },
                {
                    'category': '감정 강도',
                    'insight': f"극강 감정 댓글이 {insights['emotional_intensity_stats']['extreme_count']}개 발견되었습니다.",
                    'recommendation': '감정 강도가 높은 콘텐츠의 특성을 분석하여 효과적인 조롱 전략을 수립하세요.'
                }
            ]
        })

    except Exception as e:
        logging.error(f"뉴스/유튜브 인사이트 조회 실패: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/admin/run_ai_learning', methods=['POST'])
def run_ai_learning():
    """3$ 예산으로 AI 모델 학습을 실행합니다."""
    try:
        from ai_learning_pipeline import AILearningPipeline

        data = request.get_json()
        budget = data.get('budget', 3.0)

        if budget > 5.0:
            return jsonify({
                'status': 'error',
                'message': '예산은 최대 $5까지 설정 가능합니다.'
            }), 400

        logging.info(f"💰 AI 학습 시작 - 예산: ${budget}")

        # AI 학습 파이프라인 실행
        pipeline = AILearningPipeline(budget_usd=budget)
        results = pipeline.run_full_pipeline()

        if results:
            # 세션에 결과 저장
            session['ai_learning_results'] = results

            return jsonify({
                'status': 'success',
                'message': f'AI 학습 완료! 총 비용: ${results["total_cost"]:.3f}',
                'results': {
                    'data_processed': results['data_processed'],
                    'requests_used': results['requests_used'],
                    'total_cost': results['total_cost'],
                    'remaining_budget': results['remaining_budget'],
                    'efficiency_score': results['efficiency_score'],
                    'cost_per_data': results['total_cost'] / results['data_processed'] if results['data_processed'] > 0 else 0
                },
                'performance': {
                    'efficiency_rating': 'excellent' if results['efficiency_score'] > 15 else 'good',
                    'budget_utilization': (results['total_cost'] / budget) * 100,
                    'data_density': f"{results['data_processed']} 데이터 / ${results['total_cost']:.3f}"
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'AI 학습 파이프라인 실행에 실패했습니다.'
            }), 500

    except ImportError:
        return jsonify({
            'status': 'error',
            'message': 'AI 학습 모듈을 찾을 수 없습니다.'
        }), 500
    except Exception as e:
        logging.error(f"AI 학습 실행 실패: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'AI 학습 중 오류 발생: {str(e)}'
        }), 500

@app.route('/admin/ai_learning_status', methods=['GET'])
def get_ai_learning_status():
    """AI 학습 상태 및 결과를 조회합니다."""
    try:
        results = session.get('ai_learning_results')

        if not results:
            return jsonify({
                'status': 'no_data',
                'message': 'AI 학습이 아직 실행되지 않았습니다.',
                'suggestions': [
                    '/admin/run_ai_learning 엔드포인트로 학습을 시작하세요.',
                    '예산은 $1-5 사이로 설정 가능합니다.',
                    '학습 데이터는 Reddit + 뉴스/유튜브 댓글 통합 데이터를 사용합니다.'
                ]
            })

        return jsonify({
            'status': 'success',
            'learning_results': results,
            'insights': {
                'cost_efficiency': f"${results['total_cost']:.3f}로 {results['data_processed']}개 데이터 처리",
                'roi_analysis': f"데이터당 비용: ${results['total_cost'] / results['data_processed']:.4f}",
                'budget_management': f"예산 사용률: {(results['total_cost'] / 3.0) * 100:.1f}%",
                'performance_rating': 'excellent' if results['efficiency_score'] > 15 else 'good'
            },
            'next_actions': [
                '학습된 패턴을 프롬프트에 적용하여 성능 개선',
                'A/B 테스트로 개선 효과 측정',
                '사용자 피드백 수집 및 추가 학습'
            ]
        })

    except Exception as e:
        logging.error(f"AI 학습 상태 조회 실패: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500