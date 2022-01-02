# nearborhood

[![Maintainability](https://api.codeclimate.com/v1/badges/dc7fa47fcd809b99d087/maintainability)](https://codeclimate.com/github/NCKU-CCS/TOC-Project-2020/maintainability)

[![Known Vulnerabilities](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020/badge.svg)](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020)


Template Code for TOC Project 2020

A Line bot based on a finite state machine

## 前言
現在Google Map幾乎成為生活不可或缺的軟體，當我們在未知的還境中，Google Map成為你與陌生地的連結。因此，我們設計了一個聊天機器人，結合Google Map Api，打造一個可以方便使用者找到附近地標的工具。

## 構想
主要是藉由Google Map 的 Nearby Search找到地標。首先，請使用者確認關鍵字與類別。接著，請使用者輸入自己的座標。如此一來就可以找到地標了!並且，我們還結合Google Sheet Api 建立使用者的地標收藏地圖。

## 環境
- ubuntu 18.04
- python 3.6

### 技術
- Google Map Api
	- 提供結合Google Map 功能的Api
- Google Sheet Api
	- 提供python 結合 Google 試算表進行資料庫管理

### 使用教學
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.
#### .env
- Line
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN
- Google Api
    - GOOGLE_PLACES_API_KEY
    - AUTH_JSON_PATH
* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### a. Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

#### b. Servo

Or You can use [servo](http://serveo.net/) to expose local servers to the internet.


## Finite State Machine
![](https://i.imgur.com/lCtEKDT.png)


## 操作說明
### 介紹
![](https://i.imgur.com/aFjVDrq.jpg =500x)
### 選單:選擇類型or關鍵字
![](https://i.imgur.com/Bfb99j3.jpg =500x)
### 傳送位置
![](https://i.imgur.com/WHVOmd6.jpg =500x)
### 輸出結果
![](https://i.imgur.com/a2g0T8I.jpg =500x)
### 點擊連結google map or 點擊收藏進行收藏
![](https://i.imgur.com/3Ot2X2Y.jpg =500x)
### 查看收藏，並刪除收藏

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz
