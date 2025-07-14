
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

class TauntResearchDB:
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL 환경변수가 설정되지 않았습니다.")
    
    def get_connection(self):
        """데이터베이스 연결을 반환합니다."""
        return psycopg2.connect(self.database_url)
    
    def init_database(self):
        """조롱 연구 데이터용 테이블들을 생성합니다."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # 1. 감정선 패턴 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS emotion_patterns (
                        id SERIAL PRIMARY KEY,
                        emotion_type VARCHAR(50) NOT NULL,
                        trigger_words TEXT[],
                        psychological_effect TEXT,
                        intensity_level INTEGER CHECK (intensity_level BETWEEN 1 AND 10),
                        target_demographic VARCHAR(100),
                        success_rate DECIMAL(5,2),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 2. 조롱 톤 분석 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS taunt_tone_analysis (
                        id SERIAL PRIMARY KEY,
                        tone_name VARCHAR(100) NOT NULL,
                        description TEXT,
                        emotion_triggers TEXT[],
                        linguistic_features JSONB,
                        effectiveness_score DECIMAL(5,2),
                        age_group VARCHAR(50),
                        cultural_context VARCHAR(100),
                        sample_phrases TEXT[],
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 3. 감정 반응 데이터 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS emotion_response_data (
                        id SERIAL PRIMARY KEY,
                        content_sample TEXT NOT NULL,
                        primary_emotion VARCHAR(50),
                        secondary_emotions TEXT[],
                        arousal_level INTEGER CHECK (arousal_level BETWEEN 1 AND 10),
                        valence_score INTEGER CHECK (valence_score BETWEEN -5 AND 5),
                        engagement_metrics JSONB,
                        demographic_data JSONB,
                        response_time_ms INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 4. 조롱 기법 라이브러리 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS taunt_techniques (
                        id SERIAL PRIMARY KEY,
                        technique_name VARCHAR(100) NOT NULL,
                        category VARCHAR(50),
                        description TEXT,
                        example_usage TEXT,
                        psychological_mechanism TEXT,
                        effectiveness_rating DECIMAL(3,1),
                        safety_level INTEGER CHECK (safety_level BETWEEN 1 AND 5),
                        cultural_appropriateness JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 5. 학습 데이터 세트 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS training_datasets (
                        id SERIAL PRIMARY KEY,
                        dataset_name VARCHAR(200) NOT NULL,
                        content_type VARCHAR(50),
                        raw_data JSONB,
                        processed_data JSONB,
                        metadata JSONB,
                        quality_score DECIMAL(3,1),
                        validation_status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 6. 질문-답변 히스토리 테이블 (향후 자동 개발용)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS qa_history (
                        id SERIAL PRIMARY KEY,
                        session_id VARCHAR(100),
                        question_text TEXT NOT NULL,
                        question_type VARCHAR(50),
                        user_input JSONB,
                        generated_response TEXT,
                        response_metadata JSONB,
                        quality_metrics JSONB,
                        emotion_analysis JSONB,
                        tone_used VARCHAR(100),
                        target_subject VARCHAR(500),
                        keywords TEXT[],
                        response_length INTEGER,
                        safety_analysis JSONB,
                        user_feedback JSONB,
                        development_notes TEXT,
                        approval_status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 7. 흑화 단계 설정 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS darkness_levels (
                        id SERIAL PRIMARY KEY,
                        level_name VARCHAR(50) NOT NULL,
                        level_number INTEGER NOT NULL,
                        description TEXT,
                        intensity_score INTEGER CHECK (intensity_score BETWEEN 1 AND 10),
                        safety_level INTEGER CHECK (safety_level BETWEEN 1 AND 5),
                        psychological_effects JSONB,
                        target_emotions TEXT[],
                        example_characteristics TEXT[],
                        usage_guidelines TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 8. 개발 요청 큐 테이블 (CNN 등 미래 기능)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS development_queue (
                        id SERIAL PRIMARY KEY,
                        feature_name VARCHAR(200) NOT NULL,
                        feature_type VARCHAR(50),
                        description TEXT,
                        priority_level INTEGER DEFAULT 5,
                        technical_requirements JSONB,
                        expected_benefits JSONB,
                        estimated_complexity INTEGER,
                        related_qa_ids INTEGER[],
                        approval_status VARCHAR(20) DEFAULT 'pending',
                        implementation_status VARCHAR(20) DEFAULT 'queued',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        scheduled_date TIMESTAMP,
                        completed_at TIMESTAMP
                    );
                """)
                
                # 9. 고급 기법 탐지 테이블
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS technique_detection_log (
                        id SERIAL PRIMARY KEY,
                        qa_history_id INTEGER,
                        technique_name VARCHAR(100) NOT NULL,
                        technique_type VARCHAR(50),
                        detection_confidence DECIMAL(3,2),
                        detected_elements JSONB,
                        text_sample TEXT,
                        tone_used VARCHAR(100),
                        target_subject VARCHAR(500),
                        effectiveness_score DECIMAL(3,1),
                        user_feedback JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (qa_history_id) REFERENCES qa_history(id)
                    );
                """)
                
                print("✅ 조롱 연구 데이터베이스 테이블이 성공적으로 생성되었습니다.")
                print("✅ 질문-답변 히스토리 및 개발 큐 테이블이 추가되었습니다.")
    
    def insert_emotion_pattern(self, emotion_type, trigger_words, psychological_effect, 
                             intensity_level, target_demographic, success_rate):
        """감정선 패턴 데이터를 삽입합니다."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO emotion_patterns 
                    (emotion_type, trigger_words, psychological_effect, intensity_level, 
                     target_demographic, success_rate)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (emotion_type, trigger_words, psychological_effect, 
                      intensity_level, target_demographic, success_rate))
                return cur.fetchone()[0]
    
    def insert_taunt_tone(self, tone_name, description, emotion_triggers, 
                         linguistic_features, effectiveness_score, age_group, 
                         cultural_context, sample_phrases):
        """조롱 톤 분석 데이터를 삽입합니다."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO taunt_tone_analysis 
                    (tone_name, description, emotion_triggers, linguistic_features, 
                     effectiveness_score, age_group, cultural_context, sample_phrases)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (tone_name, description, emotion_triggers, 
                      json.dumps(linguistic_features), effectiveness_score, 
                      age_group, cultural_context, sample_phrases))
                return cur.fetchone()[0]
    
    def insert_training_data(self, dataset_name, content_type, raw_data, 
                           processed_data, metadata, quality_score):
        """학습 데이터를 삽입합니다."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO training_datasets 
                    (dataset_name, content_type, raw_data, processed_data, metadata, quality_score)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (dataset_name, content_type, json.dumps(raw_data), 
                      json.dumps(processed_data), json.dumps(metadata), quality_score))
                return cur.fetchone()[0]
    
    def get_training_data_for_gemini(self, limit=1000):
        """Gemini 학습용 데이터를 조회합니다."""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        td.dataset_name,
                        td.content_type,
                        td.processed_data,
                        td.metadata,
                        ep.emotion_type,
                        ep.trigger_words,
                        tta.tone_name,
                        tta.linguistic_features
                    FROM training_datasets td
                    LEFT JOIN emotion_patterns ep ON (td.metadata->>'emotion_type') = ep.emotion_type
                    LEFT JOIN taunt_tone_analysis tta ON (td.metadata->>'tone') = tta.tone_name
                    WHERE td.validation_status = 'approved'
                    AND td.quality_score >= 7.0
                    ORDER BY td.created_at DESC
                    LIMIT %s;
                """, (limit,))
                return cur.fetchall()
    
    def insert_qa_history(self, session_id, question_text, question_type, user_input, 
                         generated_response, response_metadata, quality_metrics, 
                         emotion_analysis, tone_used, target_subject, keywords, 
                         response_length, safety_analysis, development_notes=None):
        """질문-답변 히스토리를 저장합니다."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO qa_history 
                    (session_id, question_text, question_type, user_input, generated_response,
                     response_metadata, quality_metrics, emotion_analysis, tone_used,
                     target_subject, keywords, response_length, safety_analysis, development_notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (session_id, question_text, question_type, json.dumps(user_input),
                      generated_response, json.dumps(response_metadata), 
                      json.dumps(quality_metrics), json.dumps(emotion_analysis),
                      tone_used, target_subject, keywords, response_length,
                      json.dumps(safety_analysis), development_notes))
                return cur.fetchone()[0]
    
    def insert_development_request(self, feature_name, feature_type, description, 
                                 priority_level, technical_requirements, expected_benefits,
                                 estimated_complexity, related_qa_ids=None):
        """개발 요청을 큐에 추가합니다."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO development_queue 
                    (feature_name, feature_type, description, priority_level,
                     technical_requirements, expected_benefits, estimated_complexity, related_qa_ids)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (feature_name, feature_type, description, priority_level,
                      json.dumps(technical_requirements), json.dumps(expected_benefits),
                      estimated_complexity, related_qa_ids))
                return cur.fetchone()[0]
    
    def insert_darkness_level(self, level_name, level_number, description,
                            intensity_score, safety_level, psychological_effects,
                            target_emotions, example_characteristics, usage_guidelines):
        """흑화 단계 데이터를 삽입합니다."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO darkness_levels 
                    (level_name, level_number, description, intensity_score, safety_level,
                     psychological_effects, target_emotions, example_characteristics, usage_guidelines)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (level_name, level_number, description, intensity_score, safety_level,
                      json.dumps(psychological_effects), target_emotions, 
                      example_characteristics, usage_guidelines))
                return cur.fetchone()[0]
    
    def get_darkness_levels(self):
        """모든 흑화 단계를 조회합니다."""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM darkness_levels 
                    ORDER BY level_number ASC;
                """)
                return cur.fetchall()
    
    def get_pending_development_requests(self):
        """승인 대기 중인 개발 요청들을 조회합니다."""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM development_queue 
                    WHERE approval_status = 'pending'
                    ORDER BY priority_level DESC, created_at ASC;
                """)
                return cur.fetchall()
    
    def insert_technique_detection(self, qa_history_id, technique_name, technique_type,
                                 detection_confidence, detected_elements, text_sample,
                                 tone_used, target_subject, effectiveness_score=None):
        """고급 기법 탐지 결과를 저장합니다."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO technique_detection_log 
                    (qa_history_id, technique_name, technique_type, detection_confidence,
                     detected_elements, text_sample, tone_used, target_subject, effectiveness_score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (qa_history_id, technique_name, technique_type, detection_confidence,
                      json.dumps(detected_elements), text_sample, tone_used, target_subject,
                      effectiveness_score))
                return cur.fetchone()[0]
    
    def get_technique_usage_statistics(self, technique_name=None):
        """기법 사용 통계를 조회합니다."""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if technique_name:
                    cur.execute("""
                        SELECT 
                            technique_name,
                            COUNT(*) as usage_count,
                            AVG(detection_confidence) as avg_confidence,
                            AVG(effectiveness_score) as avg_effectiveness,
                            tone_used,
                            COUNT(DISTINCT target_subject) as unique_targets
                        FROM technique_detection_log 
                        WHERE technique_name = %s
                        GROUP BY technique_name, tone_used
                        ORDER BY usage_count DESC;
                    """, (technique_name,))
                else:
                    cur.execute("""
                        SELECT 
                            technique_name,
                            COUNT(*) as usage_count,
                            AVG(detection_confidence) as avg_confidence,
                            AVG(effectiveness_score) as avg_effectiveness
                        FROM technique_detection_log 
                        GROUP BY technique_name
                        ORDER BY usage_count DESC;
                    """)
                return cur.fetchall()

if __name__ == "__main__":
    db = TauntResearchDB()
    db.init_database()
