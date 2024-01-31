function toDoubleDigits(num) {
    num += "";
    if (num.length === 1) {
        num = "0" + num;
    }
    return num;
};

function ISO8601toUTCStringTimeonly(iso){
    var date = new Date(iso);
    return toDoubleDigits(date.getUTCHours()) + ":" +
    toDoubleDigits(date.getUTCMinutes()) + ":" +
    toDoubleDigits(date.getUTCSeconds());
};

function ISO8601toUTCStringDateonly(iso){
    var date = new Date(iso);
    return date.getUTCFullYear() + "-" +
    toDoubleDigits((date.getUTCMonth() + 1)) + "-" +
    toDoubleDigits(date.getUTCDate());
};

function ISO8601toJPNStringTimeonly(iso){
    var date = new Date(iso);
    return toDoubleDigits(date.getHours()) + ":" +
    toDoubleDigits(date.getMinutes()) + ":" +
    toDoubleDigits(date.getSeconds());
};

function ISO8601toJPNStringDateonly(iso){
    var date = new Date(iso);
    return date.getFullYear() + "-" +
    toDoubleDigits((date.getMonth() + 1)) + "-" +
    toDoubleDigits(date.getDate());
};

function sendYoutubeJSON() {
    videoId = y_idForm.y_idtextbox.value;

    Idstartnum = videoId.indexOf("v=");
    if (Idstartnum != -1) {
        videoId = videoId.substr(Idstartnum+2, 11);
    };

    Idstartnum = videoId.indexOf("youtu.be/");
    if (Idstartnum != -1) {
        videoId = videoId.substr(Idstartnum+9, 11);
    };

    var APIKEY = "AIzaSyCmUf6ZZ6qGrdXTu3RnxCcoll7acMsr9L4"
    $.ajax({
        "timeout": 5000,
        "url": "https://www.googleapis.com/youtube/v3/videos",
        "type": "GET",
        "dataType": "json",
        "async": false,
        "data": {
            "part": "id, snippet, statistics, contentDetails",
            "key": APIKEY,
            "id": videoId
        }
    }).done(function(resv) {
        if (!resv.items[0]) {
            appendError("動画が見つかりませんでした");
            return false;
        }
        responseData = convertResponse(resv, videoId);
        setData(responseData);
    }).fail(function() {
        text = "情報取得に失敗しました。URLに間違いがない場合は、不具合の可能性があります。運営に問い合わせてください。"
        $('.register-form-status').append("<p>" + text + "</p>")
        return false;
    }).always(function() {
    });

    function convertResponse(resv, videoId) {
        const responseData = {}
        if (videoId == "undefined") {
            responseData.title = "<i>動画は削除されました</i>";
            responseData.main_id = "";
            responseData.channel_name = "-";
            responseData.channelId = "-";
            responseData.duration = "-";
            responseData.n_view = "-";
            responseData.n_like = "-";
            responseData.n_dislike = "-";
            responseData.n_comment = "-";
            responseData.description = "";
            responseData.descriptionReplaced = "-";
            responseData.dateU = "";
            responseData.timeU = "";
            responseData.published_at_U = "-";
            responseData.dateJ = "";
            responseData.timeJ = "";
            responseData.published_at_J = "-";
        } else {
            responseData.title = resv.items[0].snippet.title;
            responseData.main_id = videoId;
            responseData.channel_name = resv.items[0].snippet.channelTitle;
            responseData.channelId = resv.items[0].snippet.channelId;
            responseData.duration = resv.items[0].contentDetails.duration;
            responseData.n_view = resv.items[0].statistics.viewCount;

            responseData.n_like = resv.items[0].statistics.likeCount;
            responseData.n_dislike = resv.items[0].statistics.dislikeCount;
            if (!responseData.n_like) {
                responseData.n_like= "-1";
                responseData.n_dislike = "-1";
            }

            responseData.n_comment = resv.items[0].statistics.commentCount;
            if (!responseData.n_comment) {
                responseData.n_comment = "-1";
            }

            responseData.description = resv.items[0].snippet.description;
            responseData.descriptionReplaced = responseData.description.replace( /\n/g, "<br>");

            var isodate = resv.items[0].snippet.publishedAt;
            responseData.dateU = ISO8601toUTCStringDateonly(isodate);
            responseData.timeU = ISO8601toUTCStringTimeonly(isodate);
            responseData.published_at_U = `${responseData.dateU} ${responseData.timeU}`;
            responseData.dateJ = ISO8601toJPNStringDateonly(isodate);
            responseData.timeJ = ISO8601toJPNStringTimeonly(isodate);
            responseData.published_at_J = `${responseData.dateJ} ${responseData.timeJ}`;
        };

        return responseData;
    }
}

function setData(data) {

    appendError("")

    const dom = createVideoItemDOM(data)
    $('#list-area').html(dom);

    setValue(data);

    $('.submit-button').prop('disabled', false);

}

function appendError(txt) {
    $('.register-form-status').text(txt);
}

function createVideoItemDOM(data) {
    const likeClassFont20 = (data.n_like == "-1") ? " font-20" : "";
    const commentClassFont20 = (data.n_comment == "-1") ? " font-20" : "";

    const dom = `
        <section class="video-item-section">
            <div class="video-item">
                <article class="videoTile">
                    <div class="video-number"></div>
                    <div class="videoTile-inner">
                        <div class="videoTile-head">
                            <a href="https://www.youtube.com/watch?v=${data.main_id}" target="_blank" class="video-link">
                                <div class="videoTile-img-box">
                                    <div class="videoTile-img"
                                        style="background-image:url(https://i.ytimg.com/vi/${data.main_id}/hqdefault.jpg)"></div>
                                </div>
                                <div class="videoTile-content">
                                    <h2 class="video-title">${data.title}</h2>
                                    <div class="video-channel"><span>${data.channel_name}</span></div>
                                </div>
                            </a>
                        </div>
                        <div class="video-middle">
                            <div class="video-middle-1">
                                <div class="video-statistics">
                                    <div class="video-statistics-item">
                                        <div class="video-statistics-num">${data.n_view}</div>
                                        <div class="video-statistics-name">再生回数</div>
                                    </div>
                                    <div class="video-statistics-item">
                                        <div class="video-statistics-num${likeClassFont20}">${data.n_like}</div>
                                        <div class="video-statistics-name">高評価数</div>
                                    </div>
                                    <div class="video-statistics-item">
                                        <div class="video-statistics-num${commentClassFont20}">${data.n_comment}</div>
                                        <div class="video-statistics-name">コメント数</div>
                                    </div>
                                </div>
                                <div class="video-time">
                                    <h3 class="video-time-head">投稿日時</h3>
                                    <table class="video-time-content">
                                        <tbody>
                                            <tr>
                                                <td>世界標準時</td>
                                                <td class="video-time-iso">${data.published_at_U}</td>
                                            </tr>
                                            <tr>
                                                <td>日本時間</td>
                                                <td class="video-time-jpn">${data.published_at_J}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div class="video-description">
                                <p>${data.descriptionReplaced}</p>
                            </div>
                        </div>
                    </div>
                </article>
            </div>
        </section>
    `
    return dom
}

function setValue(data) {
    const now = new Date().toUTCString();
    const nowText = ISO8601toUTCStringDateonly(now) + " " + ISO8601toUTCStringTimeonly(now);
    
    $('input.title').val(data.title);
    $('input#channel').val(data.channelId);
    $('input.main_id').val(data.main_id);
    $('input.youtube_id').val(data.main_id);
    $('input.published_at').val(data.published_at_U);
    $('input.published_at_year').val(data.dateJ.split('-')[0]);
    $('input.published_at_month').val(data.dateJ.split('-')[1]);
    $('input.published_at_day').val(data.dateJ.split('-')[2]);
    $('input.published_at_hour').val(data.timeJ.split(':')[0]);
    $('input.published_at_minute').val(data.timeJ.split(':')[1]);
    $('input.published_at_second').val(data.timeJ.split(':')[2]);
    $('input.duration').val(data.duration);
    $('input.n_view').val(data.n_view);
    $('input.n_like').val(data.n_like);
    $('input.n_dislike').val(data.n_dislike);
    $('input.n_comment').val(data.n_comment);
    $('input.description').val(data.descriptionReplaced);
    $('input.reg_date').val(nowText);
    $('input.statistics_update_date').val(nowText);
}

function applyBeforeData() {
    const data = {}
    data.title = $('#before-title').text();
    data.main_id = $('#before-main_id').text();
    data.channel_name = $('#before-channel_name').text();
    data.published_at_U = $('#before-published_at_U').text();
    data.published_at_J = $('#before-published_at_J').text();
    data.n_view = $('#before-n_view').text();
    data.n_like = $('#before-n_like').text();
    data.n_dislike = $('#before-n_dislike').text();
    data.n_comment = $('#before-n_comment').text();
    data.description = $('#before-description').text();

    data.descriptionReplaced = data.description.replace(/<br>/g, '<br>');

    const dom = createVideoItemDOM(data)
    $('#list-area-before').html(dom);
}