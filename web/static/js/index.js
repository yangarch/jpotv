const player = videojs('player');

$(function() {
    fetch('/output')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {        
        /** 플레이어 세팅 */
        player.controlBar.addChild('qualitySelector');

        /** 채널 버튼 생성 */
        const listGroup = document.querySelector('.list-group');        
        const channelList = Object.keys(data);
        channelList.forEach((channel, index) => {
            const link = document.createElement('a');
            link.href = "#"
            link.textContent = channel;
            link.classList.add('list-group-item', 'list-group-item-dark');
            if (index === 0) link.classList.add('active');
            listGroup.appendChild(link);
        })

        /** 첫번째 채널 강제 셋팅 */
        player.src(
            Object.entries(data[channelList[0]]).map(([label, url], index) => ({
                src: url,
                type: 'application/x-mpegURL',
                label: label + 'P',
                selected: index === 0,
            }))
        )

        /** 채널 버튼 action */
        $(".list-group-item").click(function(e) {
            const channel = Object.entries(data[this.text]);
            console.log(channel);
            player.src(
                channel.map(([label, url], index) => ({
                    src: url,
                    type: 'application/x-mpegURL',
                    label: label + 'P',
                    selected: index === 0,
                }))
            );

            $(".list-group-item.active").removeClass("active");
            $(this).addClass("active");
            e.preventDefault();
        });

        /** 주소 복사 URL 갱신 */
        player.on('loadedmetadata', function(e) {
            document.getElementById('url').value = player.currentSrc();
        });
    })
    .catch(error => {
        console.error(error);
    });
});

function copyText() {
    const urlInput = document.getElementById('url');
    const urlValue = urlInput.value;
  
    const dummyElement = document.createElement('textarea');
    dummyElement.value = urlValue;
    document.body.appendChild(dummyElement);
    dummyElement.select();
    document.execCommand('copy');
    document.body.removeChild(dummyElement);

    alert('복사되었습니다');
}


