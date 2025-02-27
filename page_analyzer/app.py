import os

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.url_repository import UrlRepository
from page_analyzer.validator import is_valid, to_short_url

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_url = os.getenv('DATABASE_URL')
app.config['DATABASE_URL'] = db_url
repo = UrlRepository(db_url)


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages
    )


@app.route('/urls')
def urls_get():
    urls = repo.get_content()
    return render_template(
        'urls.html',
        urls=urls,
    )


@app.post('/')
def urls_post():
    data = request.form.to_dict()
    new_url = to_short_url(data['url'])
    data['url'] = new_url
    errors = is_valid(new_url)
    if errors:
        flash('Некорректный URL', 'danger')
        return render_template('index.html')
    else:
        curr_url = repo.get_by_url(new_url)
        if curr_url:
            flash('Страница уже существует', 'info')
            return redirect(url_for('urls_show', id=curr_url['id']))
        else:
            repo.save(data)
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('urls_show', id=data['id']))


@app.route('/urls/<id>')
def urls_show(id):
    messages = get_flashed_messages(with_categories=True)
    url = repo.find(id)  
    if url is None:
        render_template('not_found.html')
    return render_template(
        'url_show.html',
        messages=messages,
        url=url
    )


