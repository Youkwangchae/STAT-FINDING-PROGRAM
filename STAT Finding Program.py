import bs4, requests
from bs4 import BeautifulSoup

#olayer 리스트로 가져옴.
def get_player(soup):
    get_player=[]
    for tds in soup.find_all('td',attrs={'style':"white-space:nowrap;text-align:center;vertical-align:middle;"}):
        if(tds.find('a')):
            get_player.append(tds.find('a').text)
    player=[]
    for i in range(int(len(get_player)/2)):
        player.append(get_player[i])
    return player
                

# stat 리스트로 가져옴.
def get_stat(soup):
    get_stat = []
    stats = ""
    for tag in soup.find_all('td', attrs = {'style':"text-align:right;background:#DDDDDD;color:white;font-weight:bold;border-left:2px solid #333333; border-right:2px solid #333333;"}):
        if(tag.find('span')):
           get_stat.append(tag.find('span').text)
    stat=[]
    for i in range(int(len(get_stat)/2)):
        stat.append(get_stat[i])
    return stat
        
#player 리스트와 stat 리스트 각 데이터를 리스트로 저장.
def get_list(year,record,stat_kind,stat, soup):
    players_stats=[]
    players = get_player(soup)
    stats = get_stat(soup)
    for i in range(len(stats)):
        if(int(float(stats[i]))>=record):
            player_stats = [year,players[i],stat_kind,stats[i]]
            players_stats.append(player_stats)
    return players_stats

def find(a, stat_kind, search_kind):
    stat_string = ""
    ch = True
    j=0
    for stat in stat_kind:
        stat_string+=str(j+1)+" : "+stat_kind[j]+", "
        j+=1
    stat_string = stat_string[:-2]
    while(ch):
        b=False
        print()
        print("어떤 기록을 조회할까요?")
        print(stat_string)
        print("단, 최대 세개까지만 입력해주세요. 구분자는"+"', '"+"입니다.")
        stat = input("찾는 기록 : ")
        stat = stat.replace(',','')
        stat = stat.split()
        if(len(stat)>3):
            print("기록 조회는 최대 세개까지 가능합니다.")
            continue
        for i in stat:
            if(int(i)<=0 or int(i)>8):
                print("1~8의 양의 정수만 입력하세요")
                b = False
            else:
                b = True
            if(b):
                break
        search_list = []
        for i in stat:
            search_list.append(search_kind[int(i)-1])
        record = []
        for st in stat:                
            record.append(int(input(stat_kind[int(st)-1]+"의 기준 개수 : ")))
            
        print()
        print("기록을 조회하는 중입니다...")
        print("======================================")
        print("기준 기록이 너무 작은 경우, 시간순으로 이른 순부터 50명만 출력합니다.")
        print()
        j=0
        member_list=[]
        ty =""
        re = ""
        if(a==1):
            ty = "TPA"
            re = "0"
        else:
            ty = "OutCount"
            re = "1"
        
        for a_stat in search_list:
            m1 = []
            for year in range(1982,2021):
                url = "http://www.statiz.co.kr/stat.php?mid=stat&re="+re+"&ys="+str(year)+"&ye="+str(year)+"&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1="+a_stat+"&o2="+ty+"&de=1&lr=0&tr=&cv=&ml=1&sn=30&si=&cn="
                response = requests.get(url) 
                soup= BeautifulSoup(response.text,'html.parser')
        
                stat_list = get_list(year,record[j],stat_kind[int(stat[j])-1],stat,soup)
                for i in stat_list:
                    m1.append(i)
            j=j+1
            member_list.append(m1)
        print("조회 완료!")
        result_list = []
        if(len(member_list)==1):
            a_list = []
            for player_stat in member_list[0]:
                a_list.append(player_stat)
            for p1 in a_list:
                result_list.append(list([p1[0], p1[1], p1[2], p1[3]]))


        elif(len(member_list)==2):
            a_list = []
            b_list = []
            for player_stat in member_list[0]:
                a_list.append(player_stat)
                        
            for player_stat in member_list[1]:
                b_list.append(player_stat)

            for p1 in a_list:
                for p2 in b_list:
                    if(p1[0]==p2[0] and p1[1]==p2[1]):
                        result_list.append(list([p1[0], p1[1], p1[2], p1[3], p2[2], p2[3]]))

        elif(len(member_list)==3):
            a_list=[]
            b_list=[]
            c_list=[]
            for player_stat in member_list[0]:
                a_list.append(player_stat)
                        
            for player_stat in member_list[1]:
                b_list.append(player_stat)
                    
            for player_stat in member_list[2]:
                c_list.append(player_stat)

            for p1 in a_list:
                for p2 in b_list:
                    for p3 in c_list:
                        if(p1[0]==p2[0] and p2[0]==p3[0] and p1[1]==p2[1] and p2[1]==p3[1]):
                            result_list.append(list([p1[0], p1[1], p1[2], p1[3], p2[2], p2[3], p3[2], p3[3]]))
        if(len(result_list)==0 or result_list == list([[]])):
            print("기준을 만족하는 선수가 없습니다!")
            print("기준을 낮춰서 입력하거나 다른 기준으로 검색하세요!")
        elif(len(result_list)>50):
            for i in range(50):
                print(result_list[i])
            print("기준을 만족하는 선수가 너무 많아 이른 시간 기준으로 50명만 출력했습니다.")
        else:
            for result in result_list:
                print(result)
        while(True):
            c = input("다시 조회하시겠습니까?(Y또는 N입력):")
            if(c == "Y"):
                ch = True
                break
            elif(c=="N"):
                print("이전 화면으로 돌아갑니다.\n")
                ch = False
                break
            else:
                print("Y또는 N중에서 입력해주세요.\n")
            
################### main ######################
choice = True
while(choice):
    print("★☆★☆STAT Finding Program☆★☆★")
    print("1 : 타자 검색, 2 : 투수 검색, 3 : 종료")
    menu = input("메뉴를 선택해주세요 :")
    if (not menu.isnumeric()):
        print("입력하신 값은 정수가 아닙니다.")
        continue
    elif(int(menu)<=0 or int(menu)>=4):
        print("1 또는 2 또는 3만 입력하세요")
        continue
    elif(int(menu)==1):
        stat_kind = ['홈런', '타점', '안타', '도루','득점','볼넷','삼진','병살']
        search_kind = ['HR', 'RBI', 'H', "SB", "R", "BB", "SO", "GDP"]
        find(int(menu),stat_kind,search_kind)
            
    elif(int(menu)==2):
        stat_kind = ['경기 수','이닝', '다승', '세이브','다패','홀드','삼진','볼넷']
        search_kind = ['GP','OutCount', 'Win', "SV", "Loss", "HLD", "SO", "BB"]
        find(int(menu),stat_kind,search_kind)
    elif(int(menu)==3):
        print("프로그램 종료")
        choice = False
        
    
#2010 WAR 타자    
#http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=0&ys=2010&ye=2010&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=30&si=&cn=    

#2010 WAR 투수
#http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=1&ys=2010&ye=2010&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR&o2=OutCount&de=1&lr=0&tr=&cv=&ml=1&sn=30&si=&cn=
               
#홈런, 안타, 도루, 타점에 대해서 수행함.
#순위+이름+년도+소속팀+포지션의 형태인데 년도+{이름 + 기록형태}로 분리함.
#여러 기록 겹쳐서 검색
#타자 기록(득점, 볼넷, 삼진, 병살) 검색 추가
#투수 기록 검색 추가

