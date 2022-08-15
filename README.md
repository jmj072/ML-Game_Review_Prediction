# 게임 리뷰 평가 예측 API

## 프로젝트 진행 배경
- Steam은 밸브 코퍼레이션에서 개발한 게임 플랫폼으로, 인디게임에서 AAA급 대형 게임까지, 다양한 장르의 게임들을 관리 및 배급한다.
- Steam의 고객 평가(리뷰) 서비스는 실제 플레이어들의 리뷰와 부정/긍정 평가를 통해 게임 개발자와 유저들간의 적극적인 피드백을 가능하게 한다.
- 또한, 이러한 유저 평가는 게임 판매량에도 영향을 줄 수 있다.

- 실제 리뷰 예시

	<img src="https://user-images.githubusercontent.com/77204538/175938443-252b7e22-4a46-410e-b3d4-82e83f613ef3.png" height=300>
  
	<img src="https://user-images.githubusercontent.com/77204538/175938439-c3c4fae2-2788-4908-860c-fae1ee49e4f5.png" height=300>

<br>

## 프로젝트 목표

> ☑ 따라서, 게임 판매에 중요한 유저들의 평가를 예측하는 모델을 생성하여,  
> 게임 개발자들에게 어떤 게임이 판매량에 영향을 주는지 인사이트를 제공하여 도움을 주고자 한다.
 
<br>

## 개발 환경
- Python 3.8
- ElephantSQL (PostgreSQL)
- Google Colab
- 사용한 library & Tools
	- `pandas`, `scikit-learn`, `requests`, `BeautifulSoup`, `Flask`, `Bootstrap` ,`Heroku`, `Google Data Studio`

<br>

## 파일 구성

- `1_데이터 수집_저장`
	- `1_1_steamspyAPI`
		- `1_1_1_getSalesData.py`
			- steamspy API를 이용하여 게임 데이터셋 형성
			- 웹 스크래핑에 필요한 게임 id와 게임 이름을 따로 추출하였음
		- `1_1_2_steamspy_details.csv`
			-  steamspy API를 이용하여 추출된 데이터
		- `1_1_3_app_list.csv`
			- 웹 스크래핑에 이용하기 위해, 추출된 데이터 중 게임 ID와 게임 이름을 따로 저장한 데이터
	


	- `1_2_webscraping`
		- `1_2_1_webscraping.py`
			- steamspy API에서는 **게임 출시일, 게임 가격, 스팀 유저 긍정 평가 비율, 메타 크리틱 점수**는 얻을 수 없어서 직접 steamspy를 **웹 스크래핑**하여 추출함
			- 앞선 단계의 `app_list.csv`를 이용하여 **게임 id와 게임 이름을 이용해 검색 후 추출**
			- 추출된 데이터는 `steamspy_other_details.csv` 로 저장함
    	- `1_2_2_steamspy_other_details.csv`
			- 웹 스크래핑으로 추출된 게임 출시일, 게임 가격, 스팀 유저 긍정 평가 비율, 메타 크리틱 점수


	- `1_3_Database`
    	- `1_3_1_DB_load.py`
        	- `1_1_2_steamspy_details.csv`, `1_1_3_app_list.csv`, `1_2_2_steamspy_other_details.csv` 를 DB에 저장
		- `1_3_2_DataCleaning.ipynb`
			-  `1_1_2_steamspy_details.csv` 와 `1_2_2_steamspy_other_details.csv` 를 merge하고 전처리한 후, `1_3_3_steamspy_dataset.csv`, DB에 저장
		- `1_3_3_steamspy_dataset.csv`
			- `1_1_2_steamspy_details.csv` 와 `1_2_2_steamspy_other_details.csv` 를 merge한 Dataset
			
- `2_EDA_Model_training.ipynb`
	- 저장된 DB를 DataFrame으로 변환하여 EDA와 모델링 진행
- `3_웹배포`
	- 웹배포 진행한 폴더
	- `3_1_Game_Review_Prediction_API`
    	- 웹 API 배포관련 폴더
    	- `3_1_1_templates`
    		- 웹페이지 Template 저장
    	- `3_1_2___init__.py`
    		- 웹 배포 실행
    	- `3_1_3_model.pickle`
    		- 최적화된 Voing Classifier 모델
  	- `3_2_Procfile`
    	- gunicorn을 통한 Heroku 배포 관련 파일
	- `3_3_requirements.txt`
		- 웹 배포시 개발 환경 작성
<br>

## Pipeline
<img src="https://user-images.githubusercontent.com/77204538/180379973-718fb100-2de3-4875-8f42-3f2a89aadbaa.png">

<br>

## 1. Dataset
> 2022.07.22에 1만여개의 데이터를 추가로 수집하였음
- Steamspy(https://steamspy.com/)

	<img src="https://user-images.githubusercontent.com/77204538/175939213-02e3b1b9-618b-48f6-8d8f-802f215e097d.png" height=400>
	
	- Steam 사용자들의  게임  구매  이력을  이용해 게임  판매량  순위를  시각화
	- Steam 에 작성되어  있는  게임에  대한  정보, 플레이어  리뷰, 평가  점수를 제공함

<br>	

- Steamspy API에서 제공하는 기능을 이용하여, 게임 데이터를 수집함
	<details>
	<summary>💻 Steamspy API에서 수집한 데이터 </summary>
	<div markdown="1">    

	- appid - Steam Application ID. If it's 999999, then data for this application is hidden on developer's request, sorry.
	- name - game's name
	- developer - comma separated list of the developers of the game
	- publisher - comma separated list of the publishers of the game
	- score_rank - score rank of the game based on user reviews
	- owners - owners of this application on Steam as a range.
	- average_forever - average playtime since March 2009. In minutes.
	- average_2weeks - average playtime in the last two weeks. In minutes.
	- median_forever - median playtime since March 2009. In minutes.
	- median_2weeks - median playtime in the last two weeks. In minutes.
	- ccu - peak CCU yesterday. (CCU : “concurrent users”)
	- price - current US price in cents.
	- initialprice - original US price in cents.
	- discount - current discount in percents.
	- tags - game's tags with votes in JSON array.
	- languages - list of supported languages.
	- genre - list of genres.
	- 
	</div>
	</details>  

<br>

- Steamspy API에서 수집할 수 없는 **게임 출시일, 스팀 유저 긍정 평가 비율, 메타 크리틱 점수**는 steamspy 홈페이지를 웹 스크레이핑하여 수집함
- 수집한 데이터를 CSV file로 임시 저장한 후, PostgreSQL기반의 ElephantSQL 서버에 저장함
	<img src="https://user-images.githubusercontent.com/77204538/179453000-0f698d17-d46f-4b0b-8a5b-c3f185dc27fd.png" height=300>

<br>

---

### 1.1 Data Cleaning
- DB에 저장된 `steamspy_details` 와 `steamspy_otherdetails`를 load하여 아래와 같은 전처리를 진행함

<br>

#### 1.1.1 결측치 처리

- **Steam 유저 리뷰 평가점수 / 메타 스코어 결측치 처리**
   - 전체 4만 여개의 데이터 중, 2만 ~ 3만개의 결측치가 발견됨
   - 게임 평론가 평가(메타 스코어)보단 유저 평가가 개발자들에게 유용할 것으로 보이므로, `steam_userscore`의 결측치만 처리하기로 함
   - 긍정적인 리뷰 평가 갯수(`positive_review`), 부정적인 리뷰 평가 갯수(`negative_review`)를 이용하여 계산한다   
      (계산식은 [Steam DB](https://steamdb.info/blog/steamdb-rating/)를 참고함)  
	<img src='https://steamdb.info/static/img/blog/84/formula.png' width=600>

<br>  

- **결측치 제외**
  - `steam_userscore` 결측치 처리 이후, 여전히 결측치로 남아있는 데이터는 제외하였음
  - **게임 가격, 출시연도, 게임 장르와 언어 지원**도 시각화 및 모델링에 중요한 정보이므로, 해당 정보가 없는 경우는 제외하였음
  - **개발사, 유통사** 데이터가 없는 경우는 소량이고 시각화/모델링에 중요한 정보는 아니므로 제외하였음
  - 메타스코어 column은 결측치가 너무 많아 제외하였음

<br>

#### 1.1.2 특성 생성

- `genre`에서 파생 특성 생성
	- `Genre` 특성
    	- `genre` 특성을 살펴보았을때, 여러개의 장르로 분류된 게임들이 존재함
    	- ex) MazM: The Phantom of the Opera : Adventure, RPG, Simulation..
    	- 따라서, Text를 split하여 첫번째 element를 그 게임의 주요장르로 처리함
        - 주요장르를 추출한 이후, 주요장르가 'Action', 'Adventure', 'Casual','Strategy', 'Simulation', 'RPG', 'Sports', 'Racing'가 아닌 경우는 다른 element를 고려하였음
        - 게임이라 고려될 수 없는 Design, AudioProduction, VideoProduction과 같은 장르 게임은 데이터셋에서 제외하였음

			<details>
			<summary>💻 <code>Genre</code> 특성 생성 </summary>
			<div markdown="1">    

			```python
			def genre_split(string):
			split_list = str(string).replace(' ','').split(',')
			return split_list
			```

			```python
			# 장르 중, 첫번째 요소를 대표 장르로 가정함
			df2['FirstGenre'] = df2['genre'].map(lambda x: genre_split(x)[0])
			```    			
			
			```python
			genre_list = ['Action', 'Adventure', 'Casual','Strategy', 'Simulation', 'RPG', 'Sports', 'Racing']
			# Firstgenre가 Indie 인 경우
			df_temp = df2[(df2['FirstGenre'] == 'Indie')]
			for idx, row in df_temp.iterrows():
				tag = row['tags']
				tag_list = tags_split(tag)
				del tag_list[0]
				for element in tag_list :
						if element in genre_list: #첫번째 발견 요소만 if문 실행
							df2.loc[idx, 'FirstGenre'] = element

				if df2.loc[idx, 'FirstGenre'] == 'Indie':
					#print(idx, 'not exist correct genre')    
					df2.loc[idx, 'FirstGenre'] = None

			# Firstgenre가 FreetoPlay 인 경우
			df_temp = df2[(df2['FirstGenre'] == 'FreetoPlay')]
			for idx, row in df_temp.iterrows():
				tag = row['tags']
				tag_list = tags_split(tag)
				del tag_list[0]
				for element in tag_list :
						if element in genre_list: #첫번째 발견 요소만 if문 실행
							df2.loc[idx, 'FirstGenre'] = element

				if df2.loc[idx, 'FirstGenre'] == 'FreetoPlay':
					#print(idx, 'not exist correct genre')    
					df2.loc[idx, 'FirstGenre'] = None

			# Firstgenre가 MassivelyMultiplayer 인 경우  
			df_temp = df2[(df2['FirstGenre'] == 'MassivelyMultiplayer')]
			for idx, row in df_temp.iterrows():
				tag = row['tags']
				tag_list = tags_split(tag)
				del tag_list[0]
				for element in tag_list :
						if element in genre_list: #첫번째 발견 요소만 if문 실행
							df2.loc[idx, 'FirstGenre'] = element

				if df2.loc[idx, 'FirstGenre'] == 'MassivelyMultiplayer':
					#print(idx, 'not exist correct genre')    
					df2.loc[idx, 'FirstGenre'] = None

			# Firstgenre가 Violent 인 경우
			df_temp = df2[(df2['FirstGenre'] == 'Violent')]
			for idx, row in df_temp.iterrows():
				tag = row['tags']
				tag_list = tags_split(tag)
				del tag_list[0]
				for element in tag_list :
						if element in genre_list: #첫번째 발견 요소만 if문 실행
							df2.loc[idx, 'FirstGenre'] = element

				if df2.loc[idx, 'FirstGenre'] == 'Violent':
					#print(idx, 'not exist correct genre')    
					df2.loc[idx, 'FirstGenre'] = None

			# Firstgenre가 EarlyAccess 인 경우
			df_temp = df2[(df2['FirstGenre'] == 'EarlyAccess')]
			for idx, row in df_temp.iterrows():
				tag = row['tags']
				tag_list = tags_split(tag)
				del tag_list[0]
				for element in tag_list :
						if element in genre_list: #첫번째 발견 요소만 if문 실행
							df2.loc[idx, 'FirstGenre'] = element

				if df2.loc[idx, 'FirstGenre'] == 'EarlyAccess':
					#print(idx, 'not exist correct genre')    
					df2.loc[idx, 'FirstGenre'] = None

			# Firstgenre가 SexualContent 인 경우
			df_temp = df2[(df2['FirstGenre'] == 'SexualContent')]
			for idx, row in df_temp.iterrows():
				tag = row['tags']
				tag_list = tags_split(tag)
				del tag_list[0]
				for element in tag_list :
						if element in genre_list: #첫번째 발견 요소만 if문 실행
							df2.loc[idx, 'FirstGenre'] = element

				if df2.loc[idx, 'FirstGenre'] == 'SexualContent':
					#print(idx, 'not exist correct genre')    
					df2.loc[idx, 'FirstGenre'] = None

			# Firstgenre가 Nudity 인 경우
			df_temp = df2[(df2['FirstGenre'] == 'Nudity')]
			for idx, row in df_temp.iterrows():
				tag = row['tags']
				tag_list = tags_split(tag)
				del tag_list[0]
				for element in tag_list :
						if element in genre_list: #첫번째 발견 요소만 if문 실행
							df2.loc[idx, 'FirstGenre'] = element

				if df2.loc[idx, 'FirstGenre'] == 'Nudity':
					#print(idx, 'not exist correct genre')    
					df2.loc[idx, 'FirstGenre'] = None

			# Firstgenre가 Gore 인 경우
			df_temp = df2[(df2['FirstGenre'] == 'Gore')]
			for idx, row in df_temp.iterrows():
				tag = row['tags']
				tag_list = tags_split(tag)
				del tag_list[0]
				for element in tag_list :
						if element in genre_list: #첫번째 발견 요소만 if문 실행
							df2.loc[idx, 'FirstGenre'] = element

				if df2.loc[idx, 'FirstGenre'] == 'Gore':
					#print(idx, 'not exist correct genre')    
					df2.loc[idx, 'FirstGenre'] = None
			```
			
			```python
			df2 = df2[(df2['FirstGenre'] == 'Action') | (df2['FirstGenre'] == 'Adventure') | (df2['FirstGenre'] == 'Casual') | (df2['FirstGenre'] == 'Simulation') |  (df2['FirstGenre'] == 'Strategy') | (df2['FirstGenre'] == 'RPG') | (df2['FirstGenre'] == 'Racing') | (df2['FirstGenre'] == 'Sports')]
			```


			</div>
			</details> 

	<br>

	- `Indie` 특성
		- genre의 Text를 split한 것 중, Indie 장르가 포함되어 있으면 인디게임이라 분류하였음
			<details>
			<summary>💻 <code>Indie</code> 특성 생성 </summary>
			<div markdown="1">
			
			```python
			df2['Indie'] = df2['genre'].map(lambda x: 1 if 'Indie' in genre_split(x) else 0)

			```    
			</div>
			</details>  

<br>

- `Tags`에서 파생 특성 생성
  - `Multiplayer`, `Co-op`, `OpenWorld`, `Horror`, `Violent`, `Sexual` 특성 생성
    - `Tags`는 게임 내 콘텐츠 요소나 게임의 배경을 나타내는 특성임
    - 따라서 이 특성에서 게임 내 콘텐츠 요소 특성을 생성하여, 콘텐츠에 따라 리뷰 평가가 달리지는지 살펴보고자 함
  
		<details>
		<summary>💻 <code>Tags</code>의 파생 특성 생성 </summary>
		<div markdown="1">
		
		```python
		def tags_split(string):
			split_list = str(string).replace('{', '').replace(':','').replace(',', '').split("'")
			return split_list
		```    

		```python
		# 해당 게임이 멀티플레이를 지원하는지?
		df2['Multiplayer'] = df2['tags'].map(lambda x:1 if 'Multiplayer' in tags_split(x) else 0)
		# 해당 게임이 코옵 플레이 (싱글플레이 미션을 함께 플레이)를 지원하는지?
		df2['Co-op'] = df2['tags'].map(lambda x:1 if 'Co-op' in tags_split(x) or 'Co-Op' in tags_split(x) else 0)
		# 해당 게임이 오픈월드 게임인지?
		df2['OpenWorld'] = df2['tags'].map(lambda x:1 if 'Open World' in tags_split(x) else 0)
		# 해당 게임이 호러 게임인지?
		df2['Horror'] = df2['tags'].map(lambda x:1 if 'Horror' in tags_split(x) or 'Survival Horror' in tags_split(x) or 'Psychological Horror' in tags_split(x) else 0)
		# 해당 게임이 잔인/폭력성이 있는지?
		df2['Violent'] = df2['tags'].map(lambda x:1 if 'Gore' in tags_split(x) or 'Blood' in tags_split(x) or 'Violent' in tags_split(x) else 0)
		# 해당 게임이 성적인 요소가 있는지?
		df2['Sexual'] = df2['tags'].map(lambda x:1 if 'Sexual Content' in tags_split(x) else 0) #Nudity도 고려할 수 있지만, 단순히 알몸만 나오면 tag됨(다른 장르일 가능성 있음)
		```
		</div>
		</details>  

<br>

- 지원 언어 파생 특성 생성
  - 지원하는 총 언어 수
    - 다양한 국가의 게이머가 게임을 즐기게 하기 위해서, 그 국가의 언어를 지원하는 것이 유저 리뷰 평가에 영향을 줄 수 있음. 따라서 관련 특성을 생성함
		<details>
		<summary>💻 <code>Num_Language</code> 특성 생성 </summary>
		<div markdown="1">
		
		```python
		# 해당 게임의 지원 언어 수
		df2['Num_Language'] = df2['language'].map(lambda x: len(x.replace(' ','').split(',')))

		```    
		</div>
		</details>  

	<br>

  - 한국어 지원 여부
    - 최근 한국어 지원을 하는 게임이 늘어나고 있으므로, 이런 점 또한 유저 리뷰 평가에 영향을 줄 수 있는지 살펴보기 위하여 특성을 생성함
		<details>
		<summary>💻 <code>Korean</code> 특성 생성 </summary>
		<div markdown="1">
		
		```python
		# 해당 게임이 한국어를 지원하는지?
		df2['Korean'] = df2['language'].map(lambda x: 1 if 'Korean' in x.replace(' ','').split(',') else 0)

		```    
		</div>
		</details>  


<br>


- 그룹 특성 생성
	- 출시 가격에 대한 그룹화
    	- 기존 센트 단위로 되어있는 가격을 달러 단위로 변환
    	- 무료게임을 제외하고, `pd.qcut`을 이용하여 데이터수가 동일하게 4개의 그룹으로 나누었음

			<details>
			<summary>💻 <code>Initial_price</code> 그룹 특성 생성 </summary>
			<div markdown="1">

			```python
			# Cent 단위로 되어있는 게임 가격을 달러 단위로 변환
			df2['initial_price'] = df2['initial_price']*0.01
			df2['current_price'] = df2['current_price']*0.01
			```

			```python
			pd.qcut(df2[df2.initial_price > 0]['initial_price'], 4).value_counts()

			(0.899, 2.99]      8296
			(5.99, 11.99]      7742
			(11.99, 199.99]    7138
			(2.99, 5.99]       6819
			Name: initial_price, dtype: int64
			```

			```python
			# 출시 가격에 대한 그룹화
			df2['price_group'] = 'Free' # 무료게임
			df2.loc[df2[(df2['initial_price'] > 0.899)&(df2['initial_price'] <= 2.99)].index, 'price_group'] = '0.899 .. 2.99'
			df2.loc[df2[(df2['initial_price'] > 2.99)&(df2['initial_price'] <= 5.99)].index, 'price_group'] = '2.99 .. 5.99'
			df2.loc[df2[(df2['initial_price'] > 5.99)&(df2['initial_price'] <= 11.99)].index, 'price_group'] = '5.99 .. 11.99'
			df2.loc[df2[(df2['initial_price'] > 11.99)&(df2['initial_price'] <= 199.99)].index, 'price_group'] = '11.99 .. 199.99'
			```
			</div>
			</details>  

	<br>

	- 게임 소유자 수에 대한 그룹화
		- 기존에 세분화되어 그룹화 되어있던 특성을 총 4개의 그룹으로 축소
		- 게임 소유자 수를 게임 판매량과 동일하다 해석할 순 없지만, 인기게임에 대한 지표가 될 수 있다 생각됨
		- 시각화에만 특성을 사용하였고, 모델링에는 사용되지않았음
		- 예측 API 사용자 입장에서는 게임 소유자 수를 미리 알 수없기 때문에, 모델링 특성에서 제외하였음
  
			<details>
			<summary>💻 <code>Owner</code> 그룹 특성 생성 </summary>
			<div markdown="1">

			```python
			# 10만, 100만, 1000만.. 단위로 변경
			# 100,000,000 .. 200,000,000 는 데이터가 하나이므로, 마지막 그룹에 포함시킴
			df2.loc[df2[(df2['owners'] == '0 .. 20,000') | (df2['owners'] == '20,000 .. 50,000') | (df2['owners'] == '50,000 .. 100,000')].index, 'owners']= '0-100,000'

			df2.loc[df2[(df2.owners == '100,000 .. 200,000') | (df2.owners == '200,000 .. 500,000') | (df2.owners == '500,000 .. 1,000,000')].index, 'owners'] = '100,000-1,000,000'

			df2.loc[df2[(df2.owners == '1,000,000 .. 2,000,000') | (df2.owners == '2,000,000 .. 5,000,000') | (df2.owners == '5,000,000 .. 10,000,000')].index, 'owners'] = '1,000,000-10,000,000'

			df2.loc[df2[(df2.owners == '10,000,000 .. 20,000,000') | (df2.owners == '20,000,000 .. 50,000,000') | (df2.owners == '50,000,000 .. 100,000,000') | (df2.owners == '100,000,000 .. 200,000,000')].index, 'owners'] = '10,000,000-100,000,000'
			
			```
			</div>
			</details>  

	<br>


	- 유저 리뷰 점수에 대한 그룹화
		- 리뷰 점수를 이용하여, Steam에서 활용되는 평가 문구로 그룹화를 진행하였음([참고링크](https://minimap.net/magazine/steam-overwhelmingly-positive))
    		- 80 - 100% : 매우 긍정적 (Very Positive)
    		- 70 - 79% : 대체로 긍정적 (Mostly Positive)
    		- 40 - 69% : 복합적 (Mixed)
    		- 20 - 39% : 대체로 부정적 (Mostly Negative)
    		- 0 - 19% : 매우 부정적 (Very Negative)	
  
			<details>
			<summary>💻 <code>User Score</code> 그룹 특성 생성 </summary>
			<div markdown="1">

			```python
			# User Score group 
			df2.steam_userscore = df2.steam_userscore.str.replace('%', '').astype(int)
			df2['steam_userscore_group'] = 0
			df2.loc[df2[df2['steam_userscore'] < 20].index, 'steam_userscore_group'] = 'Very Negative'
			
			df2.loc[df2[(df2['steam_userscore'] >= 20)&(df2['steam_userscore'] < 40)].index, 'steam_userscore_group'] = 'Mostly Negative'
			
			df2.loc[df2[(df2['steam_userscore'] >= 40)&(df2['steam_userscore'] < 70)].index, 'steam_userscore_group'] = 'Mixed'
			
			df2.loc[df2[(df2['steam_userscore'] >= 70)&(df2['steam_userscore'] < 80)].index, 'steam_userscore_group'] = 'Mostly Positive'
			
			df2.loc[df2[df2['steam_userscore'] >= 80].index, 'steam_userscore_group'] = 'Very Positive'
			
			```
			</div>
			</details>  


<br>

#### 1.1.3 DB 저장
- DB 저장 전, 중간 저장 형태로 먼저 `steamspy_dataset.csv` 형태로 저장함
- 이후 `steamspy_dataset` Table 생성 후, 데이터 저장하였음
- DB 스키마
  
	<img src="https://user-images.githubusercontent.com/77204538/179670396-2e854047-c7bf-465c-b7fd-ff141dbf9155.png" height=400>

<br>

---

### 1.2 최종 데이터셋 구성

- **Target**
	- `steam_userscore_group` 
		- Steam 리뷰 기준으로 그룹화
    		- 매우 부정적(Very Negative)
    		- 대체로 부정적(Mostly Negative)
    		- 복합적(Mixed)
    		- 대체로 긍정적(Mostly Positive)
    		- 매우 긍정적(Very Positive)

- **Features**
	- `Genre`
		- 게임의 장르 (Action, Adventure, Casual, Simulation, Strategy, RPG, Racing, Sports)
	- `Indie`
		- 해당 게임의 인디 게임 여부  
	- `Multiplayer`
		- 해당 게임이 멀티 플레이를 지원하는 지 여부
	- `Co-op`
		- 해당 게임이 코옵 플레이를 지원하는 지 여부
	- `OpenWorld`
		- 해당 게임이 오픈월드 게임인지 여부
	- `Horror`
		- 해당 게임이 공포 게임인지 여부	 
	- `Violent`
		- 게임 내 잔인/폭력적 요소가 포함되어 있는지 여부
	- `Sexual`
		- 게임 내 성적인 요소가 포함되어 있는지 여부
	- `Korean`
		- 게임의 한국어 지원 여부
	- `discount`
		- 게임 출시 이후 게임 가격 할인 여부
	- `Num_Language`
		- 게임의 지원 언어 수
	- `price_group`
		- 게임 출시가격을 그룹화 (만원 이하, 만원-2만원, 2만원-3만원, 3만원-4만원, 4만원-5만원, 5만원-6만원, 6만원 이상)

<br>

## 2. EDA
### 2.1 Steam 유저 평가 vs 게임 장르

<img src="https://user-images.githubusercontent.com/77204538/179781137-f47ad2f3-aabc-4e5d-ba67-bae14326f2dc.png" width=500>

- 유저 평가와 상관없이, **Action, Adventure 장르** 게임들의 수가 많다
- “복합적” 평가를 받은 게임들의 경우, 다른 리뷰 평가 보다 **Casual 장르**의 게임이 많다


<br>

### 2.2 Steam 유저 평가 vs 게임 출시 연도
<img src="https://user-images.githubusercontent.com/77204538/179781144-8d2b6695-fa6c-4698-9743-bddb787182e5.png" width=500>

- "대체로 긍정적", "매우 긍정적"평가를 받은 게임들은 대체로 **2017~2018년도** 출시된 게임들이다
- "매우 부정적" 평가를 받은 게임들은 **2015년도**쯤 출시된 게임들이 많다


<br>

### 2.3 Steam 유저 평가 vs 게임 소유자 수
<img src="https://user-images.githubusercontent.com/77204538/179781146-ccb256f9-8633-4077-b0bd-de42fd05c9ad.png" width=500>

- "대체로 부정적", "복합적" 평가를 받은 게임들은 **1000만~1억 소유자** 게임의 수가 압도적으로 많다
- "매우 긍정적" 평가를 받은 게임들의 경우, 다른 평가 수준보다 **10만~100만 소유자, 100만~1000만 소유자** 게임의 수가 많다


<br>


### 2.4 Steam 유저 평가 vs 게임 가격대
<img src="https://user-images.githubusercontent.com/77204538/179781149-5d1be05d-b1f0-4605-98ad-e0eafd799280.png" width=800>

- "매우 긍정적" 평가를 받은 게임의 **출시 가격**은 다른 평가 정도보다 **높다**
- "복합적" 평가를 받은 게임들은 **할인을 진행한 게임이 제일 많다**
- "대체로 긍정적", "매우 긍정적" 평가를 받은 게임들은 **할인을 진행한 게임의 수**가 할인 하지 않은 경우보다 **더 많다**.



<br>

### 2.5 Steam 유저 평가 vs 인디 게임 여부
<img src="https://user-images.githubusercontent.com/77204538/179781154-30201685-c532-4c40-8433-fb935adeb63c.png" width=500>

- 리뷰 평가에 상관없이, **전체적으로 인디 게임의 수가 많다**
- 인디 게임들 중, **"복합적"평가**를 받은 게임이 제일 많다.

<br>

## 3. Modeling
> 2022.07.22에 Regression 모델에서 Classifier로 변경되었음
### 3.1 Base 모델 선택
- Logistic Regression, Decision Tree, Random Forests, Extra Trees, Support Vector Machine, Naive Bayes,
KNN, Gradient Boostiong, AdaBoosting, XGBoost, LightGBM, 총 11개의 모델의 성능을 비교하였음

	<img src="https://user-images.githubusercontent.com/77204538/179787850-d4a402ad-a031-4718-97f6-6b24ded072d5.png">

  - True Positive와 False Negative를 동시에 고려하며, Multiclass와 Class간의 불균형을 고려할 수 있는 `roc_auc_ovr_weighted socre` 를 평가지표로 선택함   
  (OvR : One versus the rest)
  - `StratifiedKFold`를 사용하여 모든 class의 데이터를 훈련할 수 있도록 하였음
  - Gradient Boost(AUC score=0.673), XGBoost(AUC score=0.672), LightGBM(AUC score=0.674) 모델이 가장 성능이 좋았음
  - Gradient Boosting, XGBoost, LightGBM 모델을 합친  **Voting Classifier**를 생성 후, Hyperparameter tuning을 진행함
  - Voting Classifier의 용량이 클 수 있다는 점을 고려해, 저용량이면서 좋은 성능을 낼 수 있는 LightGBM의 Hyperparameter tuning 또한 진행함
  - 이후, tuning된 Voting Classifier와 LightGBM의 성능을 비교함

<br>

### 3.2 Hyperparameter tuning
- **GridSearchCV**로 최적화를 진행함
- Tuning 시에는 `StratifiedKFold`를 이용하여 훈련 데이터셋에 모든 class가 균등하게 포함될 수 있도록 교차검증하였음
- 평가지표는 `roc_auc_ovr_weighted socre`를 이용함

	| 평가지표 		 | Tuning 후 (Voting Classifier) | Tuning 후 (LightGBM)	|
	|:--------:		|:---------:|:---------:|
	|    Precision  |   0.48   	|   0.48   	|
	|    Recall   	|   0.55   	|   0.35   	|
	|   F1 score 	|   0.55  	|   0.38  	|
	|    AUC score  |   **0.675**  	|   0.657  	|
	- *모든 score는 각 class간의 data 수를 고려한 weighted 값임*

	- Tuning 후 **Voting Classifier**의 AUC score가 높아 최종 모델로 선정하였음

<br>

### 3.3 Permutation Importance

<img src="https://user-images.githubusercontent.com/77204538/179789938-444224d3-119f-4ef5-82c6-5d8947f04ad5.png" height=300>


- **게임의 가격대(price_group)와 할인여부(discount), 지원 언어의 수(Num_Language)** 가 예측 모델에 가장 큰 영향을 주는 것으로 나타남
- EDA 상에서 인디 게임의 수가 전체적으로 많았음에도, 인디게임 여부가 예측모델에 그리 큰 영향을 주지 않음

<br>

## 4. 웹서버 구축 및 배포
> ✅ [웹 API 링크](https://game-review-prediction.herokuapp.com/)

- Home 화면
  - 네이게이션바와 버튼을 클릭하면 해당 링크로 이동
  - API : 예측 API를 이동할 수 있는 변수입력 페이지로 이동
  - Dashboard : speamspy에서 수집한 데이터를 기반으로 한 대시보드 페이지로 이동
  - Steamspy : 데이터를 수집한 steamspy 홈페이지로 이동

	<img src="https://user-images.githubusercontent.com/77204538/180365688-c1342048-c9d8-4d51-8a3b-4aeebc30f187.png">

<br>

- 변수 입력
  - 네비게이션바의 **API**, **예측하기 버튼**을 클릭하면 이동
	<img src="https://user-images.githubusercontent.com/77204538/180365689-846a9842-1052-4d42-bf17-1c55c0328b76.png" height=500>
	
<br>

- 예측 결과 출력
  - 변수입력 페이지에서 **predict! 버튼**을 클릭하면 이동
	<img src="https://user-images.githubusercontent.com/77204538/180365691-b8e6c01b-2ef1-4de2-9a0b-b512379ca880.png" height=400>

<br>

- DashBoard
  - 네비게이션바의 **Dashboard**, **이동하기 버튼**을 클릭하면 이동

	<img src="https://user-images.githubusercontent.com/77204538/180366216-f4f96d5f-4c07-4df4-9108-4e70e2cc0739.png">

	<img src="https://user-images.githubusercontent.com/77204538/180365681-e4b0e953-01a5-4038-9f67-6b8d50baff10.png">

	<img src="https://user-images.githubusercontent.com/77204538/180365685-a1602381-8e81-4f46-ad9d-c137773dabc5.png">

<br>

## 5. 결론
 
> **게임의 가격대**와 **출시 후 할인**여부, **지원 언어의 수**는 유저 리뷰 평가에 영향을 준다.

<br>


## 6. 한계점 및 개선방안
### 한계점
- API들을 비교하여 각 API를 이용해 얻을 수 있는 데이터들을 명확하게 파악한 이후에 데이터를 수집해야 했지만, 그러지 못하였음
  - Steamspy API를 이용하여 획득한 정보들은 SteamDB를 이용해도 얻을 수 있는 정보들이 포함되어 있었음
  - 또한 SteamDB를 이용해 데이터를 획득하였다면, 결측치를 최소한으로 할 수 있었음
    - Steamspy API를 통해 얻은 `appid`로 SteamDB에서 직접 확인해보았을 때, **게임 리뷰, 가격, 출시일**은 SteamDB에서도 얻을 수 있는 데이터였음
    - 또한, SteamDB 상에는 나와있지만, steamspy에서는 출시일, 게임가격이 나오지 않는 경우를 확인하였음   
  	➡ 처음부터 SteamDB에서 데이터를 수집했다면, 결측치를 최소한으로 하여 많은 데이터를 수집할 수 있었을 것이라 생각됨
  - Steamspy에서 얻은 데이터 중, `Genre`에 대한 전처리 과정에서 **어떤 장르를 이 게임을 대표하는 장르로 볼 수 있을까?** 를 고민하며 처리하였는데, SteamDB에서 `Primary ganre`라는 그 게임의 대표 장르를 나타내는 데이터가 있었음
    - 전처리 과정 중, `Genre`의 첫번째, 또는 2~3번째 요소를 대표 장르로 설정하였는데, 전처리 결과와 SteamDB의 `Primary ganre`와 다른 경우가 일부 발견되었음  
	ex) 전처리 결과: Action,  Primary genre: RPG..
    - SteamDB를 통해 데이터를 수집하였다면, 전처리 과정에서 소요되는 시간을 최소화 할 수 있고, 전처리 과정에서 추출된 대표 장르보다 더 정확한 결과를 나타낼 수 있었을 것으로 생각됨


<br>

- 예측 모델의 성능이 정확하지 않음
	- ~~예측 모델에 사용한 Feature 수가 적어서 정확도가 낮은 것으로 예상됨~~ ➡ 데이터를 추가로 수집하여 특성을 5개에서 12개로 늘림
	- 게임 개발사와 배급사도 모델에 활용할 수 있었으나, 아직 게임을 기획중인 개발자가 이용할 것이라 가정하여 해당 특성을 모델링에서 제외함
	- 회귀모델에서 Multiclass classifier로 문제를 변경하였으나, AUC socre가 0.67로 정확도가 높다고 보기 어려움
		- AUC score가 0.7이상은 성능이 준수하다 판단될 수 있음 ([참고링크](http://gim.unmc.edu/dxtests/roc3.htm))
		- **Class간의 데이터 불균형**, **추가된 데이터가 1만여개** 밖에 안된다는 점에 의하여 나타난 결과라 생각됨
		
			<details>
			<summary> 기존 회귀모델과 Clasifier의 성능 </summary>
			<div markdown="1">

			```
			- 기존 회귀모델
				- MAE: 0.153
				- MSE: 0.036
				- RMSE: 0.1900
				- R2 score: 0.061

			- Multiclass classifier
				- Precision: 0.48
				- Recall: 0.35
				- F1 score: 0.38
				- AUC score: 0.657
			```
			</div>
			</details>  		
		
	

<br>

- 수집한 데이터 수가 5만 여개였으나, 중복 데이터와 수집과정 중 오류로 인해 데이터 전처리 과정에 의하여 3면여개로 줄어들음
	-  많은 데이터를 수집하려 하였으나, API 이용 중 Error로 인해 도중에 멈추거나 데이터가 삭제되어서 예상보다 적은 데이터만 사용됨
	-  또한, 알 수없는 이유로 동일한 appid를 가진 데이터들이 반복적으로 수집된 경우가 있어 데이터 전치리과정에서 데이터 수가 많이 줄어들음
      	-  데이터를 수집할 당시 이틀에 걸쳐 수집이 되었었는데, steamspy가 하루마다 데이터를 update하기 때문에 그 사이에 변경된 appid로 인한 버그로 추정됨.

### 개선방안
- Multiclass개수를 5개에서 3개로 축소시킬 것
  - 수집한 데이터를 기준으로, Very Negative(61), Mostly Negative(1992), Mixed(18068), Mostly Positive(9122), Very Positive(9122)로 구성됨
  - Nagative 평가를 받은 데이터는 소수로, 대부분 Mixed 이상의 평가를 받음
  - **Negative(Very Negative + Mostly Negative), Mixed, Posivite(Mostly Positive + Very Postive)** 로 변경,  
    또는 **Mixed, Mostly Positive, Very Positive만 반영**한다면 성능개선이 이루어질 것으로 예상됨
	
<br>

- SteamDB를 이용한 데이터 수집
  - steamspy API로만 수집할 수 있는 데이터는 `게임 소유자 수` 
    - 게임 판매량과 동일하진 않지만, 비슷한 지표로 활용될 수 있으므로 데이터 시각화에만 이용할 것
  - 그 외 데이터 (게임가격, 장르, 할인율, 출시일 등..)들은 SteamDB를 활용해서도 수집할 수 있음
  - Steamspy API를 이용해 `appid`, `게임 소유자 수` 데이터만 얻은 후, 그 외 데이터는 SteamDB를 활용한다면 기존보다 게임에 대한 정확한 정보를 얻을 수 있을 것이라 생각됨
    - SteamDB에서 데이터를 얻기위해선 `appid`, `게임 이름` 정보가 필요하므로 미리 steamspy에서 얻을 필요가 있음

<br>

## 후기

- 전체적인  과정  중에  데이터  수집  단계에서  어려움이  많았습니다.
	- API나 웹 스크레이핑으로  데이터를  가져올 때 많은  에러를  겪었는데, 조건문으로  처음부터  필요한  데이터만  가져오려고  했기  때문인 듯합니다.
	- 데이터를  가져올  때는  처음부터  내가  필요한  정보만  수집하기  보다는, 일단  포괄적으로  가져와서  정제하는  것이 더 낫다고 느꼈습니다.(NoSQL을  활용하자)

<br>

- 처음 데이터를 수집하여 데이터 분석에 활용하다 보니, 어떤 API를 활용해야하는지에 대한 정보 수집이 부족하여 아쉽습니다.
  - 처음 프로젝트 기획당시에, 관련 API들이 어떤 것이 있는지 알아보고 정리한 뒤에 진행을 해야했는데, 프로젝트 기한을 지키기 위해 이러한 점을 많이 고려하지 못한 것 같습니다.
  - 기획 시에 데이터 수집 방법에 대해 최대한 많은 정보를 수집하고 진행하였다면, 전처리에 쏟았던 시간을 줄일 수 있었을거라 생각되어 아쉽습니다.

<br>

- 데이터를 수집하고 보니, 생각보다 모델에 사용할 특성이 많지 않았습니다.
	- Steam 내 게임들은 모두 PC 게임이고, 개발사와 배급사도 제외해야 했기때문에 생각보다 쓸 수있는 데이터가 많이 없었습니다.
	- 메타 크리틱 점수도 활용하려 하였으나, 점수가 없었던 게임이 많기도 했고 API를 이용할 유저가 메타 크리틱 점수를 미리 알수는 없기 때문에 제외해야 했습니다.
	- PC 게임의 경우는, 컴퓨터 사양도 주요 고려 사항 이므로 이를 추가할 수도 있을 것 같습니다. 

<br>

## 변경사항 (update : 2022.07.22)
- Steamspy를 이용해 1만여개의 Data 추가 수집 
- 모델을 XGBoost Regression에서 Voting Classifier로 변경함
- 모델의 특성을 5개에서 12개로 늘림
- 데이터 변경에 따른 DashBoard 업데이트 및 보고서 추가

<br>

*프로젝트의 자세한 사항은 다음 [PPT 자료](https://drive.google.com/file/d/1jsaGvADYfkfeU2SAVHtsgszMx_miEoQG/view?usp=sharing)를 확인해주세요*

