
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    if "user" in session:
        return redirect(url_for("main.dashboard"))
    return render_template("home.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = supabase.table("users").select("*").eq("username", username).eq("password", password).execute().data
        if user:
            session["user"] = user[0]
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for("main.login"))

    return render_template("login.html")

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        server = request.form.get("server")
        alliance = request.form.get("alliance")
        vip = request.form.get("vip") == "on"

        existing = supabase.table("users").select("id").eq("username", username).execute()
        if existing.data:
            flash("Username already taken.", "error")
            return redirect(url_for("main.register"))

        supabase.table("users").insert({
            "username": username,
            "password": password,
            "server": server,
            "alliance": alliance,
            "vip": vip
        }).execute()

        flash("Account created! Please log in.")
        return redirect(url_for("main.login"))

    return render_template("register.html")

@main_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("main.login"))
    return render_template("dashboard.html", user=session["user"])

@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))

from datetime import datetime, timedelta
import random

@main_bp.route("/picker", methods=["GET", "POST"])
def picker():
    if "user" not in session:
        return redirect(url_for("main.login"))

    message = ""
    defender_pick = None
    contestant_pick = None
    recent_names = set()

    if request.method == "POST":
        raw_input = request.form.get("contestants")
        contestants = [c.strip() for c in raw_input.splitlines() if c.strip()]

        if not contestants:
            flash("You must enter at least one name.", "error")
            return redirect(url_for("main.picker"))

        # get recent picks from the last 7 days
        cutoff = (datetime.utcnow() - timedelta(days=7)).isoformat()
        recent_data = supabase.table("picks").select("*").gte("picked_on", cutoff).execute().data
        if recent_data:
            recent_names = {p["name"].lower() for p in recent_data}

        # filter contestants who haven't been picked recently
        eligible_contestants = [c for c in contestants if c.lower() not in recent_names]

        if not eligible_contestants:
            flash("No eligible contestants (all have been picked in the last 7 days).", "error")
            return redirect(url_for("main.picker"))

        contestant_pick = random.choice(eligible_contestants)
        supabase.table("picks").insert({
            "name": contestant_pick,
            "role": "contestant",
            "picked_on": datetime.utcnow().isoformat()
        }).execute()

        if session["user"].get("vip"):
            defenders = supabase.table("defenders").select("*").execute().data
            eligible_defenders = [d["name"] for d in defenders if d["name"].lower() not in recent_names]

            if eligible_defenders:
                defender_pick = random.choice(eligible_defenders)
                supabase.table("picks").insert({
                    "name": defender_pick,
                    "role": "defender",
                    "picked_on": datetime.utcnow().isoformat()
                }).execute()

    return render_template("picker.html", user=session["user"], contestant_pick=contestant_pick, defender_pick=defender_pick)

