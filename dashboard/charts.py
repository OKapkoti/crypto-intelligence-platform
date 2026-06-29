import plotly.express as px


def price_history_chart(df):

    fig = px.line(
        df,
        x="timestamp",
        y="price_usd",
        title="Bitcoin Price History",
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Time",
        yaxis_title="Price (USD)"
    )

    return fig


def horizontal_bar(df, x, y, title):

    fig = px.bar(
        df.sort_values(x),
        x=x,
        y=y,
        orientation="h",
        title=title,
        text_auto=".2s"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="",
        yaxis_title=""
    )

    return fig

def trend_chart(df, x, y, title):

    fig = px.line(
        df,
        x=x,
        y=y,
        title=title,
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    return fig