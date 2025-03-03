import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
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
    return render_template(
        'index.html',
        url=''    
    )   


@app.route('/urls')
def urls_get():
    urls = repo.get_content()
    return render_template(
        'urls.html',
        urls=urls
    )


@app.post('/urls')
def urls_post():
    data = request.form.to_dict()
    new_url = to_short_url(data['url'])
    errors = is_valid(new_url)
    if errors:
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            url=data['url']  
        )
    else:
        curr_url = repo.get_by_url(new_url)
        if curr_url:
            flash('Страница уже существует', 'info')
            return redirect(url_for('urls_show', id=curr_url['id']))
        else:
            data['url'] = new_url
            repo.save(data)
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('urls_show', id=data['id']))


@app.route('/urls/<id>')
def urls_show(id):
    url = repo.find(id)
    url_checks = repo.get_all_checks(id) 
    if url is None:
        render_template('not_found.html')
    return render_template(
        'url_show.html',
        url=url,
        url_checks=url_checks
    )


@app.post('/urls/<id>/checks')
def urls_checks(id):
    url = repo.find(id)
    try:
        responce = requests.get(url['name'])
        responce.raise_for_status()
        result = {
            'status_code': responce.status_code
        }
    except (requests.ConnectionError, requests.Timeout,
        requests.TooManyRedirects, requests.HTTPError):
        result = {'status_code': False}
        print('request error')
    
    if result.get('status_code'):
        url.update(result)
        repo.save_check(url)
        flash('Страница успешно проверена', 'success')

    else:
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('url_show', id=id))
