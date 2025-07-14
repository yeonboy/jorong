
import json
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from database_setup import TauntResearchDB
import matplotlib.pyplot as plt
import pandas as pd

class UserAnalytics:
    def __init__(self):
        self.db = TauntResearchDB()
    
    def analyze_user_patterns(self, days=30):
        """사용자 사용 패턴을 분석합니다."""
        print(f"📊 최근 {days}일간 사용자 분석 시작...")
        
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                # 전체 사용량 통계
                cur.execute("""
                    SELECT 
                        COUNT(*) as total_requests,
                        COUNT(DISTINCT session_id) as unique_users,
                        AVG(response_length) as avg_response_length,
                        DATE(created_at) as date
                    FROM qa_history 
                    WHERE created_at >= %s
                    GROUP BY DATE(created_at)
                    ORDER BY date DESC;
                """, (datetime.now() - timedelta(days=days),))
                
                daily_stats = cur.fetchall()
                
                # 톤별 사용 통계
                cur.execute("""
                    SELECT 
                        tone_used,
                        COUNT(*) as usage_count,
                        AVG(CAST(quality_metrics->>'readability_score' AS FLOAT)) as avg_quality,
                        AVG(response_length) as avg_length
                    FROM qa_history 
                    WHERE created_at >= %s AND tone_used IS NOT NULL
                    GROUP BY tone_used
                    ORDER BY usage_count DESC;
                """, (datetime.now() - timedelta(days=days),))
                
                tone_stats = cur.fetchall()
                
                # 타겟 주제 분석
                cur.execute("""
                    SELECT 
                        target_subject,
                        COUNT(*) as frequency,
                        tone_used,
                        AVG(response_length) as avg_length
                    FROM qa_history 
                    WHERE created_at >= %s AND target_subject IS NOT NULL
                    GROUP BY target_subject, tone_used
                    ORDER BY frequency DESC
                    LIMIT 20;
                """, (datetime.now() - timedelta(days=days),))
                
                target_stats = cur.fetchall()
        
        return {
            'daily_stats': daily_stats,
            'tone_stats': tone_stats,
            'target_stats': target_stats
        }
    
    def analyze_advanced_techniques(self):
        """고급 기법 사용 분석"""
        print("🧠 고급 기법 사용 분석 시작...")
        
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                # Aposiopesis 기법 사용 통계
                cur.execute("""
                    SELECT 
                        technique_name,
                        COUNT(*) as usage_count,
                        AVG(detection_confidence) as avg_confidence,
                        AVG(effectiveness_score) as avg_effectiveness,
                        tone_used
                    FROM technique_detection_log
                    GROUP BY technique_name, tone_used
                    ORDER BY usage_count DESC;
                """)
                
                technique_stats = cur.fetchall()
                
                # 최근 탐지된 고급 기법들
                cur.execute("""
                    SELECT 
                        tdl.technique_name,
                        tdl.detection_confidence,
                        tdl.effectiveness_score,
                        tdl.tone_used,
                        tdl.target_subject,
                        qh.user_input,
                        qh.created_at
                    FROM technique_detection_log tdl
                    JOIN qa_history qh ON tdl.qa_history_id = qh.id
                    WHERE tdl.created_at >= %s
                    ORDER BY tdl.created_at DESC
                    LIMIT 10;
                """, (datetime.now() - timedelta(days=7),))
                
                recent_techniques = cur.fetchall()
        
        return {
            'technique_stats': technique_stats,
            'recent_techniques': recent_techniques
        }
    
    def analyze_safety_patterns(self):
        """안전성 패턴 분석"""
        print("🛡️ 안전성 패턴 분석 시작...")
        
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                # 안전성 점검 결과 통계
                cur.execute("""
                    SELECT 
                        CAST(safety_analysis->>'is_safe' AS BOOLEAN) as is_safe,
                        COUNT(*) as count,
                        tone_used,
                        AVG(response_length) as avg_length
                    FROM qa_history 
                    WHERE safety_analysis IS NOT NULL
                    GROUP BY CAST(safety_analysis->>'is_safe' AS BOOLEAN), tone_used
                    ORDER BY count DESC;
                """)
                
                safety_stats = cur.fetchall()
                
                # 위험 요소 분석
                cur.execute("""
                    SELECT 
                        safety_analysis->>'safety_message' as safety_message,
                        COUNT(*) as frequency,
                        tone_used
                    FROM qa_history 
                    WHERE CAST(safety_analysis->>'is_safe' AS BOOLEAN) = false
                    GROUP BY safety_analysis->>'safety_message', tone_used
                    ORDER BY frequency DESC;
                """)
                
                risk_patterns = cur.fetchall()
        
        return {
            'safety_stats': safety_stats,
            'risk_patterns': risk_patterns
        }
    
    def analyze_user_preferences(self):
        """사용자 선호도 분석"""
        print("❤️ 사용자 선호도 분석 시작...")
        
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                # 세션별 톤 선호도
                cur.execute("""
                    SELECT 
                        session_id,
                        tone_used,
                        COUNT(*) as usage_count,
                        AVG(CAST(quality_metrics->>'humor_rating' AS FLOAT)) as avg_humor_rating
                    FROM qa_history 
                    WHERE session_id IS NOT NULL AND tone_used IS NOT NULL
                    GROUP BY session_id, tone_used
                    HAVING COUNT(*) >= 2
                    ORDER BY usage_count DESC;
                """)
                
                user_preferences = cur.fetchall()
                
                # 키워드 트렌드 분석
                cur.execute("""
                    SELECT 
                        unnest(keywords) as keyword,
                        COUNT(*) as frequency,
                        DATE(created_at) as date
                    FROM qa_history 
                    WHERE keywords IS NOT NULL AND array_length(keywords, 1) > 0
                    AND created_at >= %s
                    GROUP BY unnest(keywords), DATE(created_at)
                    ORDER BY frequency DESC
                    LIMIT 50;
                """, (datetime.now() - timedelta(days=30),))
                
                keyword_trends = cur.fetchall()
        
        return {
            'user_preferences': user_preferences,
            'keyword_trends': keyword_trends
        }
    
    def generate_comprehensive_report(self):
        """종합 분석 보고서 생성"""
        print("📋 종합 분석 보고서 생성 중...")
        
        # 모든 분석 데이터 수집
        usage_patterns = self.analyze_user_patterns()
        technique_analysis = self.analyze_advanced_techniques()
        safety_analysis = self.analyze_safety_patterns()
        preference_analysis = self.analyze_user_preferences()
        
        # 보고서 구성
        report = {
            'report_generated': datetime.now().isoformat(),
            'summary': {
                'total_users': len(set([row[1] for row in usage_patterns['daily_stats']])) if usage_patterns['daily_stats'] else 0,
                'total_requests': sum([row[0] for row in usage_patterns['daily_stats']]) if usage_patterns['daily_stats'] else 0,
                'most_popular_tone': usage_patterns['tone_stats'][0][0] if usage_patterns['tone_stats'] else 'N/A',
                'advanced_technique_usage': len(technique_analysis['technique_stats'])
            },
            'usage_patterns': usage_patterns,
            'technique_analysis': technique_analysis,
            'safety_analysis': safety_analysis,
            'preference_analysis': preference_analysis
        }
        
        # 인사이트 생성
        insights = self.generate_insights(report)
        report['insights'] = insights
        
        return report
    
    def generate_insights(self, report_data):
        """데이터 기반 인사이트 생성"""
        insights = []
        
        # 톤 사용 인사이트
        if report_data['usage_patterns']['tone_stats']:
            top_tone = report_data['usage_patterns']['tone_stats'][0]
            insights.append({
                'category': '톤 사용 패턴',
                'insight': f"가장 인기있는 톤은 '{top_tone[0]}'로 {top_tone[1]}회 사용되었습니다.",
                'recommendation': f"이 톤의 성공 요소를 다른 톤에도 적용해보세요."
            })
        
        # 안전성 인사이트
        if report_data['safety_analysis']['safety_stats']:
            safe_ratio = sum([row[1] for row in report_data['safety_analysis']['safety_stats'] if row[0]]) / sum([row[1] for row in report_data['safety_analysis']['safety_stats']])
            insights.append({
                'category': '안전성',
                'insight': f"전체 요청의 {safe_ratio*100:.1f}%가 안전한 것으로 판정되었습니다.",
                'recommendation': "위험 요소 탐지 시스템이 효과적으로 작동하고 있습니다." if safe_ratio > 0.9 else "안전성 필터를 강화할 필요가 있습니다."
            })
        
        # 고급 기법 인사이트
        if report_data['technique_analysis']['technique_stats']:
            advanced_usage = len(report_data['technique_analysis']['technique_stats'])
            insights.append({
                'category': '고급 기법',
                'insight': f"{advanced_usage}가지 고급 기법이 탐지되었습니다.",
                'recommendation': "사용자들이 다양한 고급 기법을 활용하고 있어 시스템이 성숙해지고 있습니다."
            })
        
        return insights
    
    def export_report_to_file(self, report, filename=None):
        """보고서를 파일로 저장"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"user_analytics_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"📁 분석 보고서가 {filename}에 저장되었습니다.")
        return filename

if __name__ == "__main__":
    analytics = UserAnalytics()
    report = analytics.generate_comprehensive_report()
    
    print("\n" + "="*60)
    print("🎯 조롱 프로젝트 사용자 분석 보고서")
    print("="*60)
    
    # 요약 정보 출력
    summary = report['summary']
    print(f"\n📊 전체 요약:")
    print(f"  • 총 사용자 수: {summary['total_users']}명")
    print(f"  • 총 요청 수: {summary['total_requests']}회")
    print(f"  • 가장 인기있는 톤: {summary['most_popular_tone']}")
    print(f"  • 고급 기법 사용 종류: {summary['advanced_technique_usage']}가지")
    
    # 톤별 사용 통계
    if report['usage_patterns']['tone_stats']:
        print(f"\n🎭 톤별 사용 통계 (상위 5개):")
        for i, (tone, count, quality, length) in enumerate(report['usage_patterns']['tone_stats'][:5], 1):
            print(f"  {i}. {tone}: {count}회 사용 (품질: {quality:.1f}, 평균길이: {length:.0f}자)")
    
    # 안전성 통계
    if report['safety_analysis']['safety_stats']:
        print(f"\n🛡️ 안전성 통계:")
        for is_safe, count, tone, avg_length in report['safety_analysis']['safety_stats'][:3]:
            status = "안전" if is_safe else "위험"
            print(f"  • {status}: {count}회 ({tone} 톤)")
    
    # 인사이트 출력
    if report['insights']:
        print(f"\n💡 주요 인사이트:")
        for insight in report['insights']:
            print(f"  🔍 {insight['category']}: {insight['insight']}")
            print(f"     💬 권장사항: {insight['recommendation']}")
    
    # 파일로 저장
    filename = analytics.export_report_to_file(report)
    print(f"\n📋 상세 보고서는 {filename}에서 확인하실 수 있습니다.")
