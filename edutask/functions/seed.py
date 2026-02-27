import os
from google.cloud import firestore
from google.auth.credentials import AnonymousCredentials
import datetime
import random

# 파이어베이스 에뮬레이터 환경변수 설정 (포트는 앞서 설정한 8082로 연결)
os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8082"

# Firebase Admin 대신 google-cloud-firestore 직접 사용하여 인증 우회 (Emulator 전용)
db = firestore.Client(project="edutask-54a15", credentials=AnonymousCredentials())

def seed_data():
    print("🌱 Firestore 에뮬레이터에 샘플 데이터 파종을 시작합니다...")

    # 1. 선생님 계정 생성 (users collection)
    teacher_ref = db.collection('users').document('teacher_001')
    teacher_ref.set({
        'role': 'TEACHER',
        'name': '김선생',
        'email': 'kim@edutask.com',
        'createdAt': firestore.SERVER_TIMESTAMP
    })
    print("✅ [1/5] 선생님 계정 생성 (김선생)")

    # 2. 학급 생성 (classes collection)
    class_ref = db.collection('classes').document('class_1A')
    class_ref.set({
        'teacherId': teacher_ref.id,
        'name': '중등 1학년 A반',
        'course': '중등 수학 기본',
        'academicYear': '2026',
        'createdAt': firestore.SERVER_TIMESTAMP
    })
    print("✅ [2/5] 학급 데이터 생성 (중등 1학년 A반)")

    # 3. 학생 데이터 생성 (classes/{classId}/students sub-collection)
    students_data = [
        {'id': 'student_01', 'name': '이철수', 'personality': '집중력이 좋으나 응용에 약함', 'parentContact': '010-1111-2222'},
        {'id': 'student_02', 'name': '김영희', 'personality': '질문이 많고 적극적임', 'parentContact': '010-3333-4444'},
        {'id': 'student_03', 'name': '박지민', 'personality': '조용하고 성실함', 'parentContact': '010-5555-6666'}
    ]
    
    for s_data in students_data:
        student_doc = class_ref.collection('students').document(s_data['id'])
        student_doc.set({
            'name': s_data['name'],
            'personality': s_data['personality'],
            'parentContact': s_data['parentContact'],
            'profileImageUrl': '',
            'createdAt': firestore.SERVER_TIMESTAMP
        })
    print(f"✅ [3/5] 학생 샘플 데이터 생성 완료 ({len(students_data)}명)")

    # 4. 수업 매니저 기록 (lesson_records collection)
    record_ref = db.collection('lesson_records').document('lesson_001')
    record_ref.set({
        'classId': class_ref.id,
        'date': datetime.datetime.now(datetime.timezone.utc),
        'textbookName': '개념원리 수학 중1-1',
        'totalPages': 15,
        'progressRange': 'p.30 ~ p.45 (일차방정식의 기초)',
        'createdAt': firestore.SERVER_TIMESTAMP
    })
    print("✅ [4/5] 수업 매니저 기록 데이터 생성")

    # 5. 학생별 이해도 분석 기록 (lesson_records/{recordId}/understandings)
    for s_data in students_data:
        understanding_doc = record_ref.collection('understandings').document(s_data['id'])
        level = random.randint(2, 5) # 1~5단계 (샘플데이터를 위한 랜더마이즈)
        understanding_doc.set({
            'studentId': s_data['id'],
            'level': level,
            'weaknessType': '이항 과정에서의 부호 실수 빈번' if level <= 3 else '특이사항 없음',
            'aiFeedback': '주의: 특정 마의 구간(부호 연산)에서 정답률이 떨어지고 있으니 보충 문제가 필요합니다.' if level <= 3 else '이해도가 탁월합니다.'
        })
    print("✅ [5/5] 학생별 이해도 및 AI 분석 데이터 생성")

    print("\n🎉 모든 샘플 데이터가 Firestore 에뮬레이터에 성공적으로 업로드되었습니다!")

if __name__ == '__main__':
    seed_data()
