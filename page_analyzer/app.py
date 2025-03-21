import os

import psycopg2
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

from page_analyzer.parser import get_seo_content
from page_analyzer.url import to_short_url, validate
from page_analyzer.url_repository import UrlRepository

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
conn = psycopg2.connect(app.config['DATABASE_URL'])
repo = UrlRepository(conn)


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
    error = validate(new_url)
    if error:
        flash(f'{error}', 'danger')
        return render_template(
            'index.html',
            url=data['url']  
        ), 422
    else:
        curr_url = repo.get_by_name(new_url)
        if curr_url:
            flash('Страница уже существует', 'info')
            return redirect(url_for('urls_show', id=curr_url['id']))
        else:
            id = repo.save(new_url)
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('urls_show', id=id))


@app.route('/urls/<id>')
def urls_show(id):
    url = repo.find(id)
    if url is None:
        render_template('not_found.html'), 422
    url_checks = repo.get_all_checks(id)
    return render_template(
        'url_show.html',
        url=url,
        url_checks=url_checks
    )


@app.post('/urls/<id>/checks')
def urls_checks(id):
    url = repo.find(id)
    try:
        response = requests.get(url['name'])
        response.raise_for_status()
        result = get_seo_content(response.text)
        url.update({'status_code': response.status_code, **result})
        repo.save_check(url)
        flash('Страница успешно проверена', 'success')

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('urls_show', id=id))
