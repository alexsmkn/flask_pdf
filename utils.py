from flask import render_template
from flask_weasyprint import HTML
from sqlalchemy import func, and_
from sqlalchemy.sql.functions import coalesce

from flask_pdf import db

from models import (Assessment, QuestionGroup, Result, QuestionSubgroup, ResultItem, Answer,
                    QuestionGroupLevel, QuestionSubgroupLevel, QuestionPart)


def prepare_data_for_report(assessment_id, result_id):
    if not assessment_id and result_id:
        return
    assessment = Assessment.query.get(assessment_id)
    result = Result.query.filter_by(assessment_id=assessment_id, id=result_id).first()
    subgroups_points = dict(db.session.query(ResultItem, QuestionPart, Answer)
                            .join((ResultItem.answers, Answer))
                            .join(QuestionPart)
                            .filter(ResultItem.result == result.id)
                            .with_entities(QuestionPart.question_subgroup_id,
                                           func.sum(Answer.points).label('points_sum'))
                            .group_by(QuestionPart.question_subgroup_id).all())

    group_points = dict(db.session.query(QuestionGroup)
                        .join(QuestionSubgroup, isouter=True)
                        .join(QuestionPart, isouter=True)
                        .join(ResultItem,
                              and_(ResultItem.question_part_id == QuestionPart.id, ResultItem.result == result.id),
                              isouter=True)
                        .join((ResultItem.answers, Answer), isouter=True)
                        .with_entities(QuestionGroup.id,
                                       coalesce(func.sum(Answer.points).label('points_sum'), 0))
                        .group_by(QuestionGroup.id).all())

    result_answers_ids = db.session.query(ResultItem) \
        .join(ResultItem.answers) \
        .join(QuestionPart) \
        .with_entities(QuestionPart.id,
                       Answer).all()
    result_answers = populate_answers(result_answers_ids)
    q_group_levels = prepare_question_groups_levels(group_points)
    q_subgroups_levels = prepare_question_subgroups_levels(subgroups_points)
    return assessment, result_answers, q_group_levels, q_subgroups_levels


def get_level_for_group(q_group_id, points):
    q_group = QuestionGroup.query.get(q_group_id)
    level = QuestionGroupLevel.query.filter(
        QuestionGroupLevel.question_group_id == q_group.id,
        QuestionGroupLevel.start_range <= points,
        QuestionGroupLevel.end_range >= points).first()
    return level


def populate_answers(result_answers_ids):
    print result_answers_ids
    result_answers = dict()
    for item in result_answers_ids:
        answers = result_answers.get(item[0], [])
        answers.append(item[1])
        result_answers[item[0]] = answers
    return result_answers


def get_level_for_subgroup(q_subgroup_id, points):
    q_subgroup = QuestionSubgroup.query.get(q_subgroup_id)
    level = QuestionSubgroupLevel.query.filter(
        QuestionSubgroupLevel.question_subgroup_id == q_subgroup.id,
        QuestionSubgroupLevel.start_range <= points,
        QuestionSubgroupLevel.end_range >= points).first()
    return level


def prepare_question_groups_levels(points_by_group):
    levels = {}
    for group_id in points_by_group:
        levels[group_id] = get_level_for_group(group_id, points_by_group[group_id])
    return levels


def prepare_question_subgroups_levels(subgroups_points):
    levels = {}
    for subgroup_id in subgroups_points:
        levels[subgroup_id] = get_level_for_subgroup(subgroup_id, subgroups_points[subgroup_id])
    return levels


def get_page_body(boxes):
    for box in boxes:
        if box.element_tag == 'body':
            return box
        return get_page_body(box.all_children())


def generate_pdf_weasyprint():
    assessment, result_answers, q_group_levels, q_subgroups_levels = prepare_data_for_report(assessment_id=1,
                                                                                             result_id=1)
    template = render_template('pdf_template.html',
                               assessment=assessment,
                               result_answers=result_answers,
                               group_levels=q_group_levels,
                               subgroups_levels=q_subgroups_levels)

    html = HTML(string=template)
    main_doc = html.render()
    header_template = render_template('header_partial.html')
    html_header = HTML(string=header_template)
    header = html_header.render()
    header_page = header.pages[0]
    header_body = get_page_body(header_page._page_box.all_children())
    header_body = header_body.copy_with_children(header_body.all_children())
    # footer
    for i, page in enumerate(main_doc.pages):
        page_body = get_page_body(page._page_box.all_children())
        page_body.children += header_body.all_children()
        # footer

    pdf_file = main_doc.write_pdf()
    return pdf_file


def generate_simple_pdf():
    template = render_template('test.html')
    html = HTML(string=template)
    main_doc = html.render()
    pdf_file = main_doc.write_pdf()
    return pdf_file
