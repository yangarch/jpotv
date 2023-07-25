from mitmproxy import ctx, http


def response(flow: http.HTTPFlow) -> None:
    if "playlist.m3u8" in flow.request.pretty_url:
        if "playlist" in flow.request.pretty_url:
            ctx.log.info(
                f"Found .m3u8 URL with playlist: {flow.request.pretty_url}"
            )
            with open("output.txt", "a") as f:
                f.write(flow.request.pretty_url + "\n")
