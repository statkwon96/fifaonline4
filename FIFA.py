import urllib
import datetime
import requests
import pandas as pd
from PIL import Image
from typing import List
from bs4 import BeautifulSoup

class MetaData:
    """
    데이터는 매일 3, 9, 15, 21시에 갱신을 시작하며 최대 한시간까지 소요될 수 있습니다.
    갱신된 데이터는 갱신시작 시점을 기준으로 3시간 전 데이터까지 반영됩니다.
    """
    def __init__(self):
        pass
    
    def matchtype(self):
        """
        매치 종류(matchtype) 메타데이터를 조회합니다.
        
        Returns
        -------
        matchtype_dict : {30: '리그 친선'}
        matchtype_dict_r : {'리그 친선': 30}
        """
        matchtype_url = 'https://static.api.nexon.co.kr/fifaonline4/latest/matchtype.json'
        matchtype_res = requests.get(matchtype_url)
        print(matchtype_res)
        
        matchtype_json = matchtype_res.json()
        matchtype_json_df = pd.DataFrame(matchtype_json)
        
        matchtype_dict = matchtype_json_df.set_index('matchtype')['desc'].to_dict()
        matchtype_dict_r = matchtype_json_df.set_index('desc')['matchtype'].to_dict()
        
        return matchtype_dict, matchtype_dict_r
    
    def spid(self):
        """
        선수 고유 식별자(spid) 메타데이터를 조회합니다
        선수 고유 식별자는 시즌아이디 (seasonid) 3자리 + 선수아이디 (pid) 6자리로 구성되어 있습니다.
        
        Returns
        -------
        spid_dict : {101000001: '데이비드 시먼'}
        spid_dict_r : {'데이비드 시먼': 101000001}
        """
        spid_url = 'https://static.api.nexon.co.kr/fifaonline4/latest/spid.json'
        spid_res = requests.get(spid_url)
        print(spid_res)
        
        spid_json = spid_res.json()
        spid_json_df = pd.DataFrame(spid_json)
        
        spid_dict = spid_json_df.set_index('id')['name'].to_dict()
        spid_dict_r = spid_json_df.set_index('name')['id'].to_dict()
        
        return spid_dict, spid_dict_r
    
    def seasonid(self):
        """
        시즌아이디(seasonId) 메타데이터를 조회합니다.
        시즌아이디는 선수가 속한 클래스를 나타냅니다.
        
        Returns
        -------
        seasonid_dict : {101: 'ICON (ICON)'}
        seasonid_dict_r : {'ICON (ICON)': 101}
        """
        seasonid_url = 'https://static.api.nexon.co.kr/fifaonline4/latest/seasonid.json'
        seasonid_res = requests.get(seasonid_url)
        print(seasonid_res)
        
        seasonid_json = seasonid_res.json()
        seasonid_json_df = pd.DataFrame(seasonid_json)
        
        seasonid_dict = seasonid_json_df.set_index('seasonId')['className'].to_dict()
        seasonid_dict_r = seasonid_json_df.set_index('className')['seasonId'].to_dict()

        return seasonid_dict, seasonid_dict_r
    
    def spposition(self):
        """
        선수 포지션(spposition) 메타데이터를 조회합니다.
        
        Returns
        -------
        spposition_dict : {0: 'GK'}
        spposition_dict_r : {'GK': 0}
        """
        spposition_url = 'https://static.api.nexon.co.kr/fifaonline4/latest/spposition.json'
        spposition_res = requests.get(spposition_url)
        print(spposition_res)
        
        spposition_json = spposition_res.json()
        spposition_json_df = pd.DataFrame(spposition_json)
        
        spposition_dict = spposition_json_df.set_index('spposition')['desc'].to_dict()
        spposition_dict_r = spposition_json_df.set_index('desc')['spposition'].to_dict()
        
        return spposition_dict, spposition_dict_r
    
    def division(self):
        """
        등급 식별자(division) 메타데이터를 조회합니다.
        
        Returns
        -------
        division_dict : {800: '슈퍼챔피언스'}
        division_dict_r : {'슈퍼챔피언스': 800}
        """
        division_url = 'https://static.api.nexon.co.kr/fifaonline4/latest/division.json'
        division_res = requests.get(division_url)
        print(division_res)
        
        division_json = division_res.json()
        division_json_df = pd.DataFrame(division_json)
        
        division_dict = division_json_df.set_index('divisionId')['divisionName'].to_dict()
        division_dict_r = division_json_df.set_index('divisionName')['divisionId'].to_dict()
        
        return division_dict, division_dict_r
    
    def playersaction(self, spid: str):
        """
        playersaction(spid=None)
        
        선수 고유 식별자(spid)로 선수의 액션샷 이미지를 가져옵니다.
        
        특정 선수들은 이미지가 존재하지 않을 수 있습니다.
        
        Returns
        -------
        playersaction_png
        """
        pid = spid - round(spid, -6)
        playersaction1_url = f'https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png'
        playersaction2_url = f'https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{pid}.png'
        players1_url = f'https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/players/p{spid}.png'
        players2_url = f'https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/players/p{pid}.png'
        
        playersaction1_res = requests.get(playersaction1_url)
        playersaction2_res = requests.get(playersaction2_url)
        players1_res = requests.get(players1_url)
        players2_res = requests.get(players2_url)
        
        if playersaction1_res.ok:
            playersaction_png = Image.open(urllib.request.urlopen(playersaction1_res.url))
        elif playersaction2_res.ok:
            playersaction_png = Image.open(urllib.request.urlopen(playersaction2_res.url))
        elif players1_res.ok:
            playersaction_png = Image.open(urllib.request.urlopen(players1_res.url))
        elif players2_res.ok:
            playersaction_png = Image.open(urllib.request.urlopen(players2_res.url))
        else:
            playersaction_png = None
            print('해당 선수의 이미지가 존재하지 않습니다.')
        
        return playersaction_png

class UserData:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def top_n(self, n=100):
        """
        top_n(n=100)
        
        공식홈페이지의 '데이터센터 - 공식경기 랭킹' 창에서 상위 n등 이내의 구단주명 크롤링
        
        Parameters
        ----------
        n: 상위 등수
        
        Returns
        -------
        ranker_list : ['KDF강준호', 'GalaxyXG윤창근', ...]
        """
        if n % 10 != 0:
            raise ValueError('n을 10의 배수 단위로 입력해주세요.')
            
        ranker_list = []
        pages = n // 10
        
        for i in range(1, pages + 1):
            url = f'https://fifaonline4.nexon.com/datacenter/rank?n4pageno={i}'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            for j in range(10):
                ranker_list.append(soup.find_all('span', 'name profile_pointer')[j].text)
        
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{time_now} 기준 상위 {len(set(ranker_list))}명의 랭커 닉네임을 저장하였습니다.')
        
        return ranker_list
    
    def nick2id(self, nickname: List[str]):
        """
        nick2id(nickname=None)
        
        유저의 닉네임으로 유저 고유 식별자를 조회합니다.
        유저 고유 식별자는 유저 정보를 조회할 때에 사용됩니다.
        
        Parameters
        ----------
        nickname: 유저 닉네임 리스트
        
        Returns
        -------
        userinfo_dict : {'298dc8278f421dc3bf3c2fa6': 'Exodus박찬화'}
        userinfo_dict_r : {'Exodus박찬화': 298dc8278f421dc3bf3c2fa6}
        """
        userinfo = []
        
        for i in nickname:
            user_url = f'https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname={i}'
            user_res = requests.get(user_url, headers={'Authorization':self.api_key})
            user_json = user_res.json()
            userinfo.append(user_json)
        
        userinfo_json_df = pd.DataFrame(userinfo)
        userinfo_dict = userinfo_json_df.set_index('accessId')['nickname'].to_dict()
        userinfo_dict_r = userinfo_json_df.set_index('nickname')['accessId'].to_dict()
        
        return userinfo_dict, userinfo_dict_r

class MatchData:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def matchinfo(self, accessid: List[str], matchtype=50, offset=0, limit=10):
        """
        matchinfo(accessid=None, matchtype=50, offset=0, limit=10)
        
        유저 고유식별자{accessid}와 매치 종류{matchtype}로 유저의 공식경기 기록을 조회합니다.
        
        유저가 플레이한 매치의 매치 고유 식별자 목록이 반환됩니다.
        반환되는 매치 정보는 가장 최근 플레이한 매치부터 내림차순입니다.
        offset 과 limit을 사용하여 pagination이 가능합니다.
        
        Parameters
        ----------
        accessid : 유저 고유식별자
        matchtype : 매치 종류
        offset: 리스트에서 가져올 시작 위치
        limit: 리스트에서 가져올 갯수(최대 100개)
        
        Returns
        -------
        matchinfo_json : ['6274cc931a6484c5cdaa76d0', '6273fdd85e34db4c94ea43e7', ...]
        """
        matchinfo = []
        
        for i in accessid:
            matchinfo_url = f'https://api.nexon.co.kr/fifaonline4/v1.0/users/{i}/matches?matchtype={matchtype}&offset={offset}&limit={limit}'
            matchinfo_res = requests.get(matchinfo_url, headers={'Authorization':self.api_key})
            matchinfo_json = matchinfo_res.json()
            matchinfo.extend(matchinfo_json)
        
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{time_now} 기준 accessid에 속한 유저들의 최근 {offset + 1}~{offset + limit}번째 경기의 matchid를 저장하였습니다.')
        
        return matchinfo
    
    def matchdetail(self, matchid: List[str]):
        """
        매치 고유 식별자{matchid}로 매치의 상세 정보를 조회합니다.
        매치 시점, 매치 종류와 매치에 참여한 유저의 상세한 매치 통계가 반환됩니다.
        
        ※ 매치 통계가 생성되기 전에 상대방이 매치를 종료할 경우, 상대방의 매치 정보가 보이지 않을 수도 있습니다.
        
        Parameters
        ----------
        matchid: 매치 고유 식별자
        
        Returns
        -------
        matchdetail_json : {'matchId': '6274cc931a6484c5cdaa76d0',
                            'matchDate': '2022-05-06T16:32:02',
                            'matchType': 50,
                            'matchInfo': [...]}
        """
        matchdetail = []
        for i in matchid:
            matchdetail_url = f'https://api.nexon.co.kr/fifaonline4/v1.0/matches/{i}'
            matchdetail_res = requests.get(matchdetail_url, headers={'Authorization':self.api_key})
            matchdetail_json = matchdetail_res.json()
            matchdetail.append(matchdetail_json)
        
        return matchdetail

class Dataset:
    def __init__(self):
        pass
    
    def team_korea(self):
        """
        대한민국 팀컬러에 주로 사용되는 선수들의 리스트를 반환합니다.
        """
        self.team_korea_ = ['고정운', '기성용', '김민재', '김태환', '박주영', '손흥민', '유상철', '윤석영', '이동준',
                   '이범영', '이창민', '지동원', '차두리', '차범근', '홍명보', '홍정호', '홍철']
        
        return self.team_korea_
    
    def dataset(self, matchdetail, spid_dict):
        """
        매치 상세 정보를 데이터프레임으로 가공합니다.
        
        Parameters
        ----------
        matchdetail: 매치 상세 정보
        spid_dict: 'MetaData' 클래스의 'spid' 함수를 통해 얻을 수 있는 선수 고유 식별자 딕셔너리
        """
        team_korea = set(self.team_korea_)
        matchdetail_df = pd.DataFrame()
        
        for i in matchdetail:
            matchinfo = i['matchInfo']
            if len(matchinfo) != 2:
                continue
            
            match_dict = {}
            match_dict.update({'matchId':i['matchId']})
            
            for j in [0, 1]:
                match_dict.update(matchinfo[j]['matchDetail'])
                match_dict.update(matchinfo[j]['shoot'])
                match_dict.update(matchinfo[j]['pass'])
                match_dict.update(matchinfo[j]['defence'])
                players = set(spid_dict[i['spId']] for i in matchinfo[j]['player'])
                
                if len(team_korea.intersection(players)) > 5:
                    match_dict.update({'korea':'Y'})
                else:
                    match_dict.update({'korea':'N'})
                
                match_dict_df = pd.DataFrame([match_dict.values()], columns=match_dict.keys())
                matchdetail_df = pd.concat([matchdetail_df, match_dict_df], ignore_index=True)
        
        return matchdetail_df