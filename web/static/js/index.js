const player = videojs("player");
const capturePlayer = videojs("capturePlayer");

$(function () {
  fetch("/output")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(async (data) => {
      /** 데이터 초기화 및 플레이어 세팅 */
      const channelList = Object.keys(data);
      player.controlBar.addChild("qualitySelector");

      /** 채널 버튼 생성 (텍스트만)*/
      channelList.forEach((channel) => {
        let canvas = document.createElement("canvas");
        let context = canvas.getContext("2d");

        canvas.id = channel + "Thumbnail";
        canvas.style.border = "1px solid gray";
        canvas.style.cursor = "pointer";
        canvas.width = 192;
        canvas.height = 110;

        context.font = "16px Arial";
        context.fillStyle = "black";
        context.strokeStyle = "white";
        context.lineWidth = 3;

        context.strokeText(channel, 10, 20);
        context.fillText(channel, 10, 20);

        canvas.addEventListener("click", () => {
          let qualityList = Object.entries(data[channel]);
          player.src(
            qualityList.map(([label, url], index) => ({
              src: url,
              type: "application/x-mpegURL",
              label: label + "P",
              selected: index === "1080",
            }))
          );
        });

        document.querySelector(".list-group").appendChild(canvas);
      });

      /** 첫번째 채널 강제 셋팅 */
      player.src(
        Object.entries(data[channelList[0]]).map(([label, url], index) => ({
          src: url,
          type: "application/x-mpegURL",
          label: label + "P",
          selected: label === "1080",
        }))
      );

      /** 주소 복사 URL 갱신 */
      player.on("loadedmetadata", function (e) {
        document.getElementById("url").value = player.currentSrc();
      });

      /** 채널 버튼 썸네일 추가 */
      let video = document.querySelector("#capturePlayer video");
      for (const channel of channelList) {
        capturePlayer.src({ src: data[channel]["1080"], type: "application/x-mpegURL" });
        await new Promise((resolve) => {
          setTimeout(() => {
            let canvas = document.getElementById(channel + "Thumbnail");
            let context = canvas.getContext("2d");

            context.clearRect(0, 0, canvas.width, canvas.height);
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            context.strokeText(channel, 10, 20);
            context.fillText(channel, 10, 20);

            resolve();
          }, 1000);
        });
      }
      videojs(video).dispose();
    })
    .catch((error) => {
      console.error(error);
    });
});

function copyText() {
  const urlInput = document.getElementById("url");
  const urlValue = urlInput.value;

  const dummyElement = document.createElement("textarea");
  dummyElement.value = urlValue;
  document.body.appendChild(dummyElement);
  dummyElement.select();
  document.execCommand("copy");
  document.body.removeChild(dummyElement);

  alert("복사되었습니다");
}
