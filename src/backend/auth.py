import uuid

from flask import Blueprint, redirect, session, request, url_for, make_response
from flask.typing import ResponseReturnValue
from urllib.parse import urlencode
from src.backend import storage, client, user_repository

from src.core.helpers import get_random_string, get_absolute_url_for

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", defaults={"main_user_id": None})
@bp.route("/login/<main_user_id>")
def login(main_user_id: str | None) -> ResponseReturnValue:
    # Link is shared by the user creating the blend (main user)
    if main_user_id is not None:
        existing_data = storage.read(f"user:{main_user_id}")
        if not existing_data:
            return redirect(
                url_for("frontend.catch_all")
                + "?"
                + urlencode({"error": "Main user not logged in."})
            )
        session["main_user_id"] = main_user_id

    state = get_random_string(16)
    auth_url = client.generate_auth_url(get_absolute_url_for("auth.callback"), state)

    session["state"] = state
    return redirect(auth_url)


@bp.route("/logout")
def logout() -> ResponseReturnValue:
    resp = make_response(redirect(url_for("frontend.catch_all")))
    user_id = session.get("user_id")

    if not user_id:
        return resp

    user_repository.delete_user(user_id)
    session.clear()
    return resp


@bp.route("/callback")
def callback() -> ResponseReturnValue:
    code = request.args.get("code", "")
    state = request.args.get("state", "")
    error = request.args.get("error", "")

    redirect_to = url_for("frontend.catch_all")

    if not state or state != session["state"]:
        del session["state"]
        if "main_user_id" in session:
            del session["main_user_id"]
        return redirect(redirect_to + "?" + urlencode({"error": "state_mismatch"}))

    if error and not code:
        del session["state"]
        if "main_user_id" in session:
            del session["main_user_id"]
        return redirect(redirect_to + "?" + urlencode({"error": error}))

    auth_resp = client.authenticate(
        auth_code=code, redirect_url=get_absolute_url_for("auth.callback")
    )

    user = client.get_user(auth_resp["token"])
    user.load_auth_data_from_response(auth_resp)

    existing_user_id = user_repository.get_user_id(user.email)

    if existing_user_id is None:
        user_id = str(uuid.uuid4())
    else:
        user_id = existing_user_id

    user.id = user_id
    user_repository.save_user(user)

    del session["state"]

    if "main_user_id" in session:
        if session["main_user_id"] == user_id:
            return redirect(
                redirect_to
                + "?"
                + urlencode({"error": "You can't join your own session!"})
            )
        user_repository.add_to_session(session["main_user_id"], user_id)

        del session["main_user_id"]
        return redirect("/after_login")

    session["user_id"] = user.id
    session.permanent = True
    return redirect(redirect_to)
