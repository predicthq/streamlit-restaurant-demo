# PredictHQ Restaurant Demo App

This is a [Streamlit](https://streamlit.io) app designed to show how easy it is to get up and running quickly with the PredictHQ APIs. Please feel free to take a copy of this code and modify it for your own use, or take the bits you need to make your integration with PredictHQ easier and faster.

Learn more about integrating with the PredictHQ APIs at [https://docs.predicthq.com](https://docs.predicthq.com).


## Running the app

To run the app locally:

```
$ cd streamlit-restaurant-demo
$ python3 -m venv .venv
$ 
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ 
$ streamlit run map.py
```

You'll need to get an API token by following the instructions at [https://docs.predicthq.com/api/authenticating](https://docs.predicthq.com/api/authenticating) and create a [Streamlit secrets](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management) file `.streamlit/secrets.toml` with the following contents:

```
api_key = "<your API token>"
```

