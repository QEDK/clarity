![clarity](https://socialify.git.ci/QEDK/clarity/image?font=KoHo&forks=1&issues=1&language=1&pattern=Charlie%20Brown&pulls=1&stargazers=1&theme=Light)

As said by Blaise Pascal, "Clarity of minds means clarity of passion" and one's passion make their life worth living.
Inspired by this thought and taking into account the state of mental health in today's date, we decided to work on something that we would find amazing to use.
What if you wanted to remember how you felt a week or two ago? What if you want to know what crossed your mind then?

Presenting **clarity**, your AI journaling assistant. ✨

## 🙋 How does it work?
It's simple! Follow these steps:
1. Visit the app and you can pen down something, anything.
2. Follow your emotions, just don't hesitate to dive deep down into it.
3. Write down your emotions truly and that's it!
4. Click on submit and it will be stored as a little secret between us.
5. Want to know about your state of your mind few days back? Don't worry we will show you.
6. What to share it with someone else or your therapist? Just give them your super secret link!

## 🌐 Where can I use it?
Find us on [clarity-frontend.herokuapp.com](https://clarity-frontend.herokuapp.com)!

## 💻 Tech stack
`clarity` has a React Native frontend ⚛️ hosted with Heroku, and a FastAPI backend backed by PostgreSQL hosted on Google Cloud Platform. The UI is based on React, while the Cloud Run backend uses `SQLAlchemy` and `asyncpg` for communicating with Cloud SQL. 💽

## 👨‍💻 How do I contribute?
- To get more detailed documentation, please check out our project's [wiki](https://github.com/QEDK/clarity/wiki). 📖
- Before contributing do go through the [Code of Conduct](https://github.com/QEDK/clarity/blob/master/CODE_OF_CONDUCT.md) 🔧
- If you find any bugs in the application, or a feature you think would be nice to have, please open an [issue](https://github.com/QEDK/clarity/issues/new/choose). 🐞
- Please follow the [style guidelines](https://github.com/QEDK/clarity/wiki/Style-guidelines) when making contributions. We have automatic linting set up using GitHub Actions to check all pull requests for syntax and correct labelling. Instructions on running the linter locally can be found below. 🖌️
- Continue reading the rest of the README to get the build instructions for both the frontend and the backend. ⛏️

## 🛠️ Installation
The project can be setup by following these instructions, note that you must have `npm` and `pip` installed before proceeding further. You should ideally also be working in a virtual environment, such as Python's `venv` or the `virtualenv` module.

### 🧰 Configuration
For the default server to work normally, you must have a PostgreSQL instance running on your `localhost` (`127.0.0.1`) on port `5432`. Alternatively, if you're working on Google Cloud Platform with a Cloud SQL connection, you can set `cloud_run_instance=1` environment variable to use that connection instead and set `db_uri` to the entire connection string. You will also need to use the correct PostgreSQL environment variables for `asyncpg` to pick the settings up. ☁️

When working locally, environment variables can be set like this in a shell script 📁:
```bash
export db_server=<db_server>
export db_name=<db_name>
export db_username=<db_name>
export db_password=<db_username>
```

### 🧱 Building dependencies
```bash
$ git clone git@github.com:QEDK/clarity.git
$ cd clarity/ml
$ pip3 install -r requirements.txt
$ cd ../backend
$ pip3 install -r requirements.txt
$ cd ../frontend
$ npm install
```
That's about it. ✔️

### ⚙️ Running the server
#### 🔙 Backend
```bash
$ cd backend
$ uvicorn main:app --reload
```
Finally, navigate to http://localhost:8080/docs and you should see the Swagger UI API interface to signify that your app is now up and running! ⚡

##### 🐳 Building with Docker
We also provide a `Dockerfile` for easy containerization and deployment of the backend, all you need to do is:
```bash
$ docker build -t 'app:Dockerfile' .
$ docker run app:Dockerfile
```
The server should be accessible on all network interfaces on the port `8080`. ⏫

#### ➡️ Frontend
```bash
$ cd frontend
$ npm start
  Starting the development server....
  The app is running at: http://localhost:3000/
```
And the server should be up and running on http://localhost:3000! 🚀

### ‼️ Just tell me about the ML!
Not to fret, the entirety of `ml` module is documented at the respective [README](https://github.com/QEDK/clarity/blob/master/ml/README.md) (since it's quite large) and some more on the wiki. What you need to know - clone the repo, copy the folder, use it as an API. Et voilà! 

### 🧹 Linting
All Python scripts are linted using [flake8](https://flake8.pycqa.org). To lint your files, simply install and run the `flake8` command in the project root and it should pick up the configuration automatically. GitHub Actions will automatically check your PR against `flake8` once submitted and provide helpful annotations in case of logical or stylistic errors. ℹ️

## 🔜 What's next?
* Integrate our service with direct access to medical professionals. 👨‍⚕️
* Add analysis of more features to give more information on emotions expressed. 🤗
* Provide Spotify recommendations according to emotion analysis. 💬

Where we want to be: 
* An integrated platform for therapists, patients and people willing to track their mental state. 🧑🏿‍🤝‍🧑🏿

## 📜 License
This project is released under a free and open-source software license, Apache License 2.0 or later ([LICENSE](LICENSE) or https://www.apache.org/licenses/LICENSE-2.0). The documentation is also released under a free documentation license, namely the [GFDL v1.3](https://www.gnu.org/licenses/fdl-1.3.en.html) license or later.

### 🖊️ Contributions
Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be licensed as above, without any additional terms or conditions.
