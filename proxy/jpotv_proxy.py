from mitmproxy import ctx, http


def response(flow: http.HTTPFlow) -> None:
    if "playlist.m3u8" in flow.request.url:
        if "playlist" in flow.request.url:
            ctx.log.info(
                f"Found .m3u8 URL with playlist: {flow.request.url}"
            )
            with open("../result/output.txt", "a") as f:
                f.write(flow.request.url + "\n")
