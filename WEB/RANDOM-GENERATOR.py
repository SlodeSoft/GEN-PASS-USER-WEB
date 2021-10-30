import RandomPassword as Rdm
import os.path
from flask import Flask, render_template, request, redirect

__STATIC_DIR = os.path.abspath('./static')
__TEMPLATE_DIR = os.path.abspath('./templates')

app = Flask(__name__, static_folder=__STATIC_DIR, template_folder=__TEMPLATE_DIR)
title = "GEN TON PASS"


class GENERATOR:
    def __init__(self, leng, numb, spechar, lowcase, uppcase):
        __step1__ = Rdm.RandomPassword()
        self.__passwd__ = __step1__.generate_random_password(length=leng,
                                                             include_numbers=numb,
                                                             include_special_characters=spechar,
                                                             include_lower_case_alphabets=lowcase,
                                                             include_upper_case_alphabets=uppcase)


# gen = GENERATOR(20, True, True, True, True)


@app.route('/', methods=['GET', 'POST'])
def generatorweb():
    labellist = ("Include Number",
                 "Include Special Characters",
                 "Include Lower Case",
                 "Include UPPER Case")
    namelist = ("selector-2",
                "selector-3",
                "selector-4",
                "selector-5")
    if request.method == "POST":
        form = request.form
        allarglist = list()
        leng= 20
        num = False
        spechar = False
        lowcas = False
        uppcas = False
        leng = request.form.get('selector-1')
        num = request.form.get('selector-2')
        spechar = request.form.get('selector-3')
        lowcas = request.form.get('selector-4')
        uppcas = request.form.get('selector-5')
        allarglist.extend([num, spechar, lowcas, uppcas])
        gen = GENERATOR(int(leng), num, spechar, lowcas, uppcas)
        tachaine = gen.__passwd__
        return render_template("index.html", extract=tachaine,
                               stylesgeneral="./static/stylesgeneral.css",
                               stylesselection="./static/stylesselection.css",
                               title=title,
                               leng=leng,
                               labellist=labellist,
                               zip=zip,
                               namelist=namelist,
                               allarglist=allarglist,
                               form=form)
    if request.method == "GET":
        leng= 20
        gen = GENERATOR(20, True, True, True, True)
        tachaine = gen.__passwd__
        return render_template("index.html", extract=tachaine,
                               stylesgeneral="./static/stylesgeneral.css",
                               stylesselection="./static/stylesselection.css",
                               title=title,
                               labellist=labellist,
                               namelist=namelist,
                               leng=leng,
                               zip=zip)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
                           stylesgeneral="./static/stylesgeneral.css",
                           styles404="./static/styles404.css",
                           favicon='./static/img/favicon.png',
                           title=title), 404


if __name__ == "__main__":
    app.run(debug=True, port=80)
