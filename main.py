import pymysql

def survey():
    teams = {
        1:'LG 트윈스',
        2:'KT wiz',
        3:'삼성 라이온즈',
        4:'KIA 타이거즈',
        5:'두산 베어스',
        6:'한화 이글스',
        7:'NC 다이노스',
        8:'SSG 랜더스',
        9:'키움 히어로즈',
        10:'롯데 자이언츠'
    }
    selected_team = ""
    print('1. LG 트윈스\n2. KT wiz\n3. 삼성 라이온즈\n4.KIA 타이거즈\n5.두산 베어스\n6.한화 이글스\n7.NC 다이노스\n8.SSG 랜더스\n9.키움 히어로즈\n10.롯데 자이언츠\n11.기타(직접 입력해주세요)')
    while True:
        answer=input('선택해주세요')
        if answer.isdecimal():
            answer=int(answer)
        else:
            print('잘못된 입력입니다. 다시 선택해주세요.')
            continue
        if answer==11:
            selected_team=input('직접 입력해주세요.')
            break
        elif 0<answer<11:
            print(f'{answer}번을 선택하셨습니다.')
            selected_team =teams[answer]
            break
        else:
            print('없는 번호입니다. 다시 선택해주세요.')
            continue
    print('설문이 완료되었습니다. 감사합니다.')
    
    return selected_team

def connect_db(database_name=None):
    conn=pymysql.connect(
        host='localhost',
        user='surveyowner',
        password='survey1234',
        database=database_name
    )
    return conn

def create_db():
    conn=connect_db()
    try:
        with conn.cursor() as cursor:
            sql = 'CREATE DATABASE IF NOT EXISTS testdb;'
            cursor.execute(sql)
        conn.commit()
        print('확인&생성')
    finally:
        conn.close()

def create_table():
    conn = connect_db(database_name='testdb')
    try:
        with conn.cursor() as cursor:
            sql = """
            CREATE TABLE IF NOT EXISTS SURVEY (
                NO INT AUTO_INCREMENT PRIMARY KEY,
                TEAM VARCHAR(50)
            );
            """
            cursor.execute(sql)
        conn.commit()
        print('테이블 ok')
    finally:
        conn.close()
def save_vote(votename=None):
    conn = connect_db(database_name='testdb')
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO SURVEY (TEAM) VALUES(%s);"
            cursor.execute(sql,(votename,))
        conn.commit()
        print(f"{votename} 투표 데이터 기록 완료")
    finally:
        conn.close()

def show_result():
    teams = [
        'LG 트윈스',
        'KT wiz',
        '삼성 라이온즈',
        'KIA 타이거즈',
        '두산 베어스',
        '한화 이글스',
        'NC 다이노스',
        'SSG 랜더스',
        '키움 히어로즈',
        '롯데 자이언츠'
    ]

    vote_summary = {team: 0 for team in teams}

    conn = connect_db(database_name='testdb')

    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT TEAM, COUNT(*) AS cnt
            FROM SURVEY
            GROUP BY TEAM;
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            for team_name, count in results:
                vote_summary[team_name] = count

        print("===== 설문 결과 =====")

        for team, count in vote_summary.items():
            print(f"{team}: {count}표")

    finally:
        conn.close()
if __name__ == "__main__":
        
    create_db()
    create_table()
    print("선호하는 야구 팀 설문조사")
    print("1. 설문조사 참여하기")
    print("2. 설문 결과 확인하기")
    choice=input('선택:')
    if choice == '1':
        user_choice = survey()

        save_vote(user_choice)
    elif choice == '2':
        show_result()