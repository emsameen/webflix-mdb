# Webflix MDB

A mini Netflix-like web app built with Flask and MongoDB using the sample_mflix dataset.

## Features

- List and search movies
- View movie details
- Sky-blue modern layout with icons

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Add a `.env` file with your MongoDB URI:

```env
MONGO_URI=mongodb+srv://yourUser:yourPassword@cluster0.mongodb.net/sample_mflix?retryWrites=true&w=majority
```

3. Run the app:

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000)