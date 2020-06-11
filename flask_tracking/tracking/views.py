from flask import abort, Blueprint, current_app, flash, jsonify, Markup, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .forms import SiteForm, VisitForm
from .models import Site, Visit
from flask_tracking.data import query_to_list
from .geodata import get_geodata


tracking = Blueprint("tracking", __name__)


@tracking.route("/")
def index():
    site_form = SiteForm()
    visit_form = VisitForm()
    #current_app.logger.info('welcome home')  

    return render_template("index.html",
                           site_form=site_form,
                           visit_form=visit_form)


@tracking.route("/site", methods=("POST", ))
def add_site():
    form = SiteForm()
    if form.validate_on_submit():
        site = Site.create(**form.data)
        flash(f"Added site: {site}")
        return redirect(url_for(".index"))

    return render_template("validation_error.html", form=form)


@tracking.route("/site/<int:site_id>")
@login_required
def view_site_visits(site_id=None):
    site = Site.query.get_or_404(site_id)
    if not site.user_id == current_user.id:
        abort(401)

    
    query = Visit.query.filter(Visit.site_id == site_id)
    data = query_to_list(query)
    title = f"visits for {site.base_url}"
    return render_template("tracking/site.html", visits=data, site=site, title=title)


@tracking.route("/visit", methods=("POST", ))
@tracking.route("/site/<int:site_id>/visit", methods=("GET", "POST",))
def add_visit(site_id=None):
    if site_id is None:
        # This is only used by the visit_form on the index page.
        form = VisitForm()
    else:
        site = Site.query.get_or_404(site_id)
        
        browser = request.headers.get("User-Agent")
        url = request.values.get('url') or request.headers.get("Referer")
        event = request.values.get('event')
        ip_addr = request.access_route[0] or request.remote_addr
        geodata = get_geodata(ip_addr)
        location = f"{geodata.get('city')}, {geodata.get('zipcode')}, {geodata.get('country')}"


        # WTForms does not coerce obj or keyword arguments
        # (otherwise, we could just pass in `site=site_id`)
        # CSRF is disabled in this case because we will *want*
        # users to be able to hit the /site/:id endpoint from other sites.

        form = VisitForm(
            csrf_enabled=False,
            site=site,
            browser=browser,
            url=url,
            ip_address=ip_addr,
            latitude=geodata.get('latitude'),
            longitude=geodata.get('longitude'),
            location=location,
            event=event)

    if form.validate():
        visit = Visit.create(**form.data)
        flash(f"Added visit for site {visit}")
        return '', 204

    return jsonify(errors=form.errors), 400


@tracking.route("/sites", methods=("GET", "POST"))
@login_required
def view_sites():

    form = SiteForm()

    if form.validate_on_submit():
        Site.create(owner=current_user, **form.data)
        flash("Added Site")
        return redirect(url_for(".view_sites"))

    query = Site.query.filter(Site.user_id == current_user.id)
    data = query_to_list(query)
    results = []

    # The header row should not be linked
    try:
        results = [next(data)]
        for row in data:
            row = [_make_link(cell) if i == 0 else cell
                for i, cell in enumerate(row)]
            results.append(row)

    except StopIteration:
        pass # no sites registered

    return render_template("tracking/sites.html", sites=results, form=form)


_LINK = Markup('<a href="{url}">{name}</a>')


def _make_link(site_id):
    url = url_for(".view_site_visits", site_id=site_id)
    return _LINK.format(url=url, name=site_id)
