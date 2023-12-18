from mitmproxy import ctx, http


def response(flow: http.HTTPFlow) -> None:
    if "playlist.m3u8" in flow.request.url or "master.m3u8" in flow.request.url:
        ctx.log.info(
            f"Found .m3u8 URL with playlist: {flow.request.url}"
        )
        with open("/Users/archmacmini/Project/jpotv/result/output.txt", "a") as f:#path
            f.write(flow.request.url + "\n")
