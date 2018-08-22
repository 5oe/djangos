from . import app1


@app1.route('/user')
def user():
    return "User!!!"
