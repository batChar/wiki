# -*- coding: utf-8 -*-
""" Возвращает форму для редактирования/создания записи """

from flask import render_template, request, redirect, url_for
import flask

from flask.ext.login import current_user

from appwiki.forms.create import CreateDataForm
from appwiki.forms.edit import EditDataForm

from appwiki.methods.access import access_f


def get_url(word):
#    try:
#        word = word.encode('utf-8')
#    except:
#        pass
    url = word.strip()
    return url.replace(' ', '_')


def get_word(url):
#    url = url.encode('utf-8')
    return url.replace('_', ' ')


def get_form_edit(word):
    page = flask.g.database.get_page(get_url(word))

#    word = get_url(word)

    access_edit = True
    if page is not None:
        # Проверка на права пользователя вносить правки в статью
        access_edit = access_f(page['access'], current_user)

    if current_user.is_authenticated() is False or access_edit is False:
        return render_template('page.html',
                               page=page,
                               message=u"Вы не имеете прав на редaкатирование страницы",
                               navigation=True,
                               word=get_url(word)
                               )
    if page is None:
        # вывожу форму создания статьи
        form = CreateDataForm()
        form.title.data = get_word(word)
        form.access.data = u'All'
        return render_template('form_create.html', form=form, word=get_url(word))
    else:
#        return str(access_edit)
#
#        if access_edit is True:
#            return 'good'
#        else:
#            return 'false'
#        return str(list_access)

        # Вывожу форму редактирования статьи
        form = EditDataForm(request.form)
        form.title.data = page['title']
        form.text.data = page['text']
        form.tags.data = ", ".join(page['tags'])
        form.url.data = page['url']
        form.access.data = page['access']
#        form.tags.data  = page['tags']
        return render_template('form_edit.html', form=form, navigation=True, word=get_url(word))
