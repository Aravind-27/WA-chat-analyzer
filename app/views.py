from flask import current_app as app
from flask import render_template, request, redirect, abort
from app.functions import ExtractDataFrame, GenerateStats
from app.graphs import (
    membersBarPlot,
    busydayPolarPlot,
    msgovermonthBarPlot,
    Emojis_donut,
    activityDate_Graph,
    activityTime_Graph,
    emojiAdicts_LessPlot,
    night_morningPlot,
)
import os


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404"), 404


@app.route("/")
def home():
    """Index Page"""
    return render_template("sign-up.html")


@app.route("/Sample/", methods=["POST"])
def sample():
    """
    This function will be called if user
    wishes to use the sample file
    """
    return processing_phase("Sample.txt", "Sample/")


@app.route("/", methods=["POST"])
def upload_file():
    """ This function accepts data file(.txt)
        and saves it in uploads folder.If the
        the file is not found, Error 404 pagenotfound is called
    """
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        uploaded_file.save(os.path.join("uploads/" + uploaded_file.filename))
        return redirect(f"/{uploaded_file.filename}")
    else:
        return abort(404)


@app.route("/<file_name>")
def processing_phase(file_name, root="uploads/"):
    try:
        chats = ExtractDataFrame(os.path.join(root + file_name))
        chats.process()
        df = chats.dataframe()  # The Final Processed DataFrame

        if os.path.exists(
            os.path.join("uploads/" + file_name)
        ):  # Remove the uploaded file after processing,
            os.remove(
                os.path.join("uploads/" + file_name)
            )  # if it exists,else continue
            # (this way it won't delete sample file)
        stats = GenerateStats()
        fromdate, todate, diffdays = stats.dateRange(df)  # getting basic info/overview

        busyday = stats.busydayofweek(df)
        busydayPlot = busydayPolarPlot(busyday, "The busiest day of week")

        msgovermonth = stats.msgovermonth(df)
        msgovermonthPlot = msgovermonthBarPlot(
            msgovermonth, "Total Messages over the months"
        )

        media_ratio = round(stats.mediaRatio(df), 2)  # Media Ratio

        totalemojis = stats.totalEmojis(df)  # Total Emojis

        unique_emojis = stats.uniqueEmojis(df)  # Total Unique Emojis

        frequent_emojis = stats.frequentEmojis(df)
        emoji_donut = Emojis_donut(
            frequent_emojis, "Emoji Distribution"
        )  # Emojis Donut Plot

        active_members = stats.activeMembers(df)
        activeMemberPlot = membersBarPlot(
            active_members, "Most Active Members of The Group"
        )  # Active Members Bar Chart

        lazy_members = stats.lazyMembers(df)
        lazyMemberPlot = membersBarPlot(
            lazy_members, "Least Active Members of The Group"
        )  # Lazy Members Bar Chart

        result_dates = stats.activityOverDates(df)
        datesActivityGraph = activityDate_Graph(
            result_dates
        )  # Overall Dates Activity Line Plot

        result_time = stats.activityOverTime(df)
        timeActivityGraph = activityTime_Graph(
            result_time
        )  # Overall Day Activity Line Plot

        morn_night = stats.nightOwls_earlyBirds(df)
        morning = morn_night["morning"]
        morning_plot = night_morningPlot(
            morning, "Early Birds (6 am to 9 am)"
        )  # Morning Authors Pie Chart
        night = morn_night["night"]
        night_plot = night_morningPlot(
            night, "Night Owls (11 pm to 3 am)"
        )  # Night Authors Pie Chart

        con_less = stats.emojiCon_Emojiless(df)
        emoji_con = con_less["Emoji_con"]
        emojiAdictsPlot = emojiAdicts_LessPlot(
            emoji_con, "Emoji Addicts"
        )  # Emoji Addict Bar Chart

        return render_template(  # passing all the graphs and other values to dashboard.html
            "dashboard.html",
            total_emojis=totalemojis,
            fromdate=fromdate,
            todate=todate,
            total=df.shape[0],
            media_ratio=media_ratio,
            unique_emojis=unique_emojis,
            dategap=diffdays,
            msgovermonthPlot=msgovermonthPlot,
            activeMemberPlot=activeMemberPlot,
            busydayPlot=busydayPlot,
            lazyMemberPlot=lazyMemberPlot,
            bar_plot_dates=datesActivityGraph,
            bar_plot_time=timeActivityGraph,
            morning_plot=morning_plot,
            night_plot=night_plot,
            emojiAdictsPlot=emojiAdictsPlot,
            emoji_donut=emoji_donut,
        )

    except:
        abort(404)
