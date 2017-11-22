from flask import render_template
#from weasyprint import HTML
from flask_weasyprint import HTML

from models import Assessment, QuestionGroup, Result, QuestionSubgroup, ResultItem, Answer


def prepare_data_for_report(assessment_id, result_id):
    if not assessment_id and result_id:
        return
    assessment = Assessment.query.get(assessment_id)
    result = Result.query.filter_by(assessment_id=assessment_id, id=result_id)

    q_groups = QuestionGroup.query.filter_by(assessment_id=assessment_id).order_by('order')
    points_by_group = get_groups_points(q_groups)
    # points_by_subgroups = [points_for_question_group(x.id) for x in q_groups]
    print(points_by_group)
    for group in points_by_group:
        print('Sum by group = {} - > {}'.format(
            group,
            sum(points_by_group[group].values())))

    # print(points_by_subgroups)
    return assessment, result


def get_groups_points(q_groups):
    points_per_group = dict()
    for q_group in q_groups:
        points_dict = points_for_question_group(q_group.id)
        points_per_group[q_group.id] = points_dict
    return points_per_group


def points_for_question_group(q_group_id):
    q_group = QuestionGroup.query.get(q_group_id)
    points_by_subgroups = dict()
    for subgroup in q_group.question_subgroups:
        points_by_subgroups[subgroup] = points_for_question_subgroup(
            subgroup.id,
            assessment_id=q_group.assessment_id
        )
    return points_by_subgroups


def points_for_question_subgroup(q_subgroup_id, assessment_id):
    q_subgroup = QuestionSubgroup.query.get(q_subgroup_id)
    result = Result.query.filter_by(assessment_id=assessment_id).first()
    points = 0
    for q_part in q_subgroup.question_parts:
        res_items = ResultItem.query.filter_by(question_part_id=q_part.id, result=result.id)
        for answer in res_items:
            a = Answer.query.get(answer.id)
            points += a.points
    return points


def get_page_body(boxes):
    for box in boxes:
        if box.element_tag == 'body':
            return box
        return get_page_body(box.all_children())


def generate_pdf_weasyprint():
    assessment, result = prepare_data_for_report(assessment_id=1, result_id=1)

    template = render_template('pdf_template.html', assessment=assessment, result=result)
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