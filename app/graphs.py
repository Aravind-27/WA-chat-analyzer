import plotly
import plotly.graph_objs as go
import plotly.express as px
import json


def activityDate_Graph(df):
    fig_batch = {
        "data": [
            go.Scatter(
                x=df.index,
                y=df["Number of Messages"].values,
                # text=y,
                # textposition='auto',
                mode="lines",
            )
        ],
        "layout": go.Layout(
            xaxis={"title": "Dates"},
            yaxis={"title": "Number of Messages"},
            hovermode="closest",
            height=500,
            width=691,
            title="Overall Activity of The Group",
        ),
    }
    graphJSON = json.dumps(fig_batch, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def activityTime_Graph(df):

    fig = px.line_polar(
        df,
        r="text",
        theta="Time_hour",
        line_close=True,
        width=460,
        title="Activity Over Whole Day",
    )
    fig.update_traces(fill="toself")
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)), showlegend=True,
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def busydayPolarPlot(df, title):

    fig = px.line_polar(
        df,
        r="messagecount",
        theta="day_of_date",
        line_close=True,
        title=title,
        width=460,
    )
    fig.update_traces(fill="toself")
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)), showlegend=True,
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def Emojis_donut(df, title):
    labels = df.Emoji.values
    values = df.Count.values
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                textinfo="label+percent",
                insidetextorientation="radial",
                title=title,
            )
        ],
        layout=go.Layout(
            # height=440,
            width=460,
        ),
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def membersBarPlot(df, title):
    fig = px.line(
        df,
        x=df.index,
        y=df["Message Count"].values,
        labels={"y": "Number of Messages"},
        text=df["Message Count"].values,
        title=title,
        height=500,
        width=691,
    )
    fig.update_layout(xaxis_tickangle=-30)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def msgovermonthBarPlot(df, title):
    fig = px.bar(
        df,
        x="month",
        y="text",
        color="year",
        barmode="group",
        labels={"y": "Total messages"},
        title=title,
        height=500,
        width=691,
    )
    fig.update_layout(xaxis_tickangle=-30)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def night_morningPlot(df, title):
    labels = df.index
    values = df["Message Count"].values
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo="label+percent",
                insidetextorientation="radial",
            )
        ],
        layout=go.Layout(
            # height=440,
            width=460,
        ),
    )
    fig.update_layout(title=title)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def emojiAdicts_LessPlot(df, title):
    fig = px.bar(
        df,
        x=df.index,
        y=df["Number of Emojis"].values,
        labels={"y": "Number of Emojis"},
        text=df["Number of Emojis"].values,
        title=title,
        height=500,
        width=691,
    )
    fig.update_layout(xaxis_tickangle=-30)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
