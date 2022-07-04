# 게임 긍정 평가 예측 API

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
		- `1_3_1_DataCleaning.ipynb`
			-  `1_1_2_steamspy_details.csv` 와 `1_2_2_steamspy_other_details.csv` 를 merge하고 전처리한 후, `1_3_2_steamspy_dataset.csv` 로 저장
		- `1_3_2_steamspy_dataset.csv`
			- `1_1_2_steamspy_details.csv` 와 `1_2_2_steamspy_other_details.csv` 를 merge한 Dataset
		- `1_3_3_DB_load.py`
			- `1_3_2_steamspy_dataset.csv`를 DB에 저장
		- `1_3_4_steamspy.db`
			- 저장된 DB data
			
- `2_Model_training.ipynb`
	- 저장된 DB를 DataFrame으로 변환하여 모델링 진행
- `3_Heroku`
	- 웹배포 진행한 폴더
	- `templates`
		- 웹페이지 Template 저장
	- `__init__.py`
		- 웹 배포 실행
	- `model.pkl`
		- 최적화된 XGBoost 모델 파일
	- `requirements.txt`
		- 웹 배포시 개발 환경 작성
<br>

## Pipeline
<img src="https://user-images.githubusercontent.com/77204538/175936788-3c36307a-aceb-411f-b86a-8904d48681a6.png">

<br>

## 1. Dataset
- Steamspy(https://steamspy.com/)

	<img src="https://user-images.githubusercontent.com/77204538/175939213-02e3b1b9-618b-48f6-8d8f-802f215e097d.png" height=400>
	
	- Steam 사용자들의  게임  구매  이력을  이용해 게임  판매량  순위를  시각화
	- Steam 에 작성되어  있는  게임에  대한  정보, 플레이어  리뷰, 평가  점수를 제공함
	
- Steamspy API에서 제공하는 기능을 이용하여, 게임 데이터를 수집함
- Steamspy API에서 수집할 수 없는 **게임 출시일, 게임 가격, 스팀 유저 긍정 평가 비율, 메타 크리틱 점수**는 steamspy 홈페이지를 웹 스크레이핑하여 수집함
- 수집한 데이터를 CSV file로 임시 저장한 후, PostgreSQL기반의 ElephantSQL 서버에 저장함
	<img src="https://user-images.githubusercontent.com/77204538/175940731-83050f76-bdd4-4007-8402-1f8cd0eb10e2.png" height=200>

<br>

### 데이터 구성

- **Target**
	- `positive_ratio` 
		- 스팀 내 긍정 평가 비율
- **Features**
	- `genre`
		- 게임의 장르 (Action, Adventure, Casual, Simulation, Strategy, RPG, Racing, Sports)
	- `Korean`
		- 게임의 한국어 지원 여부
	- `indie`
		- 해당 게임의 인디 게임 여부
	- `discount`
		- 게임 출시 이후 게임 가격 할인 여부
	- `price_group`
		- 게임 출시가격을 그룹화 (만원 이하, 만원-2만원, 2만원-3만원, 3만원-4만원, 4만원-5만원, 5만원-6만원, 6만원 이상)

<br>

## 2. 데이터 전처리
- `genre` 와 `price_group` 을 object type에서 int type으로 변환
- HoldOut 방법으로 Train set과 Validation set을 분리함
- `StandardScaler`로 데이터들을 표준화함

<br>

## 3. Modeling
### 3.1 Base 모델 선택
- Linear Regression, Decision Tree, Random Forests, XGBoost 회귀 모델 중 선택함
- 특성의 개수가 많지 않아 예측 정확도가 낮을 수 있으므로, 잔차를 예민하게 감지하는 **RMSE**를 평가지표로 선택함
- 가장 성능이 좋은 Random Forests 모델을 선택함
	| 평가지표 	| Linear Regression 	| Decision Tree 	| **Random Forests** 	| XGBoost 	|
	|:--------:	|:-----------------:	|:-------------:	|:------------------:	|:-------:	|
	|    MAE   	|       0.156       	|     0.153     	|        0.152       	|  0.153  	|
	|    MSE   	|       0.037       	|     0.036     	|        0.036       	|  0.036  	|
	|   RMSE   	|       0.1929      	|     0.1901    	|     **0.1898**     	|  0.1901 	|
	|    R2    	|       0.031       	|     0.059     	|        0.062       	|  0.059  	|

### 3.2 Hyperparameter tuning
- 빠른 시간 내에 여러 파라미터를 검증할 수 있는, **RandomSearchCV**로 최적화

	| 평가지표 	| Tuning 전 	| Tuning 후 	|
	|:--------:	|:---------:	|:---------:	|
	|    MAE   	|   0.152   	|   0.153   	|
	|    MSE   	|   0.036   	|   0.036   	|
	|   RMSE   	|   0.1898  	|   0.1900  	|
	|    R2    	|   0.062   	|   0.061   	|

	- Tuning 후 모델 성능이 미세하게 감소했다


### 3.3 Feature Importance

<img src="https://user-images.githubusercontent.com/77204538/175981411-460d5cb5-0753-4979-93ee-0d42b65ac8e4.png" height=400>

- 게임의 가격이 게임 리뷰에 가장 큰 영향을 준다.
- 한국어 지원 여부와 게임의 장르가 그 다음으로 게임 리뷰에 영향을 준다.
	

## 4. 웹서버 구축 및 배포
- Home 화면

	<img src="https://user-images.githubusercontent.com/77204538/175963564-2f06d0fd-4afe-4571-9a8b-dd4884c0b684.png" height=400>

<br>

- 변수 입력

	<img src="https://user-images.githubusercontent.com/77204538/175963562-14712e5a-4e3b-4d25-8b3c-370fb2d23414.png" height=400>
	
<br>

- 예측 결과 출력

	<img src="https://user-images.githubusercontent.com/77204538/175963549-34b18018-5faa-41d7-9354-1d10cf6c07e3.png" height=400>

<br>

- DashBoard

	<img src="https://user-images.githubusercontent.com/77204538/175963958-49550e12-c01d-4283-b29c-0275d5ed5c67.png" height=400>
	<img src="https://user-images.githubusercontent.com/77204538/175963569-ae1b489c-14d7-455a-bfca-e7a02eb6adec.png" height=400>

<br>

## 5. 결론

> 게임이 나중에 할인하는지, 인디 게임인지 상관없이, 
> **초기 판매 가격과 게임의 장르, 한국어 지원 여부**가 긍정적인 리뷰에 영향을 준다.
<br>

> 웹 API를 이용하여 게임이 어떤 평가를 받을 지 대략적으로 예상할 수 있다.

<br>

## 6. 한계점 및 개선방안
### 한계점
- 예측 모델의 성능이 정확하지 않음
	- 예측 모델에 사용한 Feature 수가 적어서 정확도가 낮은 것으로 예상됨
	- 게임 개발사와 배급사도 모델에 활용할 수 있었으나, 국내 게임 개발자가 이용할 것이라 가정하여 해당 특성을 제외함
	- 이진 분류가 아니라, 회귀로 평가 정도를 정확히 예측하는 것이었기 때문에 정확도를 높이는데 어려웠던 것으로 예상됨 (특성 수에 비해 과제가 어려움)

- 수집한 데이터 수가 2만 여개임
	- 더 많은 데이터를 수집하려 하였으나, API 이용 중 Error로 인해 도중에 멈추거나 데이터가 삭제되어서 예상보다 적은 데이터만 사용됨
	- 이용한 무료 DB의 용량 제한으로 인해, 데이터를 모으는데 한계가 있었음

### 개선방안
- 회귀 모델을 이진 분류 모델로 변경할 것
	- 긍정으로 평가할 지, 부정적으로 평가할지로 과제를 단순화 한다면 지금보다 모델 성능이 향상될 것으로 예상됨
	- 이후, 긍정 평가 확률을 따로 계산하여 웹 상으로 제공한다면, 지금과 유사한 서비스로 제공할 수 있음
	
- 추가 데이터를 수집할 것

<br>

## 후기

- 전체적인  과정  중에  데이터  수집  단계에서  어려움이  많았습니다.
	- API나 웹 스크레이핑으로  데이터를  가져올 때 많은  에러를  겪었는데, 조건문으로  처음부터  필요한  데이터만  가져오려고  했기  때문인 듯합니다.
	- 데이터를  가져올  때는  처음부터  내가  필요한  정보만  수집하기  보다는, 일단  포괄적으로  가져와서  정제하는  것이 더 낫다고 느꼈습니다.(NoSQL을  활용하자)

- 데이터를 수집하고 보니, 생각보다 모델에 사용할 특성이 많지 않았습니다.
	- Steam 내 게임들은 모두 PC 게임이고, 개발사와 배급사도 제외해야 했기때문에 생각보다 쓸 수있는 데이터가 많이 없었습니다.
	- 메타 크리틱 점수도 활용하려 하였으나, 점수가 없었던 게임이 많기도 했고 API를 이용할 유저가 메타 크리틱 점수를 미리 알수는 없기 때문에 제외해야 했습니다.
	- PC 게임의 경우는, 컴퓨터 사양도 주요 고려 사항 이므로 이를 추가할 수도 있을 것 같습니다. 
