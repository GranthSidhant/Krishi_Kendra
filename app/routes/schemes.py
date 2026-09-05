from flask import Blueprint, render_template, request
from app.models import GovernmentScheme

schemes_bp = Blueprint('schemes', __name__)

@schemes_bp.route('/')
def index():
    category_filter = request.args.get('category', '')
    query_text = request.args.get('q', '').strip()

    query = GovernmentScheme.query.filter_by(is_active=True)
    if category_filter and category_filter != 'All':
        query = query.filter_by(category=category_filter)
    if query_text:
        query = query.filter(GovernmentScheme.title.ilike(f"%{query_text}%") | GovernmentScheme.description.ilike(f"%{query_text}%"))

    schemes = query.order_by(GovernmentScheme.is_featured.desc(), GovernmentScheme.created_at.desc()).all()
    categories = ['Subsidy & Financial Assistance', 'Insurance', 'Credit & Loans', 'Solar & Irrigation', 'Soil & Infrastructure']

    return render_template(
        'schemes/index.html',
        schemes=schemes,
        categories=categories,
        selected_category=category_filter,
        query_text=query_text
    )


@schemes_bp.route('/<int:scheme_id>')
def detail(scheme_id):
    scheme = GovernmentScheme.query.get_or_404(scheme_id)
    return render_template('schemes/detail.html', scheme=scheme)
