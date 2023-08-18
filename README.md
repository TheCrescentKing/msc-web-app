# Msc: Analysing Nasa's EMIT instrument data
### John A. McMenemy

## How to run this project

1. Fork/Clone

1. Install required dependencies

1. Run the server-side Flask app in one terminal window:

    ```sh
    $ cd server
    $ conda env create -f environment.yml
    (flask_emit)$ flask run --port=5001 --debug
    ```

    Navigate to [http://localhost:5001](http://localhost:5001)

1. Run the client-side Vue app in a different terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run dev
    ```

    Navigate to [http://localhost:5173](http://localhost:5173)
