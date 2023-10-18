from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from information_ret import get_most_similar_docs
app = Flask(__name__, template_folder="templates", static_folder="static")
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
import pandas as pd
import random
from googletrans import Translator
import requests
from transformers import T5ForConditionalGeneration, T5Tokenizer

from inforRet import google_custom_search

translator = Translator()
import re
#K52MP-WCBB7-UXUGA-RM2PR-DSUQ2
#hjpycyovrwdkeane

def translate_to_hebrew(text):
    translated = translator.translate(text, dest='he').text
    return translated
app.config['SECRET_KEY'] = 'womenDiseaseHELP'
app.config['MAIL_SERVER'] = "smtp.office365.com" # smtp.office365.com
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'women_org1122@hotmail.com'
app.config['MAIL_PASSWORD'] = 'hjpycyovrwdkeane'

app.secret_key = 'womenDiseaseHELP'
mail = Mail(app)

model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/fibro')
def fibro():
    # medical field:
    medical_dict = {
        'https://plotly.com/~transparentwomenproject/205/' : 'דירוג עוצמת התסמינים של שחוו הנשים',
        'https://plotly.com/~transparentwomenproject/150/' : 'תסמינים ומספר החזרות שלהן',
        'https://plotly.com/~transparentwomenproject/193/' : 'שביעת רצון המטופלות מרופא המשפחה שלהן',
        'https://plotly.com/~transparentwomenproject/197/' : 'שביעת רצון הנשים מהרופא שטיפל במחלה',
        'https://plotly.com/~transparentwomenproject/148/' : 'טיפולים שקיבלו הנשים',
        'https://plotly.com/~transparentwomenproject/199/' : 'בכמה מקומות הנשים מטופלות',
        'https://plotly.com/~transparentwomenproject/221/' : 'כמות הנשים שקיבלו אבחונים שגויים',
        'https://plotly.com/~transparentwomenproject/221/' : 'כמות הנשים שקיבלו טיפולים שגויים',
        'https://plotly.com/~transparentwomenproject/165/' : 'התפלגות קופות החולים של החולות',
        'https://plotly.com/~transparentwomenproject/43/' : 'האם הנשים מטופלות מבחינה רפואית',
        'https://plotly.com/~transparentwomenproject/33/' : 'כמות הנשים המוערכות כבעלות מגבלה רפואית',
        'https://plotly.com/~transparentwomenproject/27/' : 'כמה זמן הנשים כבר מאובחנות',
        'https://plotly.com/~transparentwomenproject/173/' : 'כמה זמן לקח עד שהמחלה של הנשים אובחנה'
    }
    
    social_groups = {
        'https://plotly.com/~transparentwomenproject/201/' : 'כמות הנשים שמשתתפות בקובצת תמיכה עבור המחלה',
        'https://plotly.com/~transparentwomenproject/203/' : "כמות הנשים שהתשמשו במקורות רפואיים למידע על המחלה",
        'https://plotly.com/~transparentwomenproject/203/' : "כמות הנשים שנעזרו בפלטפורמות מדיה חברתית כדי לקבל מידע על המחלה"
    }

    yakhas_nashem = {
        'https://plotly.com/~transparentwomenproject/207/' : 'איזה יחס חוו הנשים מהאחיות בקופות חולים?',
        'https://plotly.com/~transparentwomenproject/209/': 'איזה יחס חוו הנשים מהעובדות ההסוציאליות  בקופות חולים',
        'https://plotly.com/~transparentwomenproject/211/' :  'איזה יחס חוו הנשים מהעובדות הסוציאליות ברווחה',
        'https://plotly.com/~transparentwomenproject/213/' : 'התחושות שחשו הנשים מהביטוח לאומי',
    }

    finance_dic = {
        'https://plotly.com/~transparentwomenproject/175/' :  "כמות הנשים שעובדות" ,
        'https://plotly.com/~transparentwomenproject/185/' : 'עד כמה הנשים מדרגות את הרעה שחלה על המצב הכלכלי עקב המחלה',
        'https://plotly.com/~transparentwomenproject/181/' : "מאיפה מקבלות הנשי את הסיוע הכספי שלהם" ,
        'https://plotly.com/~transparentwomenproject/74/' : 'כמה הנשים מוציאות כסף הממוצע על צרכי המחלה'

    }

    social_life = {
        'https://plotly.com/~transparentwomenproject/161/' : "מחוז של מקום המגורים",
        'https://plotly.com/~transparentwomenproject/163/' : 'מקום מגורים',
        'https://plotly.com/~transparentwomenproject/159/' : 'התפלגות הגילאים'
    }

    emotions_ana = {
        'https://plotly.com/~transparentwomenproject/142/' : 'סוייוג רגשות של המטפלות שלנו על פי הדיווחים שלהן',
        'https://plotly.com/~transparentwomenproject/144/' : 'רגשות שחוו מספר לא מעט של הנשים שלנו',
        'https://plotly.com/~transparentwomenproject/257/' : "צירופי מילים שכיחות"
    }


    return render_template('fibro.html', medical_plotly=medical_dict, social_plotly=social_groups,
                            yakash_plotly=yakhas_nashem, finan_plotly=finance_dic,
                            social_plotly_2=social_life, emotions_plotly=emotions_ana)

@app.route('/eds')
def eds():
    plotly_dict = {}
    # plotly_urls = [
    #   https://plotly.com/~hannabaw12121313/42/   V
    # "https://plotly.com/~hannabaw12121313/44/", # question 77 V
    # "https://plotly.com/~hannabaw12121313/48/", # quetion 40 V
    # "https://plotly.com/~hannabaw12121313/46/", # question 54 V
    # "https://plotly.com/~hannabaw12121313/39/" # question 71
    #  https://plotly.com/~hannabaw12121313/53/' # question 55 to 58
    # https://plotly.com/~hannabaw12121313/56/ # ques 59 to 62
    # https://plotly.com/~hannabaw12121313/58/ # ques 67 to 70
    # https://plotly.com/~hannabaw12121313/60/ #question 72
    # https://plotly.com/~hannabaw12121313/62/ # question 74
    # https://plotly.com/~hannabaw12121313/64/ # question 39
    # ]
    plotly_urls = [
        'https://plotly.com/~hannabaw12121313/42/',
        'https://plotly.com/~hannabaw12121313/46/',
        'https://plotly.com/~hannabaw12121313/44/',
        'https://plotly.com/~hannabaw12121313/48/',
        'https://plotly.com/~hannabaw12121313/39/',
        'https://plotly.com/~hannabaw12121313/53/', 
        'https://plotly.com/~hannabaw12121313/56/',
        'https://plotly.com/~hannabaw12121313/58/',
        'https://plotly.com/~hannabaw12121313/60/',
        'https://plotly.com/~hannabaw12121313/62/',
        'https://plotly.com/~hannabaw12121313/64/',
        'https://plotly.com/~hannabaw12121313/66/'
    ]

    describe = [
        'ראשית נראה את אחוזי בחירת הטיפולים בקרב הנשים שהשתתפו בשאלון שלנו',
        'מה עוצמת התסמינים שהנשים חוו או חווים במחלה',
        'פה רואים את חווית הנשים שלנו בהתמודדות עם המחלה',
        'מקורות המידע שנעשה בהם שימוש על ידי הנשים כדי לקבל מידע אודות המחלה',
        'איך הייתה חווית הנשים לגבי הטיפול שניתן להם',
        'איזה יחס חוו הנשים מהאחיות בקופות חולים?',
        'איזה יחס חוו הנשים מהעובדות ההסוציאליות  בקופות חולים',
        'התחושות שחשו הנשים מהביטוח לאומי',
        'אחוז הנשים שהצביעו על כך שקיבלו אבחונים שגויים.',
        'אחוז הנשים שהצביעו על כך שקיבלו טיפולים שגויים.',
        'אחוז הנשים שהתשמשו במקודות מידע כדי ללמוד על המחלה',
        'איזה יחס חוו הנשים מהעובדות הסוציאליות ברווחה'
    ]

    # question 1 77 40
    indecies_1 = [0, 1, 2]
    key_tasmenem_more = [plotly_urls[i] for i in indecies_1]
    values_tasmenem_more = [describe[i] for i in indecies_1]
    dict_tasmenem_more = dict(zip(key_tasmenem_more, values_tasmenem_more))

    # question 39, 40
    indecies_2 = [10, 3]
    key_mkorot_meda3 = [plotly_urls[i] for i in indecies_2]
    values_mkorot_meda3 = [describe[i] for i in indecies_2]
    dict_mkorot_meda3 = dict(zip(key_mkorot_meda3, values_mkorot_meda3))

    #question 55-58, 59-62, 63-66, 67-70
    indecies_3 = [5, 6, 11, 7]
    key_yakhas = [plotly_urls[i] for i in indecies_3]
    values_yakhas = [describe[i] for i in indecies_3]
    dict_yakhas = dict(zip(key_yakhas, values_yakhas))

    # finanical:12, 15A, 15B, 17
    financal = {}
    financal['https://plotly.com/~hannabaw12121313/78/'] = "כמות הנשים שעובדות" # 12
    financal['https://plotly.com/~hannabaw12121313/68/'] = 'כמות הנשים שמקבלות סיוע כספי' # 15A
    financal['https://plotly.com/~hannabaw12121313/70/'] = "מאיפה מקבלות הנשי את הסיוע הכספי שלהם" #15B
    financal['https://plotly.com/~hannabaw12121313/76/'] = 'כמה הנשים מוציאות כסף הממוצע על צרכי המחלה'


    return render_template('eds.html', plotly_dict=dict_tasmenem_more, plotly_mkorot_meda3=dict_mkorot_meda3,
                           plotly_yakhas=dict_yakhas, financal_ploly=financal)


@app.route('/google-form')
def google_form():
    return render_template('google_form.html')




@app.route('/qa_page', methods=['GET', 'POST'])
def qa_page():
    answer = None
    cleaned_ans = None
    link = None
    if request.method == 'POST':
        question = request.form.get('question')
        pattern =  r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}\b'
        pattern2 = r"\."
        if question:
            try:
                answer,link = google_custom_search(question, model, tokenizer)
                answer = str(answer)
                
                if not answer:
                    answer = ("אנחנו פה כדי לספק עבורך מידע להעלאת מודעתך, "
                              "תזכרי שתמיד אנחנו איתך.")
                cleaned_ans = re.sub(pattern, '', answer)
                cleaned_ans = re.sub(pattern2, '', cleaned_ans)
            except Exception as e:  # Catch all exceptions
                flash("Please try again. Our system is under development and you may experience some issues.", "error")

    return render_template('qa_page.html', answer=cleaned_ans, link=link)



@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        customer_mail = request.form['customer_email']
        message = request.form['message']
        sender_mail = request.form['sender_mail']

        msg = Message(
            "New message from your WHLWD web",
            sender=app.config['MAIL_USERNAME'],
            recipients=[customer_mail]
        )

        msg.body = f"Mail from : {name}\n\n The sender mail: {sender_mail}\n\n{message}"

        try:
            mail.send(msg)
            flash("Your message has been sent! We will contact you soon.")
        except  Exception as e:
            s = str(e)
            flash(f"sorry there is an error, come back soon! {s}")

        return redirect(url_for('contact'))
    
    return render_template('contact.html')


@app.route('/knowus')
def knowUS():
    return render_template('knowus.html')

@app.route('/disGneral')
def disGneral():
    return render_template('disGneral.html')


from flask import flash

@app.route("/stories", methods=["GET", "POST"])
def stories():
    if request.method == "POST":
        try:
            stories = pd.read_csv('static/generateText.csv')
            topic = request.form["topic"]
            print(topic)
            if topic == 'Eds':
                eds_stories = list(stories[stories['label'] == 'eds'].iloc[:,0])
                text = random.choice(eds_stories)
                if text is not None:
                    return render_template("stories.html", text=translate_to_hebrew(text))
                else:
                    flash("Our system is having some issues because it's under development.", "error")
                    return render_template("stories.html")
            else:
                text = 'We have no stories about this topic yet'
                return render_template("stories.html", text=text)
        except Exception as e:  # Catch all exceptions
            return render_template("stories.html")
    else:
        return render_template("stories.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)