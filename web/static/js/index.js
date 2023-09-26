const player = videojs('video');
const data = {};

$(function() {
    /** output.txt 읽어오기 */
    fetch('/output')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.text();
    })
    .then(output => {
        /** data 초기화 */
        output.split('\n').forEach(url => {
            if(url !== "") {
                let channel = url.split("https://")[1].split("-")[0];
                data[channel] = url;
            }
        })

        /** 동적 버튼 생성 */
        const listGroup = document.querySelector('.list-group');
        const keys = Object.keys(data);

        keys.forEach((key, index) => {
            const link = document.createElement('a');
            link.href = "#"
            link.textContent = key;
            link.classList.add('list-group-item', 'list-group-item-dark');
            if (index === 0) link.classList.add('active');
            listGroup.appendChild(link);
        })

        /** 첫번째 채널 강제 셋팅 */
        const firstChannel = Object.keys(data)[0];
        player.src({ 
            src: data[firstChannel], 
            type: 'application/x-mpegURL'
        });
        document.getElementById('url').value = data[firstChannel];

        /** 비디오 클릭으로 무음 해제 */
        player.on('click', function() {
            if (player.muted()) {
                player.muted(false);
                player.play();
            }
        });
        
        /** 버튼 action */
        $(".list-group-item").click(function(e) {
            e.preventDefault();
            
            $(".list-group-item.active").removeClass("active");
            $(this).addClass("active");

            player.src({
                src: data[this.text],
                type: 'application/x-mpegURL'
            });
            player.play();
            player.muted(false);

            document.getElementById('url').value = data[this.text];
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
  