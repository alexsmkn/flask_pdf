from sqlalchemy.orm import relationship

from flask_pdf import db


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    question_groups = db.relation('QuestionGroup', backref='assessment', lazy=True)
    results = db.relation('Result', backref='results', lazy=True)


class QuestionGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    question_subgroups = db.relation('QuestionSubgroup', backref='question_group', lazy=True)
    question_group_levels = db.relation('QuestionGroupLevel', backref='question_group', lazy=True)


class QuestionSubgroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    question_group_id = db.Column(db.Integer, db.ForeignKey('question_group.id'), nullable=False)
    question_parts = db.relation('QuestionPart', backref='question_subgroup', lazy=True)
    levels = db.relation('QuestionSubgroupLevel', backref='question_subgroup', lazy=True)


class QuestionPart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    statement = db.Column(db.String(100))
    question_subgroup_id = db.Column(db.Integer, db.ForeignKey('question_subgroup.id'), nullable=False)


result_answers = db.Table('answers',
                          db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'), primary_key=True),
                          db.Column('resultitem_id', db.Integer, db.ForeignKey('result_item.id'), primary_key=True)
                          )


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    statement = db.Column(db.String(100))


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    result_items = db.relation('ResultItem', backref='results', lazy=True)


class ResultItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_part_id = db.Column(db.Integer, db.ForeignKey('question_part.id'), nullable=False)
    result = db.Column(db.Integer, db.ForeignKey('result.id'), nullable=False)
    answers = relationship("Answer", secondary=result_answers)


class QuestionGroupLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    start_range = db.Column(db.Integer, nullable=False)
    end_range = db.Column(db.Integer, nullable=False)
    statement = db.Column(db.String(100))
    question_group_id = db.Column(db.Integer, db.ForeignKey('question_group.id'), nullable=False)


class QuestionSubgroupLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    start_range = db.Column(db.Integer, nullable=False)
    end_range = db.Column(db.Integer, nullable=False)
    statement = db.Column(db.String(100))
    question_subgroup_id = db.Column(db.Integer, db.ForeignKey('question_subgroup.id'), nullable=False)
