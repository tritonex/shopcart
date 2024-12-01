from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.models import Category, Article

class ShoppingListForm(FlaskForm):
    name = StringField('Listenname', validators=[
        DataRequired(),
        Length(max=100, message="Name darf maximal 100 Zeichen lang sein")
    ])
    submit = SubmitField('Liste speichern')

class AddToListForm(FlaskForm):
    article_id = HiddenField('Article')
    quantity = FloatField('Menge', validators=[Optional()])
    unit = SelectField('Einheit', choices=[
        ('', 'Stück'),
        ('kg', 'kg'),
        ('g', 'g'),
        ('L', 'Liter'),
        ('ml', 'ml'),
        ('Pkg', 'Packung')
    ], validators=[Optional()])
    submit = SubmitField('Hinzufügen')

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50, message="Name muss zwischen 2 und 50 Zeichen lang sein")
    ])
    icon = StringField('Icon (Emoji)', validators=[
        DataRequired(),
        Length(max=5, message="Bitte nur ein Emoji verwenden")
    ])
    sort_order = IntegerField('Reihenfolge', validators=[
        DataRequired(),
        NumberRange(min=1, message="Bitte eine positive Zahl eingeben")
    ])
    submit = SubmitField('Kategorie speichern')

class ArticleForm(FlaskForm):
    artName = StringField('Artikelname', validators=[
        DataRequired(),
        Length(min=2, max=50, message="Name muss zwischen 2 und 50 Zeichen lang sein")
    ])
    category_id = SelectField('Kategorie', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [
            (cat.id, f"{cat.icon} {cat.name}") 
            for cat in Category.query.order_by(Category.sort_order).all()
        ]
        
class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50, message="Name muss zwischen 2 und 50 Zeichen lang sein")
    ])
    icon = StringField('Icon (Emoji)', validators=[
        DataRequired(),
        Length(max=5, message="Bitte nur ein Emoji verwenden")
    ])
    sort_order = IntegerField('Reihenfolge', validators=[
        DataRequired(),
        NumberRange(min=1, message="Bitte eine positive Zahl eingeben")
    ])
    submit = SubmitField('Kategorie speichern')