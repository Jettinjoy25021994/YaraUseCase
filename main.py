"""
Created By: Jettin Joy
Created on: 06/12/2021


main module that runs the flask app
"""


from YaraUseCase import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)